---
name: aidw-review-ui-spec
description: Check design contract for implementability, consistency, responsive behaviour and ownership; independent review.
---

# Review UI Specification — internal operation

**Internal ID:** `stage:review-ui-spec`. Selected by Auto, a recipe or the coordinator's explicit chain.
**Role:** [Reviewer](../../agents/reviewer/agent.md). Read the complete profile, selected capabilities `review-ui-spec`, `ui-design`, and
[operation policy](../operation-policy.md).
**Inputs:** `ui.spec`, `repo.snapshot`. **Outputs:** `ui.spec.review`.
**Write scope:** `record-only`. **Report filename:** `UI-SPEC-REVIEW.md`.

This is a bounded internal assignment, not a public native `stage` command or a full build.

## Exact assignment

Check UI-SPEC specificity, existing product identity, accessibility, breakpoints, token fidelity, states and verifiable screenshots. Return PASS/REVISE/BLOCK with evidence and exact amendment requests.

## Bounded procedure

1. Read the current request/corrections, assigned scope, exact selected record, actual source
   snapshot and consumed artifacts. Use Git identity where it exists; otherwise use truthful
   file/provider identities. Do not fabricate HEAD or infer missing artifacts from chat.
2. Check input freshness, dependencies, ownership and available tools. Missing required input
   or capability is blocked; the coordinator may provide authorized prerequisite work.
3. Read source and write the assigned task-record evidence only. Do not mutate product code, tests, dependencies or project documentation.
4. Save `UI-SPEC-REVIEW.md` at the coordinator-assigned path under the same record's
   `artifacts/`, for example `artifacts/review-ui-spec/attempt-001/UI-SPEC-REVIEW.md`. Preserve
   older attempts. Link real input paths/revisions, observations, checks, findings and limits.
5. Return actual evidence paths, output identity and `succeeded`, `blocked` or `failed`.
   The coordinator reconciles the real result before dependent work. No queue receipt or
   invented host lifecycle event is required.

Use an actual independent reviewer distinct from the author/executor of the reviewed work. Record the real identity and result; if that capability is absent, mark the independent review blocked.

## Completion gate

Use an actual independent reviewer of the UI specification. Bind the verdict to the current specification and source; return concrete amendments rather than silently editing the specification. A cosmetic preference unsupported by the requested design is not a blocking defect.

The report must state what was actually inspected, executed or changed and what remains
unverified. Product writers pass the shared current-plan/criticism/briefing admission before
writes. The operator does not invoke another stage, broaden scope, deploy or publish merely
because this assignment completed. Continue only the coordinator's authorized handoff.

A top-level invocation of this operation receives a second distinct useful corroborating contribution before completion. This adds an evidence duty within the selected scope, not an unrequested formal stage or repair. A bounded child assignment does not create another team.
