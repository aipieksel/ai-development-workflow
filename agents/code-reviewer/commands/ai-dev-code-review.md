---
{
  "command": "GC",
  "launcher": "ai-dev-code-review",
  "order": 14,
  "phase": "Review",
  "label": "Build and Code Review",
  "stages": "0123",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "reviewer",
      "when": "after_3_before_completion",
      "operation": "review",
      "capabilities": [
        "review-code"
      ]
    }
  ],
  "summary": "Build and test, then obtain a separate code review",
  "requires": [
    "subagent"
  ],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": false
}
---

# Build and Code Review — GC

Follow the [shared execution rules](../../../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

Run **0 → 1 → 2 → 3 → code review** on one new record in concrete Build mode.
Apply [task routing](../../../references/task-routing.md), including Architect advice
when required. Obtain independent plan criticism before assigning implementation
and scoped tests to a real execution specialist. The coordinator then calls
[code-reviewer](../agent.md), independent of the executor,
with the original requirements, final diff, tests and evidence. Wait for the review,
repair in-scope findings and rerun affected checks before closure. This review is
additional to stage 2, which critiques the plan before implementation.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
