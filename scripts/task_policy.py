"""Shared source-grounded routing and two-contributor team policy.

These are portable declarations, not host dispatch or authenticated evidence.
The host supplies facts, observes actual workers and judges useful contributions.
"""
from pathlib import Path

from agent_registry import load_registry, resolve_profile

CONCRETE_MODES = {"plan", "build", "review", "loop"}
IMPACTS = {"unknown", "small-localized", "standard", "cross-cutting"}
PRODUCT_SCOPES = {"repo-write-scoped", "tests-only", "docs-only"}
WRITE_SCOPES = PRODUCT_SCOPES | {"external-write"}
ARCHITECT = "agents/architect/agent.md"
BUILDER = "agents/builder/agent.md"
REVIEWER = "agents/reviewer/agent.md"
INVESTIGATOR = "agents/investigator/agent.md"
VERIFIER = "agents/verification-engineer/agent.md"
# Public Python aliases retain the old profile paths for explicit compatibility
# callers. Canonical dispatch uses the resolver, not these names as identities.
FAST_ENGINEER = "agents/fast-engineer/agent.md"
EXECUTOR = "agents/implementation-executor/agent.md"
PLAN_REVIEWER = "agents/plan-reviewer/agent.md"
CODE_REVIEWER = "agents/code-reviewer/agent.md"
ASSESSOR = "agents/codebase-assessor/agent.md"
PLANNER = "agents/code-goal-planner/agent.md"
UI_DIRECTOR = "agents/ui-design-director/agent.md"
VISUAL_REVIEWER = "agents/visual-fidelity/agent.md"
ROOT = Path(__file__).resolve().parents[1]
VERIFICATION_TRIGGERS = {"multiple-families", "multiple-environments", "specialized-measurement", "lifecycle",
                         "substantial-browser-journeys", "independent-deliverable"}
CONTRIBUTION_KINDS = {"authoring", "investigation", "independent-review", "verification"}
AUTHOR_CAPABILITIES = {"design-architecture", "design-ui", "plan-goals", "plan-code", "plan-tests"}
PLACEHOLDERS = {"pending", "todo", "tbd", "unknown", "not started", "not-started", "status", "running",
                "done", "complete", "completed", "looks good", "ok", "okay", "no output", "not yet reviewed"}


def _require(condition, message):
    if not condition:
        raise ValueError("task policy: " + message)


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _authored(value):
    return _text(value) and value.strip().lower().strip("_ .") not in PLACEHOLDERS


def _strings(value, *, nonempty=False):
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(_text(item) for item in value) and len(value) == len(set(value)))


def descriptor():
    return {
        "instructions": "references/task-routing.md", "registry": "agents/registry.json",
        "policy": "required", "concreteModes": sorted(CONCRETE_MODES),
        "minimumContributors": 2, "coreFamilies": 6,
        "requiresActualWorkers": True, "requiresUsefulContributions": True, "allowsSolo": False,
        "writingRequiresIndependentCriticAndReviewer": True, "independenceIncludesAllAuthors": True,
        "requiresSourceGroundedImpact": True, "assignedChildrenRecurse": False,
        "missingDispatch": "blocked", "busyWorkers": "wait-or-serialize", "dispatchesAgents": False,
    }


def validate_contexts(ui, verification):
    _require(isinstance(ui, dict) and set(ui) == {"applicable", "kind", "reason"}
             and type(ui["applicable"]) is bool and ui["kind"] in {"none", "mechanical", "design", "shared"}
             and _authored(ui["reason"]), "uiContext requires explicit applicable, none/mechanical/design/shared kind and reason")
    _require(ui["applicable"] == (ui["kind"] != "none"), "UI applicability and kind disagree")
    _require(isinstance(verification, dict) and set(verification) == {"required", "triggers", "reason"}
             and type(verification["required"]) is bool and _strings(verification["triggers"])
             and set(verification["triggers"]) <= VERIFICATION_TRIGGERS and _authored(verification["reason"]),
             "verificationContext requires required, known distinct triggers and a source-grounded reason")
    _require(verification["required"] == bool(verification["triggers"]), "substantial verification flag must agree with its triggers")


