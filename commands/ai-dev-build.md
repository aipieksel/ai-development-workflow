---
{
  "command": "G1",
  "launcher": "ai-dev-build",
  "order": 5,
  "phase": "Build",
  "label": "Standard plan and build",
  "stages": "0123",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "reviewer",
      "when": "during_2",
      "operation": "review_plan",
      "capabilities": [
        "review-plan"
      ]
    },
    {
      "agent": "builder",
      "when": "owns_3",
      "operation": "execute_and_test",
      "capabilities": [
        "execute-plan"
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
  "summary": "Plan, criticise, implement and test a normal task",
  "requires": [],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": true,
  "kind": "pipeline"
}
---

# Plan and Build — G1

Follow the [shared execution rules](../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

Run **0 → 1 → 2 → 3** on one newly selected record in concrete **Build** mode:
capture the request, plan, obtain an independent plan critique, then delegate
implementation and tests to a real [Implementation Executor](../agents/implementation-executor/agent.md).
The coordinator owns scope, records and handoffs; a real
[Plan Reviewer](../agents/plan-reviewer/agent.md) owns criticism before writes and a
[Code Reviewer](../agents/code-reviewer/agent.md), independent of the implementer,
reviews the result before completion. One independent worker may perform both reviews.
Apply [task routing](../references/task-routing.md) before finalizing the plan:
investigate unknowns, obtain Architect advice for broad/shared impact, and apply
Fast Engineer guidance for an explicitly selected small G1 task without allocating a second pipeline.

Admit stage 3 only after the current critique and readiness check pass. Finish
with actual test evidence and the reconciled checklist. Numeric modes retain their requested
operations, but `013`/`13`/`3` cannot waive completed criticism before writes. Explain and
fulfill the prerequisite or reuse exact reviewed evidence. `1` remains planning-only.

**Advanced command classification:** This is a **complete pipeline**, not a standalone stage. For bounded composition, use the atomic handlers in `commands/stages/` or the internal operation catalogue. The selected operations and record semantics are preserved; the shared mode, delegation and impact rules govern staffing.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
