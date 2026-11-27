# Loop wait and timer protocol

For an active Loop run, check the currently active reviewer or executor every **300 seconds
(five minutes)**. **Prefer the actual host's usable wait tool. If it is unavailable or
definitively unusable, use a native timer.** Use explicit active-session fallback only when
neither suitable mechanism is available. Discover capabilities in the actual execution host;
this editing session does not establish what the user's Codex exposes. Selecting, installing
or previewing Loop does not start monitoring.

## Discover and bind one monitor

Read the real tools' documented names, schemas, timeout units, event behavior and supported
status/cancellation operations. A wait tool must support this worker/mailbox coordination;
a tool that only resumes a particular shell cell is not automatically a worker wait. A
reminder delivered only to the user is not a manager wake. Never invent tool arguments,
receipt fields, persistence or cancellation APIs.

Start the real reviewer first and retain one run identity, exact task record, current phase,
source/output revision and actual active worker ID. Preserve **one monitor per run** and one
owner per phase. The run follows reviewer/executor handoffs; monitoring does not start an
extra worker. Resolve the current owner from saved state before every check.

Choose wait whenever it is suitable, even if native timers also exist. Record the observed
reason before choosing a lower-priority mechanism. A definitive failure may make a mechanism
unusable; an uncertain outstanding call or registration must be reconciled first. Do not
create a timer beside an unresolved wait, or a second timer after an ambiguous registration.

## Wait first

1. Read the actual clock and set `nextCheckAt = now + 300 seconds`. Use the discovered wait
   operation with the supported worker/mailbox binding and timeout. Preserve its actual
   tool name, run/worker identity and call context. The helper's normalized seconds are
   bookkeeping; translate to the real API's documented units and parameter names.
2. Where responsiveness requires it, compose waits of **at most 60 seconds**, capped by
   the tool's actual maximum and the remaining time. Honor its documented minimum. If a
   final minimum timeout crosses the deadline slightly, service the late check once and
   record the actual time. Do not invent a timeout the host rejects.
3. After an early message/event/timeout, read the clock and process the actual result.
   **Keep the same five-minute deadline.** Early wakes and short wait chunks do not reset
   it or count as periodic worker checks. Continue one bounded wait at a time.
4. Advance immediately when the current worker finishes. Preserve the returned evidence,
   reconcile checklist/report accounting and transition to the next phase without waiting
   for the five-minute deadline. A stale or unrelated worker result cannot advance the run.
   If an older wait is still pending, reconcile/finish it before assigning the next worker.
5. At the deadline, inspect the current worker's real status, request a concise progress or
   blocker update if needed, and record check time, worker, relevant checklist IDs and next
   coordination action. The manager accounts for progress; the reviewer judges the product.
   Set the next deadline 300 seconds after the actual serviced check. Do not replay missed
   checks in a burst or infer success from elapsed time.

A normal wait is **active-session coordination**, not proof of a persistent wake after the
manager stops. Preserve actual returns and failures; a proposed wait action or saved deadline
is not evidence that a tool was called. An ambiguous wait failure retains its pending call
context until an actual result or supported status operation proves it inactive. Only then
may a confirmed unusable wait lead to timer fallback.

## Native timer fallback

When a suitable wait is unavailable, discover the native timer's real wake, status and cleanup
contract. Reconcile existing registration before creating one. Register a run-scoped
**300-second** wake and retain the actual returned identifier, receipt and due time when
supplied. Call it armed only after a successful real tool result. Keep one recurring timer
or at most one outstanding one-shot for the run, not one per worker or phase.

Match a wake to the current run and registration. Reject duplicates and replaced/retired
handles using actual event identifiers and host semantics. Serialize completion and wake
handling so they cannot dispatch/rearm twice. Inspect the current worker, not the old worker
name copied into a callback. Service a late wake once and record its delay honestly.

For a recurring timer, retain its documented cadence. After a consumed one-shot and actual
status check, register the next wake 300 seconds later only while the run remains active and
only under the host's supported contract. Retain every actual receipt. Completion advances
immediately; update a timer binding or cancel-and-replace only if the real host requires it.

If registration fails or times out, distinguish confirmed not-created from unknown. Use
supported read/status/list operations, run correlation and documented idempotency to
reconcile. Never blindly retry an uncertain creation. Reuse a confirmed active registration;
replace it only after confirming absence or valid cleanup. Do not use ChatGPT Automations
or staggered jobs to work around that separate service's restrictions. Genuine supported
native one-shot rearming is different from such a workaround.

## Resume, change mechanisms and retain ownership

On manager restart, inspect actual saved worker ownership and the existing monitor before
any new dispatch or wait/registration. Timer persistence does not prove worker persistence;
missing local visibility does not prove that the earlier worker stopped. Unknown ownership
remains unresolved. Ignore stale results and acceptance for an earlier output revision.

Blocked/interrupted checkpoints are resumable suspensions. Preserve their prior worker and
phase. The helper's `resume` starts a reconciliation hold. For a wait, confirm that the prior
call is inactive before resuming; for a timer, reconcile its current status and required
cleanup. An active run may reuse its confirmed timer; a suspended run must resolve its old
cleanup first. `resumed` requires the actual saved worker observation. Reuse a running worker,
advance a completed worker through its normal report/accounting handoff, and return a stopped
unfinished worker to its pending phase. Never create a replacement from an unknown status.

A mechanism change uses explicit `reconfigure` / `reconfigured` bookkeeping. First preserve
the old checkpoint and actual correction/capability evidence, suspend monitoring, inspect
the original worker and reconcile/cancel/finish the old monitor. Do not dispatch or arm a
replacement while cleanup is live or unknown. Only after inactive cleanup and known worker
ownership may the new generation start. Preserve prior receipts and checkpoint history.
This is also the required path for a historical **600-second** checkpoint: retain its true
history, explicitly move to 300 seconds, and reuse the actual worker. Do not silently rewrite
old receipts or apply new deadlines to an existing old registration.

See [the exact artifact interface](loop-artifacts.md#timer-bookkeeping-interface). The helper
can validate declared binding and state transitions; it cannot authenticate observations.

## Stop and clean up

On current-revision reviewer acceptance, user cancellation or an actual blocked/interrupted
exit, persist the outcome and unresolved work. Prevent subsequent events from dispatching or
rearming. Accepted/cancelled runs remain terminal; suspension preserves ownership for recovery.

For a wait, retain any outstanding call context and confirm its return/inactivity through
supported operations. Do not invent wait cancellation or call it stopped merely because a
local binding was cleared. Late returns may reconcile cleanup but cannot restart the run.
For a native timer, call its supported cancellation operation and retain the real result.
Reconcile uncertain cancellation. An uncancellable one-shot can be retired under its actual
expiry contract; ignore its eventual wake without rearming and distinguish retirement from
confirmed cancellation. A recurring timer requires supported cancellation. Live or unknown
cleanup stays visible until resolved.

## Last fallback and evidence boundary

Only when both suitable wait and native timer capabilities are observed unavailable/unusable,
keep an explicitly labeled active-session clock checkpoint. Use available bounded mailbox
or session yields where appropriate, inspect the actual clock after returned work, and service
a due check once. Do not substitute background sleeps, callbacks or timestamp files for a
persistent host wake. Long calls or suspension may delay checks; preserve that limit and
checkpoint when monitoring ceases.

`timer` / `monitor` in `scripts/loop_checklist.py` is **pure bookkeeping**. It does not wait,
schedule, inspect workers, authenticate receipts, dispatch agents or prove persistence.
Fixture tool names/receipts are test data. Actual worker waits, timers and browser operations
require their supported tools and returned evidence.