def routing_requirements(mode, routing, ui=None, verification=None):
    _require(mode in CONCRETE_MODES, "mode must resolve to plan, build, review or loop; Auto is only a selector")
    _require(isinstance(routing, dict), "routing decision is required")
    fields = {"impact", "affectedPages", "affectedFeatures", "changedSharedContract", "architectureOrMigration", "reason", "evidence"}
    _require(set(routing) == fields, "routing needs exactly impact, affectedPages, affectedFeatures, changedSharedContract, architectureOrMigration, reason and evidence")
    impact = routing["impact"]
    _require(impact in IMPACTS, "routing impact is unknown")
    _require(_strings(routing["affectedPages"]) and _strings(routing["affectedFeatures"]), "affectedPages and affectedFeatures must be distinct nonblank lists")
    _require(_authored(routing["reason"]) and _strings(routing["evidence"], nonempty=True), "routing requires a concrete reason and source evidence")
    flags = [routing["changedSharedContract"], routing["architectureOrMigration"]]
    _require(all(type(flag) is bool or (impact == "unknown" and flag is None) for flag in flags), "known impact requires boolean shared-contract and architecture/migration facts")
    broad = (len(routing["affectedPages"]) > 1 or len(routing["affectedFeatures"]) > 1 or any(flag is True for flag in flags))
    _require(not broad or impact in {"cross-cutting", "unknown"}, "multiple pages/features or shared/architecture changes require cross-cutting impact")
    _require(impact != "small-localized" or bool(routing["affectedPages"] or routing["affectedFeatures"]), "small-localized impact needs an identified affected page or feature")
    architect = broad or impact == "cross-cutting"
    if ui is not None or verification is not None:
        validate_contexts(ui, verification)
        architect = architect or ui["kind"] == "shared"
    return {"mode": mode, "impact": impact, "impactResolved": impact != "unknown",
            "architectRequired": architect, "fastRequired": mode == "build" and impact == "small-localized" and not architect,
            "uiDirectorRequired": bool(ui and ui["kind"] in {"design", "shared"}),
            "verificationEngineerRequired": bool(verification and verification["required"]),
            "recommendedWorkflow": ("GA" if architect and mode == "build" else "GB" if mode == "build" and impact == "small-localized" else None),
            "assessmentRequired": impact == "unknown", "minimumContributors": 2}


def pending_routing():
    return {"impact": "unknown", "affectedPages": [], "affectedFeatures": [], "changedSharedContract": None,
            "architectureOrMigration": None, "reason": "", "evidence": []}


def policy_binding(selection):
    result = {key: selection.get(key) for key in ("selectionSchema", "discovery", "workflow", "mode", "originMode", "reviewPolicy", "routing", "delegation", "uiContext", "verificationContext")}
    result["registryFingerprint"] = load_registry()["fingerprint"]
    return result


def _ancestors(phases, key):
    result = set(phases[key]["dependsOn"])
    for dependency in phases[key]["dependsOn"]:
        result.update(_ancestors(phases, dependency))
    return result


