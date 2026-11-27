---
{
  "command": "GPR",
  "launcher": "ai-dev-review-plan-only",
  "order": 106,
  "phase": "Plan & review",
  "label": "Review and refine plan",
  "summary": "Independently critique the existing plan, correct it and record execution readiness; no coding",
  "requires": [
    "subagent"
  ],
  "effects": "Standalone stage; existing record preserved, no automatic other phases or deployment.",
  "stages": "2",
  "recordKind": "development",
  "createsRecord": false,
  "agentCalls": [
    {
      "agent": "reviewer",
      "when": "during_2",
      "operation": "review_plan",
      "capabilities": [
        "review-plan"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [
      "plan"
    ],
    "requiresAny": [],
    "produces": [
      "plan_review"
    ]
  }
}
---

# Review and refine plan — GPR

Select the existing record and run stage **2 only**. Invoke [plan-reviewer](../../agents/plan-reviewer/agent.md) to return independent F-ID findings. The parent reconciles the review using [criticizer](../../references/criticizer.md), edits only the plan/checklist/critique, preserves request sources/assessment, and finalises `--stage criticized` **only if** material issues are resolved. Write `artifacts/plan-review.md` with verdict ready/revised/blocked, critique revision and precise evidence. Do not modify app code or start stage 3. A simulated self-review is not an independent agent review.

Artifact rules: see [stage handoff](../../references/stage-artifacts.md). This is one bounded operation, not a full 0123 workflow. Return actual evidence, paths and a truthful outcome to the coordinator; do not launch dependent operations or fabricate execution receipts.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
