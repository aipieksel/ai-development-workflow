---
{
  "command": "GTF",
  "launcher": "ai-dev-write-red-tests",
  "order": 107,
  "phase": "Execute",
  "label": "Write failing tests (TDD red)",
  "summary": "Implement test cases only, show correct red failures and hand them to the TDD executor",
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
      "operation": "write_red_tests",
      "capabilities": [
        "write-red-tests"
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
      "red_tests"
    ]
  }
}
---

# Write failing tests (TDD red) — GTF

On an existing, reviewed and source-current plan, delegate to [red-test-author](../../agents/red-test-author/agent.md). Limit repository edits to tests/fixtures. Produce executable test files and `artifacts/red-tests.md` with exact deliberate failing assertions, baseline health and commands. A correct expected RED assertion counts as stage completion, not software quality success. Stop immediately after RED: do not change production code. The next GTE stage must reverify RED before turning it GREEN.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
