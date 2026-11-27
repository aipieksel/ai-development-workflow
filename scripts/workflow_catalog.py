#!/usr/bin/env python3
"""Read workflow resources and validate a focused task selection.

This helper validates declarations, dependencies and scope. It does not select
work for the user, authenticate evidence, create records, dispatch agents or
execute stages. Catalogue roots are read as data; foreign Python is not run.

A compact selection supplies a reasoned chain and relevant specialist IDs.
Optional evaluated rows record useful recipe choices or compatibility decisions;
there is no requirement to reject every unrelated catalogue entry.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

from agent_registry import load_registry, resolve_profile


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
INTENTS = {"implement", "assess", "plan", "review", "research", "docs"}
SCOPES = {"record-only", "test-output-only", "tests-only", "repo-write-scoped", "docs-only"}
LIMITATIONS = [
    "Structural selection validation only; the host must judge relevance and proportionality.",
    "No execution, scheduling, agent spawn, host installation, or source mutation is performed.",
    "Evidence references are not opened or authenticated; actual record, review, approval, and revision gates still apply.",
    "A valid selection does not prove independent review, passing tests, completed work, or executed proof files.",
]
RECIPE_KINDS = {"pipeline", "recipe"}
UI_SPECIALIST = "specialist:ui-design"
SEARCH_SCHEMA = "ai-development-workflow/search-index-v1"
DISCOVERY_SCHEMA = "ai-development-workflow/discovery-v1"
SELECTION_SCHEMA = "ai-development-workflow/selection-v2"
GENERATED_REFERENCE_EXCLUSIONS = {
    "references/workflow-index.md": "generated complete catalogue; indexing it would duplicate every resource",
    "references/workflow-search-index.json": "generated search output; it cannot be part of its own source corpus",
}
BASELINE_REFERENCES = [
    "references/workflow-contract.md",
    "references/task-routing.md",
    "references/automatic-selection.md",
    "references/progress-announcements.md",
]
# These are explicit catalogue operation IDs, never keywords in user prose.
UI_OPERATIONS = {
    "command:G7", "command:GDA", "command:GDS",
    "stage:design-ui", "stage:review-ui-spec", "stage:review-ui",
}

# This is an explicit translation of the two shipped artifact vocabularies,
# not a request classifier or a claim that similarly named workflows are equal.
ARTIFACT_ALIASES = {
    "assessment": "assessment.report", "research": "research.report",
    "design_audit": "design.audit", "architecture": "architecture.advice",
    "design_spec": "ui.spec", "plan": "code.plan", "plan_review": "plan.review",
    "red_tests": "tdd.red.evidence", "implementation": "execution.result",
    "unit_verification": "test.results", "e2e_verification": "e2e.results",
    "code_review": "review.findings", "security_verification": "security.review",
    "accessibility_verification": "accessibility.review",
    "performance_verification": "performance.results", "documentation": "docs.change",
}
COMMAND_SCOPES = {
    **{code: "record-only" for code in (
        "GPL", "GCP", "GAS", "GRS", "GDA", "GAA", "GDS", "GPP", "GPR", "GVR", "GVS", "GVA", "GRC"
    )},
    **{code: "test-output-only" for code in ("GUT", "GVE", "GVP")},
    **{code: "repo-write-scoped" for code in ("GEX", "GTE", "GCL")},
    "GTF": "tests-only", "GVD": "docs-only",
}


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def _json(text, context):
    def invalid_constant(value):
        raise ValueError("Non-finite JSON value: " + value)
    try:
        return json.loads(text, object_pairs_hook=_object, parse_constant=invalid_constant)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{context}: {exc}") from exc


def _string(value, context):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(context + " must be a nonempty string")
    return value


def _strings(value, context):
    if not isinstance(value, list):
        raise ValueError(context + " must be a list of strings")
    for item in value:
        _string(item, context)
    if len(value) != len(set(value)):
        raise ValueError(context + " contains duplicate values")
    return list(value)


def _mapping(value, context):
    if not isinstance(value, dict):
        raise ValueError(context + " must be an object")
    return value


def _slug(value, context):
    _string(value, context)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise ValueError(context + " is not a valid ID")
    return value


def _safe_file(root, relative):
    _string(relative, "Package path")
    path = PurePosixPath(relative)
    if (path.is_absolute() or "\\" in relative or ":" in relative or "\0" in relative
            or any(part in {"", ".", ".."} for part in relative.split("/"))):
        raise ValueError("Unsafe package path: " + relative)
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Unsafe symlink in package path: " + relative)
    if not current.is_file() or not current.resolve().is_relative_to(root):
        raise ValueError("Unknown or unsafe package file: " + relative)
    return current


def _read(root, relative, digests):
    data = _safe_file(root, relative).read_bytes()
    digests[relative] = hashlib.sha256(data).hexdigest()
    return data.decode("utf-8")


def _profile(relative):
    _string(relative, "Profile path")
    slug = r"[a-z0-9]+(?:-[a-z0-9]+)*"
    if not re.fullmatch(rf"(?:agents/{slug}/agent\.md|workflows/agents/{slug}/agent\.md|specialists/(?:profiles/)?{slug}\.md)", relative):
        raise ValueError("Unknown or unsafe profile path: " + relative)
    return relative


def _artifact(value):
    return ARTIFACT_ALIASES.get(value, value)


def _artifacts(values, context):
    return list(dict.fromkeys(_artifact(value) for value in _strings(values, context)))


def _skill_root(root):
    root = Path(root).expanduser().resolve(strict=True)
    if (root / "skills" / "ai-development-workflow").is_dir():
        root = (root / "skills" / "ai-development-workflow").resolve()
    if not root.is_dir():
        raise ValueError("Catalogue root must be an existing skill or plugin directory")
    return root


def _command_data(root, digests):
    """Read the router's entire command set, including picker-hidden commands."""
    if root == DEFAULT_ROOT:
        old_bytecode = sys.dont_write_bytecode
        sys.dont_write_bytecode = True
        added_path = str(DEFAULT_ROOT / "scripts") not in sys.path
        if added_path:
            sys.path.insert(0, str(DEFAULT_ROOT / "scripts"))
        try:
            router = importlib.import_module("route_workflow")
            if Path(router.__file__).resolve() != DEFAULT_ROOT / "scripts" / "route_workflow.py":
                raise ValueError("Imported router is not the bundled route_workflow")
            # Reload the same declarative loader which owns ROUTES/COMMAND_FILES,
            # so a long-lived caller cannot retain metadata from before an edit.
            routes, _, files, _ = router.load_commands()
        finally:
            sys.dont_write_bytecode = old_bytecode
            if added_path:
                sys.path.remove(str(DEFAULT_ROOT / "scripts"))
        paths = [files[code] for code in routes]
        if set(files) != set(routes):
            raise ValueError("Router command IDs and files disagree")
    else:
        routes = None
        paths = [p.relative_to(root).as_posix() for p in (root / "commands").rglob("ai-dev-*.md")]
        paths += [p.relative_to(root).as_posix() for p in (root / "agents").glob("*/commands/ai-dev-*.md")]
    records, seen_orders, seen_ids = [], set(), set()
    for relative in paths:
        text = _read(root, relative, digests)
        if not text.startswith("---\n") or "\n---" not in text[4:]:
            raise ValueError("Command metadata missing: " + relative)
        spec = _mapping(_json(text[4:].split("\n---", 1)[0], relative), relative)
        code = _string(spec.get("command"), relative + " command")
        order = spec.get("order")
        if not re.fullmatch(r"G[0-9A-Z]+", code) or code in seen_ids:
            raise ValueError("Duplicate or invalid command ID: " + code)
        if type(order) is not int or order < 0 or order in seen_orders:
            raise ValueError("Command order must contain unique nonnegative integers")
        if Path(relative).stem != spec.get("launcher"):
            raise ValueError("Command filename and launcher disagree: " + relative)
        seen_orders.add(order)
        seen_ids.add(code)
        if routes is not None:
            if code not in routes or files[code] != relative:
                raise ValueError("Router and command metadata disagree")
            route = routes[code]
        else:
            route = dict(spec)
            calls = spec.get("agentCalls", [])
            if not isinstance(calls, list):
                raise ValueError("Command agentCalls must be a list")
            route["agentCalls"] = [
                {**_mapping(call, "Command agent call"), "file": "agents/" + _slug(call.get("agent"), "Command agent") + "/agent.md"}
                for call in calls
            ]
            if spec.get("activeAgent") is not None:
                agent = _slug(spec["activeAgent"], "Active command agent")
                route["activeAgent"] = {"agent": agent, "file": f"agents/{agent}/agent.md"}
        records.append((order, code, relative, spec, route))
    if not records:
        raise ValueError("No command files found")
    return sorted(records, key=lambda value: value[0])


