---
{
  "command": "GRC",
  "launcher": "ai-dev-contribution-discovery",
  "order": 118,
  "phase": "Discover",
  "label": "Repository Contribution Scout",
  "summary": "Inventory an entire repository and rank evidence-backed, PR-sized contribution proposals across engineering categories; plan-only",
  "requires": [
    "subagent"
  ],
  "effects": "Read-only repository and GitHub assessment; write task-record reports only; no code edits, issue creation or pull requests.",
  "stages": "0",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "investigator",
      "when": "after_0_before_1",
      "operation": "discover_contributions",
      "capabilities": [
        "discover-contributions"
      ]
    }
  ],
  "pickerVisible": true,
  "kind": "stage",
  "queue": {
    "requiresAll": [],
    "requiresAny": [],
    "produces": [
      "contribution.portfolio"
    ]
  }
}
---

# Repository Contribution Scout — GRC

**Invocation:** `$ai-dev-contribution-discovery` or `$ai-development-workflow GRC` or `/ai-development-workflow GRC <repo/location>`. This command is **stage 0 only**. It does not invoke GS (which builds code), GCP, G1 or a complete pipeline.

1. Capture the user's repository and contribution goals in the selected development task record. Use an existing record if the host provided one; otherwise create one using the established dated `documents/tasks/development` allocator.
2. Invoke [contribution-scout](../agent.md) with repository read access, read-only upstream GitHub access when available, and write access only to record artifacts. Enforce maintainer rules and no application edits.
3. Inventory the repository, assess architecture and governance, check issues/PR overlap where authorised, produce `REPO-ASSESSMENT.md`, `CONTRIBUTIONS.md` and `portfolio.json`, and validate the machine-readable portfolio. Aim for two substantive proposals per applicable category; distinguish evidence gaps from discovered facts.
4. Write output at the assigned paths under the same task record, preserve the actual source fingerprint and evidence bindings, and report the top five with source paths and verification plans. Mark blocked if source access is unavailable. Do not invent a host receipt or a second task record.
5. Stop. A subsequent `GPP/GPR/GEX` sequence requires user selection of a specific candidate and independent approval; never implement on the scout invocation alone.

Follow [stage artifact rules](../../../references/stage-artifacts.md) and [portfolio contract](../../../references/contribution-portfolio-v1.md).

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
