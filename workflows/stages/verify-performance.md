---
name: aidw-verify-performance
description: Independently measure performance budgets and failure recovery. No implementation.
---

# Verify Performance — internal operation

**Internal ID:** `stage:verify-performance`. Selected by Auto, a recipe or the coordinator's explicit chain.
**Role:** [Verification Engineer](../../agents/verification-engineer/agent.md). Read the complete profile, selected capabilities `verify-performance`, and
[operation policy](../operation-policy.md).
**Inputs:** `repo.snapshot`. **Outputs:** `performance.results`.
**Write scope:** `test-output-only`. **Report filename:** `PERFORMANCE-RESULTS.md`.

This is a bounded internal assignment, not a public native `stage` command or a full build.

## Exact assignment

Read the actual source baseline, existing budgets, benchmark commands and expected thresholds. Run authorized bounded metrics checks and retain original logs, reproducible command, environment, exit code and budget assertions. Failed budgets or missing evidence remain failed/blocked. Do not modify source, insert a build workflow, invent timings or describe a sample as exhaustive coverage.

## Bounded procedure

1. Read the current request/corrections, assigned scope, exact selected record, actual source
   snapshot and consumed artifacts. Use Git identity where it exists; otherwise use truthful
   file/provider identities. Do not fabricate HEAD or infer missing artifacts from chat.
2. Check input freshness, dependencies, ownership and available tools. Missing required input
   or capability is blocked; the coordinator may provide authorized prerequisite work.
3. Run authorized checks and retain logs/traces in the assigned evidence directory. Do not change product code, test sources or dependencies to obtain a pass.
4. Save `PERFORMANCE-RESULTS.md` at the coordinator-assigned path under the same record's
   `artifacts/`, for example `artifacts/verify-performance/attempt-001/PERFORMANCE-RESULTS.md`. Preserve
   older attempts. Link real input paths/revisions, observations, checks, findings and limits.
5. Return actual evidence paths, output identity and `succeeded`, `blocked` or `failed`.
   The coordinator reconciles the real result before dependent work. No queue receipt or
   invented host lifecycle event is required.

The coordinator assigns this operation to a real worker under [task routing](../../references/task-routing.md), with the complete profile and bounded scope. State the actual worker count; a descriptor does not launch an agent. An already assigned child performs this operation without recursively spawning another team.

## Completion gate

Compare actual observations with the declared baseline and budget. Preserve workload/environment limits and failures. Measurements do not authorize optimization or changes to the benchmark merely to pass.

The report must state what was actually inspected, executed or changed and what remains
unverified. Product writers pass the shared current-plan/criticism/briefing admission before
writes. The operator does not invoke another stage, broaden scope, deploy or publish merely
because this assignment completed. Continue only the coordinator's authorized handoff.

A top-level invocation of this operation receives a second distinct useful corroborating contribution before completion. This adds an evidence duty within the selected scope, not an unrequested formal stage or repair. A bounded child assignment does not create another team.
