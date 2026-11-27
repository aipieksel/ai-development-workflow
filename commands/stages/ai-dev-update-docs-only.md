---
{
  "command": "GVD",
  "launcher": "ai-dev-update-docs-only",
  "order": 116,
  "phase": "Finish",
  "label": "Update documentation only",
  "summary": "Update documentation from tested code under current reviewed coverage; no product rebuild",
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
      "operation": "update_docs",
      "capabilities": [
        "update-docs"
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
      "documentation"
    ]
  }
}
---

# Update documentation only — GVD

Select the completed implementation and its actual diff/checks. Invoke [doc-updater](../../agents/doc-updater/agent.md) to modify **only authorised project documentation**: relevant README, API docs, changelog or implementation notes according to existing conventions. Save `artifacts/documentation.md` with files updated and cross-reference to implementation; mark unsupported claims blocked. Before documentation edits, reuse exact current reviewed documentation coverage or
complete a concise documentation plan and criticism in the same record. Publish the current
briefing and pass execution admission. Do not rebuild product code or auto-publish documentation.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