def validate_policy(selected, phases=None, *, root=ROOT, profile_paths=None, registry=None):
    validate_contexts(selected.get("uiContext"), selected.get("verificationContext"))
    requirements = routing_requirements(selected.get("mode"), selected.get("routing"), selected["uiContext"], selected["verificationContext"])
    registry = load_registry(root) if registry is None else registry
    delegation = selected.get("delegation")
    _require(isinstance(delegation, dict) and set(delegation) == {"policy", "reason", "evidence", "assignments"}, "delegation needs policy, reason, evidence and assignments")
    _require(delegation["policy"] == "required", "actual delegation is required for every task; there is no solo waiver")
    _require(_authored(delegation["reason"]) and _strings(delegation["evidence"], nonempty=True), "delegation requires a reason and evidence")
    assignments = delegation["assignments"]
    _require(isinstance(assignments, list) and len(assignments) >= 2, "at least two useful worker assignments are required")
    seen, resolved = set(), {}
    for row in assignments:
        _require(isinstance(row, dict) and set(row) == {"id", "phaseId", "profile", "capabilities", "independentFrom", "question"}, "each assignment needs id, phaseId, profile, capabilities, independentFrom and question")
        identity, phase, profile = row["id"], row["phaseId"], row["profile"]
        _require(_text(identity) and identity not in seen and _text(phase) and _text(profile), "assignment IDs must be distinct and phase/profile nonblank")
        seen.add(identity)
        _require(_authored(row["question"]) and _strings(row["capabilities"], nonempty=True), "each worker needs a useful bounded question and explicit capabilities")
        _require(_strings(row["independentFrom"]) and phase not in row["independentFrom"], "independentFrom must contain distinct other phase IDs")
        if profile_paths is not None:
            _require(profile in profile_paths, "assignment profile is missing from the bundled inventory: " + profile)
        phase_spec = (phases or {}).get(phase, {})
        resolved[identity] = resolve_profile(profile, phase_spec.get("operation"), phase_spec.get("writeScope"),
                                              capabilities=row["capabilities"], registry=registry, allow_custom_operation=True)
    families = {value["family"] for value in resolved.values()}
    _require("reviewer" in families, "every task requires a useful Reviewer contribution or bounded independent corroboration")
    if requirements["architectRequired"]:
        _require(any(value["family"] == "architect" and "design-architecture" in value["capabilities"] for value in resolved.values()), "cross-cutting work requires an actual Architect advice assignment before the final plan")
    fast = requirements["fastRequired"] or (selected.get("mode") == "build" and str(selected.get("workflow", "")).lower() in {"g0", "gb"})
    if fast:
        _require(any(value["family"] == "builder" and "fast-build" in value["capabilities"] for value in resolved.values()), "small Build and explicit G0/GB require the complete Fast Builder capability")
    if requirements["uiDirectorRequired"]:
        _require("ui-design-director" in families, "design-bearing UI requires a distinct UI Director assignment")
    if requirements["verificationEngineerRequired"]:
        _require("verification-engineer" in families, "substantial validation requires a distinct Verification Engineer assignment")
    requirements["resolvedAssignments"] = resolved
    if phases is None:
        return requirements

    phase_ids = set(phases)
    _require(all(row["phaseId"] in phase_ids and set(row["independentFrom"]) <= phase_ids for row in assignments), "worker assignments must refer to selected phase IDs")
    by_phase = {}
    for row in assignments:
        by_phase.setdefault(row["phaseId"], []).append(row)
    meaningful = {key for key in by_phase if phases[key]["kind"] not in {"capture", "report"}}
    _require(bool(meaningful), "delegate a meaningful operation, not only capture or reporting")
    writes = {key for key, phase in phases.items() if phase["writeScope"] in WRITE_SCOPES}
    product_writes = {key for key in writes if phases[key]["writeScope"] in PRODUCT_SCOPES}
    plans = {key for key, phase in phases.items() if phase["kind"] == "plan"}
    family_phases = {family: {row["phaseId"] for row in assignments if resolved[row["id"]]["family"] == family} for family in registry["families"]}
    architects = {row["phaseId"] for row in assignments if resolved[row["id"]]["family"] == "architect" and "design-architecture" in resolved[row["id"]]["capabilities"]}
    designers = {row["phaseId"] for row in assignments if resolved[row["id"]]["family"] == "ui-design-director" and bool({"design-ui", "visual-fidelity"} & set(resolved[row["id"]]["capabilities"]))}
    preparation_authors = plans | architects | designers
    if requirements["architectRequired"]:
        _require(all(phases[key]["kind"] == "other" and phases[key]["writeScope"] in {"read-only", "record-only"} for key in architects), "Architect must own a distinct advice operation, not a capture-only label")
        _require(all(any(architect in _ancestors(phases, plan) for architect in architects) for plan in plans), "Architect advice must be a prerequisite of the finalized plan")
    if requirements["uiDirectorRequired"]:
        _require(bool(designers), "UI Director must produce actual design/reference advice")
        _require(all(any(designer == plan or designer in _ancestors(phases, plan) for designer in designers) for plan in plans), "UI design advice must precede the finalized plan")
    for row in assignments:
        phase = phases[row["phaseId"]]
        value = resolved[row["id"]]
        if phase["kind"] == "critique":
            _require(value["family"] == "reviewer" and "review-plan" in value["capabilities"], "independent plan criticism belongs to Reviewer with review-plan capability")
        if phase["writeScope"] in PRODUCT_SCOPES:
            _require(value["family"] == "builder", "each product/test/docs writer must be a bounded Builder assignment")
    # A publication-only task can delegate inspection/preparation of the existing
    # artifact. Its external writer remains the coordinator after acceptance.
    external_preparation = {key for key in meaningful if phases[key]["kind"] in {"other", "execute", "verify"}
                            and phases[key]["writeScope"] not in WRITE_SCOPES
                            and any(not row["independentFrom"] for row in by_phase[key])}
    review_subjects = (product_writes or external_preparation) if writes else set()
    if fast:
        _require(any(row["phaseId"] in review_subjects and "fast-build" in resolved[row["id"]]["capabilities"] for row in assignments), "Fast Builder must own the selected implementation or artifact-preparation operation")
    critics = {key for key in by_phase if phases[key]["kind"] == "critique"}
    acceptance = set()
    verification_before_acceptance = {}
    counter_subjects = set()
    counters = set()
    if writes:
        _require(requirements["impactResolved"], "unknown impact must be assessed before implementation can be admitted")
        _require(selected.get("reviewPolicy") == "independent", "writing work requires independent criticism")
        delegated_writes = product_writes & set(by_phase)
        integration = product_writes - delegated_writes
        _require((bool(delegated_writes) and all(phases[key]["kind"] == "execute" and bool(delegated_writes & _ancestors(phases, key)) for key in integration))
                 if product_writes else bool(external_preparation),
                 "writing needs meaningful Builder execution; coordinator integration must follow meaningful delegated Builder work")
        _require(bool(critics) and all(any(preparation_authors <= set(row["independentFrom"]) for row in by_phase[key]) for key in critics), "writing work requires a worker critic independent from every plan/architecture/design author")
        acceptance = {key for key in by_phase if phases[key]["kind"] == "verify" and phases[key]["writeScope"] not in WRITE_SCOPES
                      and review_subjects <= _ancestors(phases, key)
                      and any(resolved[row["id"]]["family"] == "reviewer" and review_subjects | preparation_authors <= set(row["independentFrom"]) for row in by_phase[key])}
        _require(bool(acceptance), "writing work requires independent result acceptance after every source writer and adopted preparation author")
        _require(all(any(review in _ancestors(phases, writer) for review in acceptance) for writer in writes - product_writes), "coordinator publication requires independent prepared-result acceptance before every external write")
        if requirements["verificationEngineerRequired"]:
            verifiers = family_phases["verification-engineer"]
            final_verifiers = {key for key in verifiers if review_subjects <= _ancestors(phases, key)
                               and phases[key]["writeScope"] not in WRITE_SCOPES}
            _require(bool(final_verifiers), "independent substantial verification must inspect the final written result")
            verification_before_acceptance = {key: final_verifiers & _ancestors(phases, key) for key in acceptance}
            _require(all(verification_before_acceptance.values()), "final acceptance must follow the separate substantial verification of the final result")
    else:
        # A countercheck is an internal duty, not an extra claimed numeric stage.
        # Ordinary approach preparation cannot stand in for checking the later
        # requested inspection. Plan's result is its finalized plan; an explicit
        # review-plan operation (including GPR) instead makes that review itself
        # the primary result to corroborate.
        if selected["mode"] == "plan":
            counter_subjects = plans & set(by_phase)
        else:
            preparation = plans | critics | {key for key in phases if phases[key]["kind"] == "capture"}
            for plan in plans:
                preparation.update(_ancestors(phases, plan))
            candidates = meaningful - preparation
            plan_reviews = {key for key in critics if key in by_phase and
                            (phases[key]["operation"].replace("_", "-") == "review-plan"
                             or str(selected["workflow"]).upper() == "GPR")}
            if plan_reviews and all(any(set(row["independentFrom"]) & plan_reviews
                                        and resolved[row["id"]]["family"] in {"reviewer", "verification-engineer"}
                                        for row in by_phase[key]) for key in candidates):
                # A named review-plan preparation is not the requested result
                # when an actual inspection follows it. This exception is only
                # for a plan review and its own bounded corroborating duties.
                candidates.update(plan_reviews)
            captures = {key for key in by_phase if phases[key]["kind"] == "capture"}
            if captures and not plans and all(any(set(row["independentFrom"]) & captures for row in by_phase[key]) for key in candidates):
                # Numeric capture-only work can corroborate its actual capture
                # without inventing a plan or an unselected numbered operation.
                candidates.update(captures)
            counter_subjects = {key for key in candidates
                                if not any(set(row["independentFrom"]) & candidates for row in by_phase[key])}
        counters = {row["phaseId"] for row in assignments if row["independentFrom"]
                    and resolved[row["id"]]["family"] in {"reviewer", "verification-engineer"}
                    and set(row["independentFrom"]) <= _ancestors(phases, row["phaseId"])
                    and bool(set(row["independentFrom"]) & counter_subjects)}
        _require(bool(counters), "Plan and read-only work require a distinct bounded countercheck after and independent from the actual primary result")
        if selected["mode"] == "plan":
            _require(bool(families & {"architect", "ui-design-director"}), "Plan requires a real Architect/Planner or the selected UI specification owner")
    if selected["uiContext"]["applicable"]:
        relevant = review_subjects if writes else meaningful - critics
        _require(any(row["phaseId"] in relevant and "ui-design" in resolved[row["id"]]["capabilities"] for row in assignments), "applicable UI work requires complete UI expertise on actual author/inspection activity")
        _require(any(resolved[row["id"]]["family"] in {"reviewer", "verification-engineer"}
                     and "ui-design" in resolved[row["id"]]["capabilities"]
                     and (not writes or row["phaseId"] in acceptance) for row in assignments), "UI work requires an independent UI-aware rendered-result countercheck")
        if writes:
            _require(any(row["phaseId"] in acceptance and "review-ui" in resolved[row["id"]]["capabilities"] for row in assignments), "UI implementation requires assigned rendered-result acceptance")
    required_families = {"builder", "reviewer"} if product_writes else {"reviewer"}
    if requirements["architectRequired"]:
        required_families.add("architect")
    if requirements["uiDirectorRequired"]:
        required_families.add("ui-design-director")
    if requirements["verificationEngineerRequired"]:
        required_families.add("verification-engineer")
    requirements.update(meaningfulPhases=meaningful, sourceWriterPhases=product_writes, reviewSubjectPhases=review_subjects,
                        criticPhases=critics, acceptancePhases=acceptance, architectPhases=architects, designerPhases=designers,
                        preparationAuthorPhases=preparation_authors, familyPhases=family_phases, requiredFamilies=required_families,
                        verificationBeforeAcceptance=verification_before_acceptance, counterSubjectPhases=counter_subjects,
                        countercheckPhases=counters,
                        minimumContributors=max(2, len(required_families)))
    return requirements


