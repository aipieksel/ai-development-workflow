---
{
  "command": "GT",
  "launcher": "ai-dev-test-first",
  "order": 7,
  "phase": "Build",
  "label": "Full test-first build",
  "stages": "0123",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "builder",
      "when": "owns_3",
      "operation": "execute_and_test",
      "capabilities": [
        "execute-plan",
        "tdd"
      ]
    }
  ],
  "summary": "Plan and critique, then delegate test-first implementation",
  "requires": [
    "subagent"
  ],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": true,
  "kind": "pipeline"
}
---

# Test-First Development — GT

Follow the [shared execution rules](../../../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

The coordinator captures and plans, obtaining any required Architect advice, and assigns
independent stage-2 criticism under [task routing](../../../references/task-routing.md).
After **0 → 1 → 2** and current admission,
call [tdd-guide](../agent.md) as the **sole stage-3 implementation owner**.
Give it the same record, reviewed plan and [executor](../../../references/executor.md).
The child writes a meaningful failing test first, implements, refactors within
scope and reruns the required tests. The parent does not implement concurrently
or perform a competing stage 3. Reconcile the child's actual result and obtain independent
result review before closure.

**Advanced command classification:** This is a **complete pipeline**, not a standalone stage. For bounded composition, use the atomic handlers in `commands/stages/` or the internal operation catalogue. The selected operations and record semantics are preserved; the shared mode, delegation and impact rules govern staffing.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
