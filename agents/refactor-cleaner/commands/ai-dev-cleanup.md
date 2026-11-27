---
{
  "command": "GR",
  "launcher": "ai-dev-cleanup",
  "order": 11,
  "phase": "Refinement",
  "label": "Build and Cleanup",
  "stages": "0123",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "builder",
      "when": "after_3_before_completion",
      "operation": "clean_and_test",
      "capabilities": [
        "execute-plan",
        "cleanup"
      ]
    }
  ],
  "summary": "Build the requested change, then clean its affected code",
  "requires": [
    "subagent"
  ],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": false
}
---

# Build and Cleanup — GR

Follow the [shared execution rules](../../../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

Run **0 → 1 → 2 → 3 → cleanup** on one new record. Call
[refactor-cleaner](../agent.md) after implementation, with the
authorised changed area and relevant callers/tests. Consolidate or remove only
in-scope, demonstrably redundant code. Preserve unrelated work, public APIs and
dynamic registrations. Wait for its returned changes and affected test results
before closure. An example in the profile is not permission for extra commits,
broad deletion, rollback of other work or production changes.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
