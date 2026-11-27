---
{
  "command": "GVR",
  "launcher": "ai-dev-review-code-only",
  "order": 112,
  "phase": "Verify",
  "label": "Independent code review only",
  "summary": "Review the final implementation and test evidence without repeating its implementation",
  "requires": [
    "subagent"
  ],
  "effects": "Standalone stage; existing record preserved, no automatic other phases or deployment.",
  "stages": "",
  "recordKind": "development",
  "createsRecord": false,
  "agentCalls": [
    {
      "agent": "reviewer",
      "when": "standalone",
      "operation": "review",
      "capabilities": [
        "review-code"
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
      "code_review"
    ]
  }
}
---

# Independent code review only — GVR

Call [code-reviewer](../../agents/code-reviewer/agent.md) in REVIEW-ONLY mode on the selected final diff, original requirements, plan, tests, security and error boundaries. Require severity-ranked, path-specific findings and a coverage/limitations statement in `artifacts/code-review.md`. The reviewer must not become the executor or silently repair findings. Required repairs block dependent acceptance. The coordinator may send a correction through GEX only with actual implementation authority, a current concrete repair plan, completed criticism and successful admission, then rerun affected verification. This review-only assignment does not itself authorize repairs.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
