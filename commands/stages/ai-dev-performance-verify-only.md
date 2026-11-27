---
{
  "command": "GVP",
  "launcher": "ai-dev-performance-verify-only",
  "order": 115,
  "phase": "Verify",
  "label": "Performance verification only",
  "summary": "Measure performance and resilience on bounded workloads with no automatic optimisations",
  "requires": [
    "subagent"
  ],
  "effects": "Standalone stage; existing record preserved, no automatic other phases or deployment.",
  "stages": "",
  "recordKind": "development",
  "createsRecord": false,
  "agentCalls": [
    {
      "agent": "verification-engineer",
      "when": "standalone",
      "operation": "verify_performance",
      "capabilities": [
        "verify-performance"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [
      "implementation"
    ],
    "requiresAny": [],
    "produces": [
      "performance_verification"
    ]
  }
}
---

# Performance verification only — GVP

Call [performance-verifier](../../agents/performance-verifier/agent.md) in observe/test mode only on the selected implementation. Record workload, environment, budgets, measured results and failure modes in `artifacts/performance-verification.md`. No production stress tests or implementation under this command. Required failures block dependent acceptance. Record any actual user-authorized change to the acceptance scope without rewriting failed measurements as passing results.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
