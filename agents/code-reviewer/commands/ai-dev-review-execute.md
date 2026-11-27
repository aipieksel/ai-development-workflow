---
{
  "command": "GCA",
  "launcher": "ai-dev-review-execute",
  "order": 10,
  "phase": "Delegated build",
  "label": "Delegate to Code Reviewer",
  "stages": "12",
  "recordKind": "development",
  "createsRecord": false,
  "agentCalls": [
    {
      "agent": "builder",
      "when": "owns_3",
      "operation": "execute_and_test",
      "capabilities": [
        "execute-plan",
        "review-code"
      ]
    }
  ],
  "summary": "Use an existing plan; the code reviewer implements and tests",
  "requires": [
    "subagent"
  ],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": false
}
---

# Delegate to Code Reviewer — GCA

Follow the [shared execution rules](../../../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

Use the **selected existing development record**; never allocate one. Record the
preset change to GCA on that record, preserving sources/history and invalidating
materially changed readiness. The coordinator prepares stage 1 with any required Architect
advice and assigns independent stage-2 criticism under
[task routing](../../../references/task-routing.md), then calls
[code-reviewer](../agent.md) as the **sole stage-3 implementation owner**.
Pass the reviewed plan, exact record and [executor](../../../references/executor.md).
The child must implement and test, not return only a review of the plan. Require
host tools capable of those actions; otherwise report the blocked step without
granted permissions, role-play or an unrequested substitute agent. The parent
reconciles the returned result and never implements concurrently. This executor's reviewer
profile does not make its own work independent; a separate worker accepts the result.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
