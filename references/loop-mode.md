# Loop — Execute and Review

Follow the [mandatory workflow contract](workflow-contract.md): capture scope, plan and criticize proportionately, announce ordered phases/owners and the actual numeric agent count, and pass current admission before every product write.

Use Loop for an authorized review-and-repair loop over existing work. **Start with review.**
The current agent is the manager; a separate reviewer judges the work and a separate
executor changes it. The manager reconciles the checklist and coordinates the workers.
The Reviewer alone decides substantive acceptance. A clean initial result also needs a distinct Verification Engineer contribution acknowledged by that Reviewer. Continue until the applicable independent review accepts
the current result, or an actual blocker, interruption or cancellation prevents progress.

## Contents

1. [Enter and recover the task](#enter-and-recover-the-task)
2. [Own the right work](#own-the-right-work)
3. [Review the originals and result](#review-the-originals-and-result)
4. [Build the checklist and admit execution](#build-the-checklist-and-admit-execution)
5. [Execute and reconcile](#execute-and-reconcile)
6. [Review again and continue](#review-again-and-continue)
7. [Monitor every five minutes](#monitor-every-five-minutes)
8. [Checkpoint and report](#checkpoint-and-report)

## Enter and recover the task

Explicit forms include `loop <task>` and `/ai-development-workflow loop <task>`.
In ChatGPT, select the main skill from `@` autocomplete and append `loop` and the task;
a compatible local host can use `$ai-development-workflow loop <task>`.
`XR`, `/ai-dev-loop` and the historical `/ai-dev-execute-review` remain explicit router aliases,
not separately registered public skills. Quoted commands or field names inside ordinary
task prose are not invocations.

The descriptor is [modes/loop.json](../modes/loop.json). Continuation callers use
`--selected-mode loop` alongside an actual retained `--selected-preset` where present.
Legacy `--selected-mode XR` is accepted. Routing describes the mode; it does not spawn
workers, start a timer or allocate a record.

The public mode is named Loop. Existing `artifacts/xr/` evidence paths and `xr-*` serialized
schemas remain unchanged for compatibility. Do not rename old checkpoint bytes, hash chains
or wire identifiers merely to make their spelling match the public name.

Recover the original request, adopted corrections, source/reference files, latest result,
allowed changes and actual target environment. With bare Loop, use the related work already
identified in the conversation. Ask only for a genuinely missing target or source that
cannot be recovered. A request to add or explain Loop does not itself launch an indefinite
repair run. Preserve explicit audit-only, plan-only and no-publish boundaries; resolve an
explicit conflicting write-capable invocation instead of silently executing repairs.

Reuse the exact active compatible development record. If only a quick G0 checklist or
chat/artifact record exists, preserve it as source evidence and announce a one-time promotion:
allocate one six-file development record through the existing GAS stage-0 helper, cross-link
the records, and carry original request provenance, stable IDs and actual evidence/status.
Keep the original request/checklist/history unchanged; copied checkmarks do not grant Loop
acceptance. If no record exists, allocate once through the same helper and capture the request.
Use that new development record for every later round/resume; never repeatedly promote or
launch a second assessment pipeline. Do not pass a quick record to six-file admission.
Keep the record's actual `workflowPreset` and record Loop in additive mode metadata/results.
Loop is a public mode using the same record, not a new G preset. Follow
[the record contract](record-contract.md); subsequent rounds never allocate another record.

Inventory sources and required targets/states before review. Bind comparisons to actual
source/result revisions (commit plus relevant working changes, hashes or provider versions).
An original document can specify behavior without providing a runnable original page: record
that distinction. Do not invent original interactions or infer visuals from markup alone.
Use [task contracts](task-contracts.md) to distinguish reconstruction from authorized changes.

## Own the right work

| Role | Owns | Does not own |
| --- | --- | --- |
| Manager | Task context, real dispatch, review-to-checklist mapping, item accounting, timer/status checks, saved state and handoff | Product inspection, visual/code quality review, fixes, or acceptance judgments |
| [Reviewer](../agents/reviewer/agent.md) with `loop-review` | Original/result investigation, actual interactions, comparison, complete findings, repair-plan confirmation and substantive acceptance | Product/source repairs or approving its own implementation |
| [Builder](../agents/builder/agent.md) with `loop-execution` | The admitted checklist, scoped changes, appropriate tests and item-by-item implementation evidence | Deleting findings, weakening criteria, changing scope or declaring independent acceptance |
| [Verification Engineer](../agents/verification-engineer/agent.md) | Independent decisive coverage/check corroboration for a clean initial result | Repairs, manager accounting or replacing the Reviewer’s acceptance decision |

Launch actual agents with the complete assigned profile and task-local inputs. Record returned
worker IDs; a profile applied in prose is not a spawn. Preserve the host's actual models and
tools. If independent workers are unavailable, keep the missing capability explicit and do
useful preparation; never present manager self-review as the requested independent loop.

For every browser worker, supply the complete [browser recovery policy](browser-recovery.md)
and current session owner. Automatic recovery after an unexpected browser handoff requires explicit permission from the current user for the session and support from the host. Reviewers/executors recover their
own assigned browser work; the manager remains a coordinator and does not review the product.

Keep reviewer and executor phases sequential. There is one implementation owner at a time.
Never start execution while review is still changing its findings. Never start a reviewer
against a moving output from an active executor. A timer wake coordinates the existing worker;
it does not authorize a duplicate worker or concurrent manager edits.

## Review the originals and result

First launch a reviewer in fresh context with the original request/corrections, unchanged
sources, current result, inventory, allowed differences, project rules, record and output paths.
Require three explicit report sections:

1. **Original:** Document the relevant pages/files, structure/content, appearance and behavior.
   Open the originals and exercise available controls, buttons, links, navigation, tabs/panels,
   forms, states and document actions. Record what each does and what is unavailable.
2. **Current result:** Repeat the applicable investigation on the delivered work. Use equivalent
   viewport, data, theme, font, selected state and timing where meaningful. Check the actual
   latest output and its complete required target set, including hidden and below-fold content.
3. **Comparison and findings:** Record structural, visual and functional differences; missing
   content/features; broken/incomplete actions; mistakes; regressions; and concrete improvements.
   Distinguish permitted differences, confirmed defects, uncertainty and optional proposals.

Each finding needs a stable ID, affected target/state, source requirement, observation and
evidence, impact, smallest scoped correction, preserved properties and acceptance check.
Keep all findings in the report. Severity orders work; it does not erase minor requested work.
Optional unrelated improvements remain documented proposals, not hidden executable scope.
Missing access is an unresolved coverage item, never a passed check.

For UI, give the reviewer the [UI Design Director](../specialists/ui-design.md), applicable
corrections and [visual review](ui-quality-review.md) instructions. Require real rendering and
interaction for those claims; source/build checks prove narrower things. For documents, use
the actual document format/runtime where applicable. Inspect all requested targets; a contact
sheet or sample is not exhaustive evidence. Reuse domain owners instead of inventing tools.

## Build the checklist and admit execution

Wait for the completed review artifact and actual worker result. The manager converts every
in-scope actionable finding into stable, source-linked checklist items with acceptance criteria,
dependencies, allowed files/targets and evidence requirements. Preserve the finding-to-item map;
split independent commitments so a broad checkbox cannot hide unfinished work. Link duplicates
explicitly. Retain blocked and out-of-scope dispositions with their reasons; do not silently
discard an item, narrow the target inventory or replace a failed criterion with an easier one.

Use the existing `checklist.md`, `fix-plan.md`, `test-plan.md` and R/P/T mappings. Save round
evidence under `artifacts/xr/` using [Loop artifacts](loop-artifacts.md). Show the visible checklist
in ordinary Markdown, or use an actually supported and acknowledged host checklist surface. The manager
transcribes and reconciles these artifacts; it does not independently inspect the product.

The initial report cannot approve an arbitrary plan written later. Pass the exact derived
checklist/plan revision back to that reviewer for substantive confirmation of fidelity,
feasibility, scope and decisive checks. Use the reviewer's actual response in `critique.md`.
Reuse an earlier independent critique only if its exact plan and relevant source remain current.
Material changes require reviewer confirmation again. This is part of the review phase, not
another user-permission round or manager quality review. Finalize the reviewed record and
apply `resolve_plan_record.py --execution --require-critique` with its explicit record path;
use the documented resume gate after reconciling interruption. Do not manufacture readiness.

## Execute and reconcile

After the reviewer-confirmed handoff, spawn the executor. Provide the original request,
review report, entire admitted checklist, plan/critique revision, current baseline, protected
properties, expected tests, output paths and assigned write scope. The executor works through
every item, records actual changes/tests, and reports each ID as implemented, blocked or not run
with the matching evidence and output revision. It must return a partial/blocked report when
unable to finish. A statement that everything is done cannot replace the item accounting.

On return, the manager checks **the checklist only**: exact IDs, complete coverage, statuses,
dependencies, required evidence references, revision bindings and unresolved items. The
[bookkeeping helper](../scripts/loop_checklist.py) can detect structural omissions; it does not
judge whether the fix works or authenticate a claim. Missing accounting goes back to the
executor. An actual blocker remains visible; continue independent authorized work where useful.

Do not mark independently verified completion from the executor's claim. Use an explicit
implemented-awaiting-review state in the round evidence and keep final completion unresolved.
The manager must not open the app, inspect the diff or rerun product checks to decide quality.
Those are reviewer duties. The executor may not change the checklist's requirements or its
verification criteria just to obtain a pass. Necessary new scope is recorded for proper review.

## Review again and continue

When all checklist items have complete implementation accounting and the executor has stopped,
spawn a **new reviewer with a new identity and fresh context**. Give it the original sources,
latest instructions, exact new result revision, expected inventory and prior finding IDs.
Include execution evidence as claims to investigate, not proof to trust. Have it repeat the
original/result comparison and relevant interactions, verify each fix, and look for omissions
and regressions outside the executor's reported list. Reuse unchanged source inventory only
when its identity remains valid; do not shrink the actual review coverage.

A clean initial review is a proposed no-repair outcome. Dispatch a distinct **Verification Engineer**
to independently inspect decisive criteria and the required source/result/comparison coverage
against the same exact revisions. It returns corroboration with actual evidence and limitations.
The **original Reviewer** examines that result and returns an explicit acknowledgement accepting,
requiring changes or blocking the outcome. Only then can the manager record acceptance. Use the
exact [corroboration and acknowledgement contracts](loop-artifacts.md#clean-initial-review-corroboration).

Do not spawn an empty executor or manufacture a checklist defect. A corroborated defect enters
the ordinary checklist/criticize/execute/fresh-review path; unresolved coverage blocks acceptance.
All accepted outcomes require current revisions, every required target/state inspected, resolved
in-scope findings and no required blocked/not-run item. The manager checks identities, hashes and
accounting only; it does not perform either worker’s product inspection. This supplies two useful
actual contributors even when no repair is needed.

If changes remain, preserve their IDs, append new ones, reopen affected items and repeat
checklist → reviewer-confirmed plan → executor → fresh reviewer. No fixed iteration count
turns incomplete work into success. If attempts stop making progress, the reviewer diagnoses
the remaining issue; do not repeat an unchanged patch indefinitely. A genuine source/access/
permission/capability blocker pauses dependent work with the exact next action and resumable
state. Only the reviewer can accept the work; only the user can supply a waiver or change scope.

## Monitor every five minutes

Apply [Loop monitoring](loop-timers.md). **Use the actual host's wait tool first**, with a manager
check due every **300 seconds**. Discover the tool's real schema and wait on the current
worker/run. Compose shorter waits where required; early messages and short timeouts preserve
the existing due time. On a due check, read the checkpoint, inspect the current reviewer or
executor, and record progress/blockers. Advance immediately when the worker completes.

If suitable wait is absent or definitively unusable, use the host's native timer, preserving
its real registration, wake and cleanup evidence. Keep one monitoring mechanism per run and
reconcile existing ownership before switching it. A normal wait does not establish a durable
wake after the manager exits. Preserve older 600-second evidence as historical and explicitly
reconcile the checkpoint to the new cadence; never rewrite prior receipts.

Only if neither suitable capability is available, use explicit active-session monitoring
with actual clock reads and bounded waits where permitted. State the limitation.
ChatGPT Automations is a separate
connector: its limits do not describe Codex native timers. Never invent a timer tool name,
claim a saved timestamp is an armed timer, or claim monitoring continues after a session ends
without actual host support. Clean up the timer on acceptance, cancellation or suspension.

## Checkpoint and report

Keep the run ID, exact record, source/result revisions, phase/round, worker identities,
finding/item IDs, report paths, accepted revision and wait/timer handle/check-in history in
`artifacts/xr/` and concise `results.md` entries. Preserve attempts; never overwrite a failed
report with a successful one. The manager owns the state; workers own their assigned reports.
On resume, inspect actual worker/wait/timer status before dispatch, ignore stale results and do
not assume that an unknown previous executor stopped. Save cancellation/cleanup failures.

Announce role/phase transitions and report review, execution and accepted states accurately.
At finish, show the complete actual checklist (or acknowledged supported checklist surface), the fresh review verdict,
checked revision, delivered artifacts and material remaining limits. Include an HTML preview
for generated editor/layout/design/website output when requested by the user's preferences.
Do not call unverified visuals, blocked interactions or an unobserved installation complete.
