---
{
  "command": "GAA",
  "launcher": "ai-dev-architecture-advice",
  "order": 103,
  "phase": "Discover",
  "label": "Architecture assessment only",
  "summary": "Review integration boundaries and architectural trade-offs without building",
  "requires": [
    "subagent"
  ],
  "effects": "Standalone stage; existing record preserved, no automatic other phases or deployment.",
  "stages": "",
  "recordKind": "development",
  "createsRecord": false,
  "agentCalls": [
    {
      "agent": "architect",
      "when": "standalone",
      "operation": "consult",
      "capabilities": [
        "design-architecture"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [],
    "requiresAny": [
      "assessment",
      "plan"
    ],
    "produces": [
      "architecture"
    ]
  }
}
---

# Architecture assessment only — GAA

On the explicit existing record, ask [architect](../../agents/architect/agent.md) for a read-only advisory. Supply the assessment or existing plan, relevant source boundaries, requirements and compatibility constraints. Write `artifacts/architecture.md` with observed current architecture, alternatives, trade-offs, migration/rollback considerations and recommendation. Do not create a plan, change application files, or claim implementation. The later planner may adopt source-supported advice subject to scope.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
