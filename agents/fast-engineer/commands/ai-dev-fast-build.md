---
{
  "command": "GB",
  "launcher": "ai-dev-fast-build",
  "order": 6,
  "phase": "Build",
  "label": "Fast full build",
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
        "execute-plan",
        "fast-build"
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
  "inputAliases": [
    "ponytail"
  ],
  "summary": "Complete the full scope with reuse, dependency batching and consolidated acceptance",
  "requires": [],
  "effects": "Scoped specialist implementation and independent review; no automatic deployment.",
  "pickerVisible": true,
  "kind": "pipeline"
}
---

# Fast Build — Ponytail — GB

Run **0 → 1 → 2 → 3** in concrete **Build** mode with a real
[Fast Engineer](../agent.md) execution worker. Use the host's actual delegation tool;
loading the profile alone does not create a worker. Preserve the selected host model
and available capabilities. Use [shared execution](../../../references/command-runtime.md)
for one task record, scope, criticism, checklist and optional logging. A separate
[Plan Reviewer](../../plan-reviewer/agent.md) criticizes the plan before writes and an
independent [Code Reviewer](../../code-reviewer/agent.md) accepts the result; one
independent worker may hold both review roles.

Under [task routing](../../../references/task-routing.md), Auto selects GB for known,
bounded, localized changes. Investigate unknowns first. An explicit GB request with
broad/shared impact still requires Architect advice before the final plan and criticism.

Read the relevant current evidence once. Plan the complete requested outcome in
compatible dependency groups. Keep stage 2 concise but substantive: scope, existing
owners, prerequisite capabilities and decisive acceptance. Resolve in-scope prerequisites
instead of seeking permission for each smaller slice. Update only materially changed
parts of the plan/review and preserve settled evidence.

Implement continuously through eligible groups. Use targeted checks between groups,
then the deduplicated integrated acceptance suite. Existing project check runners take
precedence; [acceptance runner](../references/acceptance.md) is an optional fallback
for the reviewed acceptance-command list, not a new mandatory gate. The coordinator
assigns the required executor and independent reviewers, combining compatible profiles
where useful. Extra planning, audit, documentation or E2E workers follow actual scope
and risk; the Fast Engineer child does not recursively create another team. Requested
checks and project safeguards still apply. No predetermined batch size, deletion quota
or speed claim.

Bare selection uses the current actionable task; ordinary follow-ups reuse its existing
record. Do not reinterpret an already-selected continuing task as permission to allocate
another record. Return actual completion and residuals once the requested work is done.

**Advanced command classification:** This is a **complete pipeline**, not a standalone stage. For bounded composition, use the atomic handlers in `commands/stages/` or the internal operation catalogue. The selected operations and record semantics are preserved; the shared mode, delegation and impact rules govern staffing.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
