"""Focused regressions for the missing-runtime download failure."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "workflow_release_builder", ROOT / "tools/build_release.py"
)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class ReleasePackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)

    def copy_source(self, name="source"):
        source = self.workspace / name
        shutil.copytree(
            ROOT, source,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "dist", ".git"),
        )
        return source

    def test_plain_display_identity_is_independent_from_machine_semver(self):
        source = self.copy_source()
        version = (source / "VERSION").read_text().strip()
        headings = [
            BUILDER.first_h1((source / "README.md").read_text()),
            BUILDER.first_h1((source / "SKILL.md").read_text()),
            BUILDER.first_h1((source / "references/advanced-reference.md").read_text()),
            BUILDER.first_h1((source / "packaging/plugin-template/README.md").read_text()),
        ]
        self.assertTrue(all(heading == BUILDER.DISPLAY_HEADING or
                            heading.startswith(BUILDER.DISPLAY_HEADING + " — ")
                            for heading in headings))
        self.assertTrue(all(version not in heading for heading in headings))
        _, _, report = BUILDER.load_sources(source)
        self.assertEqual(report["version"], version)

    def test_wrong_display_identity_or_release_notes_prevents_release(self):
        versioned_display = BUILDER.DISPLAY_IDENTITY + " — Version " + "2"
        versioned_release_notes = "Version " + "2 introduces"
        mutations = [
            ("README.md", BUILDER.DISPLAY_IDENTITY, versioned_display,
             r"README display identity mismatch"),
            ("SKILL.md", BUILDER.DISPLAY_IDENTITY, versioned_display,
             r"Main skill display identity mismatch"),
            ("references/advanced-reference.md", BUILDER.DISPLAY_IDENTITY,
             versioned_display, r"Advanced reference display identity mismatch"),
            ("agents/openai.yaml", BUILDER.DISPLAY_IDENTITY, versioned_display,
             r"Main skill interface display identity mismatch"),
            ("packaging/plugin-template/README.md", BUILDER.DISPLAY_IDENTITY,
             versioned_display, r"Plugin README display identity mismatch"),
            ("packaging/plugin-template/plugin.json", BUILDER.DISPLAY_IDENTITY,
             versioned_display, r"Plugin display identity mismatch"),
            ("packaging/plugin-template/.codex-plugin/plugin.json", BUILDER.DISPLAY_IDENTITY,
             versioned_display, r"Plugin display identity mismatch"),
            ("packaging/plugin-template/plugin.json", "This release introduces",
             versioned_release_notes, r"Plugin release notes mismatch"),
            ("packaging/plugin-template/.codex-plugin/plugin.json", "This release introduces",
             versioned_release_notes, r"Plugin release notes mismatch"),
        ]
        for index, (name, old, new, message) in enumerate(mutations):
            with self.subTest(path=name, replacement=new):
                source = self.copy_source(f"display-{index}")
                path = source / name
                content = path.read_text()
                self.assertIn(old, content)
                path.write_text(content.replace(old, new, 1))
                with self.assertRaisesRegex(BUILDER.PackageError, message):
                    BUILDER.load_sources(source)

    def test_manifest_semver_mismatch_still_prevents_release(self):
        source = self.copy_source()
        path = source / "packaging/plugin-template/plugin.json"
        content = path.read_text()
        self.assertIn('"version": "2.0.0"', content)
        path.write_text(content.replace('"version": "2.0.0"', '"version": "2.0.1"', 1))
        with self.assertRaisesRegex(BUILDER.PackageError, r"Plugin manifest version mismatch"):
            BUILDER.load_sources(source)

    def test_missing_required_command_prevents_release(self):
        source = self.copy_source()
        (source / "commands/ai-dev-build.md").unlink()
        output = self.workspace / "archives"
        with self.assertRaisesRegex(
            BUILDER.PackageError, r"Missing regular source file: commands/ai-dev-build\.md"
        ):
            BUILDER.build_release(source, output)
        self.assertFalse(output.exists(), "A failed source check must not create release archives")

    def test_both_packages_have_real_runtime_and_exclude_private_development_files(self):
        source = self.copy_source()
        markers = [
            "documents/tasks/development/private-fixture.txt",
            "scripts/tests/package-only-marker.txt",
            "scripts/__pycache__/private-fixture.pyc",
        ]
        for name in markers:
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"Synthetic packaging exclusion fixture.\n")
        report = BUILDER.build_release(source, self.workspace / "archives")
        self.assertEqual(len(report["archives"]), 2)
        self.assertEqual(report["plugin_skills"], 1)
        self.assertEqual(report["launcher_aliases"], 0)
        for key, expected in {"commands": 41, "core_families": 6, "compatibility_profiles": 36,
                              "profile_files": 42, "legacy_profile_mappings": 38,
                              "capability_selectors": 37, "specialist_lenses": 21, "operations": 26}.items():
            self.assertEqual(report[key], expected, key)
        version = (source / "VERSION").read_text().strip()
        paths = {entry["name"]: Path(entry["path"]) for entry in report["archives"]}
        local_path = paths[f"ai-development-workflow-v{version}-local-skill.zip"]
        plugin_path = paths[f"ai-development-workflow-v{version}-plugin.zip"]
        required = {
            "SKILL.md", "commands/ai-dev-build.md", "agents/code-reviewer/agent.md",
            "agents/loop-reviewer/agent.md", "agents/loop-executor/agent.md",
            "scripts/route_workflow.py", "scripts/loop_checklist.py", "scripts/xr_checklist.py",
            "modes/catalog.json", "modes/loop.json", "references/loop-mode.md",
            "references/workflow-search-index.json",
            "workflows/catalog.json", "workflows/operation-policy.md",
            "agents/registry.json", "agents/capabilities/worker-contract.md", "scripts/agent_registry.py",
        }
        # Derive closure from actual source files, independently of the builder's
        # inventory/report, so an omitted command or role cannot validate itself.
        for pattern in ("commands/**/*.md", "agents/**/agent.md", "agents/**/commands/*.md",
                        "agents/capabilities/*.md", "workflows/stages/*.md", "workflows/agents/**/agent.md"):
            required.update(path.relative_to(source).as_posix() for path in source.glob(pattern))
        removed = (
            "agents-pro-v2/", "integrations/workflow-picker/", "integrations/skill-selector/",
            "agents-pro.skill.json", "agents-pro.skill.v2.json", "agents-pro.queue.json",
            "scripts/workflow_picker.py", "references/portable-picker.md",
        )
        for name in removed:
            self.assertFalse((source / name).exists(), name)
        with zipfile.ZipFile(local_path) as local, zipfile.ZipFile(plugin_path) as plugin:
            local_names, plugin_names = set(local.namelist()), set(plugin.namelist())
            self.assertTrue(required <= local_names)
            self.assertFalse(any(name.startswith("skills/") for name in local_names))
            core = "skills/ai-development-workflow/"
            self.assertTrue({core + name for name in required} <= plugin_names)
            self.assertTrue({
                "plugin.json", ".codex-plugin/plugin.json",
                "skills/ai-development-workflow/SKILL.md",
                "skills/ai-development-workflow/agents/openai.yaml",
            } <= plugin_names)
            self.assertEqual(
                {name.split("/")[1] for name in plugin_names if name.startswith("skills/")},
                {"ai-development-workflow"},
            )
            for name in required:
                self.assertEqual(local.read(name), plugin.read(core + name))
                self.assertTrue(local.read(name).strip(), name)
            for names in (local_names, {name.removeprefix(core) for name in plugin_names}):
                self.assertFalse(any(
                    any(name == removed_path or name.startswith(removed_path)
                        for removed_path in removed)
                    for name in names
                ))
            for names in (local_names, plugin_names):
                self.assertFalse(any(
                    "documents/tasks/" in name
                    or "scripts/tests/" in name
                    or "__pycache__" in Path(name).parts
                    or name.startswith(("tools/", "packaging/"))
                    for name in names
                ))

if __name__ == "__main__":
    unittest.main()
