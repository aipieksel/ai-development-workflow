---
{
  "command": "GTE",
  "launcher": "ai-dev-execute-tdd",
  "order": 109,
  "phase": "Execute",
  "label": "Execute TDD plan (green)",
  "summary": "Consume reviewed plan and demonstrated red tests; implement green/refactor and verify",
  "requires": [
    "subagent"
  ],
  "effects": "Standalone stage; existing record preserved, no automatic other phases or deployment.",
  "stages": "",
  "recordKind": "development",
  "createsRecord": false,
  "agentCalls": [
    {
      "agent": "builder",
      "when": "standalone",
      "operation": "execute_tdd",
      "capabilities": [
        "execute-plan",
        "green-refactor"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [
      "plan_review",
      "red_tests"
    ],
    "requiresAny": [],
    "produces": [
      "implementation"
    ]
  }
}
---

# Execute TDD plan (green) — GTE

Select the existing ready plan and proven red-tests artifact. Invoke [tdd-implementer](../../agents/tdd-implementer/agent.md) after admission through the same reviewed-plan execution gate. Reconfirm RED, implement production change, demonstrate GREEN and regression checks, record `artifacts/implementation.md`. Never silently rewrite expected test behaviour. Stop on stale plan, contradictory tests or missing evidence; do not rerun discovery or plan automatically.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
