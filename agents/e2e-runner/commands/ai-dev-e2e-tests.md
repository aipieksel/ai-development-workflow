---
{
  "command": "GE",
  "launcher": "ai-dev-e2e-tests",
  "order": 17,
  "phase": "Validation",
  "label": "Build and E2E Tests",
  "stages": "0123",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "verification-engineer",
      "when": "after_3_before_completion",
      "operation": "test",
      "capabilities": [
        "run-e2e"
      ]
    }
  ],
  "summary": "Build and test, then run end-to-end verification",
  "requires": [
    "subagent",
    "browser"
  ],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": false
}
---

# Build and E2E Tests — GE

Follow the [shared execution rules](../../../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

Run **0 → 1 → 2 → 3 → E2E testing** on one new record. After scoped implementation
and its normal tests, call [e2e-runner](../agent.md) with the requested
journeys, target environment and current evidence. Wait for actual test results,
repair in-scope failures and rerun affected checks before closure. No browser or
agent result may be inferred from a passing build or a saved screenshot.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
