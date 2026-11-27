---
{
  "command": "GX",
  "launcher": "ai-dev-security",
  "order": 15,
  "phase": "Review",
  "label": "AI Security Verification",
  "summary": "Test access boundaries and fix scoped security defects",
  "requires": [
    "subagent"
  ],
  "effects": "Runs authorised security checks and scoped fixes in controlled environments.",
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
        "review-security"
      ]
    }
  ],
  "pickerVisible": false
}
---

# AI Security Verification — GX

Follow the [shared execution rules](../../../references/command-runtime.md) and
[task routing](../../../references/task-routing.md). The coordinator captures and plans,
obtains required Architect advice before the final plan, and assigns independent stage-2
criticism. After **0 → 1 → 2** and current admission,
[security-verifier](../agent.md) is the sole stage-3 owner. Give the child this command,
the reviewed plan and [executor](../../../references/executor.md); wait for actual results
and obtain independent result acceptance before completion.
Keep one record/checklist and optional log. Do not execute a competing parent stage 3.
A fresh invocation creates one scoped task; prior feature plans are input evidence,
not records to overwrite. Explicit planning-only instructions stop before execution.

## Plan and critique

Map the requested feature's roles, protected objects, entry points and trust boundaries.
Select applicable versioned OWASP ASVS/WSTG controls; no automatic whole-application
certification claim. Review customer A/customer B/admin restrictions where those roles
exist. Cover direct requests and object identifiers, not just hidden UI controls.
Confirm the actual local or authorised test target and safe test identities before use.

## Execute and verify

Use existing security components. Test relevant authorisation, validation, escaping,
sessions, secret exposure and replay/business-logic boundaries with separate identities.
Verify denied operations leave protected data unchanged; check returned content and
side effects as well as status codes. Reproduce scoped defects, repair authorised
causes and add regression tests demonstrating the failure and correction.

Do not scan unrelated public systems, use real customer credentials or broaden privileges.
Protect captured evidence and avoid leaking tokens or personal data. Deliver a role/action
matrix, reproducible findings, scoped patches, retained test results and unverified
boundaries. A dependency scan or absent scanner warnings alone is not completion.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
