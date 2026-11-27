"""Synthetic declarations for isolated structural tests, never live receipts.

The helper deliberately authors fixtures and rebinds their synthetic revisions;
production finalizers never fabricate these identities, contributions or reviews.
"""
import copy
from functools import lru_cache

from plan_record import PLAN_FILES, definition_hash, digest, seal_request_sources
from workflow_contract import briefing_binding, canonical_hash, pending_contract, render_briefing, review_binding
from agent_registry import load_registry, resolve_profile
from task_policy import CODE_REVIEWER, EXECUTOR, FAST_ENGINEER, PLAN_REVIEWER


@lru_cache(maxsize=1)
def fixture_discovery_index():
    from workflow_catalog import build_catalog, build_search_index
    catalog = build_catalog()
    return build_search_index(catalog=catalog)


def declare_discovery(contract, query="Plan and review a workflow fixture dispatch"):
    """Attach a current synthetic search receipt; this is not production evidence."""
    from workflow_catalog import DISCOVERY_SCHEMA, SELECTION_SCHEMA, search_resources
    index = fixture_discovery_index()
    report = search_resources(query, index)
    contract["selection"]["selectionSchema"] = SELECTION_SCHEMA
    contract["selection"]["discovery"] = {
        "schema": DISCOVERY_SCHEMA, "initialQuery": query, "refinedQuery": None,
        "indexFingerprint": index["indexFingerprint"],
        "matches": [{"id": row["id"], "score": row["score"]}
                    for rows in report["groups"].values() for row in rows],
        "selected": [], "recipeRecommendations": [],
    }
    return contract


def fixture_assignment(phase, profile, independent=(), *, identity=None, capabilities=None, question=None):
    role = resolve_profile(profile, capabilities=capabilities)
    return {"id": identity or phase, "phaseId": phase, "profile": profile,
            "capabilities": role["capabilities"], "independentFrom": list(independent),
            "question": question or "Inspect the concrete fixture source and produce the assigned " + phase + " result."}


def normalize_fixture_assignments(contract):
    """Adapt old test construction syntax only; this is never a runtime migration."""
    for index, row in enumerate(contract["selection"]["delegation"]["assignments"]):
        row.setdefault("id", row["phaseId"] + "-" + str(index))
        if "capabilities" not in row:
            row["capabilities"] = resolve_profile(row["profile"])["capabilities"]
        row.setdefault("question", "Inspect the concrete fixture boundary for duty " + row["id"] + ".")


def declare_policy(contract, *, mode="build", impact="standard", assignments=None):
    selected = contract["selection"]
    selected.update(mode=mode, routing={
        "impact": impact, "affectedPages": [], "affectedFeatures": ["fixture dispatch"],
        "changedSharedContract": False, "architectureOrMigration": False,
        "reason": "The fixture declares one inspected dispatch owner and no shared changes.",
        "evidence": ["fixture:source-inspection"],
    }, uiContext={"applicable": False, "kind": "none", "reason": "The fixture changes backend dispatch only."},
       verificationContext={"required": False, "triggers": [], "reason": "One bounded fixture check suffices for this synthetic case."})
    executor = FAST_ENGINEER if selected["workflow"] in {"G0", "GB"} or impact == "small-localized" else EXECUTOR
    selected["delegation"] = {
        "policy": "required", "reason": "Exercise useful independent worker declarations in an isolated fixture.",
        "evidence": ["fixture:task-policy"], "assignments": assignments if assignments is not None else [
            fixture_assignment("critique", PLAN_REVIEWER, ["plan"]),
            fixture_assignment("execute", executor, capabilities=["execute-plan", "update-docs"]
                               if any(phase["id"] == "execute" and phase["writeScope"] == "docs-only" for phase in selected["phases"]) else None),
            fixture_assignment("accept", CODE_REVIEWER, ["plan", "execute"]),
        ],
    }
    normalize_fixture_assignments(contract)
    declare_discovery(contract)
    return contract


