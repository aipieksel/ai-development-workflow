#!/usr/bin/env python3
"""Validate and package the canonical workflow. Python 3.10+, standard library only."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import sys
from urllib.parse import unquote, urlsplit
import zipfile


class PackageError(ValueError):
    """An incomplete or inconsistent source must not become a release."""


RUNTIME_DIRS = {
    "agents", "workflows", "assets", "commands", "modes",
    "references", "scripts", "specialists", "task-recipes",
}
ROOT_FILES = {"SKILL.md", "VERSION", "LICENSE", "NOTICE.md", "README.md", "CHANGELOG.md"}
ROOT_JSON: set[str] = set()
FORBIDDEN_ROOTS = {"agents-pro-v2", "integrations", "documents", "tasks", "node_modules", ".git"}
FORBIDDEN_FILES = {"agents-pro.queue.json", "agents-pro.skill.json", "agents-pro.skill.v2.json",
                   "scripts/workflow_picker.py", "references/portable-picker.md", "specialists/vscode-agents-pro.md"}
BT = chr(96)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PackageError(message)


def safe_name(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(
        part not in ("", ".", "..") for part in path.parts
    ) and path.as_posix() == name


def ignored(name: str) -> bool:
    parts = PurePosixPath(name).parts
    return "__pycache__" in parts or name.endswith((".pyc", ".pyo")) or (
        parts and parts[-1] == ".DS_Store"
    ) or name.startswith("scripts/tests/")


def read_source(root: Path, name: str) -> bytes:
    require(safe_name(name), f"Unsafe source path: {name!r}")
    path = root / name
    require(path.is_file() and not path.is_symlink(), f"Missing regular source file: {name}")
    require(path.resolve().is_relative_to(root.resolve()), f"Escaped source path: {name}")
    content = path.read_bytes()
    require(bool(content.strip()), f"Empty source file: {name}")
    return content


def markdown_prose(text: str) -> str:
    """Remove fenced/inline examples before checking real Markdown link targets."""
    lines, marker, length = [], None, 0
    for line in text.splitlines():
        stripped = line.lstrip(" ")
        if len(line) - len(stripped) <= 3 and stripped and stripped[0] in (BT, "~"):
            run = len(stripped) - len(stripped.lstrip(stripped[0]))
            if run >= 3:
                if marker is None:
                    marker, length = stripped[0], run
                    continue
                if stripped[0] == marker and run >= length and not stripped[run:].strip():
                    marker = None
                    continue
        if marker is None:
            lines.append(line)
    prose = "\n".join(lines)
    return re.sub(re.escape(BT) + r"+[^\n]*?" + re.escape(BT) + r"+", "", prose)


def local_target(source: str, target: str) -> str | None:
    target = target.strip("<>")
    url = urlsplit(target)
    if url.scheme or url.netloc or not url.path or url.path.startswith("/"):
        return None
    return posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(url.path)))


def validate_links(members: dict[str, bytes], label: str) -> int:
    directories = {
        str(parent)
        for name in members
        for parent in PurePosixPath(name).parents
        if str(parent) != "."
    }
    checked = 0
    for name, content in members.items():
        if not name.endswith(".md"):
            continue
        prose = markdown_prose(content.decode("utf-8"))
        targets = re.findall(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)", prose)
        targets += re.findall(r"(?m)^\s{0,3}\[[^\]\n]+\]:\s*(<[^>]+>|[^\s]+)", prose)
        for target in targets:
            path = local_target(name, target)
            if path is None:
                continue
            require(not path.startswith("../"), f"{label}: link escapes package: {name} -> {target}")
            require(path in members or path in directories,
                    f"{label}: missing link target: {name} -> {target}")
            checked += 1
    return checked


def validate_static_imports(members: dict[str, bytes], label: str) -> int:
    checked = 0
    for name, content in members.items():
        if not name.endswith((".js", ".cjs", ".ts")):
            continue
        text = content.decode("utf-8")
        imports = re.findall(
            r"""(?:require\s*\(\s*|from\s+|import\s*)['"](\.[^'"]+)['"]""", text
        )
        for target in imports:
            path = local_target(name, target)
            require(path is not None and not path.startswith("../"),
                    f"{label}: import escapes package: {name} -> {target}")
            choices = [path, path + ".js", path + ".cjs", path + ".json",
                       path + ".ts", path + "/index.js", path + "/index.cjs"]
            require(any(choice in members for choice in choices),
                    f"{label}: missing static import: {name} -> {target}")
            checked += 1
    return checked


def command_inventory(members: dict[str, bytes]) -> list[dict]:
    commands = []
    for name, content in members.items():
        if not name.endswith(".md"):
            continue
        match = re.match(r"\A---\r?\n(\{.*?\})\r?\n---", content.decode("utf-8"), re.S)
        if match:
            metadata = json.loads(match.group(1))
            if "command" in metadata:
                commands.append({"code": metadata["command"], "path": name,
                                 "launcher": metadata["launcher"]})
    codes = [item["code"] for item in commands]
    require(len(codes) == len(set(codes)), "Duplicate command definitions")
    return sorted(commands, key=lambda item: item["code"])


def load_sources(root: Path) -> tuple[dict[str, bytes], dict[str, bytes], dict]:
    root = root.resolve()
    for name in FORBIDDEN_FILES | {"agents-pro-v2", "integrations"}:
        require(not (root / name).exists(), "Retired editor component remains: " + name)
    inventory = json.loads(read_source(root, "packaging/runtime-files.json"))
    require(inventory.get("schema") == "ai-development-workflow/runtime-files-v1",
            "Unsupported runtime inventory schema")
    paths = inventory.get("files", [])
    require(isinstance(paths, list) and paths and len(paths) == len(set(paths)),
            "Runtime inventory is empty or contains duplicate paths")
    for name in paths:
        require(isinstance(name, str) and safe_name(name), f"Unsafe runtime path: {name!r}")
        require(not ignored(name) and name.split("/")[0] not in FORBIDDEN_ROOTS,
                f"Development/cache file in runtime inventory: {name}")
        require(name.split("/")[0] in RUNTIME_DIRS or name in ROOT_FILES | ROOT_JSON,
                f"Unapproved runtime source root: {name}")
    runtime = {name: read_source(root, name) for name in sorted(paths)}
    require(ROOT_FILES | ROOT_JSON <= set(runtime), "Missing required root runtime files")
    for directory in RUNTIME_DIRS:
        for path in (root / directory).rglob("*"):
            if path.is_file():
                name = path.relative_to(root).as_posix()
                if not ignored(name):
                    require(name in runtime, f"Unlisted runtime file; update inventory: {name}")
    version = runtime["VERSION"].decode().strip()
    require(bool(re.fullmatch(r"\d+\.\d+\.\d+", version)), "Invalid release VERSION")
    require(f"# AI Development Workflow v{version}" in runtime["SKILL.md"].decode(),
            "Main skill heading and VERSION disagree")
    require(f"## {version}" in runtime["CHANGELOG.md"].decode(),
            "CHANGELOG does not include this source version")
    require(version in runtime["README.md"].decode(), "README omits this source version")
    commands = command_inventory(runtime)
    profiles = sorted(name for name in runtime if name.endswith("/agent.md"))
    expected = inventory.get("expected", {})
    require(len(commands) == expected.get("commands"), "Unexpected command count")
    require(len(profiles) == expected.get("profile_files"),
            "Unexpected physical agent-profile count")
    guide = "references/advanced-reference.md"
    require(guide in runtime, "Missing complete advanced command reference")
    for item in commands:
        require(item["code"] in runtime[guide].decode(),
                f"Advanced reference omits command {item['code']}")
    module_path = Path(__file__).resolve().parents[1] / "scripts/workflow_catalog.py"
    spec = importlib.util.spec_from_file_location("_aidw_release_catalogue", module_path)
    require(spec is not None and spec.loader is not None, "Cannot load catalogue validator")
    catalogue_module = importlib.util.module_from_spec(spec)
    prior_bytecode = sys.dont_write_bytecode
    prior_import_path = list(sys.path)
    sys.dont_write_bytecode = True
    # Dependencies come from this validator's own source, never the inspected root.
    sys.path.insert(0, str(module_path.parent))
    try:
        spec.loader.exec_module(catalogue_module)
        catalogue = catalogue_module.build_catalog(root)
        expected_index = catalogue_module.markdown_index(catalogue).encode("utf-8")
        expected_search_index = (json.dumps(
            catalogue_module.build_search_index(root, catalogue), indent=2, ensure_ascii=False
        ) + "\n").encode("utf-8")
    finally:
        sys.dont_write_bytecode = prior_bytecode
        sys.path[:] = prior_import_path
    require(runtime.get("references/workflow-index.md") == expected_index,
            "Generated workflow index is stale; regenerate it from the current source")
    require(runtime.get("references/workflow-search-index.json") == expected_search_index,
            "Generated workflow search index is stale; regenerate it from the current source")
    require([m["id"] for m in catalogue["publicModes"]] == ["auto", "plan", "build", "review", "loop"],
            "Public mode catalogue does not match the five supported modes")
    registry = catalogue["agentRegistry"]
    canonical_profiles = {row["profile"] for row in registry["families"].values()}
    legacy_profiles = set(registry["legacyProfiles"])
    require(set(profiles) == canonical_profiles | legacy_profiles,
            "Role files and canonical/compatibility registry disagree")
    counts = {
        "core_families": len(canonical_profiles),
        "compatibility_profiles": len(legacy_profiles - canonical_profiles),
        "profile_files": len(profiles),
        "legacy_profile_mappings": len(legacy_profiles),
        "capability_selectors": len(registry["capabilities"]),
        "specialist_lenses": catalogue["counts"].get("specialist", 0),
        "operations": len(registry["operations"]),
    }
    for key, value in counts.items():
        require(value == expected.get(key), f"Unexpected {key} count: {value}")
    for name, digest in registry["sourceDigests"].items():
        require(name in runtime and hashlib.sha256(runtime[name]).hexdigest() == digest,
                "Registry dependency missing or stale in package: " + name)
    runtime_links = validate_links(runtime, "local skill")
    import_count = validate_static_imports(runtime, "local skill")
    for name, content in runtime.items():
        if name.endswith(".json"):
            json.loads(content)

    template_root = root / "packaging/plugin-template"
    require(template_root.is_dir(), "Missing plugin template directory")
    plugin = {}
    for path in sorted(template_root.rglob("*")):
        if path.is_file():
            name = path.relative_to(template_root).as_posix()
            require(not ignored(name), f"Cache/development file in plugin template: {name}")
            require(
                name in {"plugin.json", ".codex-plugin/plugin.json", "README.md"}
                or name in {"assets/logo.png", "assets/composer.png"},
                f"Unapproved plugin template file: {name}",
            )
            require(not name.startswith("skills/ai-development-workflow/"),
                    "A second canonical runtime must not live in the plugin template")
            plugin[name] = read_source(template_root, name)
    aliases = sorted(name for name in plugin if re.fullmatch(r"skills/[^/]+/SKILL\.md", name))
    require(not aliases and expected.get("launcher_aliases") == 0,
            "A public plugin must contain one main skill and no launcher alias skills")
    plugin.update({f"skills/ai-development-workflow/{name}": content
                   for name, content in runtime.items()})
    for name in ("LICENSE", "NOTICE.md"):
        plugin[name] = runtime[name]
    manifests = [json.loads(plugin[name]) for name in ("plugin.json", ".codex-plugin/plugin.json")]
    for manifest in manifests:
        require(manifest.get("name") == "ai-development-workflow", "Plugin identity changed")
        require(manifest.get("version") == version, "Plugin manifest version mismatch")
        interface = manifest.get("interface") or manifest.get("extensions", {}).get(
            "com.openai", {}).get("interface", {})
        require(isinstance(interface.get("shortDescription"), str)
                and 0 < len(interface["shortDescription"]) <= 30,
                "Plugin short description must contain 1 to 30 characters")
        prompts = interface.get("defaultPrompt", [])
        prompts = [prompts] if isinstance(prompts, str) else prompts
        require(isinstance(prompts, list) and len(prompts) <= 3
                and all(isinstance(value, str) and 0 < len(value) <= 128 and "@" not in value for value in prompts),
                "Plugin starter prompts are invalid")
        require(not manifest.get("apps") and not manifest.get("extensions", {}).get("com.openai", {}).get("apps"),
                "Public skills-only package must not contain app bindings")
        for field in ("logo", "composerIcon"):
            asset = interface.get(field, "").removeprefix("./")
            require(asset in plugin, f"Missing plugin {field}: {asset}")
    require(manifests[1].get("skills") == "./skills", "Unexpected plugin skills location")
    require(manifests[0]["extensions"]["com.openai"]["interface"] == manifests[1]["interface"],
            "Plugin interface manifests disagree")
    require(manifests[0].get("$schema") == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "Portable plugin manifest has an unsupported schema")
    skill_entries = sorted(name for name in plugin if re.fullmatch(r"skills/[^/]+/SKILL\.md", name))
    require(skill_entries == ["skills/ai-development-workflow/SKILL.md"],
            "Plugin must expose exactly one canonical main skill")
    metadata = runtime.get("agents/openai.yaml", b"").decode("utf-8")
    require(f"AI Development Workflow v{version}" in metadata,
            "Main skill interface version is stale")
    plugin_links = validate_links(plugin, "full plugin")
    report = {
        "status": "passed", "version": version, "runtime_files": len(runtime),
        "plugin_files": len(plugin), "commands": len(commands),
        **counts, "launcher_aliases": len(aliases),
        "agent_registry_fingerprint": registry["fingerprint"],
        "plugin_skills": len(skill_entries), "public_modes": [m["id"] for m in catalogue["publicModes"]],
        "catalogue_fingerprint": catalogue["catalogueFingerprint"], "internal_operations": catalogue["counts"].get("stage", 0),
        "runtime_relative_links": runtime_links,
        "plugin_relative_links": plugin_links, "relative_code_imports": import_count,
        "boundary": "Source/package integrity only; no host installation, worker dispatch or publication.",
    }
    return runtime, plugin, report


def with_manifest(members: dict[str, bytes], version: str, kind: str) -> dict[str, bytes]:
    require("PACKAGE-CONTENTS.json" not in members, "Manifest name collides with source")
    manifest = {
        "schema": "ai-development-workflow/package-contents-v1", "version": version,
        "format": kind, "files": [
            {"path": name, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
            for name, content in sorted(members.items())
        ],
        "note": "This manifest lists all other archive files; it does not hash itself.",
    }
    return {**members, "PACKAGE-CONTENTS.json": (json.dumps(manifest, indent=2) + "\n").encode()}


def write_zip(path: Path, members: dict[str, bytes]) -> dict:
    temp = path.with_suffix(path.suffix + ".tmp")
    try:
        with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, content in sorted(members.items()):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED,
                                 compresslevel=9)
        with zipfile.ZipFile(temp) as archive:
            require(archive.testzip() is None, f"Archive CRC failure: {path.name}")
            require(set(archive.namelist()) == set(members), f"Archive inventory mismatch: {path.name}")
            for name, expected in members.items():
                require(archive.read(name) == expected, f"Archive byte mismatch: {name}")
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()
    content = path.read_bytes()
    return {"name": path.name, "path": str(path), "files": len(members), "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest()}


def build_release(root: Path, output_dir: Path) -> dict:
    root, output_dir = root.resolve(), output_dir.resolve()
    for protected in RUNTIME_DIRS | {"packaging", "tools"}:
        require(not output_dir.is_relative_to(root / protected),
                "Output directory must be outside runtime, packaging and tools source directories")
    runtime, plugin, report = load_sources(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    version = report["version"]
    report["archives"] = [
        write_zip(output_dir / f"ai-development-workflow-v{version}-local-skill.zip",
                  with_manifest(runtime, version, "standalone-skill")),
        write_zip(output_dir / f"ai-development-workflow-v{version}-plugin.zip",
                  with_manifest(plugin, version, "full-plugin")),
    ]
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate all sources without writing archives")
    parser.add_argument("--output-dir", type=Path, default=Path("dist"),
                        help="Archive destination relative to the current working directory (default: dist)")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        report = load_sources(root)[2] if args.check else build_release(root, args.output_dir)
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as error:
        print(f"PACKAGE ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
