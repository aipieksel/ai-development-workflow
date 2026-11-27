# Browser control recovery

## Permission belongs to the current user

Apply this policy to each workflow and delegated browser worker. Installing this plugin or starting a task alone grants no permission to reclaim browser control. Respect host handoff rules and any instruction from the current user to pause, stop, or keep control.

When a browser reports that a person took control, pause browser actions and preserve the session checkpoint. Resume when the current user returns control. If the current user has explicitly opted into automatic recovery for unexpected browser handoffs in this session, and the host supports and permits it, follow the recovery steps below. A general request to complete a task is insufficient. When a handoff may be intentional, wait for the user. Independent work may continue.

Pass the session owner, the scope of the current user's permission, and the handoff state to an assigned browser worker. Permission ends when withdrawn or when the session or user changes.

## Recover the same task and session

1. Preserve the current task, assigned browser owner, selected device/account/tab, last confirmed
   page state, pending action and its observed outcome. The notice does not complete a check
   or release another agent's ownership. Keep one browser controller for the shared session.
2. Inspect the actual browser tool documentation/capabilities and current control status. Use
   its supported reclaim/resume operation for that same authorized session. Do not invent a
   method name or treat a local flag, retry instruction or saved checkpoint as reclamation.
3. If the documented recovery needs reconnecting or refreshing the same browser handle first,
   do that automatically within the existing authorization. Preserve tab/session identity;
   do not reset the browser, discard unsaved work or switch accounts to obtain control.
4. Read the actual tool result and confirm that automation can control the intended session.
   An attempted call, a dismissed banner or a successful connection alone is not ownership
   confirmation. Reconcile ambiguous results with the supported status/read operation before
   making another reclaim attempt.
5. Obtain fresh page state and fresh interaction targets. Reconcile whether the interrupted
   action already happened before repeating it, especially submit, save, publish or purchase.
   Continue from the last verified effect; do not replay a potentially completed action merely
   because its response was interrupted. Existing permissions for that action still apply.
6. Resume the same worker, task and checklist. Record the notice, actual recovery operation,
   returned result and resumed state in the permitted task evidence. A short progress note
   may explain recovery; it must not become a routine approval question.

In Loop, the assigned reviewer/executor handles its browser recovery. The manager coordinates
ownership and checklist/status accounting; it does not take over product inspection. A
reviewer's authority to reclaim the browser does not authorize source repairs or allow it
to mark an unobserved interaction as passed.

## Genuine recovery limits

Standing user authorization does not create a missing API or override tool-enforced access,
device/origin restrictions, authentication requirements or an explicit later user pause.
Use only supported recovery operations under their actual contract. Do not disable a safety
control, use an undocumented control channel, switch browser families or bypass a sign-in wall.

If a reclaim attempt fails, inspect its reason and apply a documented, materially relevant
recovery when available. Avoid an unchanged retry loop or competing agents repeatedly taking
the session from each other. If no supported operation exists or recovery remains denied or
unavailable, save a resumable capability blocker with the actual response and exact missing
operation; continue independent authorized work. Do not describe that technical limitation
as missing user permission or ask the user to repeat the authorization already given.

This file is an instruction policy. It does not connect to a browser, grant platform-level
access, prove that a browser is available or establish that a live recovery was performed.