def declare_returned_contributions(contract):
    """Create explicit useful fixture outputs for completed assigned duties."""
    states = {row["id"]: row for row in contract["progress"]["phases"]}
    bound = {row["assignmentId"]: row["workerId"] for row in contract["roster"]["assignments"]}
    rows = []
    for assignment in contract["selection"]["delegation"]["assignments"]:
        phase = assignment["phaseId"]
        if states[phase]["status"] != "complete":
            continue
        actor = bound[assignment["id"]]
        family = resolve_profile(assignment["profile"], capabilities=assignment["capabilities"])["family"]
        kind = ("authoring" if actor in states[phase]["authorIds"] else
                "independent-review" if family == "reviewer" else "verification" if family == "verification-engineer" else "investigation")
        rows.append({"id": "fixture-contribution-" + assignment["id"], "assignmentId": assignment["id"], "workerId": actor,
                     "kind": kind, "summary": "Fixture inspection accounts for the actual declared " + phase + " output and preserved boundary.",
                     "evidence": ["fixture:source-and-result-" + phase], "limitations": ["Synthetic structural fixture; no live host dispatch is claimed."],
                     "workHash": "fixture:pending-binding", "artifactRevision": "fixture:artifact-" + phase,
                     "resultRevision": contract["progress"].get("resultRevision") if phase == "accept" or family == "verification-engineer" else None,
                     "disposition": "incorporated", "effect": "The fixture resolves the assigned " + phase + " duty without widening scope."})
    contract["contributions"] = rows


def refresh_contract(record, data):
    contract = data["workflowContract"]
    normalize_fixture_assignments(contract)
    binding = review_binding(record, data)
    contract["review"]["binding"] = binding
    for row in contract["progress"]["phases"]:
        if row["status"] == "complete":
            row["workHash"] = canonical_hash(binding)
    for row in contract["contributions"]:
        row["workHash"] = canonical_hash(binding)
    contract["briefing"].update(binding=briefing_binding(data, contract, binding), text=render_briefing(data, contract))
    return binding


def declare_review(record, data, *, outcome="ready", finalized=True):
    data["critiqueOutcome"] = outcome
    (record / "critique.md").write_text(
        "# Synthetic unit-test critique\n\nThis is fixture data, not evidence of a real reviewer or public message.\n\n"
        f"Declared review for fixture revision {data['planRevision']}.\n"
        "The fixture covers its R/P/T mapping, ordered preparation, scope exclusions and preserved source identities.\n")
    contract = pending_contract(data.get("workflowPreset", "G1"))
    contract["selection"]["reason"] = "Exercise the portable admission contract on an isolated unit-test record."
    declare_policy(contract)
    actor, critic, executor = "fixture:coordinator", "fixture:critic", "fixture:executor"
    contract["roster"].update(coordinatorId=actor, activeAgentCount=2, workers=[
        {"id": critic, "role": "independent reviewer", "status": "completed", "evidence": ["fixture:critic-result"]},
        {"id": executor, "role": "specialist executor", "status": "running", "evidence": ["fixture:executor-dispatch"]},
    ], profiles=[{"name": row["profile"], "ownerId": executor if row["phaseId"] == "execute" else critic}
                 for row in contract["selection"]["delegation"]["assignments"]],
       assignments=[{"assignmentId": row["id"], "workerId": executor if row["phaseId"] == "execute" else critic}
                    for row in contract["selection"]["delegation"]["assignments"]])
    for phase in contract["selection"]["phases"]:
        if phase["id"] in {"critique", "accept"}:
            phase["owner"] = "independent reviewer"
        elif phase["id"] == "execute":
            phase["owner"] = "specialist executor"
    contract["progress"]["currentPhase"] = "execute"
    for row in contract["progress"]["phases"]:
        if row["id"] in {"scope", "plan", "critique"}:
            row.update(status="complete", ownerId=critic if row["id"] == "critique" else actor,
                       authorIds=[actor] if row["id"] == "plan" else [], evidence=["fixture:preparation"])
        elif row["id"] == "execute":
            row.update(status="in-progress", ownerId=executor, authorIds=[executor])
    declare_returned_contributions(contract)
    prospective = copy.deepcopy(data)
    prospective["requestHashes"] = seal_request_sources(data)
    prospective["workflowContract"] = contract
    binding = review_binding(record, prospective, contract)
    observations = {
        "scope": "The synthetic R1 preserves requester identity and excludes deployment.",
        "feasibility": "P1 names the fixture dispatch path; no real project execution is claimed.",
        "dependencies": "The fixture preparation phases precede its single implementation phase.",
        "verification": "T1 describes two requester identities and states its fixture-only boundary.",
        "preservation": "The append-only source seal retains the fixture original user request.",
    }
    contract["review"].update(status="complete", decision=outcome, mode="independent", authorId=actor, reviewerId=critic,
        binding=binding, checks=[{"area": area, "observation": observation, "evidence": ["fixture:critique.md"]}
                                 for area, observation in sorted(observations.items())], findings=[],
        noFindingsRationale="This valid synthetic declaration isolates structural admission checks and makes no production review claim.",
        evidence=["fixture:critique.md"])
    for row in contract["progress"]["phases"]:
        if row["status"] == "complete":
            row["workHash"] = canonical_hash(binding)
    for row in contract["contributions"]:
        row["workHash"] = canonical_hash(binding)
    contract["briefing"].update(status="declared", kind="portable-declaration",
        binding=briefing_binding(prospective, contract, binding), text=render_briefing(prospective, contract),
        context="Synthetic unit-test message context; no actual chat delivery.", evidence=["fixture:simulated-public-briefing"])
    data["workflowContract"] = contract
    if finalized:
        data["requestHashes"] = prospective["requestHashes"]
        data["readiness"] = "ready"
        data["reviewedPlanRevision"] = data["planRevision"]
        data["critiqueHash"] = digest(record / "critique.md")
        data["planHashes"] = {name: digest(record / name) for name in PLAN_FILES}
        data["definitionHash"] = definition_hash(data)
    return data


