---
name: aidw-discover-contributions
description: Inventory a repository, assess maintainer priorities, and rank verifiable open-source contributions. No code changes.
---

# Repository Contribution Scout — internal operation

**Internal ID:** `stage:discover-contributions`. Selected by Auto, a recipe or the coordinator's explicit chain.
**Role:** [Investigator](../../agents/investigator/agent.md). Read the complete profile, selected capabilities `discover-contributions`, and
[operation policy](../operation-policy.md).
**Inputs:** `request`, `repo.snapshot`. **Outputs:** `contribution.portfolio`.
**Write scope:** `record-only`. **Report filename:** `CONTRIBUTIONS.md`.

This is a bounded internal assignment, not a public native `stage` command or a full build.

## Exact assignment

Perform a full tracked-file inventory with explicit exclusions, then representative deep tracing and relevant maintainer/governance/issue/PR investigation. Do not claim every source file was semantically examined. Produce source-grounded candidates across applicable contribution categories; aim for two per supported category, up to 24, and rank the top five. Mark insufficient evidence rather than invent suggestions. Save REPO-ASSESSMENT.md, CONTRIBUTIONS.md and portfolio.json in the assigned evidence directory. Validate the actual portfolio with scripts/contribution_scout.py validate and retain the result. Cite chosen RC IDs and the exact portfolio when later planning a contribution.

## Bounded procedure

1. Read the current request/corrections, assigned scope, exact selected record, actual source
   snapshot and consumed artifacts. Use Git identity where it exists; otherwise use truthful
   file/provider identities. Do not fabricate HEAD or infer missing artifacts from chat.
2. Check input freshness, dependencies, ownership and available tools. Missing required input
   or capability is blocked; the coordinator may provide authorized prerequisite work.
3. Read source and write the assigned task-record evidence only. Do not mutate product code, tests, dependencies or project documentation.
4. Save `CONTRIBUTIONS.md` at the coordinator-assigned path under the same record's
   `artifacts/`, for example `artifacts/discover-contributions/attempt-001/CONTRIBUTIONS.md`. Preserve
   older attempts. Link real input paths/revisions, observations, checks, findings and limits.
5. Return actual evidence paths, output identity and `succeeded`, `blocked` or `failed`.
   The coordinator reconciles the real result before dependent work. No queue receipt or
   invented host lifecycle event is required.

The coordinator assigns this operation to a real worker under [task routing](../../references/task-routing.md), with the complete profile and bounded scope. State the actual worker count; a descriptor does not launch an agent. An already assigned child performs this operation without recursively spawning another team.

## Completion gate

Stop at contribution discovery and planning. Implementation needs an actual user-selected candidate, project-policy check and reviewed concrete plan. Do not open issues/PRs, modify the repository or infer unavailable live GitHub access from local source.

The report must state what was actually inspected, executed or changed and what remains
unverified. Product writers pass the shared current-plan/criticism/briefing admission before
writes. The operator does not invoke another stage, broaden scope, deploy or publish merely
because this assignment completed. Continue only the coordinator's authorized handoff.

A top-level invocation of this operation receives a second distinct useful corroborating contribution before completion. This adds an evidence duty within the selected scope, not an unrequested formal stage or repair. A bounded child assignment does not create another team.
