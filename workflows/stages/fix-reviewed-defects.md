---
name: aidw-fix-reviewed-defects
description: Apply only separately authorised actionable findings; do not self-authorise scope changes.
---

# Fix Reviewed Defects — internal operation

**Internal ID:** `stage:fix-reviewed-defects`. Selected by Auto, a recipe or the coordinator's explicit chain.
**Role:** [Builder](../../agents/builder/agent.md). Read the complete profile, selected capabilities `fix-reviewed-defects`, and
[operation policy](../operation-policy.md).
**Inputs:** `code.plan`, `plan.review`, `review.findings`, `repo.snapshot`. **Outputs:** `execution.result`.
**Write scope:** `repo-write-scoped`. **Report filename:** `EXECUTION.md`.

This is a bounded internal assignment, not a public native `stage` command or a full build.

## Exact assignment

Require scoped approved finding IDs with paths and severity and a concrete repair plan independently criticized against the current post-implementation source. Modify only defects covered by that exact approved repair plan and selected findings; rerun impacted checks and record diffs per finding. No unsolicited refactors.

## Bounded procedure

1. Read the current request/corrections, assigned scope, exact selected record, actual source
   snapshot and consumed artifacts. Use Git identity where it exists; otherwise use truthful
   file/provider identities. Do not fabricate HEAD or infer missing artifacts from chat.
2. Check input freshness, dependencies, ownership and available tools. Missing required input
   or capability is blocked; the coordinator may provide authorized prerequisite work.
3. After current execution admission, change only the paths and behavior covered by the reviewed plan. Preserve existing owners, protected behavior and unrelated work.
4. Save `EXECUTION.md` at the coordinator-assigned path under the same record's
   `artifacts/`, for example `artifacts/fix-reviewed-defects/attempt-001/EXECUTION.md`. Preserve
   older attempts. Link real input paths/revisions, observations, checks, findings and limits.
5. Return actual evidence paths, output identity and `succeeded`, `blocked` or `failed`.
   The coordinator reconciles the real result before dependent work. No queue receipt or
   invented host lifecycle event is required.

The coordinator assigns this operation to a real worker under [task routing](../../references/task-routing.md), with the complete profile and bounded scope. State the actual worker count; a descriptor does not launch an agent. An already assigned child performs this operation without recursively spawning another team.

## Completion gate

Require the exact actionable finding IDs, current source and a concrete independently criticized repair plan. A rejected earlier review remains rejection/rework evidence; do not mark it successful. The coordinator supplies the necessary plan, review, repair, tests and fresh review sequence. Findings alone do not admit source writes or authorize unrelated improvements.

The report must state what was actually inspected, executed or changed and what remains
unverified. Product writers pass the shared current-plan/criticism/briefing admission before
writes. The operator does not invoke another stage, broaden scope, deploy or publish merely
because this assignment completed. Continue only the coordinator's authorized handoff.

A top-level invocation of this operation receives a second distinct useful corroborating contribution before completion. This adds an evidence duty within the selected scope, not an unrequested formal stage or repair. A bounded child assignment does not create another team.
