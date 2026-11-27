---
{
  "command": "GUT",
  "launcher": "ai-dev-unit-verify-only",
  "order": 110,
  "phase": "Verify",
  "label": "Unit and integration verification",
  "summary": "Run existing unit/integration checks against delivered code without building",
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
      "operation": "verify_unit",
      "capabilities": [
        "run-tests"
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
      "unit_verification"
    ]
  }
}
---

# Unit and integration verification — GUT

Select an implemented change and call [unit-verifier](../../agents/unit-verifier/agent.md) for read-only verification commands. Store `artifacts/unit-verification.md` with exact commands, pass/fail/not-run and coverage. Do not implement new features or silently fix failing tests. Required failures block dependent acceptance until a separately authorized executor resolves the issues under current reviewed-plan admission and affected checks are rerun.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