def _portable_recipes(root, digests, operations, specialist_ids):
    """Read portable recommendations as data; never dispatch or load package code."""
    relative = "task-recipes/catalog.json"
    if (root / "task-recipes").is_symlink():
        raise ValueError("Unsafe symlink in portable recipe directory")
    if not (root / relative).exists() and not (root / relative).is_symlink():
        # Older installed cores remain valid alternate catalogue roots.
        return []
    data = _mapping(_json(_read(root, relative, digests), relative), relative)
    _read(root, "task-recipes/README.md", digests)
    if set(data) != {"schemaVersion", "recipes"} or type(data["schemaVersion"]) is not int or data["schemaVersion"] != 1:
        raise ValueError("Unsupported portable recipe catalogue contract")
    if not isinstance(data["recipes"], list) or not data["recipes"]:
        raise ValueError("Portable recipe catalogue requires a nonempty recipes list")
    entries, seen = [], set()
    required_fields = {"id", "label", "summary", "instructions", "expansion", "recommendedSpecialists", "writeScope", "useWhen", "avoidWhen"}
    for spec in data["recipes"]:
        _mapping(spec, "Portable recipe")
        if not required_fields <= set(spec) or set(spec) - required_fields - {"requiredBindings"}:
            raise ValueError("Portable recipe fields are missing or unknown")
        slug = _slug(spec["id"], "Portable recipe ID")
        identity = "recipe:" + slug
        if identity in seen:
            raise ValueError("Duplicate portable recipe ID: " + identity)
        seen.add(identity)
        instructions = _string(spec["instructions"], identity + " instructions")
        if instructions != "task-recipes/" + slug + ".md":
            raise ValueError("Portable recipe handler must match its ID: " + identity)
        _read(root, instructions, digests)
        expansion = _strings(spec["expansion"], identity + " expansion")
        if not expansion or any(value not in operations or operations[value]["workflowKind"] != "stage" for value in expansion):
            raise ValueError("Portable recipe requires existing atomic operations: " + identity)
        lenses = _strings(spec["recommendedSpecialists"], identity + " recommendedSpecialists")
        if not set(lenses) <= specialist_ids:
            raise ValueError("Unknown portable recipe specialist: " + identity)
        scopes = {operations[value]["writeScope"] for value in expansion}
        scope = spec["writeScope"]
        # A recipe's advertised ceiling cannot hide a writer in its expansion.
        permits = {
            "record-only": {"record-only"},
            "test-output-only": {"record-only", "test-output-only"},
            "tests-only": {"record-only", "test-output-only", "tests-only"},
            "docs-only": {"record-only", "test-output-only", "docs-only"},
            "repo-write-scoped": SCOPES,
        }
        if not isinstance(scope, str) or scope not in permits or not scopes <= permits[scope]:
            raise ValueError("Portable recipe scope does not cover its operations: " + identity)
        bindings = _mapping(spec.get("requiredBindings", {}), identity + " requiredBindings")
        required = {}
        for stage, values in bindings.items():
            if stage not in expansion:
                raise ValueError("Portable recipe binding names an operation outside its expansion")
            required[stage] = _artifacts(values, identity + " binding")
        available = {"request", "repo.snapshot"}
        for stage in expansion:
            operation = operations[stage]
            needed = set(operation.get("requiresAll", [])) | set(operation.get("portableRequiresAll", [])) | set(required.get(stage, []))
            if needed - available:
                raise ValueError(identity + " has unsatisfied ordered prerequisites for " + stage + ": " + ", ".join(sorted(needed - available)))
            any_needed = set(operation.get("requiresAny", []))
            if any_needed and not any_needed & available:
                raise ValueError(identity + " has unsatisfied alternative prerequisites for " + stage)
            produced = set(operation.get("produces", []))
            if "code.plan" in produced:
                available.difference_update({"plan.review", "tdd.red.evidence", "execution.result"})
            if "plan.review" in produced:
                available.discard("tdd.red.evidence")
            available.update(produced)
        entries.append({
            "id": identity, "kind": "recipe", "workflowKind": "recipe",
            "label": _string(spec["label"], identity + " label"),
            "summary": _string(spec["summary"], identity + " summary"),
            "instructions": instructions, "profiles": [], "expansion": expansion,
            "recommendedSpecialists": lenses, "writeScope": scope,
            "useWhen": _strings(spec["useWhen"], identity + " useWhen"),
            "avoidWhen": _strings(spec["avoidWhen"], identity + " avoidWhen"),
            "requiredBindings": required,
            "invocation": "/ai-development-workflow recipe " + slug,
            "requiresNativeHost": False,
        })
    return entries


def public_modes(root=DEFAULT_ROOT, digests=None):
    """Read the five public controls from their single declarative source."""
    root = _skill_root(root)
    digests = {} if digests is None else digests
    relative = "modes/catalog.json"
    data = _mapping(_json(_read(root, relative, digests), relative), relative)
    if (set(data) != {"schemaVersion", "default", "modes"}
            or type(data["schemaVersion"]) is not int or data["schemaVersion"] != 1
            or data["default"] != "auto" or not isinstance(data["modes"], list)):
        raise ValueError("Unsupported public mode catalogue")
    expected = {
        "auto": ("task-defined", "", True),
        "plan": ("record-only", "012", True),
        "build": ("repo-write-scoped", "0123", True),
        "review": ("record-only", "", True),
        "loop": ("repo-write-scoped", "", True),
    }
    fields = {"id", "label", "summary", "instructions", "writeScope", "stages", "requiresIndependentAgents", "requiresActualWorkers", "minimumContributors"}
    modes = []
    for row in data["modes"]:
        _mapping(row, "Public mode")
        if set(row) != fields or row.get("id") not in expected:
            raise ValueError("Unknown public mode or fields")
        for field in ("label", "summary", "instructions"):
            _string(row[field], "Public mode " + field)
        scope, stages, independent = expected[row["id"]]
        if (row["writeScope"] != scope or row["stages"] != stages
                or row["requiresIndependentAgents"] is not independent or row["requiresActualWorkers"] is not True
                or type(row["minimumContributors"]) is not int or row["minimumContributors"] != 2):
            raise ValueError("Public mode changes its declared scope or independence: " + row["id"])
        _read(root, row["instructions"], digests)
        modes.append(dict(row))
    if [row["id"] for row in modes] != list(expected):
        raise ValueError("Public modes must be exactly auto, plan, build, review and loop")
    return modes