def preparation_authorship(contract):
    """Adopted preparation authors participate in exact critique bindings."""
    selected = contract["selection"]
    phases = {row["id"]: row for row in selected["phases"]}
    requirements = validate_policy(selected, phases)
    states = {row["id"]: row for row in contract.get("progress", {}).get("phases", [])}
    return {key: sorted(states.get(key, {}).get("authorIds", [])) for key in sorted(requirements["preparationAuthorPhases"])}


def _distinct_representatives(groups):
    """Required duties need distinct actors, while secondary duties may overlap."""
    ordered = sorted(groups, key=len)
    def visit(index, used):
        return index == len(ordered) or any(visit(index + 1, used | {actor}) for actor in ordered[index] - used)
    return visit(0, set())


def validate_actual_workers(contract, *, completing=False, work_hash=None):
    selected = contract["selection"]
    phases = {row["id"]: row for row in selected["phases"]}
    requirements = validate_policy(selected, phases)
    states = {row["id"]: row for row in contract["progress"]["phases"]}
    roster = contract["roster"]
    coordinator = roster["coordinatorId"]
    workers = {row["id"]: row for row in roster["workers"]}
    actors = set(workers) | {coordinator}
    applied = {(row["ownerId"], row["name"]) for row in roster["profiles"]}
    assignments = {row["id"]: row for row in selected["delegation"]["assignments"]}
    resolved = requirements["resolvedAssignments"]
    _require(bool(workers), "at least one actual worker is required during admission; plans/profiles are not dispatch")
    bindings = roster.get("assignments")
    _require(isinstance(bindings, list), "roster.assignments must bind observed dispatches explicitly")
    bound = {}
    for row in bindings:
        _require(isinstance(row, dict) and set(row) == {"assignmentId", "workerId"}
                 and row["assignmentId"] in assignments and row["assignmentId"] not in bound and row["workerId"] in workers,
                 "actual assignment bindings require unique selected assignment IDs and actual worker IDs")
        bound[row["assignmentId"]] = row["workerId"]
    for key, state in states.items():
        _require(_strings(state.get("authorIds")) and set(state["authorIds"]) <= actors, "every phase needs all substantive actual authorIds: " + key)
        if state["status"] != "pending" and (key in requirements["preparationAuthorPhases"] or key in requirements["sourceWriterPhases"]):
            _require(bool(state["authorIds"]) and state.get("ownerId") in state["authorIds"], "substantive phase owner and all adopted authors must be declared: " + key)
    by_phase = {}
    for identity, assignment in assignments.items():
        phase = assignment["phaseId"]
        by_phase.setdefault(phase, []).append(identity)
        owner = bound.get(identity)
        state = states[phase]
        if state["status"] != "pending":
            _require(owner in workers, "started delegated duty needs actual observed assignment binding: " + identity)
        if owner is not None:
            _require(workers[owner]["status"] != "failed", "failed worker cannot satisfy required delegation: " + identity)
            _require((owner, assignment["profile"]) in applied or (owner, resolved[identity]["profile"]) in applied, "actual worker must apply the assigned bundled profile: " + identity)
            for other in assignment["independentFrom"]:
                other_actors = set(states[other]["authorIds"]) | {states[other].get("ownerId")}
                other_actors.update(bound.get(key) for key, value in assignments.items() if value["phaseId"] == other)
                _require(owner not in other_actors, "required independent duty shares an actual author/worker identity: " + identity)
        if completing:
            _require(state["status"] == "complete", "task completion requires every delegated operation and acceptance to finish: " + phase)
    for phase in requirements["sourceWriterPhases"] - set(by_phase):
        if states[phase]["status"] != "pending":
            _require(states[phase].get("ownerId") == coordinator, "only the coordinator may own separately declared integration after actual Builder work")
    for phase, identities in by_phase.items():
        if states[phase]["status"] != "pending":
            assigned_actors = {bound.get(identity) for identity in identities} - {None}
            coordinator_plan = (states[phase].get("ownerId") == coordinator
                                and phases[phase]["kind"] == "plan"
                                and phases[phase]["writeScope"] in {"record-only", "read-only"}
                                and bool(assigned_actors & set(states[phase]["authorIds"])))
            _require(states[phase].get("ownerId") in assigned_actors or coordinator_plan,
                     "delegated phase owner must be one of its actual assigned workers, except a coordinator-finalized coauthored record-only plan: " + phase)
    current = contract["progress"]["currentPhase"]
    current_index = list(phases).index(current)
    overdue = {key for key in requirements["meaningfulPhases"] if list(phases).index(key) <= current_index}
    _require(all(states[key]["status"] in {"in-progress", "complete"} for key in overdue), "the current meaningful operation needs actual workers, not only planned roles")
    if requirements["architectRequired"]:
        _require(any(states[key]["status"] == "complete" for key in requirements["architectPhases"]), "actual Architect advice must finish before finalized plan admission")
    if requirements["uiDirectorRequired"]:
        _require(any(states[key]["status"] == "complete" for key in requirements["designerPhases"]), "actual UI Director advice must finish before finalized plan admission")
    writer_ids = {actor for key in requirements["reviewSubjectPhases"] for actor in states[key]["authorIds"]}
    writer_ids.update(bound.get(identity) for identity, row in assignments.items() if row["phaseId"] in requirements["sourceWriterPhases"])
    preparation_ids = {actor for key in requirements["preparationAuthorPhases"] for actor in states[key]["authorIds"]}
    for identity, row in assignments.items():
        if row["phaseId"] in requirements["criticPhases"] | requirements["acceptancePhases"]:
            _require(bound.get(identity) is None or bound[identity] not in writer_ids | preparation_ids, "a substantive plan/architecture/design/source/integration author cannot provide independent criticism or acceptance")
        if requirements["verificationEngineerRequired"] and resolved[identity]["family"] == "verification-engineer":
            _require(bound.get(identity) is None or bound[identity] not in writer_ids | preparation_ids, "required independent Verification Engineer cannot be an adopted author")
    family_actors = {family: {bound[identity] for identity in bound if resolved[identity]["family"] == family} for family in requirements["familyPhases"]}
    groups = [family_actors[family] for family in sorted(requirements["requiredFamilies"]) if family_actors[family]]
    _require(_distinct_representatives(groups), "required Architect/UI Director/Builder/Reviewer/Verifier duties need distinct actual identities")

    ledger = contract.get("contributions")
    _require(isinstance(ledger, list), "contributions must record actual useful returned work")
    seen, contributions, qualified = set(), {}, set()
    returned_family_actors = {family: set() for family in requirements["familyPhases"]}
    final_verifier_phases = set().union(*requirements["verificationBeforeAcceptance"].values())
    fields = {"id", "assignmentId", "workerId", "kind", "summary", "evidence", "limitations", "workHash",
              "artifactRevision", "resultRevision", "disposition", "effect"}
    for row in ledger:
        _require(isinstance(row, dict) and set(row) == fields, "each contribution needs exact identity/output/binding/disposition/effect and explicit limitations fields")
        identity, assignment_id, worker = row["id"], row["assignmentId"], row["workerId"]
        _require(_text(identity) and identity not in seen and assignment_id in assignments and bound.get(assignment_id) == worker, "contribution identity or actual assignment binding is invalid")
        seen.add(identity)
        _require(row["kind"] in CONTRIBUTION_KINDS and row["disposition"] in {"incorporated", "rejected", "unresolved"}, "status-only/unknown contribution kind or disposition cannot count")
        _require(all(_authored(row[key]) for key in ("summary", "artifactRevision", "effect")) and _strings(row["evidence"], nonempty=True)
                 and all(_authored(ref) for ref in row["evidence"]), "useful contributions need substantive result, inspected evidence, revision and synthesis effect")
        _require(_strings(row["limitations"]) and all(_authored(limit) for limit in row["limitations"]), "limitations must explicitly record known substantive limits or an empty list; placeholders cannot claim completeness")
        _require(_text(row["workHash"]) and (work_hash is None or row["workHash"] == work_hash), "contribution is stale for the current reviewed work")
        _require(row["resultRevision"] is None or _authored(row["resultRevision"]), "resultRevision must be null or an exact substantive revision")
        phase = assignments[assignment_id]["phaseId"]
        _require(states[phase]["status"] == "complete", "only completed assigned phases may return qualifying contributions")
        if row["kind"] == "authoring" and row["disposition"] != "rejected":
            _require(worker in states[phase]["authorIds"], "incorporated substantive contributor is missing from all-author accounting")
        if row["kind"] in {"independent-review", "verification"}:
            _require(worker not in states[phase]["authorIds"], "an independent check cannot hide substantive authorship in the same phase")
        if phase in requirements["acceptancePhases"]:
            _require(row["kind"] == "independent-review", "final acceptance needs the independent Reviewer's substantive result")
            _require(_authored(contract["progress"].get("resultRevision")) and row["resultRevision"] == contract["progress"]["resultRevision"], "acceptance is not bound to the exact current integrated result revision")
        if phase in final_verifier_phases and resolved[assignment_id]["family"] == "verification-engineer":
            _require(row["kind"] == "verification", "required final-result Verifier duty needs an actual verification contribution")
            _require(_authored(contract["progress"].get("resultRevision")) and row["resultRevision"] == contract["progress"]["resultRevision"], "substantial verification is not bound to the exact current integrated result revision")
        contributions.setdefault(assignment_id, []).append(row)
        if row["disposition"] != "unresolved":
            qualified.add(worker)
            returned_family_actors[resolved[assignment_id]["family"]].add(worker)
    for identity, row in assignments.items():
        if states[row["phaseId"]]["status"] == "complete":
            _require(identity in contributions, "completed worker duty lacks a useful current contribution: " + identity)
    for phase, state in states.items():
        if state["status"] == "complete":
            authored = {row["workerId"] for row in ledger if assignments[row["assignmentId"]]["phaseId"] == phase
                        and row["kind"] == "authoring" and row["disposition"] != "rejected"}
            _require(set(state["authorIds"]) - {coordinator} == authored, "complete substantive phase must account for every actual contributing author: " + phase)
    publication = phases[current]["writeScope"] == "external-write"
    for acceptance, verifier_phases in requirements["verificationBeforeAcceptance"].items():
        if states[acceptance]["status"] == "complete":
            reviewer_ids = {bound[identity] for identity in by_phase[acceptance]
                            if resolved[identity]["family"] == "reviewer" and identity in bound}
            verifier_ids = {row["workerId"] for identity, rows in contributions.items()
                            if assignments[identity]["phaseId"] in verifier_phases
                            and resolved[identity]["family"] == "verification-engineer"
                            for row in rows if row["disposition"] != "unresolved"}
            _require(bool(verifier_ids - reviewer_ids), "substantial verification needs a separate Verifier's completed final-result prerequisite contribution before acceptance")
    if completing or publication:
        _require(not any(row["disposition"] == "unresolved" for row in ledger), "unresolved in-scope contributions block completion/publication")
        _require(len(qualified) >= requirements["minimumContributors"], "completion/publication requires at least the required number of distinct useful actual contributors")
        _require(all(returned_family_actors[family] for family in requirements["requiredFamilies"]), "required family duty has not actually contributed a completed resolved result")
        _require(_distinct_representatives([returned_family_actors[family] for family in requirements["requiredFamilies"]]), "required family duties are not covered by distinct useful actual contributions in those duties")
    requirements["returnedContributorCount"] = len(qualified)
    return requirements
