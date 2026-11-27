---
{
  "command": "GPL",
  "launcher": "ai-dev-goal-plan",
  "order": 2,
  "phase": "Planning",
  "label": "Goal Planner — plan only",
  "stages": "01",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "architect",
      "when": "during_1_before_2",
      "operation": "consult",
      "capabilities": [
        "plan-goals"
      ]
    }
  ],
  "inputAliases": [
    "agent-goal-planner"
  ],
  "summary": "Plan goals, preconditions, dependencies and the most efficient credible sequence",
  "requires": [],
  "effects": "Planning records only; no application edits, implementation, deployment or automatic acceptance.",
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [],
    "requiresAny": [],
    "produces": [
      "plan"
    ]
  }
}
---

# Goal Planner — plan only — GPL

Run **0 → 1 only** in concrete **Plan** mode, assigning the meaningful planning
operation to a real [Goal Planner](../agent.md) worker. Follow
[task routing](../../../references/task-routing.md) and [shared execution](../../../references/command-runtime.md)
for staffing, records, scope and progress. Capture the request once and use the existing
[planner](../../../references/planner.md) record format. For broad/shared changes, obtain
Architect advice before finalizing the plan. Planning does not grant execution authority.

Inspect source read-only, derive one complete dependency-aware plan and check its
internal consistency. The coordinator integrates the worker's actual plan and evidence
using the existing planning tools. Record implementation and acceptance as not started. Do not mark
product requirements complete because their plan is written. Leave stage 2 pending
for the later execution workflow. A disclosed check of the planning approach is not
independent implementation acceptance; do not launch implementation under this command.

Stop after the planning handoff. Ordinary continuation, a picker selection or `resume`
stays planning-only. Only a separate explicit execution instruction may continue into
critique/implementation on this record. Do not fetch or run upstream SPARC/MCP examples.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