def portable_modes(root, digests=None):
    """Read the canonical Loop descriptor; saved XR checkpoint schemas stay valid."""
    root = _skill_root(root)
    digests = {} if digests is None else digests
    relative = "modes/loop.json"
    spec = _mapping(_json(_read(root, relative, digests), relative), relative)
    fields = {"schemaVersion", "id", "label", "launcher", "summary", "instructions",
              "profiles", "references", "writeScope", "requiresNativeHost",
              "requiresIndependentAgents", "monitorIntervalSeconds",
              "monitorPreference", "monitorFallbacks", "minimumContributors", "capabilities", "noRepairCorroboration"}
    if set(spec) != fields:
        raise ValueError("Portable mode fields are missing or unknown")
    if type(spec["schemaVersion"]) is not int or spec["schemaVersion"] != 1:
        raise ValueError("Unsupported portable mode contract")
    if spec["id"] != "loop" or spec["launcher"] != "ai-dev-loop":
        raise ValueError("Unknown portable mode identity or launcher")
    if (spec["writeScope"] != "repo-write-scoped" or spec["requiresNativeHost"] is not False
            or spec["requiresIndependentAgents"] is not True):
        raise ValueError("Loop must preserve scoped writes and independent agents")
    if (type(spec["monitorIntervalSeconds"]) is not int or spec["monitorIntervalSeconds"] != 300
            or spec["monitorPreference"] != "wait-first"
            or spec["monitorFallbacks"] != ["native-timer", "active-session"]):
        raise ValueError("Loop requires wait-first 300-second checks, then supported timer or active-session monitoring")
    profiles = _strings(spec["profiles"], "Loop profiles")
    if profiles != ["agents/reviewer/agent.md", "agents/builder/agent.md", "agents/verification-engineer/agent.md"]:
        raise ValueError("Loop requires canonical Reviewer, Builder and no-repair Verifier profiles")
    if (type(spec["minimumContributors"]) is not int or spec["minimumContributors"] != 2
            or spec["capabilities"] != ["loop-review", "loop-execution"]
            or spec["noRepairCorroboration"] != "independent-verifier-then-original-reviewer-acknowledgement"):
        raise ValueError("Loop requires two useful contributors and acknowledged independent no-repair corroboration")
    references = _strings(spec["references"], "Loop references")
    required = {"references/loop-artifacts.md", "references/loop-timers.md", "scripts/loop_checklist.py", "references/browser-recovery.md"}
    if not required <= set(references) or spec["instructions"] != "references/loop-mode.md":
        raise ValueError("Loop requires its authoritative handler and supporting contracts")
    for path in [spec["instructions"], *profiles, *references]:
        _read(root, path, digests)
    return [{
        "id": "mode:loop", "kind": "mode", "workflowKind": "loop",
        "label": _string(spec["label"], "Loop label"),
        "summary": _string(spec["summary"], "Loop summary"),
        "instructions": spec["instructions"], "profiles": profiles,
        "references": references, "writeScope": spec["writeScope"],
        "launcher": spec["launcher"], "invocation": "/ai-development-workflow loop",
        "aliases": ["XR", "ai-dev-execute-review"],
        "requiresNativeHost": False, "requiresIndependentAgents": True,
        "monitorIntervalSeconds": spec["monitorIntervalSeconds"],
        "monitorPreference": spec["monitorPreference"], "monitorFallbacks": spec["monitorFallbacks"],
        "minimumContributors": 2, "capabilities": list(spec["capabilities"]),
        "noRepairCorroboration": spec["noRepairCorroboration"],
    }]


