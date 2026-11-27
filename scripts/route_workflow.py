#!/usr/bin/env python3
"""Resolve commands to existing workflows and agent files; never fake a spawn."""
from __future__ import annotations
import argparse
import copy
import json
import re
import sys

# Command files own routing metadata and human-readable command instructions.
from pathlib import Path
from workflow_log import traced
from task_policy import descriptor as task_policy_descriptor, routing_requirements
from agent_registry import load_registry, resolve_profile


def load_commands():
    root = Path(__file__).resolve().parents[1]
    registry = load_registry(root)
    records = []
    paths = list((root / "commands").rglob("ai-dev-*.md"))
    paths += list((root / "agents").glob("*/commands/ai-dev-*.md"))
    for path in paths:
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("Command path escapes the installed skill")
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            raise ValueError("Command metadata missing: " + path.name)
        spec = json.loads(text.split("---", 2)[1])  # JSON is also valid YAML frontmatter.
        if path.stem != spec["launcher"]:
            raise ValueError("Command filename and launcher disagree")
        if spec["stages"] not in {"", "0", "1", "2", "3", "01", "0123", "012", "12"}:
            raise ValueError("Unsupported command stage declaration")
        if type(spec["createsRecord"]) is not bool or spec["recordKind"] not in {"checklist", "development"}:
            raise ValueError("Invalid command record policy")
        spec["commandFile"] = path.relative_to(root).as_posix()
        records.append(spec)
    if any(type(e["order"]) is not int or e["order"] < 0 for e in records) or len({e["order"] for e in records}) != len(records):
        raise ValueError("Command order must contain unique nonnegative integers")
    records.sort(key=lambda entry: entry["order"])
    routes, launchers, files, aliases = {}, {}, {}, {}
    for entry in records:
        code, name = entry["command"], entry["launcher"]
        if not re.fullmatch(r"G[0-9A-Z]+", code) or code in routes or name in launchers:
            raise ValueError("Duplicate or invalid command/launcher")
        calls = []
        for spec in entry["agentCalls"]:
            agent, when, operation = (spec[k] for k in ("agent", "when", "operation"))
            profile = root / "agents" / agent / "agent.md"
            if (not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", agent)
                    or not profile.is_file() or profile.is_symlink()
                    or not profile.resolve().is_relative_to(root.resolve())):
                raise ValueError("Unknown bundled agent or unsafe profile path")
            if when not in {"after_0_before_1", "during_1_before_2", "during_2", "owns_3", "after_3_before_completion", "standalone"}:
                raise ValueError("Invalid agent timing")
            valid_operations = {
                "after_0_before_1": {"assess_codebase", "research", "audit_design", "discover_contributions"},
                "during_1_before_2": {"consult", "inspect_reference"},
                "during_2": {"review_plan"},
                "standalone": {"consult", "design_spec", "write_red_tests", "execute_plan", "execute_tdd", "verify_unit", "verify_e2e", "review", "verify_security", "verify_accessibility", "verify_performance", "update_docs", "cleanup"},
                "owns_3": {"execute_and_test"},
                "after_3_before_completion": {"review", "test", "update_docs", "clean_and_test"},
            }
            if operation not in valid_operations[when]:
                raise ValueError("Agent operation does not match its handoff phase")
            role = resolve_profile(f"agents/{agent}/agent.md", operation, capabilities=spec.get("capabilities"), registry=registry)
            calls.append({"agent": role["family"], "file": role["profile"], "family": role["family"], "capabilities": role["capabilities"], "when": when,
                          "operation": operation, "independent": True,
                          **({"executionWorkflow": "references/executor.md"}
                             if operation in {"execute_and_test", "execute_plan", "execute_tdd"} else {})})
        if sum(c["when"] == "owns_3" for c in calls) > 1:
            raise ValueError("More than one implementation owner")
        routes[code] = {k: entry[k] for k in ("label", "stages", "recordKind", "createsRecord")}
        routes[code]["agentCalls"] = calls
        routes[code]["pickerVisible"] = entry.get("pickerVisible", True)
        routes[code]["kind"] = entry.get("kind", "pipeline")
        routes[code]["queue"] = entry.get("queue", {})
        routes[code]["requires"] = entry.get("requires", [])
        active = entry.get("activeAgent")
        if active is not None:
            if not isinstance(active, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", active):
                raise ValueError("Invalid active agent")
            profile = root / "agents" / active / "agent.md"
            if (not profile.is_file() or profile.is_symlink()
                    or not profile.resolve().is_relative_to(root.resolve())):
                raise ValueError("Unknown bundled active agent or unsafe profile path")
            if calls:
                raise ValueError("Active-agent workflows cannot also declare subagent calls")
            routes[code]["activeAgent"] = {"agent": active, "file": profile.relative_to(root).as_posix(), "independent": False}
        input_aliases = entry.get("inputAliases", [])
        if not isinstance(input_aliases, list) or any(not isinstance(a, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", a) for a in input_aliases):
            raise ValueError("Invalid input aliases")
        if input_aliases:
            routes[code]["inputAliases"] = input_aliases
        launchers[name], files[code] = code, entry["commandFile"]
        for alias in entry.get("aliases", []):
            if not isinstance(alias, str) or not re.fullmatch(r"G[0-9A-Z]+", alias) or alias in aliases:
                raise ValueError("Duplicate or invalid command alias")
            aliases[alias] = code
    input_names = [a for spec in routes.values() for a in spec.get("inputAliases", [])]
    if len(input_names) != len(set(input_names)) or set(input_names) & set(launchers):
        raise ValueError("Duplicate or shadowing input alias")
    if not routes:
        raise ValueError("No command files found")
    if set(aliases) & set(routes):
        raise ValueError("Alias shadows another command")
    return routes, launchers, files, aliases


ROUTES, LAUNCHERS, COMMAND_FILES, COMMAND_ALIASES = load_commands()

MODES = {"0", "01", "012", "013", "0123", "1", "2", "3", "12", "13", "23", "123"}
ALIASES = {"criticize": "2", "criticise": "2", "execute": "3", "revise": "revise", "r": "revise", "resume": "resume"}
HISTORICAL_PRESETS = {"A", "A1", "A2", "A3", "A4", "A0"}
PRIMARY_MODES = {"auto", "plan", "build", "review", "loop"}
LOOP_ALIASES = {"xr", "ai-dev-loop", "ai-dev-execute-review"}


def canonical(name: str) -> str:
    if not isinstance(name, str):
        raise ValueError("Command must be a string.")
    value = name.upper()
    return COMMAND_ALIASES.get(value, value)


def preset_options(name: str) -> dict:
    """Compatibility with existing record helpers, not the retired A profiles."""
    value = canonical(name)
    if value in HISTORICAL_PRESETS:
        return {"label": "Historical record"}
    if value not in ROUTES or value == "G0":
        raise ValueError("Use a development command for a six-file record; G0/GO uses task-checklist.")
    return copy.deepcopy(ROUTES[value])


def selector() -> dict:
    """Return ordinary help; no custom popup or native picker is required."""
    from workflow_catalog import public_modes
    return {"action": "help", "createsRecord": False,
            "choices": [{"id": mode["id"], "label": mode["label"], "summary": mode["summary"]}
                        for mode in public_modes()],
            "workflow": "references/public-modes.md"}


def _with_workflow_contract(result: dict) -> dict:
    """Declare universal obligations; a route is neither admission nor delivery proof."""
    if result["action"] in {"auto", "run", "quick", "follow_up", "inspect", "modular", "recipe", "mode", "help", "select"}:
        result["taskPolicy"] = task_policy_descriptor()
        result["workflowContract"] = {
            "schema": "ai-development-workflow/contract-v2",
            "instructions": "references/workflow-contract.md",
            "announcements": "references/progress-announcements.md",
            "records": "references/workflow-contract-records.md",
            "requiredBeforeWork": ["scope", "proportional-plan", "approach-criticism", "public-briefing"],
            "requiredBeforeProductWrites": ["current-plan", "completed-criticism", "current-briefing", "execution-admission"],
            "requestedStages": result.get("stages", result.get("parentStages", "")),
            "prerequisitesCanBeSkipped": False,
            "preservesRequestedScope": True,
            "actualAgentCountRequiresObservedLifecycle": True,
            "dispatchesAgents": False,
            "provesPublication": False,
            "requiresConcreteMode": True,
            "requiresActualWorkers": True, "minimumContributors": 2,
            "requiresUsefulContributions": True, "requiresAllAuthorIndependence": True,
            "requiresRoutingDecision": True,
        }
    return result


def _resolved_mode(result):
    """Read explicit controls/operation metadata; never infer intent from prose."""
    if result.get("resumeSelectedWorkflow") and result.get("intentBoundary") == "read-only":
        return "review"
    if result.get("mode") in {"plan", "build", "review", "loop"}:
        return result["mode"]
    if result["action"] in {"auto", "help", "select", "recipe"}:
        return None
    if result["action"] == "inspect":
        return "review"
    if result["action"] == "quick":
        return "build"
    stages = result.get("stages", "")
    if "3" in stages:
        return "build"
    calls = result.get("agentCalls", [])
    operations = {call["operation"] for call in calls}
    if operations & {"execute_and_test", "execute_plan", "execute_tdd", "write_red_tests", "update_docs", "cleanup", "clean_and_test"}:
        return "build"
    if operations & {"assess_codebase", "research", "audit_design", "discover_contributions",
                     "review_plan", "review", "verify_unit", "verify_e2e", "verify_security",
                     "verify_accessibility", "verify_performance"} and "1" not in stages:
        return "review"
    if "1" in stages or "0" in stages or operations & {"consult", "design_spec"}:
        return "plan"
    if "2" in stages or operations:
        return "review"
    return None


def apply_routing_decision(result, decision=None):
    """Consume host-declared facts; incomplete descriptors cannot admit work."""
    explicit_mode = _resolved_mode(result)
    result["resolvedMode"] = explicit_mode
    if result.get("resumeSelectedWorkflow") and result.get("mode") in {"build", "loop"} and explicit_mode == "review":
        result["selectedModeContext"] = result["mode"]
    result["routingStatus"] = "needs-source-grounded-decision"
    if decision is None:
        return _with_workflow_contract(result)
    if not isinstance(decision, dict) or set(decision) != {"mode", "routing", "uiContext", "verificationContext"}:
        raise ValueError("Routing decision needs exactly mode, routing, uiContext and verificationContext; actual assignments remain in the selected task contract")
    requirements = routing_requirements(decision["mode"], decision["routing"], decision["uiContext"], decision["verificationContext"])
    mode = decision["mode"]
    if explicit_mode and explicit_mode != mode:
        raise ValueError("Routing decision cannot change the explicit concrete mode or operation intent")
    if result.get("intentBoundary") in {"read-only", "plan-only"} and mode in {"build", "loop"}:
        raise ValueError("Routing decision cannot widen the read-only boundary")
    if result["action"] == "auto" and requirements["impactResolved"]:
        request = result["request"]
        if mode == "build" and requirements["recommendedWorkflow"]:
            # Parse only the selected control. The natural-language task stays
            # literal even when it starts with --record or another control.
            result = _route(requirements["recommendedWorkflow"])
            result["request"] = request
            result["commandFile"] = COMMAND_FILES[result["preset"]]
        else:
            result = primary_mode_route(mode, request)
        result["originMode"] = "auto"
    result.update(resolvedMode=mode, routingDecision=copy.deepcopy(decision),
                  routingRequirements=requirements,
                  routingStatus="resolved" if requirements["impactResolved"] else "assessment-required")
    return _with_ui_policy(result)


def _with_ui_policy(result: dict) -> dict:
    """Describe a conditional host obligation; never classify prose or dispatch.

    Explicit commands keep their stage and write boundaries. A fresh policy
    object per descriptor prevents callers from mutating subsequent routes.
    """
    if result["action"] in {"auto", "run", "quick", "follow_up", "inspect", "modular", "recipe", "mode"}:
        result["uiPolicy"] = {
            "specialist": "specialist:ui-design",
            "profile": "specialists/ui-design.md",
            "instructions": "references/ui-routing.md",
            "applicability": "host-semantic",
            "requiredWhenApplicable": True,
            "inheritsScope": True,
            "dispatchesAgents": False,
        }
        result["discoveryIndex"] = "references/workflow-search-index.json"
        result["discoveryPolicy"] = {
            "schema": "ai-development-workflow/discovery-policy-v1",
            "requiredBeforeFinalSelection": True,
            "initialQuery": "literal-current-request",
            "refineWithProjectEvidence": True,
            "groupedCandidates": ["recipe", "specialist", "operation", "reference"],
            "candidateOnly": True,
            "fallback": "search-packaged-index-with-host-file-tools",
        }
    return _with_workflow_contract(result)


def automatic(request: str) -> dict:
    """Request focused, reasoned selection; never classify prose or run it."""
    return _with_ui_policy({"action": "auto", "mode": "auto", "createsRecord": False, "request": request,
            "agentCalls": [], "workflow": "references/automatic-selection.md",
            "catalogue": "references/workflow-index.md",
            "catalogueTool": "scripts/workflow_catalog.py",
            "requiresFullCatalogueReview": False, "selectionPolicy": "focused",
            "needsTaskContext": not bool(request.strip())})


def modular_route(kind: str, value: str) -> dict:
    """Reject retired native selectors instead of silently choosing implementation."""
    raise ValueError("The native " + kind + " selector has been removed. Use auto, plan, build, review, loop or a portable recipe.")


def portable_recipe_route(value: str) -> dict:
    """Describe a validated portable starting pattern without dispatch or authority."""
    parts = value.split(maxsplit=1)
    if not parts:
        raise ValueError("A portable recipe needs an exact recipe ID.")
    selected_id, request = parts[0], parts[1] if len(parts) > 1 else ""
    # Import lazily: the catalogue itself reads this module's declarative commands.
    from workflow_catalog import build_catalog
    catalog = build_catalog()
    entry = next((item for item in catalog["entries"]
                  if item["kind"] == "recipe" and item["id"] == "recipe:" + selected_id), None)
    if entry is None:
        raise ValueError("Unknown portable recipe ID: " + selected_id)
    return _with_ui_policy({"action": "recipe", "kind": "recipe", "id": selected_id,
            "request": request, "createsRecord": False, "agentCalls": [],
            "workflow": entry["instructions"], "requiresNativeHost": False,
            "adaptsToTaskIntent": True, "writeScope": entry["writeScope"],
            "suggestedExpansion": list(entry["expansion"]),
            "recommendedSpecialists": list(entry["recommendedSpecialists"]),
            "catalogueFingerprint": catalog["catalogueFingerprint"]})


def portable_mode_route(request: str, *, resume: bool = False,
                        selected_preset: str | None = None, read_only: bool = False) -> dict:
    """Describe Loop without allocating a record, dispatching or starting a timer."""
    if read_only and not resume:
        raise ValueError("Read-only intent conflicts with Loop execution; use review or inspect the current run.")
    from workflow_catalog import portable_modes
    entry = portable_modes(Path(__file__).resolve().parents[1])[0]
    result = {"action": "follow_up" if resume else "mode", "mode": "loop",
              "label": entry["label"], "request": request, "createsRecord": False,
              "recordPolicy": "reuse-or-allocate-once", "agentCalls": [],
              "workflow": entry["instructions"], "profiles": list(entry["profiles"]),
              "writeScope": "record-only" if read_only else "repo-write-scoped",
              "requiresNativeHost": False, "requiresIndependentAgents": True,
              "monitorIntervalSeconds": entry["monitorIntervalSeconds"],
              "monitorPreference": entry["monitorPreference"], "monitorFallbacks": entry["monitorFallbacks"],
              "needsTaskContext": not bool(request.strip()), "minimumContributors": 2,
              "noRepairCorroboration": entry["noRepairCorroboration"]}
    if resume:
        result.update(preset=selected_preset, resumeSelectedWorkflow=True)
    elif selected_preset is not None:
        result["preset"] = selected_preset
    if read_only:
        result["intentBoundary"] = "read-only"
    return _with_ui_policy(result)


def primary_mode_route(mode: str, request: str, *, resume: bool = False,
                       selected_preset: str | None = None, read_only: bool = False) -> dict:
    if mode == "loop":
        return portable_mode_route(request, resume=resume, selected_preset=selected_preset, read_only=read_only)
    if mode == "auto":
        result = automatic(request)
        if resume:
            result.update(action="follow_up", preset=selected_preset, resumeSelectedWorkflow=True)
        if read_only:
            result["intentBoundary"] = "read-only"
        return result
    from workflow_catalog import public_modes
    entry = next((entry for entry in public_modes() if entry["id"] == mode), None)
    if entry is None:
        raise ValueError("Unknown public mode: " + mode)
    if read_only and mode == "build" and not resume:
        raise ValueError("Read-only intent conflicts with Build; use plan or review.")
    result = {"action": "follow_up" if resume else "mode", "mode": mode,
              "label": entry["label"], "request": request, "createsRecord": False,
              "recordPolicy": "reuse-or-allocate-once", "agentCalls": [],
              "workflow": entry["instructions"], "stages": entry["stages"],
              "writeScope": "record-only" if read_only else entry["writeScope"],
              "requiresNativeHost": False, "requiresIndependentAgents": entry["requiresIndependentAgents"],
              "needsTaskContext": not bool(request.strip())}
    if mode in {"plan", "review"}:
        result["intentBoundary"] = "plan-only" if mode == "plan" else "read-only"
        result["allowsProductWrites"] = False
    if read_only:
        result.update(intentBoundary="read-only", allowsProductWrites=False)
    if resume:
        result.update(preset=selected_preset, resumeSelectedWorkflow=True)
    elif selected_preset is not None:
        result["preset"] = selected_preset
    return _with_ui_policy(result)


def _mode_context(selected_mode: str | None) -> str | None:
    if selected_mode is None:
        return None
    if not isinstance(selected_mode, str):
        raise ValueError("Selected mode must be text")
    value = selected_mode.lower()
    if value in LOOP_ALIASES:
        value = "loop"
    if value not in PRIMARY_MODES:
        raise ValueError("Unknown selected mode; use auto, plan, build, review or loop separately from a G preset")
    return value


def leading_record_option(text: str) -> bool:
    """Only leading controls (optionally after a time anchor) are record selectors.

    The task body is never tokenised or rewritten. '--' starts a literal body.
    """
    prefix = text.lstrip()
    anchor = re.match(r'^(?:\d{4}-\d{2}-\d{2}\s+)?\d{1,2}:\d{2}'
                      r'(?:\s*[AP]M)?(?:\s+"[^"\n]*")?\s+', prefix, re.I)
    if anchor:
        prefix = prefix[anchor.end():]
    return bool(re.match(r'^--(?:plan|record)(?:=|\s|$)', prefix))


def _route(text: str, *, follow_up: bool = False, selected_preset: str | None = None,
           selected_mode: str | None = None, read_only: bool = False) -> dict:
    if not isinstance(text, str):
        raise ValueError("Invocation must be text.")
    selected = canonical(selected_preset) if selected_preset is not None else None
    if selected is not None and selected not in ROUTES and selected not in HISTORICAL_PRESETS:
        raise ValueError("Unknown selected command.")
    mode_context = _mode_context(selected_mode)
    value = text.strip()
    invocation = r"^(?:[/$@]ai-development-workflow(?::ai-development-workflow)?|/aidw)(?:\s+|$)"
    has_main_invocation = bool(re.match(invocation, value, flags=re.I))
    value = re.sub(invocation, "", value, flags=re.I)
    head = re.match(r"^(\S+)(.*)$", value, re.S)
    if head:
        name = head[1].lstrip("/$").lower()
        if name.startswith("ai-development-workflow:"):
            name = name.split(":", 1)[1]
        if name in LOOP_ALIASES:
            value = "loop" + head[2]
        elif name in PRIMARY_MODES:
            value = name + head[2]
        else:
            input_alias = next((c for c, spec in ROUTES.items() if name in spec.get("inputAliases", [])), None)
            if input_alias:
                value = input_alias + head[2]
            if name in LAUNCHERS:
                value = LAUNCHERS[name] + head[2]
    retired = re.match(r"^(stage|pipeline)(?:\s+(.*))?$", value, re.S | re.I)
    if retired:
        return modular_route(retired[1].lower(), retired[2] or "")
    parts = value.split(maxsplit=1)
    token, tail = (parts[0], parts[1] if len(parts) > 1 else "") if parts else ("", "")
    explicit_primary = token.lower() if token.lower() in PRIMARY_MODES else None
    if read_only:
        if explicit_primary in {"auto", "plan", "review"} and not follow_up:
            return primary_mode_route(explicit_primary, tail, selected_preset=selected, read_only=True)
        resume_control = token.lower() == "resume" and mode_context is not None
        if mode_context and (follow_up or resume_control):
            request = tail if resume_control else value
            return primary_mode_route(mode_context, request, resume=True, selected_preset=selected, read_only=True)
        explicit = re.sub(r'^(?:aidw|/)', '', token, flags=re.I)
        if (canonical(explicit) in ROUTES or canonical(explicit) in {"XR", "LOOP"} or explicit_primary in {"build", "loop"}
                or explicit in MODES or explicit.lower() in ALIASES):
            raise ValueError("Read-only intent conflicts with an explicit workflow command; resolve intent first.")
        return {"action": "inspect", "preset": selected, "createsRecord": False,
                "request": value, "agentCalls": [], "parentStages": "", "writeScope": "record-only"}
    if follow_up:
        if mode_context:
            return primary_mode_route(mode_context, value, resume=True, selected_preset=selected)
        return {"action": "follow_up", "preset": selected, "createsRecord": False,
                "request": value, "agentCalls": [], "resumeSelectedWorkflow": True}
    manual = re.match(r"^--(?:menu|help)(?:\s+(.*))?$", value, re.S | re.I)
    if has_main_invocation:
        manual = manual or re.match(r"^(?:menu|help)(?:\s+(.*))?$", value, re.S | re.I)
    elif value.lower() in {"menu", "help"}:
        manual = re.match(r"^(?:menu|help)(?:\s+(.*))?$", value, re.S | re.I)
    if manual:
        return {**selector(), "request": manual[1] or ""}
    if has_main_invocation:
        portable = re.match(r"^recipe(?:\s+(.*))?$", value, re.S | re.I)
        if portable:
            return portable_recipe_route(portable[1] or "")
    prefixes = "|".join(re.escape(c) for c in sorted((*ROUTES, *COMMAND_ALIASES, "XR", "LOOP"), key=len, reverse=True))
    value = re.sub(rf"^(?:aidw|/)(?=(?:{prefixes}|[0-3]+)(?:\s|$))", "", value, flags=re.I)
    match = re.match(r"^(\S+)(?:\s+(.*))?$", value, re.S)
    first, rest = (match[1], match[2] or "") if match else ("", "")
    key = canonical(first)
    public = _mode_context(first) if first.lower() in PRIMARY_MODES | LOOP_ALIASES else None
    if public:
        return primary_mode_route(public, rest, selected_preset=selected)
    if key in ROUTES:
        result = copy.deepcopy(ROUTES[key])
        if result["createsRecord"] and leading_record_option(rest):
            raise ValueError("A new-task command conflicts with an existing record. Use a continuation or GCA.")
        result.update(action="quick" if key == "G0" else "run", preset=key, request=rest)
        result["workflow"] = "commands/quick-task/workflow.md" if key == "G0" else "references/standard-workflow.md"
        result["parentStages"] = result["stages"].replace("3", "") if any(c["when"] == "owns_3" for c in result["agentCalls"]) else result["stages"]
        return result
    if re.fullmatch(r"(?:A\d*|G(?:\d+|[A-Z]{1,3}\d*))", key):
        raise ValueError("Use " + ", ".join(ROUTES) + " (GO is G0).")
    if mode_context and first.lower() == "resume":
        return primary_mode_route(mode_context, rest, resume=True, selected_preset=selected)
    if mode_context == "loop" and (first.isdigit() or first.lower() in ALIASES):
        raise ValueError("Legacy numeric/stage controls conflict with Loop context; select the intended legacy workflow explicitly")
    if first.isdigit():
        digits = first
        while len(first) == 1 and re.match(r"^[0-3](?:\s|$)", rest):
            parts = rest.split(maxsplit=1)
            digits += parts[0]
            rest = parts[1] if len(parts) > 1 else ""
        if digits not in MODES:
            raise ValueError("Unsupported stage sequence; preserve the leading zero and stage order.")
        mode = digits
    else:
        mode = ALIASES.get(first.lower())
    if mode == "resume" and selected in ROUTES and ROUTES[selected]["stages"] == "01":
        mode = "1"
    if mode == "resume" and selected == "G0":
        return {"action": "follow_up", "preset": "G0", "createsRecord": False,
                "recordKind": "checklist", "workflow": "commands/quick-task/workflow.md",
                "request": rest, "agentCalls": [], "parentStages": "",
                "resumeSelectedWorkflow": True}
    if mode is not None:
        if "0" in mode and leading_record_option(rest):
            raise ValueError("Stage 0 conflicts with an existing record.")
        if "0" not in mode and selected == "G0":
            raise ValueError("Numeric stages need a development record, not a quick checklist. Continue that checklist normally or start G1.")
        inherited = "G1" if "0" in mode else (selected or "G1")
        child_owns_execution = ("0" not in mode and selected in ROUTES and
                                any(c["when"] == "owns_3" for c in ROUTES[selected]["agentCalls"]))
        parent = mode.replace("3", "") if child_owns_execution else mode
        if mode == "resume" and child_owns_execution:
            parent = ""
        return {"action": "run", "stages": mode, "parentStages": parent,
                "preset": inherited, "createsRecord": "0" in mode,
                "recordKind": "development", "workflow": "references/standard-workflow.md",
                "request": rest, "agentCalls": [],
                "resumeSelectedWorkflow": "0" not in mode}
    return automatic(value)


@traced("route")
def route(text: str, *, follow_up: bool = False, selected_preset: str | None = None,
          selected_mode: str | None = None, read_only: bool = False, project_root=None, decision=None) -> dict:
    result = _route(text, follow_up=follow_up, selected_preset=selected_preset,
                    selected_mode=selected_mode, read_only=read_only)
    preset = result.get("preset")
    if result["action"] not in {"auto", "select", "help", "inspect", "modular", "recipe", "mode"} and result.get("mode") not in PRIMARY_MODES:
        if "label" in result or result["action"] == "follow_up":
            result["commandFile"] = COMMAND_FILES.get(preset, "commands/numeric-stages.md")
        else:
            result["commandFile"] = "commands/numeric-stages.md"
            if preset in COMMAND_FILES:
                result["presetCommandFile"] = COMMAND_FILES[preset]
    return apply_routing_decision(_with_ui_policy(result), decision)


@traced("route.task")
def route_task(text: str, *, follow_up: bool = False,
               selected_preset: str | None = None, selected_mode: str | None = None, read_only: bool = False,
               project_root=None, decision=None) -> dict:
    """Route a natural-language task without interpreting its words as commands.

    The host decides whether input is a task or an explicit invocation. Preserve
    the legacy route/--text parser for explicit GO, numeric and named controls.
    """
    if not isinstance(text, str):
        raise ValueError("Task must be text.")
    _mode_context(selected_mode)
    if follow_up:
        result = route("", follow_up=True, selected_preset=selected_preset,
                       selected_mode=selected_mode, read_only=read_only if selected_mode else False,
                       project_root=project_root)
        result["request"] = text
        if result.get("mode") in PRIMARY_MODES:
            result["needsTaskContext"] = not bool(text.strip())
    else:
        result = automatic(text)
    if read_only:
        # The full task remains literal; selection must preserve its read-only boundary.
        result["intentBoundary"] = "read-only"
    return apply_routing_decision(result, decision)


def _execution_schedule(result: dict) -> list[dict]:
    """Describe order for diagnostics/tests. This does not execute stages or agents."""
    if result.get("resumeSelectedWorkflow"):
        return [{"kind": "reconcile", "reason": "Inspect actual record and prior calls before resuming",
                 "beforeProductWrites": ["current-criticism", "current-briefing", "execution-admission"]}]
    if result["action"] == "mode" and result.get("mode") == "loop":
        return [
            {"kind": "capability-check", "operation": "resolve_targets_workers_and_timer",
             "owner": "manager", "dispatchesAgents": False},
            {"kind": "agent", "agent": "loop-reviewer", "operation": "inspect_original_and_result",
             "file": result["profiles"][0], "independent": True,
             "onAccepted": "obtain_independent_corroboration_then_acknowledge"},
            {"kind": "agent", "agent": "verification-engineer", "file": result["profiles"][2],
             "capabilities": ["run-tests"], "operation": "corroborate_no_repair", "independent": True,
             "condition": "initial_review_has_no_repair", "workerGroup": "no-repair-verifier",
             "distinctFrom": ["initial-reviewer"], "writeScope": "test-output-only"},
            {"kind": "agent", "agent": "reviewer", "file": result["profiles"][0],
             "capabilities": ["loop-review", "review-code"], "operation": "acknowledge_corroboration",
             "condition": "initial_review_has_no_repair", "workerGroup": "initial-reviewer",
             "writeScope": "read-only"},
            {"kind": "checklist", "operation": "map_findings_and_reconcile_items", "owner": "manager",
             "condition": "actionable_findings"},
            {"kind": "admission", "operation": "confirm_exact_repair_plan", "owner": "reviewer",
             "requireCritique": True, "requireBriefing": True, "condition": "checklist_requires_execution"},
            {"kind": "agent", "agent": "loop-executor", "operation": "execute_checklist",
             "file": result["profiles"][1], "soleWriter": True, "condition": "current_admission_passes"},
            {"kind": "checklist", "operation": "reconcile_execution_items", "owner": "manager",
             "condition": "executor_returns"},
            {"kind": "agent", "agent": "loop-reviewer", "operation": "review_current_result",
             "file": result["profiles"][0], "independent": True, "fresh": True,
             "condition": "checklist_accounting_complete"},
            {"kind": "conditional-repeat", "until": "current_independent_review_accepts",
             "onBlocked": "preserve_unfinished_work_and_reconcile", "cycleLimit": None},
        ]
    if result["action"] == "mode" and result.get("mode") in {"plan", "build", "review"}:
        if result["mode"] == "review":
            return [{"kind": "review", "operation": operation,
                     "owner": "worker" if operation == "inspect_current_work" else "coordinator",
                     **({"agent": "code-reviewer", "file": "agents/code-reviewer/agent.md"}
                        if operation == "inspect_current_work" else {}), "writeScope": "record-only"}
                    for operation in ("capture_scope", "plan_inspection", "criticize_inspection_plan", "inspect_current_work", "report_findings")]
        schedule = [{"kind": "stage", "stage": stage, "owner": "coordinator", "writeScope": "record-only"}
                    for stage in "012"]
        if result["mode"] == "plan":
            schedule[1].update(owner="worker", agent="code-goal-planner", file="agents/code-goal-planner/agent.md")
            schedule[2].update(owner="worker", agent="plan-reviewer", file="agents/plan-reviewer/agent.md", independent=True)
        if result["mode"] == "build":
            schedule[2].update(owner="worker", agent="plan-reviewer", file="agents/plan-reviewer/agent.md", independent=True)
            schedule += [{"kind": "admission", "requireCritique": True, "requireBriefing": True},
                         {"kind": "stage", "stage": "3", "owner": "worker", "agent": "implementation-executor",
                          "file": "agents/implementation-executor/agent.md", "writeScope": "repo-write-scoped"},
                         {"kind": "verify", "operation": "verify_authorized_result", "owner": "worker",
                          "agent": "code-reviewer", "file": "agents/code-reviewer/agent.md", "independent": True}]
        schedule.append({"kind": "report", "operation": "report_result", "owner": "coordinator"})
        return schedule
    if result["action"] == "quick":
        return ([{"kind": "quick", "operation": name, "owner": "coordinator"}
                 for name in ("capture", "checklist", "plan")]
                + [{"kind": "agent", "agent": "plan-reviewer", "file": "agents/plan-reviewer/agent.md",
                    "operation": "review_plan", "independent": True},
                   {"kind": "quick", "operation": "announce", "owner": "coordinator"}]
                + [{"kind": "admission", "requireCritique": True, "requireBriefing": True,
                    "recordKind": "checklist"}]
                + [{"kind": "agent", "agent": "fast-engineer", "file": "agents/fast-engineer/agent.md",
                    "operation": "execute_and_test", "soleWriter": True},
                   {"kind": "agent", "agent": "code-reviewer", "file": "agents/code-reviewer/agent.md",
                    "operation": "review", "independent": True}])
    if result["action"] != "run":
        return []
    stages, calls = result["stages"], list(result["agentCalls"])
    # Metadata preserves special operations. Universal duties fill only absent
    # worker roles; these remain planned descriptors, never spawn receipts.
    def default_call(agent, when, operation):
        if not any(call["when"] == when for call in calls):
            calls.append({"agent": agent, "file": f"agents/{agent}/agent.md",
                          "when": when, "operation": operation, "independent": True})
    if "3" in stages:
        default_call("plan-reviewer", "during_2", "review_plan")
        default_call("implementation-executor", "owns_3", "execute_and_test")
        default_call("code-reviewer", "after_3_before_completion", "review")
    elif not calls and stages:
        if "1" in stages:
            default_call("code-goal-planner", "during_1_before_2", "consult")
        elif "2" in stages:
            default_call("plan-reviewer", "during_2", "review_plan")
        else:
            default_call("codebase-assessor", "after_0_before_1", "assess_codebase")
    schedule = []
    def agents(when):
        return [{"kind": "agent", **c} for c in calls if c["when"] == when]
    for stage in stages.replace("3", ""):
        if stage == "1":
            schedule.extend(agents("after_0_before_1"))
            schedule.append({"kind": "stage-start", "stage": "1", "owner": "parent"})
            schedule.extend(agents("during_1_before_2"))
        if stage == "2":
            schedule.extend(agents("during_2"))
        schedule.append({"kind": "stage", "stage": stage, "owner": "parent"})
    if "0" in stages and "1" not in stages:
        schedule.extend(agents("after_0_before_1"))
    if not stages:
        if result.get("kind") == "stage":
            schedule.append({"kind": "artifact-gate", "requirements": result.get("queue", {}).get("requiresAll", [])})
            # Existing source-owned artifact vocabulary identifies standalone writers.
            # This diagnostic does not replace the universal runtime admission gate.
            if set(result.get("queue", {}).get("produces", [])) & {"implementation", "red_tests", "documentation", "cleanup"}:
                schedule.append({"kind": "admission", "requireCritique": True, "requireBriefing": True,
                                 "prerequisitePolicy": "complete-or-reuse-current-evidence"})
        schedule.extend(agents("standalone"))
    delegated = agents("owns_3")
    if "3" in stages or delegated:
        if "2" not in stages:
            schedule.append({"kind": "prerequisite", "operation": "current-plan-criticism",
                             "requestedStages": stages, "policy": "complete-or-reuse-current-evidence"})
        schedule.append({"kind": "admission", "requireCritique": True, "requireBriefing": True})
        schedule.extend(delegated or [{"kind": "stage", "stage": "3", "owner": "parent"}])
        schedule.extend(agents("after_3_before_completion"))
    return schedule


def execution_schedule(result: dict) -> list[dict]:
    """Describe canonical duties and distinct worker groups, never real dispatch."""
    if result.get("resumeSelectedWorkflow"):
        return _execution_schedule(result)
    requirements = result.get("routingRequirements", {})
    registry = load_registry()
    if requirements.get("assessmentRequired"):
        return [
            {"kind": "prerequisite", "operation": "bound-inspection-scope-and-brief-workers"},
            {"kind": "agent", "agent": "investigator", "family": "investigator", "file": "agents/investigator/agent.md",
             "capabilities": ["assess-codebase"], "operation": "assess_impact", "writeScope": "record-only", "workerGroup": "investigator"},
            {"kind": "agent", "agent": "reviewer", "family": "reviewer", "file": "agents/reviewer/agent.md",
             "capabilities": ["review-code"], "operation": "corroborate", "writeScope": "read-only",
             "workerGroup": "assessment-countercheck", "distinctFrom": ["investigator"], "independent": True,
             "question": "Independently check the consequential impact claim or unresolved boundary."},
            {"kind": "reconcile", "operation": "resolve-impact-before-final-plan-or-product-writes"},
        ]
    schedule = _execution_schedule(result)
    if not schedule:
        return schedule
    if requirements.get("architectRequired") and not any(row.get("agent") == "architect" for row in schedule):
        insertion = next((i for i, row in enumerate(schedule) if row.get("stage") == "1" or row.get("operation") in {"plan", "plan_inspection"}), 0)
        schedule.insert(insertion, {"kind": "agent", "agent": "architect", "file": "agents/architect/agent.md",
                                    "capabilities": ["design-architecture"], "operation": "consult", "beforeFinalizedPlan": True})
    if requirements.get("uiDirectorRequired") and not any(row.get("agent") == "ui-design-director" for row in schedule):
        insertion = next((i for i, row in enumerate(schedule) if row.get("stage") == "1" or row.get("operation") in {"plan", "plan_inspection"}), 0)
        schedule.insert(insertion, {"kind": "agent", "agent": "ui-design-director", "file": "agents/ui-design-director/agent.md",
                                    "capabilities": ["design-ui", "ui-design"], "operation": "design_spec", "beforeFinalizedPlan": True})
    # Convert existing command/default duties through the same registry. Distinct
    # group labels are scheduling requirements, never observed worker identities.
    for row in schedule:
        if not row.get("agent"):
            continue
        operation = row.get("operation")
        if operation is None and row.get("kind") == "stage":
            operation = {"1": "plan-code", "2": "review-plan", "3": "execute-plan"}.get(row.get("stage"))
        caps = row.get("capabilities")
        if row.get("agent") == "loop-reviewer":
            caps = ["loop-review", "review-code"]
        if row.get("agent") == "loop-executor":
            caps = ["loop-execution", "execute-plan"]
        role = resolve_profile(row.get("file", "agents/" + row["agent"] + "/agent.md"), operation,
                               row.get("writeScope"), capabilities=caps, registry=registry, allow_custom_operation=True)
        row.update(agent=role["family"], family=role["family"], file=role["profile"], capabilities=role["capabilities"])
        row.setdefault("workerGroup", role["family"])
        if role["family"] == "builder" and requirements.get("fastRequired") and "fast-build" not in row["capabilities"]:
            row["capabilities"].append("fast-build")
        if result.get("routingDecision", {}).get("uiContext", {}).get("applicable") and role["family"] in {"builder", "reviewer", "ui-design-director", "verification-engineer"}:
            if "ui-design" not in row["capabilities"]:
                row["capabilities"].append("ui-design")
            if role["family"] == "reviewer" and operation != "review-plan" and "review-ui" not in row["capabilities"]:
                row["capabilities"].append("review-ui")
        if role["family"] in {"reviewer", "verification-engineer"}:
            row["independent"] = True
            row.setdefault("distinctFrom", ["builder", "architect", "ui-design-director"] + (["reviewer"] if role["family"] == "verification-engineer" else []))
    if result.get("mode") == "loop":
        reviews = [row for row in schedule if row.get("family") == "reviewer"]
        for row in reviews:
            row["workerGroup"] = "fresh-reviewer" if row.get("fresh") else "initial-reviewer"
        return schedule

    worker_rows = [row for row in schedule if row.get("agent")]
    writing = (result.get("resolvedMode") == "build" or "3" in result.get("stages", "")
               or any(row["family"] == "builder" and row.get("operation") in {"write_red_tests", "execute_plan", "execute_tdd", "cleanup", "update_docs", "clean_and_test", "execute_and_test"} for row in worker_rows))
    # A standalone writer must still receive independent criticism/acceptance;
    # these are prerequisite/countercheck duties, not fabricated numeric stages.
    if writing:
        writers = [i for i, row in enumerate(schedule) if row.get("family") == "builder"]
        if writers:
            first, last = min(writers), max(writers)
            has_prior_critic = any(row.get("family") == "reviewer" and "review-plan" in row.get("capabilities", []) for row in schedule[:first])
            if not has_prior_critic:
                schedule.insert(first, {"kind": "agent", "agent": "reviewer", "family": "reviewer", "file": "agents/reviewer/agent.md",
                                        "capabilities": ["review-plan"], "operation": "review_plan", "workerGroup": "reviewer",
                                        "independent": True, "distinctFrom": ["builder", "architect", "ui-design-director"],
                                        "prerequisitePolicy": "complete-or-reuse-current-evidence"})
                last += 1
            # Documentation/cleanup after a build is still writing. Acceptance
            # belongs after the last writer, not only after the first build.
            last = max(i for i, row in enumerate(schedule) if row.get("family") in {"builder", "verification-engineer"})
            accepts = [i for i, row in enumerate(schedule) if row.get("family") == "reviewer" and "review-code" in row.get("capabilities", [])]
            if not any(index > last for index in accepts):
                caps = ["review-code"]
                if result.get("routingDecision", {}).get("uiContext", {}).get("applicable"):
                    caps += ["ui-design", "review-ui"]
                schedule.insert(last + 1, {"kind": "agent", "agent": "reviewer", "family": "reviewer", "file": "agents/reviewer/agent.md",
                                          "capabilities": caps, "operation": "review", "workerGroup": "reviewer",
                                          "independent": True, "distinctFrom": ["builder", "architect", "ui-design-director"],
                                          "covers": "final-integrated-result"})
    else:
        # A separate worker must examine the primary artifact. Preserve Reviewer
        # as primary for GVR/GPR; another Reviewer is a valid bounded corroborator.
        primary = worker_rows[0] if worker_rows else None
        if primary is not None:
            primary["workerGroup"] = "primary-" + primary["family"]
            primary_group = primary["workerGroup"]
            counter_family = "reviewer"
            caps = ["review-plan" if result.get("resolvedMode") == "plan" else "review-code"]
            if result.get("routingDecision", {}).get("uiContext", {}).get("applicable"):
                caps += ["ui-design", "review-ui"]
            counter = {"kind": "agent", "agent": counter_family, "family": counter_family, "file": "agents/reviewer/agent.md",
                       "capabilities": caps, "operation": "corroborate", "workerGroup": "independent-countercheck",
                       "distinctFrom": [primary_group, "architect", "ui-design-director"], "independent": True,
                       "writeScope": "read-only", "withinSelectedOperation": True,
                       "question": "Inspect the primary source/artifact and independently check a consequential claim, omission or boundary."}
            existing = [row for row in worker_rows[1:] if row.get("family") == "reviewer" and row.get("independent")]
            if existing:
                for row in existing:
                    row.setdefault("distinctFrom", [])
                    if primary_group not in row["distinctFrom"]:
                        row["distinctFrom"].append(primary_group)
            else:
                insertion = next((i for i, row in enumerate(schedule) if row.get("kind") == "report" or row.get("operation") == "report_findings"), len(schedule))
                schedule.insert(insertion, counter)
    if requirements.get("verificationEngineerRequired") and not any(row.get("family") == "verification-engineer" for row in schedule):
        insertion = next((i for i, row in reversed(list(enumerate(schedule))) if row.get("family") == "reviewer" and "review-plan" not in row.get("capabilities", [])), len(schedule))
        schedule.insert(insertion, {"kind": "agent", "agent": "verification-engineer", "family": "verification-engineer",
                                    "file": "agents/verification-engineer/agent.md", "capabilities": ["run-tests"],
                                    "operation": "verify_unit", "workerGroup": "verification-engineer", "independent": True,
                                    "distinctFrom": ["builder", "architect", "ui-design-director", "reviewer"],
                                    "writeScope": "test-output-only", "scope": "selected-substantial-validation"})
    return schedule

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--text", help="Explicit invocation/control text; legacy parsing is preserved")
    inputs.add_argument("--task", help="Natural-language task body; never parse words or quantities as commands")
    parser.add_argument("--follow-up", action="store_true")
    parser.add_argument("--read-only", action="store_true", help="Host-classified read-only request; preserve the product-write boundary")
    parser.add_argument("--selected-preset")
    parser.add_argument("--selected-mode", help="Public mode context: auto, plan, build, review or loop (XR alias); separate from a G preset")
    parser.add_argument("--project-root", help="Explicit project root for optional diagnostics")
    parser.add_argument("--decision", type=Path, help="JSON file with mode, routing, uiContext and verificationContext; source-grounded declarations, never dispatch receipts")
    parser.add_argument("--schedule", action="store_true", help="Describe planned order; does not execute it")
    args = parser.parse_args()
    try:
        handler = route_task if args.task is not None else route
        value = args.task if args.task is not None else (args.text or "")
        decision = json.loads(args.decision.read_text()) if args.decision else None
        result = handler(value, follow_up=args.follow_up, selected_preset=args.selected_preset,
                         selected_mode=args.selected_mode, read_only=args.read_only, project_root=args.project_root, decision=decision)
        print(json.dumps({"route": result, "plannedSchedule": execution_schedule(result)} if args.schedule else result, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
