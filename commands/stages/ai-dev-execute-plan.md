---
{
  "command": "GEX",
  "launcher": "ai-dev-execute-plan",
  "order": 108,
  "phase": "Execute",
  "label": "Execute reviewed plan",
  "summary": "Implement and test the accepted existing plan without re-planning or allocating a record",
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
      "operation": "execute_plan",
      "capabilities": [
        "execute-plan"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [
      "plan_review"
    ],
    "requiresAny": [],
    "produces": [
      "implementation"
    ]
  }
}
---

# Execute reviewed plan — GEX

Select the **existing** development record and validate its current critique/readiness via `resolve_plan_record.py --execution --require-critique` and source-drift review. Invoke [implementation-executor](../../agents/implementation-executor/agent.md) as sole mutation owner. Use the plan, not a new discovery/plan/critique sequence; make in-scope changes, run scoped tests and store `artifacts/implementation.md` plus record results. On a material plan/scope change, stop and return to review before making that change. Do not auto-close unverified objectives or deploy.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
