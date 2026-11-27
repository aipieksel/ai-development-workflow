---
{
  "command": "GD",
  "launcher": "ai-dev-documentation",
  "order": 20,
  "phase": "Documentation",
  "label": "Build and Documentation",
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
    }
  ],
  "summary": "Build and test, then update affected documentation",
  "requires": [
    "subagent"
  ],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": false
}
---

# Build and Documentation — GD

Follow the [shared execution rules](../../../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

Run **0 → 1 → 2 → 3 → documentation** on one new record. After implementation,
call [doc-updater](../agent.md) for documentation affected by the
requested work. Supply actual changes, existing documentation conventions and
verified commands. Wait for the returned updates and check the relevant paths,
links and examples before closure. Do not turn this into an unrelated whole-repo
documentation rewrite or a deployment.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
