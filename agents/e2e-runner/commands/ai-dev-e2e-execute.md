---
{
  "command": "GEA",
  "launcher": "ai-dev-e2e-execute",
  "order": 9,
  "phase": "Delegated build",
  "label": "Delegate to E2E Agent",
  "stages": "012",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "builder",
      "when": "owns_3",
      "operation": "execute_and_test",
      "capabilities": [
        "execute-plan",
        "run-e2e"
      ]
    }
  ],
  "summary": "Plan and critique, then let the E2E agent implement and test",
  "requires": [
    "subagent",
    "browser"
  ],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": false
}
---

# Delegate to E2E Agent — GEA

Follow the [shared execution rules](../../../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

The coordinator captures and plans on a new record, obtains any required Architect advice,
then assigns independent stage-2 criticism under
[task routing](../../../references/task-routing.md). After **0 → 1 → 2** and admission, call
[e2e-runner](../agent.md) as the **sole stage-3 implementation owner**,
not just a tester of an unfinished parent implementation. Pass the reviewed plan,
exact record and [executor](../../../references/executor.md); the child implements and
tests its scope. Wait for its real result and obtain independent result review before closure.
The parent must not execute a competing stage 3. Missing edit/browser permissions
leave dependent work blocked; do not grant or invent capabilities.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
