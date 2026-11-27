---
name: aidw-write-red-tests
description: Write tests, capture expected RED assertion, and refuse to treat infrastructure errors as RED.
---

# Write Failing Tests — internal operation

**Internal ID:** `stage:write-red-tests`. Selected by Auto, a recipe or the coordinator's explicit chain.
**Role:** [Builder](../../agents/builder/agent.md). Read the complete profile, selected capabilities `write-red-tests`, and
[operation policy](../operation-policy.md).
**Inputs:** `code.plan`, `plan.review`, `repo.snapshot`. **Outputs:** `tdd.red.evidence`.
**Write scope:** `tests-only`. **Report filename:** `TDD-RED.md`.

This is a bounded internal assignment, not a public native `stage` command or a full build.

## Exact assignment

After approved current plan, write only the planned test files and fixtures. Execute tests to observe the *right* RED; store exact command, exit code and failing assertion. Infrastructure, import and syntax failures never count as valid RED.

## Bounded procedure

1. Read the current request/corrections, assigned scope, exact selected record, actual source
   snapshot and consumed artifacts. Use Git identity where it exists; otherwise use truthful
   file/provider identities. Do not fabricate HEAD or infer missing artifacts from chat.
2. Check input freshness, dependencies, ownership and available tools. Missing required input
   or capability is blocked; the coordinator may provide authorized prerequisite work.
3. After current execution admission, edit only the planned test files and fixtures. Do not implement production code.
4. Save `TDD-RED.md` at the coordinator-assigned path under the same record's
   `artifacts/`, for example `artifacts/write-red-tests/attempt-001/TDD-RED.md`. Preserve
   older attempts. Link real input paths/revisions, observations, checks, findings and limits.
5. Return actual evidence paths, output identity and `succeeded`, `blocked` or `failed`.
   The coordinator reconciles the real result before dependent work. No queue receipt or
   invented host lifecycle event is required.

The coordinator assigns this operation to a real worker under [task routing](../../references/task-routing.md), with the complete profile and bounded scope. State the actual worker count; a descriptor does not launch an agent. An already assigned child performs this operation without recursively spawning another team.

## Completion gate

The current plan and completed independent review must cover the exact test changes before writing. Count RED only when the expected missing-feature assertion fails for the intended reason. Import, syntax, infrastructure, timeout and harness failures are not valid RED evidence.

The report must state what was actually inspected, executed or changed and what remains
unverified. Product writers pass the shared current-plan/criticism/briefing admission before
writes. The operator does not invoke another stage, broaden scope, deploy or publish merely
because this assignment completed. Continue only the coordinator's authorized handoff.

A top-level invocation of this operation receives a second distinct useful corroborating contribution before completion. This adds an evidence duty within the selected scope, not an unrequested formal stage or repair. A bounded child assignment does not create another team.
