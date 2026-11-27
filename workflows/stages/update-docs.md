---
name: aidw-update-docs
description: Update affected docs from real code diff; do not rebuild source code.
---

# Update Documentation — internal operation

**Internal ID:** `stage:update-docs`. Selected by Auto, a recipe or the coordinator's explicit chain.
**Role:** [Builder](../../agents/builder/agent.md). Read the complete profile, selected capabilities `update-docs`, and
[operation policy](../operation-policy.md).
**Inputs:** `code.plan`, `plan.review`, `repo.snapshot`. **Outputs:** `docs.change`.
**Write scope:** `docs-only`. **Report filename:** `DOCS-CHANGE.md`.

This is a bounded internal assignment, not a public native `stage` command or a full build.

## Exact assignment

Require a current independently criticized docs plan, or exact documentation coverage in the selected approved implementation plan. Update only affected README/API/reference/codemap or examples based on actual diff, tests and exported public interfaces; mark undocumented/unknown features rather than invent. No production code edits.

## Bounded procedure

1. Read the current request/corrections, assigned scope, exact selected record, actual source
   snapshot and consumed artifacts. Use Git identity where it exists; otherwise use truthful
   file/provider identities. Do not fabricate HEAD or infer missing artifacts from chat.
2. Check input freshness, dependencies, ownership and available tools. Missing required input
   or capability is blocked; the coordinator may provide authorized prerequisite work.
3. After current execution admission, edit only the planned project documentation. Do not change production code or broaden the documented feature set beyond actual behavior.
4. Save `DOCS-CHANGE.md` at the coordinator-assigned path under the same record's
   `artifacts/`, for example `artifacts/update-docs/attempt-001/DOCS-CHANGE.md`. Preserve
   older attempts. Link real input paths/revisions, observations, checks, findings and limits.
5. Return actual evidence paths, output identity and `succeeded`, `blocked` or `failed`.
   The coordinator reconciles the real result before dependent work. No queue receipt or
   invented host lifecycle event is required.

The coordinator assigns this operation to a real worker under [task routing](../../references/task-routing.md), with the complete profile and bounded scope. State the actual worker count; a descriptor does not launch an agent. An already assigned child performs this operation without recursively spawning another team.

## Completion gate

Require a current reviewed docs plan or exact documentation coverage in the adopted implementation plan, plus successful shared execution admission. Reconcile actual implementation-to-documentation changes under that review; unrelated drift requires renewed criticism. Keep docs-only scope and do not invent interfaces or command behavior.

The report must state what was actually inspected, executed or changed and what remains
unverified. Product writers pass the shared current-plan/criticism/briefing admission before
writes. The operator does not invoke another stage, broaden scope, deploy or publish merely
because this assignment completed. Continue only the coordinator's authorized handoff.

A top-level invocation of this operation receives a second distinct useful corroborating contribution before completion. This adds an evidence duty within the selected scope, not an unrequested formal stage or repair. A bounded child assignment does not create another team.
