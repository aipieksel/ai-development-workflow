---
{
  "command": "GP",
  "launcher": "ai-dev-performance",
  "order": 19,
  "phase": "Validation",
  "label": "AI Performance and Resilience",
  "summary": "Measure performance budgets and verify failure recovery",
  "requires": [
    "subagent"
  ],
  "effects": "Runs bounded workloads and scoped optimisations; no production load.",
  "stages": "0123",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "builder",
      "when": "owns_3",
      "operation": "execute_and_test",
      "capabilities": [
        "execute-plan",
        "verify-performance"
      ]
    }
  ],
  "pickerVisible": false
}
---

# AI Performance and Resilience — GP

Follow the [shared execution rules](../../../references/command-runtime.md) and
[task routing](../../../references/task-routing.md). The coordinator captures and plans,
obtains required Architect advice before the final plan, and assigns independent stage-2
criticism. After **0 → 1 → 2** and current admission,
[performance-verifier](../agent.md) is the sole stage-3 owner. Give the child this command,
the reviewed plan and [executor](../../../references/executor.md); wait for actual results
and obtain independent result acceptance before completion.
Keep one record/checklist and optional log. Do not execute a competing parent stage 3.
A fresh invocation creates one scoped task; prior feature plans are input evidence,
not records to overwrite. Explicit planning-only instructions stop before execution.

## Plan and critique

Record the relevant workload, environment, datasets, concurrency and baseline. Use
existing agreed budgets; label proposed thresholds instead of inventing acceptance.
Choose relevant latency percentiles, errors, throughput, queries, resources or queue
measures. Challenge misleading averages, short samples, unsafe loads and fast errors
counted as success. Bound concurrency, duration and resources before running anything.

## Execute and verify

Reuse existing benchmark/load tools; use k6 where appropriate, not as a mandatory new
dependency. Compare equivalent workloads and environments before/after targeted changes.
Use protocol-level load plus a small browser sample where the feature requires both.
Record samples, percentile/error/resource results and enforce agreed budgets through
repeatable assertions. Do not hide errors, reduce work or relax thresholds to pass.

Exercise scoped slow/unavailable dependencies, interrupted jobs, duplicate delivery
and recovery. Verify retries preserve data and do not create duplicate billable services.
Keep external effects isolated and non-billable. Do not run unbounded production load,
introduce speculative caching/platform changes, or infer production capacity from a
small fixture. Deliver test scripts, workload configuration, fixes, measured comparison,
replay commands and limits. Without an agreed budget, report measurements, not budget compliance.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
