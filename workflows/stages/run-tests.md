---
name: aidw-run-tests
description: Run existing build/lint/typecheck/unit/integration commands; capture exits and logs without feature implementation.
---

# Run Tests & Validation — internal operation

**Internal ID:** `stage:run-tests`. Selected by Auto, a recipe or the coordinator's explicit chain.
**Role:** [Verification Engineer](../../agents/verification-engineer/agent.md). Read the complete profile, selected capabilities `run-tests`, and
[operation policy](../operation-policy.md).
**Inputs:** `repo.snapshot`. **Outputs:** `test.results`.
**Write scope:** `test-output-only`. **Report filename:** `TEST-RESULTS.md`.

This is a bounded internal assignment, not a public native `stage` command or a full build.

## Exact assignment

Execute discovered project scripts for build, typecheck, lint and scoped unit/integration checks. Capture each command and exit code; no source edits or fake green tests.

## Bounded procedure

1. Read the current request/corrections, assigned scope, exact selected record, actual source
   snapshot and consumed artifacts. Use Git identity where it exists; otherwise use truthful
   file/provider identities. Do not fabricate HEAD or infer missing artifacts from chat.
2. Check input freshness, dependencies, ownership and available tools. Missing required input
   or capability is blocked; the coordinator may provide authorized prerequisite work.
3. Run authorized checks and retain logs/traces in the assigned evidence directory. Do not change product code, test sources or dependencies to obtain a pass.
4. Save `TEST-RESULTS.md` at the coordinator-assigned path under the same record's
   `artifacts/`, for example `artifacts/run-tests/attempt-001/TEST-RESULTS.md`. Preserve
   older attempts. Link real input paths/revisions, observations, checks, findings and limits.
5. Return actual evidence paths, output identity and `succeeded`, `blocked` or `failed`.
   The coordinator reconciles the real result before dependent work. No queue receipt or
   invented host lifecycle event is required.

The coordinator assigns this operation to a real worker under [task routing](../../references/task-routing.md), with the complete profile and bounded scope. State the actual worker count; a descriptor does not launch an agent. An already assigned child performs this operation without recursively spawning another team.

## Completion gate

Provide primary evidence for the assigned outcome. Preserve source and acceptance boundaries; an artifact path or a conversational completion claim is not enough.

The report must state what was actually inspected, executed or changed and what remains
unverified. Product writers pass the shared current-plan/criticism/briefing admission before
writes. The operator does not invoke another stage, broaden scope, deploy or publish merely
because this assignment completed. Continue only the coordinator's authorized handoff.

A top-level invocation of this operation receives a second distinct useful corroborating contribution before completion. This adds an evidence duty within the selected scope, not an unrequested formal stage or repair. A bounded child assignment does not create another team.
