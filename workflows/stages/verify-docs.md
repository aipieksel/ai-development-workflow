---
name: aidw-verify-docs
description: Check each documentation claim and command against actual code.
---

# Verify Documentation — internal operation

**Internal ID:** `stage:verify-docs`. Selected by Auto, a recipe or the coordinator's explicit chain.
**Role:** [Reviewer](../../agents/reviewer/agent.md). Read the complete profile, selected capabilities `verify-docs`, and
[operation policy](../operation-policy.md).
**Inputs:** `repo.snapshot`, `docs.change`. **Outputs:** `docs.verification`.
**Write scope:** `record-only`. **Report filename:** `DOCS-VERIFICATION.md`.

This is a bounded internal assignment, not a public native `stage` command or a full build.

## Exact assignment

Independently check changed docs for factual truth against live code and real commands. Return evidence-backed PASS or actionable corrections. Do not edit docs while reviewing.

## Bounded procedure

1. Read the current request/corrections, assigned scope, exact selected record, actual source
   snapshot and consumed artifacts. Use Git identity where it exists; otherwise use truthful
   file/provider identities. Do not fabricate HEAD or infer missing artifacts from chat.
2. Check input freshness, dependencies, ownership and available tools. Missing required input
   or capability is blocked; the coordinator may provide authorized prerequisite work.
3. Read source and write the assigned task-record evidence only. Do not mutate product code, tests, dependencies or project documentation.
4. Save `DOCS-VERIFICATION.md` at the coordinator-assigned path under the same record's
   `artifacts/`, for example `artifacts/verify-docs/attempt-001/DOCS-VERIFICATION.md`. Preserve
   older attempts. Link real input paths/revisions, observations, checks, findings and limits.
5. Return actual evidence paths, output identity and `succeeded`, `blocked` or `failed`.
   The coordinator reconciles the real result before dependent work. No queue receipt or
   invented host lifecycle event is required.

Use an actual independent reviewer distinct from the author/executor of the reviewed work. Record the real identity and result; if that capability is absent, mark the independent review blocked.

## Completion gate

The actual docs author cannot serve as the required independent reviewer. Check claims, paths and commands against current source and actual execution where appropriate. Return evidenced corrections without editing the documentation being reviewed.

The report must state what was actually inspected, executed or changed and what remains
unverified. Product writers pass the shared current-plan/criticism/briefing admission before
writes. The operator does not invoke another stage, broaden scope, deploy or publish merely
because this assignment completed. Continue only the coordinator's authorized handoff.

A top-level invocation of this operation receives a second distinct useful corroborating contribution before completion. This adds an evidence duty within the selected scope, not an unrequested formal stage or repair. A bounded child assignment does not create another team.
