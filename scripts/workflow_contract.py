#!/usr/bin/env python3
"""Shared portable admission declarations; these do not authenticate people or delivery.

The template/snapshot commands only print data. They never write a record, complete a
review, emit a public message, inspect repository drift, or grant tool permissions.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

from task_policy import pending_routing, policy_binding, preparation_authorship, validate_actual_workers, validate_policy

SCHEMA = "ai-development-workflow/contract-v2"
LEGACY_SCHEMA = "ai-development-workflow/contract-v1"
BOUNDARY = ("Portable declarations only: validates structure and current declared bindings, "
            "not chat delivery, worker authenticity, review quality, repository drift, or tool permissions.")
WRITE_SCOPES = {"repo-write-scoped", "tests-only", "docs-only", "external-write"}
SCOPES = WRITE_SCOPES | {"read-only", "record-only", "test-output-only", "none"}
KINDS = {"capture", "plan", "critique", "execute", "verify", "report", "other"}
REVIEW_AREAS = {"scope", "feasibility", "dependencies", "verification", "preservation"}
PHASE_STATES = {"pending", "in-progress", "complete", "blocked"}


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def file_hash(path, *, checklist=False):
    """Only checkbox state is progress. Wording, source references and evidence stay bound."""
    raw = Path(path).read_bytes()
    if checklist:
        text = raw.decode("utf-8")
        # Preserve fenced examples byte-for-byte; normalize only actual task-line markers.
        lines, fence = [], None
        for line in text.splitlines(keepends=True):
            marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
            if marker:
                token = marker.group(1)
                if fence is None:
                    fence = (token[0], len(token))
                elif token[0] == fence[0] and len(token) >= fence[1] and not marker.group(2).strip():
                    fence = None
                lines.append(line)
                continue
            if fence is None:
                line = re.sub(r"^(\s*(?:[-*+]|\d+[.)])\s+)\[[ xX~!]\](?=\s)",
                              r"\1[ ]", line)
            lines.append(line)
        raw = "".join(lines).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _texts(value):
    return isinstance(value, list) and bool(value) and all(_text(item) for item in value)


def _authored(value):
    """Reject obvious unfinished tokens, without pretending to judge semantic quality."""
    return _text(value) and value.strip().lower().strip("_ .") not in {
        "pending", "todo", "tbd", "not started", "not-started", "pending investigation",
        "no critique has been performed", "not yet reviewed"}


def _require(condition, message):
    if not condition:
        raise ValueError("workflow contract: " + message)


def _object(value, label):
    _require(isinstance(value, dict), label + " must be an object")
    return value


def _rows(value, label, *, nonempty=True):
    _require(isinstance(value, list) and (bool(value) or not nonempty), label + " must be a list")
    _require(all(isinstance(row, dict) for row in value), label + " entries must be objects")
    ids = [row.get("id") for row in value]
    _require(all(_text(key) for key in ids) and len(set(ids)) == len(ids),
             label + " needs distinct nonblank IDs")
    return {row["id"]: row for row in value}


def _selected_control(value):
    """Normalize public controls and their retained compatibility declarations."""
    value = str(value or "").strip().lower()
    if value.startswith("mode:"):
        value = value[5:]
    return {"xr": "loop", "ai-dev-loop": "loop",
            "ai-dev-execute-review": "loop"}.get(value, value)


def selection(contract, *, registry=None):
    _require(contract.get("schema") == SCHEMA,
             "active workflowContract requires contract-v2; reconcile legacy evidence explicitly without rewriting archived records")
    selected = _object(contract.get("selection"), "selection")
    _require(_text(selected.get("workflow")) and _text(selected.get("reason")),
             "selected workflow and reason are required")
    _require(selected.get("reviewPolicy") in {"self-permitted", "independent"},
             "selection.reviewPolicy must declare self-permitted or independent")
    controls = {_selected_control(selected.get(field)) for field in ("workflow", "mode")}
    read_only_mode = bool(controls & {"plan", "review"})
    phases = _rows(selected.get("phases"), "selection.phases")
    earlier = set()
    for key, phase in phases.items():
        _require(all(_text(phase.get(field)) for field in ("title", "operation", "owner")),
                 "each ordered phase needs a title, operation and responsible owner role")
        _require(phase.get("kind") in KINDS and phase.get("writeScope") in SCOPES,
                 "phase kind/writeScope is missing or unknown")
        _require(not (read_only_mode and phase["writeScope"] in WRITE_SCOPES),
                 "Plan and Review modes cannot authorize product writes")
        deps = phase.get("dependsOn")
        _require(isinstance(deps, list) and all(_text(dep) for dep in deps)
                 and len(deps) == len(set(deps)) and set(deps) <= earlier,
                 "phase dependencies must reference preceding ordered phases")
        if phase["kind"] in {"capture", "plan", "critique"}:
            _require(phase["writeScope"] not in WRITE_SCOPES,
                     "preparation phases cannot authorize product writes")
        earlier.add(key)
    preparation_kinds = set()
    previous_preparation = -1
    for phase in phases.values():
        if phase["kind"] in {"capture", "plan", "critique"}:
            order = {"capture": 0, "plan": 1, "critique": 2}[phase["kind"]]
            _require(order >= previous_preparation,
                     "preparation order must be capture, then plan, then criticism")
            previous_preparation = order
            preparation_kinds.add(phase["kind"])
        if phase["writeScope"] in WRITE_SCOPES:
            _require(preparation_kinds == {"capture", "plan", "critique"},
                     "capture, plan and critique must precede every selected product mutation")
    validate_policy(selected, phases, registry=registry)
    return selected, phases


def _scope(data):
    value = _object(data.get("scope"), "scope")
    _require(_texts(value.get("in")) and _texts(value.get("out")), "scope and exclusions are required")
    return value


def review_binding(record, data, contract=None, *, kind="development"):
    """Compute present inputs only, not a completed-review receipt."""
    record = Path(record).resolve()
    contract = data.get("workflowContract") if contract is None else contract
    contract = _object(contract, "workflowContract")
    _, phases = selection(contract)
    revision = data.get("planRevision")
    _require(type(revision) is int and revision > 0, "planRevision must be a positive integer")
    baseline = _object(data.get("sourceBaseline"), "sourceBaseline")
    _require(_text(baseline.get("description")), "declared sourceBaseline.description is required")
    _scope(data)
    if kind == "development":
        from plan_record import definition_hash, PLAN_FILES
        definition = definition_hash(data)
        hashes = {name: file_hash(record / name, checklist=name == "checklist.md") for name in PLAN_FILES}
        critique_hash = file_hash(record / "critique.md")
    elif kind == "quick":
        definition = canonical_hash({key: data.get(key) for key in ("scope", "plan", "planRevision", "sourceBaseline")})
        hashes = {name: file_hash(record / name, checklist=name == "checklist.md")
                  for name in ("request.md", "checklist.md")}
        critique_hash = None  # Quick criticism is inline in this one compact contract.
    else:
        raise ValueError("unknown record kind")
    # Deliberately exclude dynamic phase status, display labels and worker identities.
    operations = [{key: phase[key] for key in ("id", "kind", "operation", "writeScope", "dependsOn")}
                  for phase in phases.values()]
    return {"recordPath": str(record), "kind": kind, "planRevision": revision,
            "definitionHash": definition, "planHashes": hashes, "critiqueHash": critique_hash,
            "sourceBaselineHash": canonical_hash(baseline), "operationsHash": canonical_hash(operations),
            "taskPolicyHash": canonical_hash(policy_binding(contract["selection"])),
            "preparationAuthorsHash": canonical_hash(preparation_authorship(contract))}


def briefing_binding(data, contract, binding):
    return {"workHash": canonical_hash(binding), "scopeHash": canonical_hash(data.get("scope")),
            "selectionHash": canonical_hash(contract.get("selection")),
            "progressHash": canonical_hash(contract.get("progress")),
            "rosterHash": canonical_hash(contract.get("roster")),
            "reviewHash": canonical_hash(contract.get("review")),
            "contributionsHash": canonical_hash(contract.get("contributions"))}


def validate_roster(contract):
    roster = _object(contract.get("roster"), "roster")
    coordinator = roster.get("coordinatorId")
    _require(_text(coordinator), "roster.coordinatorId must identify the current actual agent")
    workers = _rows(roster.get("workers"), "roster.workers", nonempty=False)
    _require(coordinator not in workers, "coordinator cannot also be counted as a worker")
    for worker in workers.values():
        _require(worker.get("status") in {"running", "completed", "failed"},
                 "workers must be actual running/completed/failed agents; keep plans separate")
        _require(_text(worker.get("role")) and _texts(worker.get("evidence")),
                 "actual workers need their role and observed spawn/result evidence references")
    active = 1 + sum(worker["status"] == "running" for worker in workers.values())
    _require(type(roster.get("activeAgentCount")) is int and roster["activeAgentCount"] == active,
             "activeAgentCount must equal one current agent plus actually running workers")
    planned = roster.get("plannedWorkers")
    _require(isinstance(planned, list) and all(isinstance(row, dict) and _text(row.get("role"))
             and _texts(row.get("phaseIds")) for row in planned),
             "plannedWorkers needs role/phaseIds and adds zero actual agents")
    phases = {row["id"] for row in contract["selection"]["phases"]}
    _require(all(set(row["phaseIds"]) <= phases for row in planned), "planned worker references unknown phase")
    profiles = roster.get("profiles")
    actors = {coordinator} | set(workers)
    _require(isinstance(profiles, list) and all(isinstance(row, dict) and _text(row.get("name"))
             and row.get("ownerId") in actors for row in profiles),
             "profiles need a name and actual applying agent; profiles add zero agents")
    return actors


def validate_review(record, contract, binding, actors, *, kind="development"):
    review = _object(contract.get("review"), "review")
    _require(review.get("status") == "complete" and review.get("decision") in {"ready", "revised"},
             "current criticism is incomplete or blocked")
    _require(review.get("binding") == binding, "criticism does not cover the exact current plan/source/operations")
    author, critic = review.get("authorId"), review.get("reviewerId")
    _require(author in actors and critic in actors, "plan author and critic must be declared actual actors")
    _require(not any(worker["id"] == critic and worker["status"] == "failed"
                     for worker in contract["roster"]["workers"]),
             "a failed worker cannot supply completed criticism")
    mode = review.get("mode")
    _require(mode in {"self", "independent"} and ((mode == "self") == (author == critic)),
             "self/independent criticism does not match the author and reviewer identities")
    selected = contract["selection"]
    controls = {_selected_control(selected.get(field)) for field in ("workflow", "mode")}
    if selected["reviewPolicy"] == "independent" or controls & {"gpr", "loop"}:
        _require(mode == "independent", "this workflow requires independent criticism")
    checks = review.get("checks")
    _require(isinstance(checks, list) and len(checks) == len(REVIEW_AREAS),
             "criticism needs scope, feasibility, dependencies, verification and preservation checks")
    _require(all(isinstance(row, dict) and _authored(row.get("observation")) and _texts(row.get("evidence"))
                 and all(_authored(ref) for ref in row["evidence"])
                 for row in checks) and {row.get("area") for row in checks} == REVIEW_AREAS,
             "each criticism check needs its concrete observation and evidence")
    findings = _rows(review.get("findings"), "review.findings", nonempty=False)
    for finding in findings.values():
        _require(_authored(finding.get("issue")) and _authored(finding.get("resolution"))
                 and _texts(finding.get("evidence")) and finding.get("disposition") in {"resolved", "out-of-scope"},
                 "criticism findings need resolved/out-of-scope dispositions, reasons and evidence")
    _require(bool(findings) or _authored(review.get("noFindingsRationale")),
             "empty findings needs a grounded no-findings rationale")
    _require(_texts(review.get("evidence")), "completed criticism needs actual review evidence references")
    if kind == "development":
        report = (Path(record) / "critique.md").read_text(encoding="utf-8")
        _require(not re.search(r"(?mi)^>\s*Status:\s*(pending|not[- ]started)\b|^_?No critique has been performed\._?\s*$", report),
                 "pending critique placeholder cannot be finalized as completed criticism")
    return review


def validate_progress(contract, binding, actors, *, require_product_write=True):
    _, phases = selection(contract)
    progress = _object(contract.get("progress"), "progress")
    states = _rows(progress.get("phases"), "progress.phases")
    _require(set(states) == set(phases), "progress must account for every selected phase exactly")
    _require(progress.get("resultRevision") is None or _authored(progress.get("resultRevision")),
             "resultRevision must identify the exact stable output or remain null")
    current = progress.get("currentPhase")
    _require(current in states, "currentPhase must identify a selected phase")
    active = []
    active_actors = {contract["roster"]["coordinatorId"]} | {
        worker["id"] for worker in contract["roster"]["workers"] if worker["status"] == "running"}
    for key, row in states.items():
        status = row.get("status")
        _require(status in PHASE_STATES, "phase status must be pending/in-progress/complete/blocked")
        if status != "pending":
            _require(row.get("ownerId") in actors, "started phases need an actual responsible agent")
        if status == "in-progress":
            _require(row.get("ownerId") in active_actors, "in-progress phase cannot be owned by a completed/failed worker")
            active.append(key)
        if status == "in-progress" or (key == current and phases[key]["writeScope"] in WRITE_SCOPES):
            _require(all(states[dep].get("status") == "complete" for dep in phases[key]["dependsOn"]),
                     "current or in-progress phase has an incomplete prerequisite")
        if status == "complete":
            _require(_texts(row.get("evidence")) and row.get("workHash") == canonical_hash(binding),
                     "complete phase claims need evidence bound to current work")
            _require(all(states[dep].get("status") == "complete" for dep in phases[key]["dependsOn"]),
                     "complete phase has an incomplete prerequisite")
        if status == "blocked":
            _require(_text(row.get("reason")) and _texts(row.get("evidence")), "blocked phases need reasons and evidence")
    _require(not active or active == [current], "currentPhase must match the single in-progress phase")
    _require(not any(row.get("status") == "blocked" for row in states.values()),
             "a selected phase is blocked; reconcile that obligation before execution admission")
    preparations = {phase["kind"] for phase in phases.values()
                    if phase["kind"] in {"capture", "plan", "critique"}}
    _require(preparations == {"capture", "plan", "critique"}, "capture, plan and critique phases must be disclosed")
    for key, phase in phases.items():
        if phase["kind"] in preparations:
            _require(states[key].get("status") == "complete", "capture, plan and criticism must finish before execution")
    review = contract["review"]
    for kind, actor in (("plan", review["authorId"]), ("critique", review["reviewerId"])):
        _require(any(phase["kind"] == kind and states[key].get("ownerId") == actor
                     for key, phase in phases.items()),
                 "completed plan/critique phase owners must include the actual declared author/reviewer")
    if require_product_write:
        _require(any(phase["writeScope"] in WRITE_SCOPES for phase in phases.values()),
                 "no product mutation operation selected; plain inspection does not authorize a build")


def render_briefing(data, contract):
    """Produce the required block; printing it is not public delivery."""
    selected, phases = selection(contract)
    team = validate_policy(selected, phases)
    scope = _scope(data)
    progress = _object(contract.get("progress"), "progress")
    states = _rows(progress.get("phases"), "progress.phases")
    roster = _object(contract.get("roster"), "roster")
    review = _object(contract.get("review"), "review")
    lines = ["Scope: " + "; ".join(scope["in"]), "Boundaries: " + "; ".join(scope["out"]),
             "Workflow: " + selected["workflow"] + " — " + selected["reason"],
             "Mode: " + selected["mode"],
             "Impact: " + selected["routing"]["impact"] + " — " + selected["routing"]["reason"],
             "Required delegation: " + "; ".join(row["phaseId"] + " → " + row["profile"]
                                                   for row in selected["delegation"]["assignments"]),
             "Ordered phases:"]
    for index, (key, phase) in enumerate(phases.items(), 1):
        state = states.get(key, {})
        lines.append(f"{index}. {phase['title']} [{state.get('status', 'pending')}] — "
                     f"owner: {phase['owner']} ({state.get('ownerId') or 'not yet assigned'}); "
                     f"operation: {phase['operation']}; scope: {phase['writeScope']}")
    returned = {row.get("workerId") for row in contract.get("contributions", [])
                if row.get("disposition") in {"incorporated", "rejected"}} - {None, roster.get("coordinatorId")}
    lines += ["Current phase: " + str(progress.get("currentPhase")),
              f"Required useful worker contributors: {team['minimumContributors']}; returned contributor identities: {len(returned)}.",
              f"Actual active agents: {roster.get('activeAgentCount')} (current agent: {roster.get('coordinatorId')})."]
    workers = roster.get("workers", [])
    lines.append("Actual workers: " + ("; ".join(f"{row['id']} — {row['role']} ({row['status']})" for row in workers) or "none"))
    lines.append("Planned workers (not running): " + ("; ".join(row["role"] + " for " + ", ".join(row["phaseIds"])
                  for row in roster.get("plannedWorkers", [])) or "none"))
    lines.append("Applied profiles (zero extra agents): " + ("; ".join(row["name"] + " by " + row["ownerId"]
                  for row in roster.get("profiles", [])) or "none"))
    lines.append(f"Plan criticism: {review.get('status', 'pending')} / {review.get('decision', 'pending')}; "
                 f"mode: {review.get('mode', 'pending')}; critic: {review.get('reviewerId') or 'not yet assigned'}.")
    lines.append("Admission: product writes require a successful current admission check; this briefing alone does not grant execution.")
    return "\n".join(lines)


def validate_contract(record, data, contract=None, *, kind="development", require_product_write=True, completing=None):
    contract = data.get("workflowContract") if contract is None else contract
    _require(isinstance(contract, dict) and contract.get("schema") == SCHEMA,
             "active workflowContract requires contract-v2; reconcile legacy evidence explicitly without rewriting archived records")
    if require_product_write:
        validate_current_discovery(contract["selection"])
    binding = review_binding(record, data, contract, kind=kind)
    actors = validate_roster(contract)
    validate_review(record, contract, binding, actors, kind=kind)
    validate_progress(contract, binding, actors, require_product_write=require_product_write)
    states = {row["id"]: row for row in contract["progress"]["phases"]}
    if completing is None:
        completing = (data.get("status") in {"complete", "completed"}
                      or any(phase["kind"] == "report" and states[phase["id"]]["status"] != "pending"
                             for phase in contract["selection"]["phases"]))
    if completing:
        _require(all(states[phase["id"]]["status"] == "complete" for phase in contract["selection"]["phases"]
                     if phase["kind"] != "report"), "completion requires every selected non-report phase to be complete")
    team = validate_actual_workers(contract, completing=completing, work_hash=canonical_hash(binding))
    briefing = _object(contract.get("briefing"), "briefing")
    _require(briefing.get("status") == "declared" and briefing.get("kind") == "portable-declaration",
             "public briefing declaration is missing; a local snapshot is not delivery")
    _require(briefing.get("binding") == briefing_binding(data, contract, binding),
             "briefing is stale for the current workflow, phases, review or actual roster")
    _require(_text(briefing.get("context")) and _texts(briefing.get("evidence")),
             "briefing needs actual public-message context and evidence references")
    # Markdown blank lines and hard-break spaces do not change disclosed facts.
    # Preserve every nonblank line, its content and order; do not normalize words,
    # field values, leading indentation, omissions, or reordered phases.
    def presentation_lines(value):
        return [line.rstrip() for line in value.splitlines() if line.strip()]
    required_lines = presentation_lines(render_briefing(data, contract))
    actual_lines = presentation_lines(briefing.get("text", "")) if isinstance(briefing.get("text"), str) else []
    contains_block = any(actual_lines[index:index + len(required_lines)] == required_lines
                         for index in range(len(actual_lines) - len(required_lines) + 1))
    _require(_text(briefing.get("text")) and contains_block,
             "briefing text must contain the current complete required block")
    return {"admitted": bool(require_product_write), "reviewValidated": True,
            "workHash": canonical_hash(binding), "requiredContributors": team["minimumContributors"],
            "returnedContributors": team["returnedContributorCount"], "completionValidated": bool(completing), "boundary": BOUNDARY}


def pending_discovery():
    """Return an explicitly incomplete current receipt for a newly allocated task."""
    return {"schema": "ai-development-workflow/discovery-v1", "initialQuery": "", "refinedQuery": None,
            "indexFingerprint": "", "matches": [], "selected": [], "recipeRecommendations": []}


def validate_current_discovery(selected):
    """Require current authoritative discovery before an execution gate can pass."""
    from workflow_catalog import (SELECTION_SCHEMA, build_catalog, build_search_index,
                                  validate_discovery)
    _require(selected.get("selectionSchema") == SELECTION_SCHEMA,
             "current selectionSchema and discovery reconciliation are required before execution")
    root = Path(__file__).resolve().parents[1]
    index = build_search_index(root, build_catalog(root))
    errors = validate_discovery(selected.get("discovery"), selected, index)
    _require(not errors, "current discovery receipt is invalid before execution: " + "; ".join(errors))


def pending_contract(workflow="G1", *, write_scope="repo-write-scoped"):
    definitions = [("scope", "Capture scope", "capture", "capture-scope", "record-only"),
                   ("plan", "Plan", "plan", "plan-changes", "record-only"),
                   ("critique", "Criticize and revise", "critique", "criticize-plan", "record-only"),
                   ("execute", "Implement", "execute", "implement-plan", write_scope),
                   ("verify", "Verify", "verify", "verify-outcomes", "test-output-only"),
                   ("accept", "Independent acceptance", "verify", "review-result", "read-only")]
    phases = [{"id": key, "title": title, "kind": kind, "operation": operation, "writeScope": scope,
               "owner": "coordinator", "dependsOn": [] if index == 0 else [definitions[index - 1][0]]}
              for index, (key, title, kind, operation, scope) in enumerate(definitions)]
    return {"schema": SCHEMA,
            "selection": {"selectionSchema": "ai-development-workflow/selection-v2",
                          "discovery": pending_discovery(),
                          "workflow": workflow, "mode": None, "reason": "", "reviewPolicy": "independent",
                          "routing": pending_routing(),
                          "uiContext": {"applicable": None, "kind": None, "reason": ""},
                          "verificationContext": {"required": None, "triggers": [], "reason": ""},
                          "delegation": {"policy": "required", "reason": "", "evidence": [], "assignments": []},
                          "phases": phases},
            "progress": {"currentPhase": "scope", "resultRevision": None, "phases": [{"id": phase["id"], "status": "pending",
                         "ownerId": None, "authorIds": [], "evidence": [], "workHash": None} for phase in phases]},
            "roster": {"coordinatorId": "", "workers": [], "plannedWorkers": [], "profiles": [], "assignments": [], "activeAgentCount": 1},
            "contributions": [],
            "review": {"status": "pending", "decision": "pending", "mode": "independent", "authorId": "",
                       "reviewerId": "", "binding": None,
                       "checks": [{"area": area, "observation": "", "evidence": []} for area in sorted(REVIEW_AREAS)],
                       "findings": [], "noFindingsRationale": "", "evidence": []},
            "briefing": {"status": "pending", "kind": "portable-declaration", "binding": None,
                         "text": "", "context": "", "evidence": []}}



def migration_proposal(old):
    """Preserve old evidence while enumerating explicit active reconciliation.

    No new identity, contribution, review receipt or source rewrite is invented.
    The returned template cannot pass admission until genuine missing work is done.
    """
    _require(isinstance(old, dict) and old.get("schema") == LEGACY_SCHEMA,
             "migration-proposal expects an archived/active contract-v1 declaration")
    proposed = pending_contract(old.get("selection", {}).get("workflow", "G1"))
    for key in ("coordinatorId", "workers", "plannedWorkers", "profiles", "activeAgentCount"):
        if key in old.get("roster", {}):
            proposed["roster"][key] = copy.deepcopy(old["roster"][key])
    # Keep references/history verbatim for human reconciliation. They do not
    # become v2 phase status, author sets, contributions or current criticism.
    proposed["legacyEvidence"] = {"sourceContractHash": canonical_hash(old), "contract": copy.deepcopy(old)}
    return {"status": "reconciliation-required", "executionAdmitted": False,
            "sourceContractHash": canonical_hash(old), "proposedContract": proposed,
            "requiredActions": [
                "Preserve the original record and archived evidence bytes.",
                "Reconcile the actual current source, scope, phases and all substantive authors.",
                "Resolve legacy profiles and operation-specific capabilities against the current registry.",
                "Observe actual assignments and obtain any missing useful independent contributions.",
                "Declare current UI/verification facts and exact final-result revision where available.",
                "Obtain genuine current criticism and acceptance; never silently rehash historical review.",
                "Deliver the current briefing and pass the current execution/completion gate.",
            ], "boundary": BOUNDARY}

def load_quick(record):
    record = Path(record).expanduser()
    _require(not record.is_symlink(), "quick record directory cannot be a symlink")
    record = record.resolve(strict=True)
    for name in ("request.md", "checklist.md", "workflow-contract.json"):
        path = record / name
        _require(path.is_file() and not path.is_symlink() and path.stat().st_size > 0,
                 "missing, empty or symlinked quick file: " + name)
    data = _object(json.loads((record / "workflow-contract.json").read_text()), "quick contract")
    return record, data


def validate_quick(record):
    record, data = load_quick(record)
    plan = _object(data.get("plan"), "quick plan")
    steps = _rows(plan.get("steps"), "quick plan.steps")
    earlier = set()
    for key, step in steps.items():
        _require(_text(step.get("change")) and _texts(step.get("paths")), "quick steps need concrete changes and paths")
        deps = step.get("dependsOn")
        _require(isinstance(deps, list) and all(_text(dep) for dep in deps) and set(deps) <= earlier,
                 "quick plan dependencies must refer to preceding steps")
        earlier.add(key)
    checks = _rows(plan.get("checks"), "quick plan.checks")
    covered = set()
    for check in checks.values():
        _require(all(_text(check.get(key)) for key in ("method", "expected", "boundary"))
                 and _texts(check.get("steps")) and set(check["steps"]) <= steps.keys(),
                 "quick checks need mapped steps, method, expected result and evidence boundary")
        covered.update(check["steps"])
    _require(covered == set(steps), "quick checks must cover every plan step")
    return validate_contract(record, data, data, kind="quick")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["template", "migration-proposal", "validate", "snapshot", "briefing-text"])
    parser.add_argument("--record", required=True, type=Path)
    parser.add_argument("--kind", choices=["development", "quick"], default="development")
    parser.add_argument("--workflow")
    parser.add_argument("--completion", action="store_true", help="With validate, require current closure; never changes record status or grants execution")
    parser.add_argument("--write-scope", choices=sorted(WRITE_SCOPES), default="repo-write-scoped")
    args = parser.parse_args()
    try:
        record = args.record.expanduser().resolve(strict=True)
        if args.command == "migration-proposal":
            data = json.loads((record / ("workflow-contract.json" if args.kind == "quick" else "record.json")).read_text())
            old = data if args.kind == "quick" else data.get("workflowContract")
            print(json.dumps(migration_proposal(old), indent=2))
            return 0
        if args.command == "template":
            workflow = args.workflow or ("G0" if args.kind == "quick" else
                       json.loads((record / "record.json").read_text()).get("workflowPreset", "G1"))
            result = pending_contract(workflow, write_scope=args.write_scope)
            if args.kind == "quick":
                result.update(planRevision=1, scope={"in": [], "out": []},
                              sourceBaseline={"description": ""}, plan={"steps": [], "checks": []})
            print(json.dumps(result, indent=2))
            return 0
        if args.kind == "quick":
            record, data = load_quick(record)
            contract = data
        else:
            data = json.loads((record / "record.json").read_text())
            contract = data.get("workflowContract")
            # Match the finalizer's prospective append-only seal without writing anything.
            # This supports a reviewed revision with new source addenda; edited old sources fail.
            from plan_record import seal_request_sources
            data["requestHashes"] = seal_request_sources(data)
        if args.completion and args.command != "validate":
            raise ValueError("--completion is only valid with the read-only validate command")
        if args.command == "validate":
            result = validate_contract(record, data, contract, kind=args.kind, require_product_write=False,
                                       completing=True if args.completion else None)
            result.update(executionAdmitted=False, validationOnly=True)
            print(json.dumps(result, indent=2))
            return 0
        binding = review_binding(record, data, contract, kind=args.kind)
        if args.command == "briefing-text":
            print(render_briefing(data, contract))
        else:
            print(json.dumps({"status": "snapshot-only", "reviewBinding": binding,
                              "workHash": canonical_hash(binding),
                              "briefingBinding": briefing_binding(data, contract, binding),
                              "boundary": BOUNDARY}, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
