---
{
  "command": "GRS",
  "launcher": "ai-dev-research-only",
  "order": 101,
  "phase": "Discover",
  "label": "Research only",
  "summary": "Research a technical question with source evidence and a decision-ready summary, without coding",
  "requires": [
    "subagent"
  ],
  "effects": "Standalone stage; existing record preserved, no automatic other phases or deployment.",
  "stages": "0",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "investigator",
      "when": "after_0_before_1",
      "operation": "research",
      "capabilities": [
        "research-technical"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [],
    "requiresAny": [],
    "produces": [
      "research"
    ]
  }
}
---

# Research only — GRS

Capture request and a new record (stage 0). Invoke [researcher](../../agents/researcher/agent.md) for bounded read-only research, confirming repo facts and external sources using authorised tools only. Save `artifacts/research.md` containing source links, updated dates, license notes and clearly separated facts/recommendations. This does not imply that a researched proposal was authorised, planned or implemented.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
