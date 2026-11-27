---
name: aidw-execute-plan
description: Apply approved plan against current reviewed revision. Preserve scope, checkpoints and evidence.
---

# Execute Approved Plan — internal operation

**Internal ID:** `stage:execute-plan`. Selected by Auto, a recipe or the coordinator's explicit chain.
**Role:** [Builder](../../agents/builder/agent.md). Read the complete profile, selected capabilities `execute-plan`, and
[operation policy](../operation-policy.md).
**Inputs:** `code.plan`, `plan.review`, `repo.snapshot`. **Outputs:** `execution.result`.
**Write scope:** `repo-write-scoped`. **Report filename:** `EXECUTION.md`.

This is a bounded internal assignment, not a public native `stage` command or a full build.

## Exact assignment

Validate approved plan SHA, reviewer identity, authorization, baseline and write lock before changes. Implement tasks in dependency order; preserve existing code ownership and tests. If TDD evidence exists, follow GREEN and REFACTOR. Produce diff summary and test exits; stop on material plan drift.

## Bounded procedure

1. Read the current request/corrections, assigned scope, exact selected record, actual source
   snapshot and consumed artifacts. Use Git identity where it exists; otherwise use truthful
   file/provider identities. Do not fabricate HEAD or infer missing artifacts from chat.
2. Check input freshness, dependencies, ownership and available tools. Missing required input
   or capability is blocked; the coordinator may provide authorized prerequisite work.
3. After current execution admission, change only the paths and behavior covered by the reviewed plan. Preserve existing owners, protected behavior and unrelated work.
4. Save `EXECUTION.md` at the coordinator-assigned path under the same record's
   `artifacts/`, for example `artifacts/execute-plan/attempt-001/EXECUTION.md`. Preserve
   older attempts. Link real input paths/revisions, observations, checks, findings and limits.
5. Return actual evidence paths, output identity and `succeeded`, `blocked` or `failed`.
   The coordinator reconciles the real result before dependent work. No queue receipt or
   invented host lifecycle event is required.

The coordinator assigns this operation to a real worker under [task routing](../../references/task-routing.md), with the complete profile and bounded scope. State the actual worker count; a descriptor does not launch an agent. An already assigned child performs this operation without recursively spawning another team.

## Completion gate

Require the actual current code plan, completed plan review, user authority, source reconciliation and successful shared execution admission. A stale plan hash, missing required reviewer identity, unresolved ownership or material source drift blocks writes. Continue reviewed changes only while that concrete authority and plan coverage remain current.

The report must state what was actually inspected, executed or changed and what remains
unverified. Product writers pass the shared current-plan/criticism/briefing admission before
writes. The operator does not invoke another stage, broaden scope, deploy or publish merely
because this assignment completed. Continue only the coordinator's authorized handoff.

A top-level invocation of this operation receives a second distinct useful corroborating contribution before completion. This adds an evidence duty within the selected scope, not an unrequested formal stage or repair. A bounded child assignment does not create another team.
