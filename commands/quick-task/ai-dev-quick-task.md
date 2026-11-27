---
{
  "command": "G0",
  "launcher": "ai-dev-quick-task",
  "order": 0,
  "phase": "Quick task",
  "label": "Quick Task",
  "stages": "",
  "recordKind": "checklist",
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
  "aliases": [
    "GO"
  ],
  "summary": "Quick change with a source log, checklist and scoped verification",
  "requires": [],
  "effects": "One compact checklist; actual Fast Engineer execution and independent plan/result review; no automatic deployment.",
  "pickerVisible": false
}
---

# Quick Task — G0

Follow the bundled [quick checklist](workflow.md),
not the standard six-file plan. Preserve the request, publish its checklist, perform
a compact plan and completed criticism, pass admission, make the requested change,
run scoped verification and update that same checklist.
GO is an alias. A bare invocation uses the quick workflow’s context-only rules;
follow-ups and `resume` amend its existing record. Store the compact contract at <task-record-dir>/workflow-contract.json in the selected
quick task record. Keep that compact record rather than allocating a second GB or
six-file record. Follow [task routing](../../references/task-routing.md): select and
announce the concrete mode and assign real workers. A small localized write uses a
Fast Engineer execution worker plus independent plan criticism and result review.
Broad/shared effects require Architect advice before the final plan; investigate
unknowns first. A read-only quick task delegates its inspection and remains read-only.
Quick never means unreviewed or solo.

Resolve the allocator, auditor and publisher relative to
`commands/quick-task/`, not the skill’s top-level scripts. For UI changes,
read only Existing UI first in [coding standards](../../references/coding-standards.md).
Use the host’s acknowledged Tasks publication or the complete Markdown fallback.
Optional [debug logging](../../references/debug-logging.md) does not replace verification.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
