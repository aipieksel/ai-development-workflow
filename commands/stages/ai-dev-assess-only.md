---
{
  "command": "GAS",
  "launcher": "ai-dev-assess-only",
  "order": 100,
  "phase": "Discover",
  "label": "Codebase assessment only",
  "summary": "Inspect relevant code and document proven owners and conventions, without planning or implementing",
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
      "operation": "assess_codebase",
      "capabilities": [
        "assess-codebase"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [],
    "requiresAny": [],
    "produces": [
      "assessment"
    ]
  }
}
---

# Codebase assessment only — GAS

Run **stage 0 once** on a fresh selected record, capture the exact user request and repository context. Call the existing [codebase assessor](../../agents/codebase-assessor/agent.md) read-only after capture. Require its C-ID contract with maintained source paths, actual callers, tests, code owner, conventions, exclusions, uncertainties and affected boundaries. Preserve the raw findings as `artifacts/assessment.md` and source CA1 in record metadata using the existing GS evidence mechanism. Do not begin stage 1, critique or implementation. A broad repository traversal is scoped to requested dependencies, not every generated/vendor file. Report actual inspected scope and inaccessible portions. The artifact is the authoritative handoff for GPP.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
