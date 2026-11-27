# Loop handoff artifacts and accounting

Keep Loop evidence inside the **same selected six-file development record**. These are
additive round artifacts, not another plan schema or an execution permission. Use a
stable run ID and round directories such as `artifacts/xr/round-001/`; preserve earlier
reports. Keep the manager's current phase, active worker and timer checkpoint in the
record's existing results/state evidence. Do not publish raw private source material in
the reusable plugin.

## Compatibility names

The public invocation is `loop`. Canonical Reviewer and Builder families load `loop-review` and `loop-execution`; old `loop-reviewer`/`loop-executor` paths remain compatibility entries. A clean initial review also uses Verification Engineer.
The `ai-development-workflow/xr-*` schemas and `artifacts/xr/` paths below are retained wire
and evidence identifiers. Preserve those exact bytes and earlier hashes when reading or
continuing existing checkpoints. The renamed helper is `scripts/loop_checklist.py`; it still
understands the retained checkpoint schemas. `XR` is also an invocation compatibility alias.

## Contents

1. [Review report](#review-report)
2. [Manager checklist](#manager-checklist)
3. [Executor report](#executor-report)
4. [Clean initial review corroboration](#clean-initial-review-corroboration)
5. [Fresh review and acceptance](#fresh-review-and-acceptance)
6. [Run the accounting helper](#run-the-accounting-helper)
7. [Timer bookkeeping interface](#timer-bookkeeping-interface)

## Review report

Produce the actual readable source inventory, result inventory and comparison report.
The structured `review.json` points to those observations. Use this shape; values below
are examples, not evidence of a real review:

```json
{
  "schema": "ai-development-workflow/xr-review/v1",
  "runId": "example-run",
  "round": 1,
  "sourceRevision": "actual-original-snapshot-identity",
  "outputRevision": "actual-reviewed-output-identity",
  "reviewerId": "actual-reviewer-tool-identity",
  "verdict": "changes-required",
  "coverage": [
    {"id": "source:primary-flow", "side": "source", "status": "reviewed", "evidence": ["source-inventory.md#primary-flow"]},
    {"id": "result:primary-flow", "side": "result", "status": "reviewed", "evidence": ["result-inventory.md#primary-flow"]},
    {"id": "compare:primary-flow", "side": "comparison", "status": "reviewed", "evidence": ["comparison.md#primary-flow"]}
  ],
  "findings": [
    {"id": "F1", "disposition": "actionable", "summary": "The requested destination does not open.", "acceptance": "The source-equivalent control opens its specified destination.", "evidence": ["comparison.md#F1"]}
  ]
}
```

Use actual source/output revisions, such as a Git identity plus relevant dirty-file hashes
or an exact non-Git file-manifest digest. A filename alone does not identify checked bytes.
The reviewer records how live pages/documents map to those revisions.

Coverage IDs represent every required source, result and comparable state. Reuse them
across rounds. `status` is `reviewed`, `blocked` or `not-run`; reviewed rows require
nonempty evidence references, and unresolved rows require a nonblank `reason`. Evidence
references can identify files, report anchors or actual tool records. The helper does not
open those references or authenticate their contents. The reviewer owns substantive coverage,
actual visual/structural/functional inspection and evidence adequacy.

Each finding has a unique stable ID, summary and evidence. `actionable` findings also
need a decisive `acceptance` criterion. `suggestion` and `out-of-scope` findings require
a `reason`; preserve them in the report without silently making them executable or
dropping requested work. User-authorized improvements belong in actionable findings.
`verdict` is `changes-required`, `accepted` or `blocked`. Acceptance cannot coexist with
actionable findings or required unreviewed coverage. A clean initial review needs no empty executor pass, but its accepted verdict is not recorded as final until separate verifier corroboration and original Reviewer acknowledgement pass.

## Manager checklist

Mechanically convert every actionable finding into the repair checklist and existing
R/P/T plan. Preserve the readable checklist in `checklist.md` and the host's visible
checklist. Keep the structured handoff immutable during that execution attempt:

```json
{
  "schema": "ai-development-workflow/xr-checklist/v1",
  "runId": "example-run",
  "round": 1,
  "sourceRevision": "actual-original-snapshot-identity",
  "outputRevision": "actual-reviewed-output-identity",
  "managerId": "actual-manager-identity",
  "planRevision": 2,
  "reviewHash": "canonical SHA-256 of the complete review JSON",
  "items": [
    {"id": "R1", "findingIds": ["F1"], "task": "Restore the specified destination through the existing owner.", "acceptance": "The source-equivalent control opens its specified destination."}
  ]
}
```

Item IDs are stable existing R IDs. One finding may require several distinct tasks; a task
may resolve several findings. Every actionable finding must appear, no non-actionable
finding may become a repair accidentally, and every task needs concrete acceptance.
Do not use an aggregate checkbox to conceal independent unresolved commitments.

This conversion is accounting, not a manager quality review. The reviewer confirms the
exact derived repair plan/checklist under the existing current-critique gate before the
executor changes source. A hash match does not provide that critique. Use the existing
`resolve_plan_record.py --execution --require-critique` admission and actual authorization.
The immutable JSON has no item `status`; execution outcomes belong in the executor report.

## Executor report

Bind the report to the exact handoff, current plan and input revision:

```json
{
  "schema": "ai-development-workflow/xr-execution/v1",
  "runId": "example-run",
  "round": 1,
  "sourceRevision": "actual-original-snapshot-identity",
  "planRevision": 2,
  "checklistHash": "canonical SHA-256 of the complete checklist JSON",
  "executorId": "actual-executor-tool-identity",
  "inputRevision": "actual-reviewed-output-identity",
  "outputRevision": "actual-result-after-execution",
  "outcome": "complete",
  "items": [
    {"id": "R1", "status": "implemented", "note": "Restored the route and ran its stated checks.", "evidence": ["execution.md#R1", "checks/navigation.txt"]}
  ]
}
```

The result ID set must exactly equal the checklist ID set. Each item has a nonblank note
and `status: implemented | blocked | not-run`. Implemented items require evidence references;
unresolved items explain their blocker or remaining work. No `skipped`, `waived`, renamed
or omitted item counts as implementation. `outcome` is `complete`, `partial` or `blocked`,
consistent with the item statuses. The executor cannot report independent acceptance.

The manager reconciles IDs, status, report bindings and evidence-reference presence. Missing
accounting goes back to the executor; disputed quality goes to the reviewer. An executor's
`implemented` report is not a verified `[x]` in the final acceptance checklist. Keep the
requirement open or in progress until the fresh reviewer verifies it. Report real blockers
without erasing items, and continue any independently authorized work that remains possible.

## Clean initial review corroboration

A first review with no required repair needs a second actual contributor. The manager supplies
the exact review, source/output identities and full coverage inventory to a distinct Verification
Engineer. It independently checks the decisive criteria, reports real evidence and known limits,
and returns a corroboration document:

```json
{
  "schema": "ai-development-workflow/loop-corroboration/v1",
  "runId": "example-run",
  "round": 1,
  "sourceRevision": "actual-original-snapshot-identity",
  "outputRevision": "actual-reviewed-output-identity",
  "reviewHash": "canonical SHA-256 of the exact initial review JSON",
  "verifierId": "actual-distinct-verifier-identity",
  "coverage": [
    {"id": "source:primary-flow", "side": "source", "status": "reviewed", "evidence": ["corroboration.md#source"]},
    {"id": "result:primary-flow", "side": "result", "status": "reviewed", "evidence": ["corroboration.md#result"]},
    {"id": "compare:primary-flow", "side": "comparison", "status": "reviewed", "evidence": ["corroboration.md#comparison"]}
  ],
  "verdict": "confirmed",
  "findings": [],
  "evidence": ["corroboration.md"]
}
```

Use all actual required coverage IDs, not only the example rows. Verifier must differ from
manager and initial Reviewer. Verdict is `confirmed`, `changes-required` or `blocked`; actual
findings/limits cannot be omitted to claim confirmed. The task's contribution ledger separately
records the verifier's limitations, exact artifact revision and effect on synthesis.

The original Reviewer reads the corroboration and returns its own acknowledgement:

```json
{
  "schema": "ai-development-workflow/loop-acknowledgement/v1",
  "runId": "example-run",
  "round": 1,
  "sourceRevision": "actual-original-snapshot-identity",
  "outputRevision": "actual-reviewed-output-identity",
  "reviewHash": "canonical SHA-256 of the exact initial review JSON",
  "corroborationHash": "canonical SHA-256 of the complete corroboration JSON",
  "reviewerId": "actual-original-reviewer-identity",
  "decision": "accepted",
  "evidence": ["reviewer-acknowledgement.md"]
}
```

Decision is `accepted`, `changes-required` or `blocked`. A stale/missing/partial corroboration,
nonconfirmed verdict, remaining actionable finding, incorrect identity or unreviewed coverage
cannot become acceptance. Manager performs accounting only and cannot author either worker's
verdict. No repair means no invented executor or empty repair pass. New defects enter the
ordinary reviewed checklist path. Existing XR review/checklist/execution/timer schemas stay intact.

## Fresh review and acceptance

Spawn a new independent reviewer after fully accounted execution. Its `review.json` uses
the same schema, run/source identity and coverage IDs, the **next round number**, the actual
executor output revision, and a fresh reviewer ID distinct from the manager, executor and
previous reviewer. Reinspect the original and result under equivalent conditions. Retain
all required coverage; genuinely added coverage may extend the inventory.

Add `resolutions` with exactly the prior actionable finding IDs:

```json
"resolutions": [
  {"id": "F1", "status": "resolved", "evidence": ["comparison.md#F1-recheck"]}
]
```

Each resolution is `resolved` or `unresolved` with actual evidence references. Preserve an
unresolved finding's stable ID in the next round's actionable findings. New defects receive
new IDs. Never reuse a known ID for a different issue. A reviewer may conclude
`changes-required` or `blocked`; that is valid evidence, not acceptance. The next checklist
covers that review's current actionable findings. Preserve every previous report.
The helper rejects an unresolved prior finding missing from the new actionable set, and
rejects a resolved finding simultaneously declared actionable under the same ID.

`verdict: accepted` requires every prior actionable finding resolved, complete observed
coverage and no current actionable finding. The manager records that reviewer's decision
without substituting its own product judgment. Later output changes invalidate earlier
acceptance; carry only evidence that still applies to the new revision.

## Run the accounting helper

```bash
python3 <skill>/scripts/loop_checklist.py check \
  --review <round-001>/review.json \
  --checklist <round-001>/checklist.json \
  --execution <round-001>/execution.json \
  --acceptance <round-002>/review.json
```

Omit `--execution` when reconciling a new checklist. Omit `--acceptance` until the fresh
review actually returns. For an initial clean review, use its empty checklist and no executor,
plus the actual verifier and original Reviewer documents:

```bash
python3 <skill>/scripts/loop_checklist.py check \
  --review <round-001>/review.json \
  --checklist <round-001>/checklist.json \
  --corroboration <round-001>/corroboration.json \
  --acknowledgement <round-001>/acknowledgement.json
```

Do not manufacture execution, corroboration or acknowledgement to satisfy the shape. These
flags cannot replace a fresh post-execution review on a repair path.

Use the importable `canonical_hash(document)` for `reviewHash` and `checklistHash`:

```python
import json, sys
sys.path.insert(0, "/actual/skill/scripts")
from loop_checklist import canonical_hash
review_hash = canonical_hash(json.loads(open("review.json", encoding="utf-8").read()))
```

The helper returns `valid`, `errors`, pending item IDs, `readyForFreshReview` and
`reviewerAcceptanceRecorded`. Exit 0 means the declared accounting is valid, including a
truthful partial/blocked report; **check the flags**, since exit 0 alone does not mean ready
or accepted. Exit 2 means malformed or inconsistent accounting. The helper is read-only.
It does not execute tests, inspect pixels, open evidence links, authenticate identities,
dispatch workers or approve the plan. Its acceptance flag records a structurally consistent
reviewer assertion; actual review and real tool identities remain mandatory.

## Timer bookkeeping interface

Follow [the wait-first monitoring protocol](loop-timers.md). The optional
`monitor_transition(state, event)` function (also `timer_transition`) proposes checkpoint
changes/actions; it never performs host operations. The historical `timer` CLI name and
`ai-development-workflow/xr-timer/v1` state schema remain supported for compatibility.

```bash
python3 <skill>/scripts/loop_checklist.py monitor --event <actual-start-event.json>
python3 <skill>/scripts/loop_checklist.py timer --state <checkpoint.json> --event <actual-event.json>
```

Every event supplies `type`, `runId` and timezone-aware `now`. Start also requires an actual
active `workerId`, `phase: review | execute`, and the discovered capabilities below. These
are normalized **helper fields**, not a guessed host-tool call signature.

| Capability | Exact helper fields |
| --- | --- |
| Preferred wait | `waitTool: {"name":"<actual exposed tool>","contract":"<schema/evidence reference>","minWaitSeconds":1,"maxWaitSeconds":300}`. Use the actual documented limits; a usable minimum must be at most 60 seconds. The example values are illustrative, not claims about Codex's API. |
| Timer fallback | Omit `waitTool`; supply an observed `waitUnavailableReason` and `nativeTimer: {"kind":"one-shot","canCancel":true,"contract":"<actual schema reference>"}`. `kind: recurring` requires cancellation support. |
| Final fallback | Omit both capabilities; provide both `waitUnavailableReason` and the observed native timer `unavailableReason`. |

If both capabilities are supplied, usable wait wins. Invalid capability declarations fail;
record an actual definitive unusability reason before selecting a lower-priority mechanism.
The state contains the 300-second interval, fixed deadline, current worker, monitor generation,
mode (`wait`, `native` or `active-session`), pending call/registration and real evidence
references supplied by the caller. `executesHostActions` is always false. A proposed
`wait-host`/`register-native` action is not a successful call or registration.

### Wait events

Each proposed `wait-host` action reserves one context with `generation`, `attempt`, `tool`,
`workerId` and bounded `seconds`. Carry the first four unchanged in its actual result event,
with the same run identity. Translate timeout seconds to the documented host arguments.
Do not issue a second wait while `activeWait` is unresolved. Early results preserve
`nextCheckAt`; a due result requests one worker inspection.

| Event | Additional fields and effect |
| --- | --- |
| `wait-returned` | Matching generation/attempt/tool/worker, actual `receipt`, and `outcome: timeout | event | worker-completed`. Completion also needs actual `workerReceipt`. A current completion advances immediately; early ordinary returns propose the next bounded wait against the same deadline. |
| `wait-failed` | Matching context, actual `receipt`, `reason`, and `outcome: not-waiting | unknown`. Unknown retains the pending call and requires reconciliation. Confirmed inactivity with unusability permits explicit mechanism reconfiguration. |
| `wait-reconciled` | Current `generation`, `attempt`, `tool`, actual `receipt`, and `waitStatus: active | inactive | unknown`. If a call is pending, also preserve its `workerId`. Active/unknown status blocks a second monitor. Inactivity clears the pending call; a held run does not restart from this event alone. |
| `tick` | Actual clock observation. An outstanding wait produces `await-current-wait`, never another wait. With no pending call, respect the same deadline; a pending status check/failure remains unresolved. |

A pending wait result from the wrong worker, tool, attempt, generation or run is ignored.
Returned evidence cannot authenticate itself; the caller must retain the actual host result.
A return for a stopped run may finish cleanup but cannot dispatch/rearm. An external
`worker-completed` advances accounting immediately but preserves an unresolved wait; finish
that wait before `worker-started` binds the next worker.

### Timer events

| Event | Additional fields and effect |
| --- | --- |
| `registered` | Matching registration `attempt`, actual `timerId`, `receipt`; optional host `nextCheckAt`. Armed status requires supplied successful host evidence. |
| `registration-failed` | Matching `attempt`, `outcome: not-created | unknown`, `reason`. Unknown requires reconciliation; definitive failure remains explicit until an observed valid fallback is configured. |
| `reconciled` | Matching `attempt`, boolean `exists`, actual `receipt`; for an existing timer also `timerId` and optional host deadline. Reuse a confirmed registration; only confirmed absence permits replacement. |
| `wake` | Actual current `timerId` and unique `eventId`. Due wakes inspect the current worker. Retain all `handledWakeIds` for the run, so nonconsecutive duplicates cannot replay. |
| `cancelled` | Matching `timerId` and actual cancellation `receipt`. Records confirmed cleanup. |
| `cancel-failed` | Matching `timerId` and `reason`. Retains cleanup pending. |

Preserve each registration attempt in its real call context. A stale attempt cannot arm or
fail the current timer. A native `tick` awaits the actual native event. A genuine consumed
one-shot proposes the next 300-second registration only after an observed check and while
active. Recurring registration is retained without a burst of missed checks.

### Shared coordination events

| Event | Additional fields and effect |
| --- | --- |
| `checked` | Actual status-check `receipt`; requires a pending check. Wait/final-fallback next deadline is 300 seconds after actual service. Native mode follows its real one-shot/recurring semantics. |
| `worker-completed` | Nonblank matching actual `workerId`. Immediately advances once. Missing, blank, null or stale IDs do not advance. |
| `worker-started` | Actual new `workerId` and `phase`; requires prior completion and resolved outstanding wait. A stopped unfinished phase must resume that same phase. |
| `resume` | Hold further work and inspect saved ownership plus monitor status. Accepted/cancelled runs cannot resume. |
| `resumed` | Matching saved `workerId`, observed `workerStatus: running | completed | stopped | unknown` and actual `workerReceipt`. A saved ownerless handoff uses null ID and `none | unknown`. Requires preceding resume and current monitor reconciliation. |
| `stop` | `phase: accepted | blocked | cancelled | interrupted`. Prevent further work and clean up through actual supported tools. Suspension preserves the old worker/phase; accepted/cancelled stays terminal. |

### Resume a suspended checkpoint

Keep the same state and original `suspended` worker/phase after blocked/interrupted stop.
`resume` establishes `resumePending` and never dispatches by itself. Observe actual worker
ownership. For wait mode, send matching `wait-reconciled` inactive evidence (or consume the
actual pending return); active/unknown wait still holds. For native mode, send `reconciled`
with real boolean existence/receipt or confirmed cancellation. Suspended cleanup must be
inactive; an active resumed run may reuse its verified timer. Final fallback checks the
actual clock and still requires worker reconciliation.

Only then send `resumed`. Running workers are reused; completed workers advance through
normal accounting once; stopped unfinished workers return `resume-phase` with `pendingPhase`.
Unknown ownership stays held. Wait mode preserves its original deadline and checks immediately
if overdue; it does not reset the deadline on an early return or ordinary resume. No observation
here establishes product quality, native persistence or an agent's tool permission.

### Reconfigure or migrate a historical checkpoint

A 600-second checkpoint remains historical until explicitly reconciled. Ordinary work events
return `reconfigure-monitor`; terminal cleanup can still finish without reopening the run.
Use this same sequence to change mechanisms after an actual capability failure:

1. `reconfigure`: supply the new discovered capability fields (wait takes precedence), plus
   `receipt` referencing the actual correction/capability observation. This preserves the
   old checkpoint/context, holds work, inspects the prior worker and proposes old-monitor cleanup.
2. Complete actual wait return/status or timer cleanup. Feed its normal matching event into
   the held checkpoint. Live/unknown old monitoring cannot be replaced. Repeated reconfigure
   requests do not create another generation or restart the worker.
3. `reconfigured`: supply the saved `workerId`, actual `workerStatus`, `workerReceipt` and
   `cleanupReceipt`. The state must also show no pending wait/timer and confirmed stopped
   monitoring. Unknown ownership or unfinished cleanup remains held regardless of prose.
4. The new generation uses 300 seconds and the preferred observed mechanism. Running workers
   are reused. Completed/stopped/ownerless handoffs do not start a wait on a finished worker;
   the next real worker gets the new binding. `monitorHistory` retains the old checkpoint,
   correction, cleanup, worker observation and transition time. Do not truncate receipt history.

A new monitor generation invalidates old wait contexts. Native registration attempts remain
monotonic across mechanism changes. Accepted/cancelled runs cannot be reopened through this
path. Cleanup or structural checks do not authenticate receipts or execute any host tool.
