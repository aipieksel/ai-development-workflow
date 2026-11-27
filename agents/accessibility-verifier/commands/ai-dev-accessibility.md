---
{
  "command": "GU",
  "launcher": "ai-dev-accessibility",
  "order": 16,
  "phase": "Review",
  "label": "AI Accessibility and Interaction QA",
  "summary": "Verify keyboard, focus, forms and responsive interactions",
  "requires": [
    "subagent",
    "browser"
  ],
  "effects": "Tests and repairs existing UI controls; no redesign or certification claim.",
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
        "review-accessibility",
        "ui-design"
      ]
    }
  ],
  "pickerVisible": false
}
---

# AI Accessibility and Interaction QA — GU

Follow the [shared execution rules](../../../references/command-runtime.md) and
[task routing](../../../references/task-routing.md). The coordinator captures and plans,
obtains required Architect advice before the final plan, and assigns independent stage-2
criticism. After **0 → 1 → 2** and current admission,
[accessibility-verifier](../agent.md) is the sole stage-3 owner. Give the child this command,
the reviewed plan and [executor](../../../references/executor.md); wait for actual results
and obtain independent result acceptance before completion.
Keep one record/checklist and optional log. Do not execute a competing parent stage 3.
A fresh invocation creates one scoped task; prior feature plans are input evidence,
not records to overwrite. Explicit planning-only instructions stop before execution.

## Plan and critique

Identify real component primitives and scoped user tasks, not their guessed visual names. Use
applicable W3C guidance and ARIA patterns for the actual popover, menu, select, combobox
or dialog. Map keyboard navigation, focus order, labels, error/status messages, zoom,
reflow and supported responsive states. Check existing component behaviour first.

## Execute and verify

Combine automated scans with actual browser and keyboard interactions: open, navigate,
select, cancel, Escape, outside-click where applicable, focus return, validation and
recovery. Test real page zoom where supported; viewport resizing or magnifying screenshots
is not page-zoom verification. Verify essential content/actions at supported sizes.

Fix the owning reusable component rather than adding lookalike markup or unnecessary
ARIA. Recheck affected shared callers and protect existing handlers, state and theme.
Leave regression assertions and actual evidence. A clean scan cannot establish complete
accessibility; identify assistive-technology and screen-reader/browser combinations and criteria not exercised.
Do not replace G7 visual targets with invented design requirements or claim formal
conformance from partial testing. Required inaccessible/unverified journeys remain open.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
