---
{
  "command": "GDS",
  "launcher": "ai-dev-design-spec",
  "order": 104,
  "phase": "Plan & review",
  "label": "Design specification only",
  "summary": "Write a reusable design specification from a verified UI audit without implementing it",
  "requires": [
    "subagent"
  ],
  "effects": "Standalone stage; existing record preserved, no automatic other phases or deployment.",
  "stages": "",
  "recordKind": "development",
  "createsRecord": false,
  "agentCalls": [
    {
      "agent": "ui-design-director",
      "when": "standalone",
      "operation": "design_spec",
      "capabilities": [
        "design-ui",
        "ui-design"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [
      "design_audit"
    ],
    "requiresAny": [],
    "produces": [
      "design_spec"
    ]
  }
}
---

# Design specification only — GDS

Read the selected `artifacts/design-audit.md` and source request, call [design-specialist](../../agents/design-specialist/agent.md) in SPEC mode and produce `artifacts/design-spec.md`: proposed structure, reused tokens/components, exact behaviours, responsive, accessible states and measurable acceptance checks. No application edits. A missing or stale audit is a blocker; do not guess design tokens.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
