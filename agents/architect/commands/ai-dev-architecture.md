---
{
  "command": "GA",
  "launcher": "ai-dev-architecture",
  "order": 4,
  "phase": "Architecture",
  "label": "Architecture, plan and build",
  "stages": "0123",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "architect",
      "when": "during_1_before_2",
      "operation": "consult",
      "capabilities": [
        "design-architecture"
      ]
    }
  ],
  "summary": "Consult architecture while planning, then build and test",
  "requires": [
    "subagent"
  ],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": true,
  "kind": "pipeline"
}
---

# Architecture and Build — GA

Follow the [shared execution rules](../../../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

Run **0 → 1 (architecture consultation) → 2 → 3** on one new record.
During stage 1, call [architect](../agent.md) with the scoped request,
current source and relevant constraints. Wait for its real result and incorporate
accepted, source-backed advice into the plan before stage 2. Advice cannot add
unrequested scope. Under [task routing](../../../references/task-routing.md), select
concrete Build mode, obtain independent plan criticism, delegate implementation and tests
to a real execution specialist, and obtain independent result review before completion.
The coordinator integrates those handoffs and maintains the record.
A missing agent blocks that consultation; it does not mean this command is absent.

**Advanced command classification:** This is a **complete pipeline**, not a standalone stage. For bounded composition, use the atomic handlers in `commands/stages/` or the internal operation catalogue. The selected operations and record semantics are preserved; the shared mode, delegation and impact rules govern staffing.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
