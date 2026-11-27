---
{
  "command": "GVA",
  "launcher": "ai-dev-a11y-verify-only",
  "order": 114,
  "phase": "Verify",
  "label": "Accessibility verification only",
  "summary": "Verify keyboard, focus, interaction and responsive accessibility without rewriting the UI",
  "requires": [
    "subagent",
    "browser"
  ],
  "effects": "Standalone stage; existing record preserved, no automatic other phases or deployment.",
  "stages": "",
  "recordKind": "development",
  "createsRecord": false,
  "agentCalls": [
    {
      "agent": "verification-engineer",
      "when": "standalone",
      "operation": "verify_accessibility",
      "capabilities": [
        "review-accessibility",
        "ui-design"
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
      "accessibility_verification"
    ]
  }
}
---

# Accessibility verification only — GVA

Run [accessibility-verifier](../../agents/accessibility-verifier/agent.md) in verification-only mode against the selected change, with authorized browser/tools. Record focus order, semantic controls, states, labels, responsive behaviour, test environment and failures in `artifacts/accessibility-verification.md`. Do not redesign or silently make application edits; send repairs to separate execution and retest.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
