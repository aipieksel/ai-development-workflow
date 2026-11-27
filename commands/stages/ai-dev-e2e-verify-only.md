---
{
  "command": "GVE",
  "launcher": "ai-dev-e2e-verify-only",
  "order": 111,
  "phase": "Verify",
  "label": "End-to-end verification only",
  "summary": "Validate real customer journeys from delivered code, without repeating the build",
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
      "operation": "verify_e2e",
      "capabilities": [
        "run-e2e"
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
      "e2e_verification"
    ]
  }
}
---

# End-to-end verification only — GVE

Select the existing implemented change and invoke [e2e-runner](../../agents/e2e-runner/agent.md) for **verification**, not its separate delegated-build preset. Scope journeys to user requirements and available test environment. Save `artifacts/e2e-verification.md` with fixtures, screenshots/traces where available, exact pass/fail/not-run and limitations. Do not claim browser execution without browser access, alter production data or implement new features.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
