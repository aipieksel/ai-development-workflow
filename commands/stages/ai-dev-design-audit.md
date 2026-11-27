---
{
  "command": "GDA",
  "launcher": "ai-dev-design-audit",
  "order": 102,
  "phase": "Discover",
  "label": "Design audit only",
  "summary": "Inspect existing UI and design tokens and document measurable gaps before proposing changes",
  "requires": [
    "subagent",
    "browser"
  ],
  "effects": "Standalone stage; existing record preserved, no automatic other phases or deployment.",
  "stages": "0",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "ui-design-director",
      "when": "after_0_before_1",
      "operation": "audit_design",
      "capabilities": [
        "audit-ui",
        "ui-design"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [],
    "requiresAny": [],
    "produces": [
      "design_audit"
    ]
  }
}
---

# Design audit only — GDA

Capture a scoped UI request and allocate one record (stage 0). Invoke [design-specialist](../../agents/design-specialist/agent.md) in AUDIT mode, inspect the existing interface, design system and references with available browser/screenshot capability. Save `artifacts/design-audit.md` with files/components/tokens, responsive states, captured measurements, preserved elements and unknowns. If no render is accessible say so; do not claim screenshot-based fidelity. Do not design or implement yet.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