def build_catalog(root=DEFAULT_ROOT):
    """Return a deterministic, complete catalogue; never mutate the package."""
    root = _skill_root(root)
    digests, entries = {}, []
    registry = load_registry(root)
    digests.update(registry["sourceDigests"])
    # These shared instructions govern every selection and admission path.
    # Hash source rules only; live phase/roster state belongs in the task record.
    for relative in ("references/workflow-contract.md", "references/workflow-contract-records.md",
                     "references/progress-announcements.md", "references/task-routing.md", "scripts/task_policy.py", "scripts/agent_registry.py"):
        _read(root, relative, digests)
    for order, code, relative, spec, route in _command_data(root, digests):
        kind = route.get("kind", "pipeline")
        if kind not in {"stage", "pipeline"}:
            raise ValueError("Unknown command kind: " + code)
        scope = "repo-write-scoped" if kind == "pipeline" else spec.get("writeScope", COMMAND_SCOPES.get(code))
        if scope not in SCOPES:
            raise ValueError("Command needs an explicit known write scope: " + code)
        calls = []
        for call in route.get("agentCalls", []):
            role = resolve_profile(call["file"], call.get("operation"), capabilities=call.get("capabilities"), registry=registry)
            calls.append({**call, **role})
        profiles = [call["profile"] for call in calls]
        if route.get("activeAgent"):
            profiles.append(route["activeAgent"]["file"])
        queue = _mapping(route.get("queue", {}), code + " queue")
        entries.append({
            "id": "command:" + code, "kind": "command", "workflowKind": kind,
            "label": _string(route.get("label"), code + " label"),
            "summary": _string(spec.get("summary", route.get("label")), code + " summary"),
            "instructions": relative, "profiles": sorted(set(profiles)),
            "workerDuties": [{key: call[key] for key in ("family", "profile", "capabilities", "operation", "when")} for call in calls],
            "minimumContributors": 2,
            "pickerVisible": route.get("pickerVisible", True), "order": order,
            "writeScope": scope, "invocation": "/" + spec["launcher"],
            "requiresAll": _artifacts(queue.get("requiresAll", []), code + " requiresAll"),
            "requiresAny": _artifacts(queue.get("requiresAny", []), code + " requiresAny"),
            "produces": _artifacts(queue.get("produces", []), code + " produces"),
            "hostRequirements": _strings(route.get("requires", []), code + " host requirements"),
        })

    primary_modes = public_modes(root, digests)
    for mode in primary_modes:
        if mode["id"] in {"auto", "loop"}:
            continue
        produced = {
            "plan": ["code.plan", "plan.review"],
            "build": ["code.plan", "plan.review", "execution.result", "test.results"],
            "review": ["review.findings"],
        }[mode["id"]]
        entries.append({
            "id": "mode:" + mode["id"], "kind": "mode", "workflowKind": "pipeline",
            "label": mode["label"], "summary": mode["summary"],
            "instructions": mode["instructions"], "profiles": [],
            "writeScope": mode["writeScope"], "requiresAll": ["request", "repo.snapshot"],
            "requiresAny": [], "produces": produced,
            "invocation": "/ai-development-workflow " + mode["id"],
            "requiresIndependentAgents": mode["requiresIndependentAgents"],
            "requiresActualWorkers": True, "minimumContributors": 2,
        })
    entries.extend(portable_modes(root, digests))

    operation_path = "workflows/catalog.json"
    operation_data = _mapping(_json(_read(root, operation_path, digests), operation_path), operation_path)
    if (operation_data.get("catalogContract") != "ai-development-workflow/operations-v1"
            or type(operation_data.get("schemaVersion")) is not int
            or operation_data["schemaVersion"] != 1):
        raise ValueError("Unsupported internal operation catalogue")
    _read(root, "workflows/operation-policy.md", digests)
    stages = operation_data.get("stages")
    agents = operation_data.get("agents")
    if not isinstance(stages, list) or not stages or not isinstance(agents, list):
        raise ValueError("Operation catalogue requires stages and agent profiles")
    for name, values in (("stageCount", stages), ("agentCount", agents)):
        if type(operation_data.get(name)) is not int or operation_data[name] != len(values):
            raise ValueError("Operation catalogue declared " + name + " does not match its entries")
    for spec in stages:
        _mapping(spec, "Stage")
        identity = "stage:" + _slug(spec.get("id"), "Stage ID")
        scope = spec.get("writeScope")
        if scope not in SCOPES:
            raise ValueError("Unknown stage write scope: " + identity)
        if (scope in {"repo-write-scoped", "tests-only", "docs-only"}
                and spec.get("requiresPlanApproval") is not True):
            raise ValueError("A writing operation requires a reviewed plan: " + identity)
        role = resolve_profile(spec.get("agentPath"), spec["id"], scope, capabilities=spec.get("capabilities"), registry=registry)
        if spec.get("agentId") != role["family"]:
            raise ValueError("Operation owner disagrees with the canonical registry: " + identity)
        entries.append({
            "id": identity, "kind": "stage", "workflowKind": "stage",
            "label": _string(spec.get("label"), identity + " label"),
            "summary": _string(spec.get("summary", spec.get("description")), identity + " summary"),
            "instructions": _string(spec.get("instructions"), identity + " instructions"),
            "profiles": [role["profile"]], "family": role["family"], "capabilities": role["capabilities"],
            "minimumContributors": 2,
            "writeScope": scope, "category": spec.get("category", ""),
            "requiresAll": _artifacts(spec.get("consumes", []), identity + " consumes"),
            "requiresAny": [], "produces": _artifacts(spec.get("produces", []), identity + " produces"),
            "requiresPlanApproval": spec.get("requiresPlanApproval", False),
        })

    specialist_path = "specialists/catalog.json"
    specialist_data = _json(_read(root, specialist_path, digests), specialist_path)
    specialists = specialist_data if isinstance(specialist_data, list) else _mapping(specialist_data, specialist_path).get("specialists")
    if not isinstance(specialists, list):
        raise ValueError("Specialist catalogue requires a specialists list")
    source_path = "specialists/sources.json"
    sources = []
    if (root / source_path).is_file():
        source_data = _mapping(_json(_read(root, source_path, digests), source_path), source_path)
        sources = source_data.get("sources")
    if not isinstance(sources, list):
        raise ValueError("Specialist sources must be a list")
    source_ids = [_string(_mapping(item, "Source").get("id"), "Source ID") for item in sources]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Duplicate specialist source ID")
    for spec in specialists:
        _mapping(spec, "Specialist")
        identity = "specialist:" + _slug(spec.get("id"), "Specialist ID")
        references = _strings(spec.get("sources", []), identity + " sources")
        if not set(references) <= set(source_ids):
            raise ValueError("Unknown specialist source: " + identity)
        dependencies = _strings(spec.get("references", []), identity + " references")
        for relative in dependencies:
            # Authoritative linked rules must invalidate stale selections too.
            # Alternate packages are read as UTF-8 data, never imported.
            _read(root, relative, digests)
        entries.append({
            "id": identity, "kind": "specialist", "workflowKind": "lens",
            "label": _string(spec.get("label"), identity + " label"),
            "summary": _string(spec.get("summary"), identity + " summary"),
            "profiles": [_string(spec.get("profile"), identity + " profile")],
            "useWhen": _strings(spec.get("useWhen"), identity + " useWhen"),
            "avoidWhen": _strings(spec.get("avoidWhen"), identity + " avoidWhen"),
            "sources": references, "acceptance": _strings(spec.get("acceptance"), identity + " acceptance"),
            **({"references": dependencies} if "references" in spec else {}),
            "writeScope": "inherit-stage",
        })
    # Explicit executor prerequisites remain visible in the catalogue and index.
    portable_inputs = {
        "command:GEX": ["code.plan", "plan.review"],
        "command:GTE": ["code.plan", "plan.review", "tdd.red.evidence"],
        "stage:execute-plan": ["code.plan", "plan.review"],
        "stage:fix-reviewed-defects": ["code.plan", "plan.review"],
    }
    for entry in entries:
        extra = [value for value in portable_inputs.get(entry["id"], [])
                 if value not in entry.get("requiresAll", [])]
        if extra:
            entry["portableRequiresAll"] = extra
    entries.extend(_portable_recipes(
        root, digests,
        {entry["id"]: entry for entry in entries if entry["kind"] in {"command", "stage"}},
        {entry["id"] for entry in entries if entry["kind"] == "specialist"},
    ))
    counts = Counter(entry["id"] for entry in entries)
    if any(count != 1 for count in counts.values()):
        raise ValueError("Duplicate catalogue entry ID")

    # Inventory real files, including profiles which no selected command uses.
    profiles = set()
    for pattern in ("agents/*/agent.md", "workflows/agents/*/agent.md", "specialists/*.md", "specialists/profiles/*.md"):
        for path in root.glob(pattern):
            relative = path.relative_to(root).as_posix()
            # README/SOURCES files are documentation, not instruction profiles.
            if pattern.startswith("specialists/") and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*\.md", path.name):
                continue
            profiles.add(relative)
    for agent in operation_data["agents"]:
        profiles.add(_profile(_mapping(agent, "Agent profile").get("path")))
    for entry in entries:
        if "instructions" in entry:
            _read(root, entry["instructions"], digests)
        profiles.update(_profile(relative) for relative in entry["profiles"])
    inventory = []
    for relative in sorted(profiles):
        _profile(relative)
        text = _read(root, relative, digests)
        frontmatter = text.split("---", 2)[1] if text.startswith("---\n") else ""
        match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", frontmatter)
        if match:
            heading = match[1].replace("-", " ").title()
        else:
            heading, fence = None, None
            for line in text.splitlines():
                stripped = line.lstrip()
                boundary = re.match(r"^(`{3,}|~{3,})", stripped)
                if boundary:
                    token = boundary[1]
                    if fence is None:
                        fence = token
                    elif token[0] == fence[0] and len(token) >= len(fence):
                        fence = None
                    continue
                if fence is None and line.startswith("# "):
                    heading = line[2:].strip()
                    break
            heading = heading or Path(relative).parent.name
        inventory.append({
            "path": relative, "label": heading,
            "type": ("core-family" if relative in {row["profile"] for row in registry["families"].values()}
                     else "compatibility-profile" if relative in registry["legacyProfiles"] else "domain-lens"),
            "usedBy": [entry["id"] for entry in entries if relative in entry["profiles"]],
        })
    result = {
        "schema": "ai-development-workflow/catalogue/v1",
        "entries": entries, "profiles": inventory, "agentRegistry": registry,
        "coreFamilies": [{"id": family, **row} for family, row in registry["families"].items()],
        "counts": dict(sorted(Counter(entry["kind"] for entry in entries).items())),
        "sources": sources, "publicModes": primary_modes, "sourceDigests": dict(sorted(digests.items())),
        "limitations": list(LIMITATIONS),
    }
    from task_policy import descriptor
    result["taskPolicy"] = descriptor()
    encoded = json.dumps(result, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    result["catalogueFingerprint"] = hashlib.sha256(encoded).hexdigest()
    return result


def _cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_index(catalog):
    """Render every option and every discovered profile, without choosing any."""
    lines = ["# Complete AI Development Workflow catalogue", "",
             "Catalogue fingerprint: `" + catalog["catalogueFingerprint"] + "`", "",
             "Reference material for selected work. Load relevant handlers and their prerequisites; specialist lenses inherit the chosen operation's scope.", ""]
    lines += ["## Public controls", "", "| Mode | Purpose | Scope |", "| --- | --- | --- |"]
    for mode in catalog["publicModes"]:
        lines.append("| " + " | ".join(_cell(value) for value in (mode["id"], mode["summary"], mode["writeScope"])) + " |")
    lines.append("")
    lines += ["## Six canonical worker families", "", "The coordinator is additional. Every new task needs at least two useful actual worker contributions; profiles and capabilities are not running agents.", "", "| Family | Instruction owner |", "| --- | --- |"]
    for family in catalog["coreFamilies"]:
        lines.append("| " + _cell(family["label"]) + " | [" + family["id"] + "](../" + family["profile"] + ") |")
    lines.append("")
    for kind, title in (("command", "All commands, including hidden compatibility commands"),
                        ("mode", "Public mode contracts"),
                        ("stage", "Internal workflow operations"),
                        ("recipe", "Portable task recipes — adapt to current scope"),
                        ("specialist", "Specialist instruction profiles")):
        lines += ["## " + title, "", "| ID | Option | Scope | Summary |", "| --- | --- | --- | --- |"]
        for entry in catalog["entries"]:
            if entry["kind"] != kind:
                continue
            label = entry["label"]
            if entry.get("pickerVisible") is False:
                label += " (hidden compatibility command)"
            target = entry.get("instructions") or entry["profiles"][0]
            label = "[" + label + "](../" + target + ")"
            lines.append("| " + " | ".join(_cell(value) for value in (entry["id"], label, entry["writeScope"], entry["summary"])) + " |")
        lines.append("")
    lines += ["## Dependencies and recipe expansions", ""]
    for entry in catalog["entries"]:
        details = []
        for key, label in (("requiresAll", "needs all"), ("requiresAny", "needs one"),
                           ("portableRequiresAll", "ordinary-agent additional inputs"), ("produces", "produces")):
            if entry.get(key):
                details.append(label + ": " + ", ".join(entry[key]))
        if entry.get("expansion"):
            details.append(" → ".join(entry["expansion"]))
        if entry.get("requiredBindings"):
            details.append("additional recipe inputs: " + json.dumps(entry["requiredBindings"], sort_keys=True))
        if entry.get("recommendedSpecialists"):
            details.append("recommended lenses: " + ", ".join(entry["recommendedSpecialists"]))
        if details:
            lines.append("- **" + entry["id"] + "** — " + "; ".join(details))
    lines += ["", "## Portable recipe selection", "",
              "Adapt these starting patterns to actual scope and evidence. Expand selected operations in dependency order and preserve read-only and continuation boundaries. Recommended lenses do not assert running agents.", ""]
    for entry in catalog["entries"]:
        if entry["kind"] != "recipe":
            continue
        lines += ["### " + entry["id"], "", entry["summary"], ""]
        for key, label in (("useWhen", "Use when"), ("avoidWhen", "Avoid when")):
            lines += ["**" + label + ":**", ""] + ["- " + value for value in entry[key]] + [""]
    lines += ["## Specialist selection and acceptance", ""]
    for entry in catalog["entries"]:
        if entry["kind"] != "specialist":
            continue
        lines += ["### " + entry["id"], "", entry["summary"], ""]
        for key, label in (("useWhen", "Use when"), ("avoidWhen", "Avoid when"), ("acceptance", "Acceptance evidence")):
            lines += ["**" + label + ":**", ""] + ["- " + value for value in entry[key]] + [""]
        lines += ["Profile: `" + entry["profiles"][0] + "`.", ""]
        if entry["sources"]:
            lines += ["Sources: " + ", ".join(entry["sources"]) + ".", ""]
        if entry.get("references"):
            lines += ["Authoritative references: " + ", ".join(
                "[" + relative + "](../" + relative + ")" for relative in entry["references"]
            ) + ".", ""]
    lines += ["## Existing profile inventory", "",
              "Six core families are active roster choices. Compatibility entries preserve old paths and operation boundaries; domain lenses add knowledge. None proves running workers.", "",
              "| Profile path | Type | Label | Used by |", "| --- | --- | --- | --- |"]
    for profile in catalog["profiles"]:
        lines.append("| " + " | ".join(_cell(value) for value in (profile["path"], profile["type"], profile["label"], ", ".join(profile["usedBy"]) or "Inventory only")) + " |")
    lines += ["", "## Validation limits", ""] + ["- " + value for value in catalog["limitations"]]
    return "\n".join(lines) + "\n"


def _plain_markdown(text):
    """Return searchable prose without treating examples, links or formatting as metadata."""
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token[0]
            elif token[0] == fence:
                fence = None
            continue
        if fence is None:
            lines.append(line)
    value = "\n".join(lines)
    value = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"[`*_>#|]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _search_terms(value):
    stop = {"and", "or", "the", "a", "an", "to", "of", "in", "on", "for", "from",
            "with", "without", "is", "are", "be", "this", "that", "not", "selected",
            "select", "recipe", "recipes", "specialist", "specialists", "reference",
            "references", "resource", "resources", "task"}
    stop.update({"work", "working"})
    terms = []
    for token in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", value.lower()):
        if len(token) < 2 or token in stop:
            continue
        terms.append(token)
        if token.endswith("ies") and len(token) > 4:
            terms.append(token[:-3] + "y")
        elif token.endswith("s") and len(token) > 3 and not token.endswith("ss"):
            terms.append(token[:-1])
    return set(terms)


def _query_terms(value):
    """Split a small explicit exclusion vocabulary from positive search terms.

    This is intentionally not general natural-language negation. A marker applies
    until punctuation or a contrast word; conjunctions keep named terms excluded.
    """
    positive, negative, excluded = [], [], False
    for token in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*|[,.;:]", value.lower()):
        if token in {",", ".", ";", ":"}:
            excluded = False
            continue
        if token in {"but", "however", "while"}:
            excluded = False
            continue
        if token in {"no", "not", "without", "exclude", "excluding"}:
            excluded = True
            continue
        (negative if excluded else positive).append(token)
    return _search_terms(" ".join(positive)), _search_terms(" ".join(negative))


def _reference_summary(text):
    title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), "Reference")
    paragraphs = re.split(r"\n\s*\n", text)
    summary = ""
    for paragraph in paragraphs:
        clean = _plain_markdown(paragraph)
        if clean and clean != title and not clean.lower().startswith(("contents", "```")):
            summary = clean
            break
    return title, summary[:500]


