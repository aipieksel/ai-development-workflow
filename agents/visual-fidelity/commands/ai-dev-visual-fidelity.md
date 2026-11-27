---
{
  "command": "G7",
  "launcher": "ai-dev-visual-fidelity",
  "order": 8,
  "phase": "Build",
  "label": "Visual Fidelity",
  "stages": "0123",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "ui-design-director",
      "when": "during_1_before_2",
      "operation": "inspect_reference",
      "capabilities": [
        "visual-fidelity",
        "ui-design"
      ]
    },
    {
      "agent": "builder",
      "when": "owns_3",
      "operation": "execute_and_test",
      "capabilities": [
        "execute-plan",
        "visual-fidelity",
        "ui-design"
      ]
    }
  ],
  "summary": "Inspect existing UI, compare the target, implement and verify",
  "requires": [
    "subagent",
    "browser"
  ],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": false
}
---

# Visual Fidelity — G7

Follow the [shared execution rules](../../../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

The coordinator captures and plans; an independent critic owns stage 2 and a real
[visual-fidelity](../agent.md) worker owns stage 3. Apply
[task routing](../../../references/task-routing.md), including Architect advice before
the final plan when required. The reference-inventory and implementation handoffs share
one execution owner; independent acceptance remains separate.

During stage 1, obtain a **read-only inventory**: verify the current UI and actual
component owners first, then compare the requested reference and measured gaps.
Incorporate it **before stage 2** and publish the same checklist. Do not implement
before the current/reference comparison. Keep already-correct items and leave
unrequested reference features outside scope. No feature-selection questionnaire
or routine approval stop is added.

After current critique/admission, resume that child for stage 3 when supported,
or pass its complete profile, original baseline, inventory, exact record and
reviewed plan to a new child. Follow the [executor](../../../references/executor.md).
Implement only requested gaps through existing components and handlers; perform
verification afterwards against the inventory, including original comparable
controls. Have an independent reviewer compare the actual measurements, interactions
and screenshots with the request and reference before closure.

For “look at this and fix what is wrong”, apply [repair and data presentation](../references/data-presentation.md).
Keep this same G7 sequence; no separate audit, questionnaire or additional command is needed.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
