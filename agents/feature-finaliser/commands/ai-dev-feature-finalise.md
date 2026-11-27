---
{
  "command": "GF",
  "launcher": "ai-dev-feature-finalise",
  "order": 13,
  "phase": "Refinement",
  "label": "AI Feature Finalisation",
  "summary": "Finalise one feature and test its exact delivery package",
  "requires": [
    "subagent"
  ],
  "effects": "Cleans scoped leftovers and builds a package; no deployment.",
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
        "delivery"
      ]
    }
  ],
  "pickerVisible": false
}
---

# AI Feature Finalisation — GF

Follow the [shared execution rules](../../../references/command-runtime.md) and
[task routing](../../../references/task-routing.md). The coordinator captures and plans,
obtains required Architect advice before the final plan, and assigns independent stage-2
criticism. After **0 → 1 → 2** and current admission,
[feature-finaliser](../agent.md) is the sole stage-3 owner. Give the child this command,
the reviewed plan and [executor](../../../references/executor.md); wait for actual results
and obtain independent result acceptance before completion.
Keep one record/checklist and optional log. Do not execute a competing parent stage 3.
A fresh invocation creates one scoped task; prior feature plans are input evidence,
not records to overwrite. Explicit planning-only instructions stop before execution.

## Plan and critique

Inventory only the completed feature, its entry points, callers and package boundary.
Classify runtime files, maintained tests/development support, documentation and disposable
artefacts. Follow verified local conventions and the installed platform's lifecycle.
Review scratch/debug files, duplicate implementations, assets and dependencies against
actual callers before moving or removing them. Preserve licences and compatibility files.

## Execute and verify

Clean proven feature leftovers and consolidate through existing owners. Keep regression
tests in the source repository even when excluded from the production archive. Reuse the
existing build/package process with an explicit runtime allowlist; reject secrets,
local configuration, scratch files and missing required assets. No whole-repo cleanup.

Build the deliverable and test that exact archive after extraction into a clean,
disposable installation. Exercise supported install, upgrade, configuration, role-specific
entry points, removal and recovery. Establish data retention expectations before lifecycle
tests; WHMCS deactivation may delete module data and must not touch a live installation.
Rebuild and repeat affected checks after any change to packaged code/assets. Do not test
one build and deliver another. Record archive identity, contents, dependencies,
installation/upgrade instructions and observed results. A working development checkout
alone is not release evidence; missing platform access leaves those checks unverified.
No production deployment, database destruction or automatic publication is authorised.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
