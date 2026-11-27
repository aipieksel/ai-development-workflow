---
{
  "command": "GJ",
  "launcher": "ai-dev-journey-tests",
  "order": 18,
  "phase": "Validation",
  "label": "AI Journey Test Automation",
  "summary": "Build rerunnable customer and admin browser test suites",
  "requires": [
    "subagent",
    "browser"
  ],
  "effects": "Writes tests, test fixtures and CI configuration; no production effects.",
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
        "author-e2e",
        "run-e2e"
      ]
    }
  ],
  "pickerVisible": false
}
---

# AI Journey Test Automation — GJ

Follow the [shared execution rules](../../../references/command-runtime.md) and
[task routing](../../../references/task-routing.md). The coordinator captures and plans,
obtains required Architect advice before the final plan, and assigns independent stage-2
criticism. After **0 → 1 → 2** and current admission,
[e2e-runner](../agent.md) is the sole stage-3 owner. Give the child this command,
the reviewed plan and [executor](../../../references/executor.md); wait for actual results
and obtain independent result acceptance before completion.
Keep one record/checklist and optional log. Do not execute a competing parent stage 3.
A fresh invocation creates one scoped task; prior feature plans are input evidence,
not records to overwrite. Explicit planning-only instructions stop before execution.

## Plan and critique

Map the implemented feature's customer and administrator journeys, their shared business
record, permissions, validation, cancellation, persistence and relevant background work.
Use existing tests and local conventions; do not rebuild the feature or expand its scope.
In stage 2, require a decisive assertion for every required outcome and check that the
suite detects broken behaviour, not merely loaded pages or buttons. Include cross-role
state changes on the same test-owned object without dependencies between test cases.

## Execute and verify

Reuse the project's browser framework; choose Playwright only when no suitable runner
exists. Create separate customer/admin browser contexts and isolated backend fixtures;
protect authentication state and sensitive traces. Do not confuse browser isolation
with independent server-side data. Assert user-visible outcomes, server-side changes
where applicable, and relevant denied operations. Do not mock away the feature under test.

Deliver versioned tests, setup/cleanup fixtures, configuration, a feature-to-test map
and documented headed, headless and debug commands. Reruns must need no LLM. Integrate
with existing CI, including an explicit manual trigger and suitable existing automatic
triggers; schedule recurring runs only when requested. Verify clean setup and repeated
runs. Where practical, show that a controlled seeded defect makes a relevant test fail,
then restore the fixture. Keep first-attempt failures; retries are not fixes.

Use local/staging identities and non-billable infrastructure. No real payments, customer
emails, production data or unbounded external side effects. Label mocked boundaries.
Fix only authorised product defects; report others. Missing roles, unavailable browser
or skipped critical scenarios remain unverified, never a passing suite. Reconcile
coverage, results and replay commands in the same checklist before closure.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