def build_search_index(root=DEFAULT_ROOT, catalog=None):
    """Build a deterministic candidate index from authoritative runtime sources."""
    root = _skill_root(root)
    catalog = build_catalog(root) if catalog is None else catalog
    resources = []
    for entry in catalog["entries"]:
        if entry["kind"] not in {"recipe", "specialist", "stage", "command", "mode"}:
            continue
        path = entry.get("instructions") or (entry.get("profiles") or [""])[0]
        related = list(entry.get("recommendedSpecialists", []))
        related += list(entry.get("expansion", []))
        related += ["reference:" + Path(value).stem for value in entry.get("references", [])
                    if value.startswith("references/")]
        resources.append({
            "id": entry["id"], "kind": entry["kind"], "title": entry["label"],
            "path": path, "summary": entry.get("summary", ""),
            "useWhen": list(entry.get("useWhen", [])),
            "avoidWhen": list(entry.get("avoidWhen", [])),
            "related": list(dict.fromkeys(related)),
            "body": "",
        })
    registry = catalog["agentRegistry"]
    for identity, spec in sorted(registry["capabilities"].items()):
        resources.append({
            "id": "capability:" + identity, "kind": "capability",
            "title": identity.replace("-", " ").title(), "path": spec["instructions"],
            "summary": "Capability for " + ", ".join(spec["families"]) + ": " + identity.replace("-", " ") + ".",
            "useWhen": [], "avoidWhen": [],
            "related": ["family:" + family for family in spec["families"]], "body": "",
        })
    eligible = []
    for path in sorted((root / "references").glob("*.md")):
        relative = path.relative_to(root).as_posix()
        if relative in GENERATED_REFERENCE_EXCLUSIONS:
            continue
        text = _read(root, relative, {})
        title, summary = _reference_summary(text)
        eligible.append(relative)
        resources.append({
            "id": "reference:" + path.stem, "kind": "reference", "title": title,
            "path": relative, "summary": summary, "useWhen": [], "avoidWhen": [],
            "related": [], "body": _plain_markdown(text)[:12000],
        })
    resources.sort(key=lambda row: (row["kind"], row["id"]))
    core = {
        "schema": SEARCH_SCHEMA,
        "catalogueFingerprint": catalog["catalogueFingerprint"],
        "baselineReferences": list(BASELINE_REFERENCES),
        "eligibleReferences": eligible,
        "excludedReferences": [
            {"path": path, "reason": reason}
            for path, reason in sorted(GENERATED_REFERENCE_EXCLUSIONS.items())
        ],
        "resources": resources,
        "limitations": [
            "Search returns explainable candidates; it does not select a workflow, grant authority, dispatch workers or prove semantic applicability.",
            "Refine the request query with inspected project evidence when ownership, stack or impact is initially unknown.",
            "A recorded instruction path cannot prove that a model intellectually read or applied it; independent review checks the effect.",
        ],
    }
    encoded = json.dumps(core, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return {**core, "indexFingerprint": hashlib.sha256(encoded).hexdigest()}


def search_resources(initial_query, search_index, *, refined_query=None, limit=5, kinds=None):
    """Rank bounded groups deterministically; source-grounded judgment still selects resources."""
    if not isinstance(initial_query, str) or not initial_query.strip():
        raise ValueError("Task discovery requires a nonempty initial query")
    if refined_query is not None and (not isinstance(refined_query, str) or not refined_query.strip()):
        raise ValueError("Refined discovery query must be nonempty when supplied")
    if type(limit) is not int or limit < 1 or limit > 50:
        raise ValueError("Discovery limit must be between 1 and 50")
    query = (refined_query or initial_query).strip()
    query_terms, excluded_terms = _query_terms(query)
    if not query_terms:
        raise ValueError("Task discovery query has no searchable positive terms")
    allowed = set(kinds or {"recipe", "specialist", "operation", "reference"})
    unknown = allowed - {"recipe", "specialist", "operation", "reference"}
    if unknown:
        raise ValueError("Unknown discovery kinds: " + ", ".join(sorted(unknown)))
    kind_group = {"recipe": "recipe", "specialist": "specialist", "reference": "reference",
                  "stage": "operation", "command": "operation", "mode": "operation", "capability": "operation"}
    scored = []
    for resource in search_index["resources"]:
        group = kind_group[resource["kind"]]
        if group not in allowed:
            continue
        fields = {
            "id": resource["id"], "title": resource["title"], "path": resource["path"],
            "summary": resource["summary"], "useWhen": " ".join(resource["useWhen"]),
            "body": resource["body"], "avoidWhen": " ".join(resource["avoidWhen"]),
        }
        weights = {"id": 14, "title": 12, "useWhen": 9, "summary": 7, "path": 4, "body": 1}
        matches, score = [], 0
        for field, weight in weights.items():
            terms = sorted(query_terms & _search_terms(fields[field]))
            if terms:
                score += weight * len(terms)
                matches.append({"field": field, "terms": terms})
        normalized_query = re.sub(r"\s+", " ", query.lower()).strip()
        if normalized_query and normalized_query in (resource["id"] + " " + resource["title"]).lower():
            score += 20
            matches.append({"field": "exact", "terms": [normalized_query]})
        avoided = sorted(query_terms & _search_terms(fields["avoidWhen"]))
        if avoided:
            score -= 5 * len(avoided)
            matches.append({"field": "avoidWhen", "terms": avoided})
        excluded_identity = sorted(excluded_terms & (_search_terms(fields["id"])
                                                      | _search_terms(fields["title"])
                                                      | _search_terms(fields["useWhen"])))
        if excluded_identity:
            continue
        excluded_context = sorted(excluded_terms & (_search_terms(fields["summary"])
                                                     | _search_terms(fields["path"])
                                                     | _search_terms(fields["body"])))
        if excluded_context:
            score -= 20 * len(excluded_context)
            matches.append({"field": "explicit-exclusion", "terms": excluded_context})
        if score > 0:
            scored.append({"id": resource["id"], "kind": resource["kind"], "group": group,
                           "title": resource["title"], "path": resource["path"],
                           "score": score, "matched": matches, "related": resource["related"]})
    # A relevant recipe makes its declared lenses visible without forcing their selection.
    recipe_scores = {row["id"]: row["score"] for row in scored if row["kind"] == "recipe"}
    boosts = Counter()
    for resource in search_index["resources"]:
        if resource["id"] in recipe_scores:
            for related in resource["related"]:
                if related.startswith("specialist:"):
                    boosts[related] = max(boosts[related], max(1, recipe_scores[resource["id"]] // 4))
    for row in scored:
        if row["id"] in boosts:
            row["score"] += boosts[row["id"]]
            row["matched"].append({"field": "recipe-recommendation", "terms": ["related"]})
    groups = {name: [] for name in ("recipes", "specialists", "operations", "references")}
    labels = {"recipe": "recipes", "specialist": "specialists", "operation": "operations", "reference": "references"}
    for group in labels:
        rows = sorted((row for row in scored if row["group"] == group), key=lambda row: (-row["score"], row["id"]))
        groups[labels[group]] = rows[:limit]
    return {
        "schema": "ai-development-workflow/search-results-v1",
        "initialQuery": initial_query.strip(), "refinedQuery": refined_query.strip() if refined_query else None,
        "effectiveQuery": query, "excludedTerms": sorted(excluded_terms),
        "indexFingerprint": search_index["indexFingerprint"],
        "candidateOnly": True, "baselineReferences": search_index["baselineReferences"],
        "groups": groups, "limitations": list(search_index["limitations"]),
    }


def _ordered_subset(needles, haystack):
    cursor = iter(haystack)
    return all(any(value == needle for value in cursor) for needle in needles)


def validate_discovery(discovery, selection, search_index):
    """Validate a compact current receipt without claiming that paths prove comprehension."""
    errors = []
    resources = {row["id"]: row for row in search_index["resources"]}
    required = {"schema", "initialQuery", "refinedQuery", "indexFingerprint", "matches",
                "selected", "recipeRecommendations"}
    if not isinstance(discovery, dict) or set(discovery) != required:
        return ["Current discovery receipt requires exactly " + ", ".join(sorted(required))]
    if discovery.get("schema") != DISCOVERY_SCHEMA:
        errors.append("Unsupported discovery receipt schema")
    if discovery.get("indexFingerprint") != search_index["indexFingerprint"]:
        errors.append("Discovery index fingerprint is missing or stale")
    if not isinstance(discovery.get("initialQuery"), str) or not discovery["initialQuery"].strip():
        errors.append("Discovery initialQuery must be nonempty")
    refined = discovery.get("refinedQuery")
    if refined is not None and (not isinstance(refined, str) or not refined.strip()):
        errors.append("Discovery refinedQuery must be null or nonempty")
    matches, seen = discovery.get("matches"), set()
    if not isinstance(matches, list):
        errors.append("Discovery matches must be a list")
        matches = []
    for row in matches:
        if (not isinstance(row, dict) or set(row) != {"id", "score"}
                or row.get("id") not in resources or row.get("id") in seen
                or not isinstance(row.get("score"), (int, float))):
            errors.append("Discovery matches need unique known IDs and numeric scores")
            continue
        seen.add(row["id"])
    if isinstance(matches, list) and isinstance(discovery.get("initialQuery"), str) and discovery["initialQuery"].strip():
        try:
            report = search_resources(discovery["initialQuery"], search_index,
                                      refined_query=discovery.get("refinedQuery"))
            actual = {(row["id"], row["score"]) for rows in report["groups"].values() for row in rows}
            for row in matches:
                if isinstance(row, dict) and set(row) == {"id", "score"} and (row.get("id"), row.get("score")) not in actual:
                    errors.append("Discovery match is not in the current grouped search result: " + str(row.get("id")))
        except (TypeError, ValueError) as error:
            errors.append("Discovery queries are not executable against the current index: " + str(error))
    selected, selected_ids = discovery.get("selected"), set()
    if not isinstance(selected, list):
        errors.append("Discovery selected must be a list")
        selected = []
    for row in selected:
        fields = {"id", "reason", "instructionPaths", "assignment", "question", "acceptance"}
        if not isinstance(row, dict) or set(row) != fields or row.get("id") not in resources:
            errors.append("Each discovered selection needs a known ID, reason, instruction paths, assignment, question and acceptance")
            continue
        identity = row["id"]
        if identity in selected_ids:
            errors.append("Discovery selected contains duplicate ID: " + identity)
        selected_ids.add(identity)
        if identity not in seen:
            errors.append("Discovered selection is absent from the recorded matched shortlist: " + identity)
        if not all(isinstance(row.get(key), str) and row[key].strip() for key in ("reason", "assignment", "question")):
            errors.append("Discovered selections need substantive reasons and assignment questions: " + identity)
        paths = row.get("instructionPaths")
        if not isinstance(paths, list) or not paths or len(paths) != len(set(paths)) or not all(isinstance(path, str) and path for path in paths):
            errors.append("Discovered selections need distinct instruction paths: " + identity)
        elif resources[identity]["path"] not in paths:
            errors.append("Discovered selection omits its authoritative instruction path: " + identity)
        acceptance = row.get("acceptance")
        if not isinstance(acceptance, list) or not acceptance or not all(isinstance(value, str) and value.strip() for value in acceptance):
            errors.append("Discovered selection needs specialist/resource-specific acceptance: " + identity)
    declared_lenses = selection.get("specialists")
    lenses = (set(declared_lenses) if isinstance(declared_lenses, list)
              else {identity for identity in selected_ids
                    if identity in resources and resources[identity]["kind"] == "specialist"})
    for identity in lenses:
        if identity not in selected_ids:
            errors.append("Selected specialist lacks a discovery selection receipt: " + identity)
    for identity in selected_ids:
        if resources[identity]["kind"] == "specialist" and identity not in lenses:
            errors.append("Discovered specialist is absent from selection.specialists: " + identity)
    decisions = discovery.get("recipeRecommendations")
    if not isinstance(decisions, list):
        errors.append("recipeRecommendations must be a list")
        decisions = []
    evaluated = {row.get("id"): row for row in selection.get("evaluated", []) if isinstance(row, dict)}
    selected_recipes = {identity for identity, row in evaluated.items()
                        if identity in resources and resources[identity]["kind"] == "recipe"
                        and row.get("disposition") in {"selected", "covered"}}
    selected_recipes.update(identity for identity in selected_ids
                            if identity in resources and resources[identity]["kind"] == "recipe")
    expected = {(recipe, lens) for recipe in selected_recipes for lens in resources[recipe]["related"]
                if lens.startswith("specialist:")}
    observed = set()
    for row in decisions:
        if (not isinstance(row, dict) or set(row) != {"recipe", "specialist", "disposition", "reason"}
                or (row.get("recipe"), row.get("specialist")) in observed
                or row.get("disposition") not in {"selected", "not-applicable"}
                or not isinstance(row.get("reason"), str) or not row["reason"].strip()):
            errors.append("Recipe recommendations need unique recipe/specialist selected-or-not-applicable decisions with reasons")
            continue
        pair = (row["recipe"], row["specialist"])
        observed.add(pair)
        if row["disposition"] == "selected" and row["specialist"] not in lenses:
            errors.append("Selected recipe recommendation is absent from specialists: " + row["specialist"])
    if expected != observed:
        errors.append("Selected recipes require a focused disposition for every recommended specialist")
    return errors


def validate_selection(selection, catalog, search_index=None, *, execution=False):
    """Return a structural report; never read evidence, execute, or grant approval."""
    errors = []
    by_id = {entry["id"]: entry for entry in catalog["entries"]}
    result = {"valid": False, "errors": errors, "catalogueFingerprint": catalog["catalogueFingerprint"],
              "checkedEntryCount": 0, "catalogueEntryCount": len(by_id), "limitations": list(LIMITATIONS)}
    if not isinstance(selection, dict):
        errors.append("Selection must be an object")
        return result
    allowed = {"selectionSchema", "discovery", "catalogueFingerprint", "intent", "request", "evaluated", "chain", "specialists", "existingEvidence", "uiContext", "reason",
               "mode", "originMode", "routing", "delegation", "reviewPolicy", "phases", "verificationContext"}
    if set(selection) - allowed:
        errors.append("Unknown selection fields: " + ", ".join(sorted(set(selection) - allowed)))
    if selection.get("catalogueFingerprint") != catalog["catalogueFingerprint"]:
        errors.append("Catalogue fingerprint is missing or stale; reconcile the selected chain with the current catalogue")
    schema = selection.get("selectionSchema")
    if schema is None:
        result["discoveryStatus"] = "legacy-reconciliation-required"
        result["limitations"].append("Legacy selection remains readable, but new execution requires current task discovery reconciliation.")
        if execution:
            errors.append("Legacy selection requires current task discovery reconciliation before execution")
    elif schema != SELECTION_SCHEMA:
        errors.append("Unsupported selectionSchema")
    elif "discovery" not in selection:
        errors.append("Current selection requires a discovery receipt")
    else:
        if search_index is None:
            search_index = build_search_index(DEFAULT_ROOT, catalog if catalog.get("catalogueFingerprint") else None)
        discovery_errors = validate_discovery(selection["discovery"], selection, search_index)
        errors.extend(discovery_errors)
        result["discoveryStatus"] = "current" if not discovery_errors else "invalid"
    intent = selection.get("intent")
    if not isinstance(intent, str) or intent not in INTENTS:
        errors.append("Intent must be implement, assess, plan, review, research, or docs")
    if not isinstance(selection.get("request"), str) or not selection["request"].strip():
        errors.append("Request must be a nonempty summary")
    from task_policy import validate_policy
    from workflow_contract import SCHEMA, selection as contract_selection
    policy_selection = {key: selection.get(key) for key in
                        ("mode", "originMode", "reason", "routing", "delegation", "reviewPolicy", "phases", "uiContext", "verificationContext")}
    policy_selection["workflow"] = "catalogue-selection"
    try:
        # Reuse the contract's ordered phase representation and its exact policy.
        _, phases = contract_selection({"schema": SCHEMA, "selection": policy_selection}, registry=catalog["agentRegistry"])
        validate_policy(policy_selection, phases, profile_paths={row["path"] for row in catalog["profiles"]}, registry=catalog["agentRegistry"])
    except (ValueError, TypeError, KeyError) as error:
        errors.append(str(error))

    if "reason" in selection and (not isinstance(selection["reason"], str) or not selection["reason"].strip()):
        errors.append("Selection reason must be a nonempty explanation")
    if not selection.get("evaluated") and not (isinstance(selection.get("reason"), str) and selection["reason"].strip()):
        errors.append("Compact selection needs a reason for the chosen workflow")
    if "uiContext" not in selection:
        errors.append("Selection needs uiContext applicability and reason")

    ui_applicable = None
    if "uiContext" in selection:
        ui_context = selection["uiContext"]
        if not isinstance(ui_context, dict) or set(ui_context) != {"applicable", "kind", "reason"}:
            errors.append("uiContext requires exactly applicable, kind and reason")
        else:
            if type(ui_context["applicable"]) is not bool:
                errors.append("uiContext applicable must be a boolean")
            else:
                ui_applicable = ui_context["applicable"]
            if not isinstance(ui_context["reason"], str) or not ui_context["reason"].strip():
                errors.append("uiContext reason must be a nonempty explanation of host judgment")

    evaluated, chain, lenses = {}, [], []
    for field, fields in (("evaluated", {"id", "disposition", "reason", "coveredBy"}), ("chain", {"id", "why"})):
        rows = selection.get(field, [] if field == "evaluated" else None)
        if not isinstance(rows, list):
            errors.append(field + " must be a list")
            continue
        seen = set()
        for index, row in enumerate(rows):
            context = f"{field}[{index}]"
            if not isinstance(row, dict):
                errors.append(context + " must be an object")
                continue
            if set(row) - fields:
                errors.append(context + " has unknown fields")
            identity = row.get("id")
            if isinstance(identity, str) and identity.lower() == "mode:xr":
                identity = "mode:loop"
            if not isinstance(identity, str) or identity not in by_id:
                errors.append(context + " contains an unknown entry ID")
                continue
            if identity in seen:
                errors.append(field + " contains duplicate ID " + identity)
            seen.add(identity)
            reason = row.get("reason" if field == "evaluated" else "why")
            if not isinstance(reason, str) or not reason.strip():
                errors.append(context + " needs a nonempty reason")
            if field == "evaluated":
                if not isinstance(row.get("disposition"), str) or row["disposition"] not in {"selected", "covered", "not-applicable"}:
                    errors.append(context + " has an invalid disposition")
                evaluated[identity] = row
            else:
                chain.append(identity)
    if not chain:
        errors.append("Chain must contain at least one workflow step")
    if not isinstance(selection.get("specialists"), list):
        errors.append("specialists must be a list of specialist IDs")
    else:
        for identity in selection["specialists"]:
            if not isinstance(identity, str) or identity not in by_id or by_id[identity]["kind"] != "specialist":
                errors.append("Unknown or non-specialist lens ID")
            elif identity in lenses:
                errors.append("Duplicate specialist lens ID: " + identity)
            else:
                lenses.append(identity)

    # Old alternate-root catalogues remain valid. In current catalogues this
    # checks declared/explicit UI scope, not the correctness of semantic intent.
    if UI_SPECIALIST in by_id:
        visual_operations = UI_OPERATIONS.intersection(chain)
        if visual_operations and ui_applicable is False:
            errors.append("uiContext cannot exclude UI for explicit visual operations: "
                          + ", ".join(sorted(visual_operations)))
        if (ui_applicable is True or visual_operations) and UI_SPECIALIST not in lenses:
            errors.append("UI scope requires the selected " + UI_SPECIALIST + " lens")

    selected_ids = set(chain) | set(lenses)
    bindings = {}
    for identity, row in evaluated.items():
        entry, disposition = by_id[identity], row.get("disposition")
        if identity in selected_ids and disposition != "selected":
            errors.append("Chain/lens entry must be selected: " + identity)
        if "coveredBy" in row and disposition != "covered":
            errors.append("coveredBy is only valid for covered recipe decisions: " + identity)
        if isinstance(disposition, str) and disposition in {"selected", "covered"} and identity not in selected_ids:
            if entry["kind"] not in RECIPE_KINDS:
                errors.append("Selected/covered entry is absent from chain/lenses: " + identity)
                continue
            expansion = entry["expansion"]
            coverage = row.get("coveredBy", expansion)
            if (not isinstance(coverage, list) or not coverage or any(not isinstance(v, str) for v in coverage)
                    or len(set(coverage)) != len(coverage)):
                errors.append("Recipe coverage must be a nonempty list of unique stage IDs: " + identity)
                continue
            if disposition == "selected" and coverage != expansion:
                errors.append("Selected recipe requires its complete expansion: " + identity)
            if not _ordered_subset(coverage, expansion) or not _ordered_subset(coverage, chain):
                errors.append("Recipe coverage must appear in recipe and chain order: " + identity)
            if coverage == expansion or entry["kind"] == "recipe":
                for stage, values in entry.get("requiredBindings", {}).items():
                    if stage in coverage:
                        bindings.setdefault(stage, set()).update(values)

    known_artifacts = {"request", "repo.snapshot"}
    for entry in by_id.values():
        for key in ("requiresAll", "requiresAny", "portableRequiresAll", "produces"):
            known_artifacts.update(entry.get(key, []))
        for values in entry.get("requiredBindings", {}).values():
            known_artifacts.update(values)
    available = {"request", "repo.snapshot"}
    evidence = selection.get("existingEvidence", [])
    if not isinstance(evidence, list):
        errors.append("existingEvidence must be a list of artifact/record references")
    else:
        seen_artifacts = set()
        for record in evidence:
            if not isinstance(record, dict) or set(record) != {"artifact", "record"}:
                errors.append("Each existingEvidence item requires exactly artifact and record")
                continue
            name, reference = record["artifact"], record["record"]
            if not isinstance(name, str) or _artifact(name) not in known_artifacts:
                errors.append("Unknown existingEvidence artifact")
                continue
            name = _artifact(name)
            if not isinstance(reference, str) or not reference.strip():
                errors.append("existingEvidence record must be a nonempty stable reference")
                continue
            if name in seen_artifacts:
                errors.append("Duplicate existingEvidence artifact: " + name)
            seen_artifacts.add(name)
            available.add(name)
    allowed_scopes = SCOPES if intent == "implement" else {"record-only", "test-output-only"}
    if intent == "docs":
        allowed_scopes = allowed_scopes | {"docs-only"}
    declared_phases = selection.get("phases", [])
    if isinstance(declared_phases, list):
        for phase in declared_phases:
            if isinstance(phase, dict) and phase.get("writeScope") not in allowed_scopes | {"read-only", "none"}:
                errors.append("Intent does not permit selected phase scope: " + str(phase.get("id")))
        writes_selected = any(isinstance(phase, dict) and phase.get("writeScope") in
                              {"repo-write-scoped", "tests-only", "docs-only", "external-write"}
                              for phase in declared_phases)
    else:
        writes_selected = False
    for identity in chain:
        entry = by_id[identity]
        if entry["kind"] not in {"command", "stage", "mode"}:
            errors.append("Chain needs concrete atomic command/stage IDs or one portable mode; expand recipes and list lenses separately: " + identity)
            continue
        if entry["kind"] == "mode" and len(chain) != 1:
            errors.append("A public mode must be the only chain item: " + identity)
        if entry["workflowKind"] == "pipeline" and len(chain) != 1:
            errors.append("A whole command pipeline must be the only chain item: " + identity)
        if entry["writeScope"] not in allowed_scopes:
            errors.append("Intent does not permit " + entry["writeScope"] + ": " + identity)
        if entry["writeScope"] in {"repo-write-scoped", "tests-only", "docs-only", "external-write"} and not writes_selected:
            errors.append("Writing operation requires declared specialist execution and independent acceptance phases: " + identity)
        if selection.get("mode") in {"plan", "review"} and entry["writeScope"] in {"repo-write-scoped", "tests-only", "docs-only", "external-write"}:
            errors.append("Concrete mode does not permit product writes: " + identity)
        if entry["kind"] == "mode" and identity != "mode:" + str(selection.get("mode")):
            errors.append("Selected public mode disagrees with the concrete mode: " + identity)
        needed = (set(entry.get("requiresAll", []))
                  | set(entry.get("portableRequiresAll", []))
                  | bindings.get(identity, set()))
        missing = needed - available
        if missing:
            errors.append(identity + " requires prior evidence: " + ", ".join(sorted(missing)))
        any_needed = set(entry.get("requiresAny", []))
        if any_needed and not any_needed & available:
            errors.append(identity + " requires prior evidence of at least one: " + ", ".join(sorted(any_needed)))
        produced = set(entry.get("produces", []))
        if "code.plan" in produced:
            # A newly produced plan cannot reuse an older review or RED receipt.
            available.difference_update({"plan.review", "tdd.red.evidence", "execution.result"})
        if "plan.review" in produced:
            available.discard("tdd.red.evidence")
        available.update(produced)
    result.update(valid=not errors, chain=chain, specialists=lenses,
                  actualWorkerAdmission="requires-current-task-contract",
                  checkedEntryCount=len(set(chain) | set(lenses) | set(evaluated)))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Skill root or plugin root; read declarative data only")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--validate-selection", type=Path, metavar="FILE", help="Validate a proposed JSON selection without executing it")
    parser.add_argument("--execution", action="store_true", help="Require a current discovery receipt for selection validation")
    parser.add_argument("--search", metavar="TASK", help="Return grouped candidate resources for literal task prose")
    parser.add_argument("--refined-query", help="Use project/source evidence to refine the initial task query")
    parser.add_argument("--kinds", nargs="+", choices=("recipe", "specialist", "operation", "reference"))
    parser.add_argument("--limit", type=int, default=5, help="Maximum candidates per resource kind (1-50)")
    parser.add_argument("--write-search-index", type=Path, metavar="FILE", help="Write the deterministic generated JSON index")
    parser.add_argument("--write-index", type=Path, metavar="FILE", help="Write the deterministic generated Markdown catalogue")
    args = parser.parse_args(argv)
    try:
        catalog = build_catalog(args.root)
        search_index = build_search_index(args.root, catalog)
        if args.write_index:
            args.write_index.write_text(markdown_index(catalog), encoding="utf-8")
            print(json.dumps({"status": "written", "path": str(args.write_index),
                              "catalogueFingerprint": catalog["catalogueFingerprint"]}, indent=2))
            return 0
        if args.write_search_index:
            args.write_search_index.write_text(json.dumps(search_index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(json.dumps({"status": "written", "path": str(args.write_search_index),
                              "indexFingerprint": search_index["indexFingerprint"]}, indent=2))
            return 0
        if args.search is not None:
            report = search_resources(args.search, search_index, refined_query=args.refined_query,
                                      limit=args.limit, kinds=args.kinds)
            if args.format == "json":
                print(json.dumps(report, indent=2, ensure_ascii=False))
            else:
                print("Task discovery candidates (candidate-only):")
                for group, rows in report["groups"].items():
                    print("\n" + group.title() + ":")
                    for row in rows:
                        fields = ", ".join(match["field"] for match in row["matched"])
                        print(f"- {row['id']} ({row['score']}) — {row['path']} [{fields}]")
                print("\n" + " ".join(report["limitations"]))
            return 0
        if args.validate_selection:
            selection = _json(args.validate_selection.read_text(encoding="utf-8"), "Selection JSON")
            report = validate_selection(selection, catalog, search_index, execution=args.execution)
            if args.format == "json":
                print(json.dumps(report, indent=2, ensure_ascii=False))
            else:
                print("Selection structure is valid." if report["valid"] else "Selection structure is invalid.")
                for error in report["errors"]:
                    print("- " + error)
                print("\n" + " ".join(LIMITATIONS))
            return 0 if report["valid"] else 2
        print(json.dumps(catalog, indent=2, ensure_ascii=False) if args.format == "json" else markdown_index(catalog), end="\n" if args.format == "json" else "")
        return 0
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        if args.format == "json":
            print(json.dumps({"valid": False, "errors": [str(exc)], "limitations": LIMITATIONS}, indent=2))
        else:
            print("Catalogue/selection error: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
