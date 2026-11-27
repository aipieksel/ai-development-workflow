---
{
  "command": "GCL",
  "launcher": "ai-dev-clean-only",
  "order": 117,
  "phase": "Finish",
  "label": "Cleanup existing implementation",
  "summary": "Make scoped, behaviour-preserving cleanup after a delivered change, not another full build",
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
      "operation": "cleanup",
      "capabilities": [
        "execute-plan",
        "cleanup"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [
      "implementation",
      "plan_review"
    ],
    "requiresAny": [],
    "produces": [
      "cleanup"
    ]
  }
}
---

# Cleanup existing implementation — GCL

On the selected reviewed change and actual diff, call [refactor-cleaner](../../agents/refactor-cleaner/agent.md) in CLEANUP ONLY mode. Limit edits to confirmed redundant/duplicated in-scope implementation and affected tests; preserve behaviour and original feature requirements. Write `artifacts/cleanup.md` and rerun touched tests. Before any cleanup edit, reuse exact current reviewed cleanup coverage or complete a
proportional cleanup plan and criticism, publish the current briefing and pass execution
admission. This applies even when behavior is preserved. Changed externally observable
contracts require updated scope/plan/review before edits. Existing GR and GH remain full/owner-specific workflows.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
