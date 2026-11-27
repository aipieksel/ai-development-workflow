---
{
  "command": "GPP",
  "launcher": "ai-dev-plan-from-evidence",
  "order": 105,
  "phase": "Plan & review",
  "label": "Plan from assessment",
  "summary": "Plan code changes from a verified assessment or design specification; do not review or build",
  "requires": [],
  "effects": "Standalone stage; existing record preserved, no automatic other phases or deployment.",
  "stages": "1",
  "recordKind": "development",
  "createsRecord": false,
  "agentCalls": [
    {
      "agent": "architect",
      "when": "during_1_before_2",
      "operation": "consult",
      "capabilities": [
        "plan-code"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [],
    "requiresAny": [
      "assessment",
      "design_spec"
    ],
    "produces": [
      "plan"
    ]
  }
}
---

# Plan from assessment — GPP

Select the **same existing record** in concrete **Plan** mode. Assign a real
[Code Goal Planner](../../agents/code-goal-planner/agent.md) worker to read the original
request, current `artifacts/assessment.md` and/or `artifacts/design-spec.md`, source
provenance and any architecture/research addenda. Follow
[task routing](../../references/task-routing.md), including required Architect advice
for broad/shared effects before finalizing the plan. Run stage **1 only** under
[planner](../../references/planner.md). Map every requested outcome to R/P/T, existing
code owners and C IDs, dependencies, exact tests and scope boundaries. Save normal
six-file plan updates plus `artifacts/plan-handoff.md` identifying the reviewed-source
hashes and unresolved assumptions. Run `finalize_plan_record.py --stage planned` where
structurally valid. Do **not** add stage 2 or execute. A missing input, unresolved user
intent or source drift remains blocked.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