def make_readonly_contract(record, data, mode, *, complete=False):
    """A real two-duty structural Plan/Review fixture with no product writes."""
    from task_policy import ASSESSOR, PLANNER
    contract = data["workflowContract"]
    selected = contract["selection"]
    selected.update(workflow=mode, mode=mode, reason="The fixture explicitly preserves its record-only " + mode + " operation.")
    selected["phases"] = selected["phases"][:3]
    states = contract["progress"]["phases"][:3]
    for state in states:
        state["authorIds"] = ["fixture:executor" if mode == "plan" else "fixture:coordinator"] if state["id"] == "plan" else []
        if state["id"] == "plan" and mode == "plan":
            state["ownerId"] = "fixture:executor"
    assignments = ([fixture_assignment("plan", PLANNER), fixture_assignment("critique", PLAN_REVIEWER, ["plan"])] if mode == "plan" else
                   [fixture_assignment("critique", PLAN_REVIEWER, ["plan"]), fixture_assignment("inspect", ASSESSOR),
                    fixture_assignment("corroborate", CODE_REVIEWER, ["plan", "inspect"])])
    previous = "critique"
    for identity, kind in (([("inspect", "other"), ("corroborate", "verify")] if mode == "review" else []) + [("report", "report")]):
        selected["phases"].append({"id": identity, "title": identity.title() + " fixture output", "kind": kind,
                                   "operation": identity + "-only", "writeScope": "record-only", "owner": "coordinator" if identity == "report" else "assigned worker",
                                   "dependsOn": [previous]})
        finished = complete and identity != "report"
        states.append({"id": identity, "status": "complete" if finished else "pending", "ownerId": ("fixture:executor" if identity == "inspect" else "fixture:critic") if finished else None,
                       "authorIds": [], "evidence": ["fixture:current-" + identity] if finished else [], "workHash": None})
        previous = identity
    contract["progress"].update(phases=states, currentPhase="corroborate" if complete and mode == "review" else "critique", resultRevision=None)
    declare_policy(contract, mode=mode, assignments=assignments)
    contract["roster"]["assignments"] = [{"assignmentId": row["id"], "workerId": "fixture:executor" if row["phaseId"] in {"plan", "inspect"} else "fixture:critic"} for row in assignments]
    contract["roster"]["profiles"] = [{"name": row["profile"], "ownerId": "fixture:executor" if row["phaseId"] in {"plan", "inspect"} else "fixture:critic"} for row in assignments]
    for worker in contract["roster"]["workers"]:
        worker["status"] = "completed" if complete or mode == "plan" or worker["id"] == "fixture:critic" else "running"
    contract["roster"]["activeAgentCount"] = 1 + sum(row["status"] == "running" for row in contract["roster"]["workers"])
    contract["review"]["authorId"] = "fixture:executor" if mode == "plan" else "fixture:coordinator"
    declare_returned_contributions(contract)
    refresh_contract(record, data)
    return contract
