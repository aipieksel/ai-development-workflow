---
{
  "command": "GVS",
  "launcher": "ai-dev-security-verify-only",
  "order": 113,
  "phase": "Verify",
  "label": "Security verification only",
  "summary": "Check delivered changes for security defects; report findings without rebuilding",
  "requires": [
    "subagent"
  ],
  "effects": "Standalone stage; existing record preserved, no automatic other phases or deployment.",
  "stages": "",
  "recordKind": "development",
  "createsRecord": false,
  "agentCalls": [
    {
      "agent": "verification-engineer",
      "when": "standalone",
      "operation": "verify_security",
      "capabilities": [
        "review-security"
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
      "security_verification"
    ]
  }
}
---

# Security verification only — GVS

Use the selected implementation and call [security-verifier](../../agents/security-verifier/agent.md) in bounded READ/TEST ONLY verification mode; no live targets without permission. Record threats, exact checks and findings in `artifacts/security-verification.md`. Unlike legacy GX, this stage does not implement fixes. Fail/blocked findings prevent downstream automatic progression until corrected and reverified.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
