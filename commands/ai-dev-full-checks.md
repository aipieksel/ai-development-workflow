---
{
  "command": "G6",
  "launcher": "ai-dev-full-checks",
  "order": 21,
  "phase": "Combined checks",
  "label": "Build, Docs, E2E and Review",
  "stages": "0123",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "builder",
      "when": "after_3_before_completion",
      "operation": "update_docs",
      "capabilities": [
        "update-docs"
      ]
    },
    {
      "agent": "verification-engineer",
      "when": "after_3_before_completion",
      "operation": "test",
      "capabilities": [
        "run-e2e"
      ]
    },
    {
      "agent": "reviewer",
      "when": "after_3_before_completion",
      "operation": "review",
      "capabilities": [
        "review-code"
      ]
    }
  ],
  "summary": "Build, then update documentation, run E2E tests and review",
  "requires": [
    "subagent",
    "browser"
  ],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": false
}
---

# Build, Docs, E2E and Review — G6

Follow the [shared execution rules](../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

Run **0 → 1 → 2 → 3**, then these actual calls in this order:

1. [doc-updater](../agents/doc-updater/agent.md) updates affected documentation.
2. [e2e-runner](../agents/e2e-runner/agent.md) exercises the required journeys.
3. [code-reviewer](../agents/code-reviewer/agent.md) reviews the final changes and evidence.

Wait for each result. Repair in-scope failures and rerun the affected checks;
if a later fix changes an earlier agent’s subject, refresh that evidence. Do not
close while a required result is missing. This preset means these three extras,
not every specialist. The display order of commands does not change this sequence.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
