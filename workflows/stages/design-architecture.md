---
name: aidw-design-architecture
description: Write an ADR and implementation boundaries; no source edits.
---

# Consult Architecture — internal operation

**Internal ID:** `stage:design-architecture`. Selected by Auto, a recipe or the coordinator's explicit chain.
**Role:** [Architect and Planner](../../agents/architect/agent.md). Read the complete profile, selected capabilities `design-architecture`, and
[operation policy](../operation-policy.md).
**Inputs:** `request`, `repo.snapshot`. **Outputs:** `architecture.advice`.
**Write scope:** `record-only`. **Report filename:** `ARCHITECTURE.md`.

This is a bounded internal assignment, not a public native `stage` command or a full build.

## Exact assignment

Write an ADR including current architecture, options, chosen boundary, interfaces, migration and rollback risks. No greenfield rewrite without source gap evidence.

## Bounded procedure

1. Read the current request/corrections, assigned scope, exact selected record, actual source
   snapshot and consumed artifacts. Use Git identity where it exists; otherwise use truthful
   file/provider identities. Do not fabricate HEAD or infer missing artifacts from chat.
2. Check input freshness, dependencies, ownership and available tools. Missing required input
   or capability is blocked; the coordinator may provide authorized prerequisite work.
3. Read source and write the assigned task-record evidence only. Do not mutate product code, tests, dependencies or project documentation.
4. Save `ARCHITECTURE.md` at the coordinator-assigned path under the same record's
   `artifacts/`, for example `artifacts/design-architecture/attempt-001/ARCHITECTURE.md`. Preserve
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
