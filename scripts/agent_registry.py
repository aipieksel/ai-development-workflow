"""Read the canonical role/capability registry as data, never as executable code.

This resolver names instruction owners. It does not dispatch workers, establish
their identities, or extend an operation's allowed write scope.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {"investigator", "architect", "builder", "ui-design-director", "reviewer", "verification-engineer"}
OPERATIONS = {
    "research-technical", "discover-contributions", "assess-codebase", "diagnose-failure", "extract-behaviour-spec",
    "plan-goals", "design-architecture", "plan-code", "plan-tests", "design-ui", "write-red-tests", "execute-plan",
    "fix-reviewed-defects", "update-docs", "review-ui-spec", "review-plan", "review-code", "review-dependencies",
    "verify-goal", "verify-docs", "run-tests", "run-e2e", "review-ui", "review-accessibility", "review-security", "verify-performance",
}
WRITE_SCOPES = {"repo-write-scoped", "tests-only", "docs-only"}


def _require(condition, message):
    if not condition:
        raise ValueError("agent registry: " + message)


def _object(pairs):
    value = {}
    for key, item in pairs:
        _require(key not in value, "duplicate JSON key " + key)
        value[key] = item
    return value


def _slug(value):
    return isinstance(value, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) is not None


def _strings(value, *, nonempty=True):
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(isinstance(item, str) and item.strip() for item in value)
            and len(value) == len(set(value)))


def _file(root, relative):
    _require(isinstance(relative, str) and relative, "instruction path must be nonblank")
    path = PurePosixPath(relative)
    _require(not path.is_absolute() and not any(part in {"", ".", ".."} for part in relative.split("/"))
             and not any(character in relative for character in ("\\", ":", "\0", "#")),
             "unsafe instruction path " + relative)
    target = root
    for part in path.parts:
        target /= part
        _require(not target.is_symlink(), "symlinked instruction path " + relative)
    _require(target.is_file() and target.resolve().is_relative_to(root), "missing instruction file " + relative)
    raw = target.read_bytes()
    _require(bool(raw.strip()), "empty instruction file " + relative)
    raw.decode("utf-8")
    return raw


def load_registry(root=ROOT):
    """Validate source closure and return a fingerprinted, declarative registry."""
    root = Path(root).expanduser().resolve(strict=True)
    raw = _file(root, "agents/registry.json")
    data = json.loads(raw, object_pairs_hook=_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError("non-finite JSON value " + value)))
    _require(isinstance(data, dict) and set(data) == {
        "schemaVersion", "domainCatalog", "families", "capabilities", "operations", "operationAliases", "legacyProfiles"},
        "missing or unknown registry fields")
    _require(type(data["schemaVersion"]) is int and data["schemaVersion"] == 1, "unsupported schema version")
    families, capabilities = data["families"], data["capabilities"]
    _require(isinstance(families, dict) and set(families) == FAMILIES, "registry must declare exactly six canonical families")
    files = {"agents/registry.json": raw}
    # Every canonical family adopts this substantive shared contract. It is
    # mandatory runtime input even though it is not a selectable capability.
    common = "agents/capabilities/worker-contract.md"
    files[common] = _file(root, common)
    for family, row in families.items():
        _require(isinstance(row, dict) and set(row) == {"label", "profile"}
                 and isinstance(row["label"], str) and row["label"].strip(), "invalid family " + family)
        _require(row["profile"] == f"agents/{family}/agent.md", "canonical family path mismatch " + family)
        files[row["profile"]] = _file(root, row["profile"])
    _require(isinstance(capabilities, dict) and bool(capabilities), "capabilities must be a nonempty map")
    for identity, row in capabilities.items():
        _require(_slug(identity) and isinstance(row, dict) and set(row) == {"instructions", "families"},
                 "invalid capability " + str(identity))
        _require(_strings(row["families"]) and set(row["families"]) <= FAMILIES, "unknown capability family " + identity)
        files[row["instructions"]] = _file(root, row["instructions"])

    def mapping(row, label):
        _require(isinstance(row, dict) and set(row) == {"family", "capabilities"}, "invalid mapping " + label)
        _require(row["family"] in families and _strings(row["capabilities"]), "unknown family/empty capabilities " + label)
        _require(set(row["capabilities"]) <= capabilities.keys(), "unknown capability " + label)
        _require(all(row["family"] in capabilities[cap]["families"] for cap in row["capabilities"]),
                 "incompatible family/capability mapping " + label)

    _require(isinstance(data["operations"], dict) and set(data["operations"]) == OPERATIONS,
             "registry must preserve all 26 bounded operations")
    for operation, row in data["operations"].items():
        mapping(row, operation)
        _require(operation in row["capabilities"], "operation must retain its own capability " + operation)
    aliases = data["operationAliases"]
    _require(isinstance(aliases, dict) and all(isinstance(key, str) and key.strip() and key not in OPERATIONS
             and value in OPERATIONS for key, value in aliases.items()),
             "operation aliases must point directly to canonical operations; chained/circular aliases are forbidden")
    legacy = data["legacyProfiles"]
    _require(isinstance(legacy, dict) and len(legacy) == 38, "registry must preserve all 38 original profile mappings")
    for path, row in legacy.items():
        _require(re.fullmatch(r"(?:agents|workflows/agents)/[a-z0-9-]+/agent\.md", path) is not None,
                 "invalid legacy profile path " + str(path))
        _require(isinstance(row, dict) and set(row) == {"family", "capabilities", "operationOverrides"},
                 "invalid legacy mapping " + path)
        mapping({key: row[key] for key in ("family", "capabilities")}, path)
        _require(isinstance(row["operationOverrides"], dict), "legacy overrides must be a map " + path)
        for operation, override in row["operationOverrides"].items():
            _require(isinstance(operation, str) and operation.strip(), "invalid legacy operation")
            mapping(override, path + " / " + operation)
        files[path] = _file(root, path)
    _require(data["domainCatalog"] == "specialists/catalog.json", "domain catalogue must remain the shared specialist catalogue")
    files[data["domainCatalog"]] = _file(root, data["domainCatalog"])
    data["sourceDigests"] = {path: hashlib.sha256(contents).hexdigest() for path, contents in sorted(files.items())}
    data["fingerprint"] = hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    return data


def resolve_profile(profile, operation=None, write_scope=None, *, capabilities=None, registry=None, root=ROOT,
                    allow_custom_operation=False):
    """Resolve legacy paths and bounded operations without granting write authority.

    Canonical families plus explicit capabilities disambiguate legacy command
    verbs such as consult/review/test. A known canonical operation retains its
    declared owner; a documented legacy override may change that family.
    """
    registry = load_registry(root) if registry is None else registry
    family_by_path = {row["profile"]: family for family, row in registry["families"].items()}
    legacy = registry["legacyProfiles"].get(profile)
    _require(profile in family_by_path or legacy is not None, "unknown operational profile " + str(profile))
    explicit = capabilities is not None
    if explicit:
        _require(_strings(capabilities), "explicit capabilities must be a distinct nonempty list")
    canonical_operation = registry["operationAliases"].get(operation, operation)
    formal = registry["operations"].get(canonical_operation)
    is_canonical = profile in family_by_path
    # Architect/UI are also original legacy paths. Explicit canonical capability
    # choices must not inherit their old default consult/design specialization.
    override = None if is_canonical and explicit else (legacy or {}).get("operationOverrides", {}).get(operation)
    if override is None and not (is_canonical and explicit):
        override = (legacy or {}).get("operationOverrides", {}).get(canonical_operation)
    if override:
        family, required = override["family"], list(override["capabilities"])
    elif formal:
        family, required = formal["family"], list(formal["capabilities"])
        expected = family_by_path.get(profile, (legacy or {}).get("family"))
        _require(expected == family, "operation/profile family mismatch for " + str(operation))
        if legacy and not is_canonical:
            required += [cap for cap in legacy["capabilities"]
                         if family in registry["capabilities"][cap]["families"]]
    else:
        family = family_by_path.get(profile, (legacy or {}).get("family"))
        required = [] if is_canonical and explicit else list((legacy or {}).get("capabilities", []))
        _require(operation is None or allow_custom_operation or (is_canonical and explicit and operation in {
            "consult", "review", "test", "cleanup", "clean_and_test", "audit_design", "inspect_reference",
            "inspect_original_and_result", "review_current_result", "execute_checklist", "confirm_exact_repair_plan",
            "corroborate", "corroborate_no_repair", "acknowledge_corroboration",
        }), "unmapped operation/profile combination " + str(operation))
    selected = list(dict.fromkeys([*required, *(capabilities or [])]))
    _require(_strings(selected) and set(selected) <= registry["capabilities"].keys(), "missing or unknown selected capability")
    _require(all(family in registry["capabilities"][cap]["families"] for cap in selected),
             "selected capability is incompatible with family " + family)
    _require(write_scope not in WRITE_SCOPES or family == "builder", "only Builder owns an admitted product/test/docs writing operation")
    if write_scope == "tests-only":
        _require(bool({"write-red-tests", "author-e2e", "execute-plan"} & set(selected)), "tests-only operation lacks test-authoring capability")
    if write_scope == "docs-only":
        _require("update-docs" in selected, "docs-only operation requires documentation capability")
    return {"family": family, "profile": registry["families"][family]["profile"],
            "capabilities": list(dict.fromkeys(selected)),
            "instructions": list(dict.fromkeys(registry["capabilities"][cap]["instructions"] for cap in selected)),
            **({"legacyProfile": profile} if not is_canonical else {})}
