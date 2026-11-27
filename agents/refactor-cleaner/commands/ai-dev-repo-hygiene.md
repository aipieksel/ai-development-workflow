---
{
  "command": "GH",
  "launcher": "ai-dev-repo-hygiene",
  "order": 12,
  "phase": "Refinement",
  "label": "AI Repository Hygiene",
  "summary": "Organise repository files safely and repair their references",
  "requires": [
    "subagent"
  ],
  "effects": "Moves or removes reviewed paths; preserves source history and useful tests.",
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
        "cleanup"
      ]
    }
  ],
  "pickerVisible": false
}
---

# AI Repository Hygiene — GH

Follow the [shared execution rules](../../../references/command-runtime.md) and
[task routing](../../../references/task-routing.md). The coordinator captures and plans,
obtains required Architect advice before the final plan, and assigns independent stage-2
criticism. After **0 → 1 → 2** and current admission,
[refactor-cleaner](../agent.md) is the sole stage-3 owner. Give the child this command,
the reviewed plan and [executor](../../../references/executor.md); wait for actual results
and obtain independent result acceptance before completion.
Keep one record/checklist and optional log. Do not execute a competing parent stage 3.
A fresh invocation creates one scoped task; prior feature plans are input evidence,
not records to overwrite. Explicit planning-only instructions stop before execution.

## Plan and critique

Inventory tracked, untracked, ignored, generated and modified paths. Derive the target
layout from actual project conventions and tool configuration. Use one reviewed table:
`Current path | Keep / move / remove | Destination | Reason | References to update`.
Respect root-level configuration, workspace/symlink boundaries and file ownership.
Preserve active task records, immutable source snapshots and evidence links in place.

Review candidates against dynamic imports, hook registrations, templates, public APIs,
CI scripts and documentation links. Dead-code tool output is a lead, not proof of
non-use. Untracked and ignored files are not automatically disposable. Protect
irreplaceable local data before destructive operations; Git does not back up untracked
work. Do not use blanket git-clean or broad deletion commands.

## Execute and verify

Apply exact reviewed moves/removals in small reversible batches; update imports,
configuration, scripts and links together. Keep the existing documentation root;
use tutorial/how-to/reference/explanation groupings only where useful, not empty
folders or a new structure imposed on an established one.

Remove disposable test output and only proven obsolete/superseded tests. Preserve
useful regression tests and their assertions; a failing regression is not clutter.
Compare configured test discovery before/after so lost tests cannot masquerade as a
clean run. Check dynamic registrations, builds, links and retained neighbouring behaviour.
Leave uncertain files unchanged with reasons. Do not make extra commits, revert other
people's changes or delete global agent registrations. Deliver the actual organised
repository, move/deletion record and test results, not just a cleanup report.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
