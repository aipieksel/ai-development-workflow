# Shared record contract (revision 2)

Apply the [mandatory workflow contract](workflow-contract.md) and [admission metadata](workflow-contract-records.md). Every execution/resume requires current completed criticism and a declared public briefing; no preset or omitted flag waives them.

All stages share the bundled plan_record.py and finalize_plan_record.py. They have no third-party dependencies or sibling-skill imports.
Use Python 3.10 or newer.

The six-file development record lives under documents/tasks/development and contains record.json, checklist.md, fix-plan.md, test-plan.md, critique.md and results.md. Planning, criticism and execution share that directory. For explicit legacy numeric workflows, only stage 0 creates a record; without 0 they reuse the selected existing one. Public Auto/Plan/Build/Review/Loop can capture a fresh task once through the existing allocator as their contracts specify, or reuse the selected compatible record. They do not require the user to type a creation digit. Do not create duplicate records for operations or erase earlier results. Necessary evidence files may be added.

## Automatic composition with real workers

An automatic chain follows [task routing](task-routing.md), resolves a concrete mode, assigns
meaningful work to actual workers and uses the existing record and source/readiness gates. Allocate at most
once using an existing starter; later operations reuse that record. Store selection and
continuation in `artifacts/workflow-selection.json` and `results.md`, as described in
[automatic selection](automatic-selection.md#one-record-and-continuation). Keep the real
starter in `workflowPreset`; do not introduce an AUTO preset. Completed stage evidence is
reused only after source and plan-revision reconciliation. The selection validator does not
replace this contract, dispatch workers or authenticate evidence.

## Loop mode

[Loop](loop-mode.md) reuses the selected six-file record and keeps its actual workflowPreset.
With no compatible development record, invoke the existing GAS stage-0 allocation once.
If the selected work has only a quick G0 or chat/artifact record, explicitly preserve that
original, cross-link the one new development record and carry request provenance, stable IDs
and real evidence/status. Keep the old record kind/content; do not infer acceptance from
copying checkmarks. All later Loop rounds reuse the new record. This narrow Loop promotion
does not change normal G0 behavior, replace the record schema or start a second assessment pipeline.
Record Loop mode/run/round checkpoints as
additive artifacts. The manager derives and reconciles the checklist, the reviewer confirms
the exact current repair-plan revision, and the executor passes the existing critique gate.
Executor-reported implementation remains awaiting fresh reviewer acceptance. Manager accounting
is not substantive review, and a timer wake neither approves work nor creates another record.

## Public-mode capture and internal operations

Public [modes](public-modes.md) capture or reuse one task record. The coordinator calls the
existing allocator only for a genuinely fresh selected task; internal operations and workers
reuse that exact result. A standalone G starter retains its original allocation semantics.
An explicitly unavailable record path is a blocker, not permission to choose another record.

There is no native queue record exception in this edition. Retain historical records as
evidence without pretending their unavailable host integration ran. Loop preserves its old
`artifacts/xr/` paths and `xr-*` serialized schemas for checkpoint compatibility; the public
mode name is `loop`. An old checkpoint must be reconciled with actual current worker state.

## Metadata

Retain schema project-development-plan/v1 for identification; contractVersion: 2 adds execution gating. projectRoot is the verified absolute local project root; recordPath is relative to it. Remote-only source analysis must remain not_ready until rebound to a verified checkout; never set a repository URL as an executable projectRoot.

status: draft | planned | criticized | executing | blocked | complete.
readiness: not_ready | ready | blocked.
blockers: [] only when no unresolved implementation decision or verification prerequisite remains.
critiqueOutcome: not_requested | ready | revised | blocked.
planRevision: positive integer; increment on scope, change sequence, verification or material plan edits.
reviewedPlanRevision: revision covered by the latest completed critique.
sourceBaseline: description plus revision/dirtyPaths when Git exists; for a non-Git project record exact relevant file evidence. This is not an automatic Git cleanliness requirement.
scope: in/out arrays of concrete boundaries.
requestSources: append-only objects with id, role (user/context/policy), origin (message locator or descriptive conversation reference; policy path/section), and verbatim text.
requestHashes: per-source SHA-256 stamped by the finalizer. Keep prior hashes; append new sources, never reseal edited history.
requirements: objects with id, text, sources (source IDs), and kind (requested/necessary). Necessary items also require justification: evidence and why the requested outcome cannot be correctly achieved without this detail.
steps: objects with id, requirements (IDs), paths, change, dependsOn (step IDs).
checks: objects with id, requirements (IDs), method, expected, boundary.
planHashes: SHA-256 of checklist.md, fix-plan.md and test-plan.md at readiness review.
definitionHash: SHA-256 of normalized root/path, revision, source baseline, scope, request provenance and R/P/T mappings. Metadata edits also invalidate readiness.
critiqueHash: SHA-256 of critique.md when a critique is completed.
Preserve createdAt; update updatedAt with timezone-aware UTC.

Keep metadata concise; put detailed evidence and commands in Markdown. IDs connect metadata to corresponding Markdown sections. A syntactically valid record does not prove the plan is sensible, source is current, tests passed, or the user authorized execution.

## Request authority

Before plan derivation, capture the selected messages under [source capture](standard-workflow.md#capture-before-planning), with their original locators. Preserve historical sources; capture only new substantive amendment sources and reuse unchanged sources. Identify current amendment sources in fix-plan.md; historical retention does not require rereading all archives. Keep one checkpoint per distinct in-scope issue with decisive assertions, not a row for incidental discussion. See [source capture](standard-workflow.md#capture-before-planning) for sensitivity, verification and missing-history handling. The six core files and existing metadata schema remain; conversation snapshots are source evidence, not a replacement task record. Hash equality proves capture fidelity only, not semantic coverage.

For a time-anchored invocation, record the resolved inclusive conversation range in fix-plan.md (start date/time/timezone and start/end message locators). Preserve the invocation and scoped source text in requestSources with actual roles. Multiple matching times select the most recent matching message through the invocation, after explicit selectors; they do not require clarification. Resolve genuinely unavailable boundaries and missing range content before record mutation. Earlier context preserves constraints but adds work only when explicitly adopted; later corrections append sources and do not rewrite the original boundary. See [timestamp matching](standard-workflow.md#optional-conversation-start-time). This uses existing files and fields, not a new schema or a machine-enforced timestamp parser.

Preserve the complete relevant user messages and later corrections verbatim in requestSources, including negative constraints, uncertainty, named lists, "only", "first" and "later". A bare invocation selects the underlying related request, not a new task about creating paperwork. Include only relevant conversation context; label assistant explanations context, never user authorization. If an existing authoritative request.md already contains the text, reuse its source IDs/locators when recording the text here; do not create another source document.

After first finalization, sources are append-only. Append corrections with new IDs and identify what they supersede in the plan; retain the old text and hashes. Do not edit or clear old requestHashes to make a changed request pass. The helper detects accidental source changes during normal finalization, not malicious rewriting of both text and hashes, and cannot determine whether a quote or justification is truthful. Compare against the actual conversation at review and execution.

Each R item must be requested (citing a user source) or necessary (citing user/policy authority and evidence-backed justification). A necessary detail may preserve existing behavior, fulfill an actual dependency or satisfy mandatory safety policy; it cannot choose an optional product feature. Source references prove provenance exists, not that the requirement follows from it. Check both directions: every requested outcome/constraint is covered, and every executable item is warranted. Keep optional proposals outside executable R/P/T mappings.

### User-list coverage

Before deriving or revising the checklist, enumerate the individual items in
the selected user's bullets, numbered lists, Markdown checklists, nested
lists, and itemized table rows, including lists in the invocation and later
amendments. Read surrounding prose and parent items with each child so that
conditions, exclusions, sequence, and acceptance details remain attached.
Preserve the original list text and checkbox marks in the existing source
archive/requestSources; a formatted message is still a source request.

Give each distinct requested outcome or constraint its own source-linked R
checkpoint and corresponding checklist checkbox. Split an item with multiple
independent commitments when a single checkbox could hide unfinished work.
Keep grouping labels as context rather than creating artificial action items.
Shared implementation steps or tests do not erase individual outcomes. Reuse
stable IDs for duplicates/corrections and retain all relevant source mappings;
do not collapse an entire list into "address all requested changes."

Before finalizing planning and during criticism, compare every source-list
item against the checklist. Each must be covered or explicitly accounted for
as duplicate, non-actionable context, out of scope, deferred, superseded, or
already verified, with a reason when plausible requested work is excluded.
Explicitly requested items are in scope unless actual authority says otherwise;
the agent's preference is not an exclusion reason. Hypothetical suggestions and
assistant findings retain their existing authority boundaries. A user-supplied
`[x]` alone does not verify the item in the current execution.

For example, a message asking to show the checklist while building it, show
checked-off items after execution, and include items from user lists contains
three distinct commitments. Preserve all three as separate checkpoints rather
than one "improve checklist handling" row.

### Visible checklist and execution reporting

The durable `checklist.md` and user-visible list contain the same stable IDs, scope and state.
Show the initial draft while planning is underway, material additions/corrections, current
progress and final reconciled outcomes in ordinary Markdown. Label partial drafts and include
the durable record path. A promise or file link alone is not visible checklist publication.

An actually available host checklist/plan tool may mirror the list through its documented
schema and returned acknowledgment. This package does not install a custom panel or define
that host API. Do not report a panel updated from a local converter or an attempted call.
If a supported visible surface is unavailable, failed or incomplete, use the complete
Markdown list; do not omit items because a tool has size or state limits.

Use the record directory name as a stable list identity and retain R IDs on every update.
Keep unresolved items visible. Replace a list only to reconcile its complete intended state;
never erase unfinished work through omission. Mark complete only after decisive evidence.
The durable markers are `[ ]` pending, `[~]` in progress, `[x]` complete and `[!]` blocked.
Use ordinary unchecked Markdown boxes plus status text when an interface cannot render the
extended markers. Preserve unaffected verified outcomes; reopen only stale/affected ones.

The optional helper can convert a development record into generic local JSON:

```bash
python3 <SKILL_DIRECTORY>/scripts/checklist_payload.py --record <RECORD>
```

It prints data only. It does not contact a host, publish, prove persistence or authorize work.
Map it only through a real consumer's supported contract. Update durable and visible states
in the same work interval after meaningful changes.

After execution, expose every current item with its actual complete or unresolved state and
the reasons for remaining work. A successfully acknowledged host checklist may serve as the
visible list; otherwise render Markdown. Partial, blocked and interrupted outcomes remain
visible. A count, “all done” or results-file link is insufficient. Planning/criticism handoffs
show the resulting checklist without claiming implementation. Stage 0 alone does not invent
checklist work or execution.

### Behavioral scope review

Apply these decisions to all work, including plans, code, configuration, documents, generated artifacts and operations:

- **Requested:** identify the source phrase supporting each distinct outcome or constraint in a requirement. Paraphrases and ordinary implementation choices are allowed; a broad citation or labels such as "integration", "quality" or "recovery" cannot support extra behavior. Separate an inferred detail from a requested outcome when they have distinct effects. Use existing source locators and brief quotations in the plan or critique; do not copy entire messages again or create new metadata fields.
- **Necessary:** explain which authorized outcome or existing obligation would fail without the detail, cite the inspected evidence, and consider a narrower way to achieve it. Record this in the existing justification and plan. A preference for robustness, convenience or best practice is insufficient. Problems created solely by an optional agent-added design do not make that design or its follow-on repairs necessary. Preserve genuine dependencies and safeguards; this test does not require the user to specify internal implementation mechanics.
- **Effects:** compare behavior before and after the whole change. Include applicable effects on interfaces/defaults, inputs/outputs, data storage or transformation, dependencies, external actions, permissions/costs, and execution/failure/recovery rules. Inspect surrounding instructions, callers, adapters, configuration, orchestration and post-processing. An unchanged underlying component, document or dataset does not establish unchanged behavior. Review the effects wherever implemented, including additions hidden inside existing R/P/T items.
- **Disposition:** retain supported changes and remove unsupported additions from executable work. Continue the authorized task without asking permission to omit optional extras. Ask only when an unavoidable material expansion needs a user decision; pause that dependent part and continue independent in-scope work. Execution authorization, a reviewed plan, passing tests and a helper's success cannot supply missing scope authority.

Keep the scope delta in fix-plan.md short: each material behavior change, its supporting phrase or necessity evidence, and its disposition; identify behavior that must remain unchanged and deferred/excluded work. Criticism must reconcile this with the sources and actual proposed changes, not merely repeat "no scope expansion". Resolve contradictory evidence and unreviewed additions before declaring ready. Unchanged items can reuse existing evidence; internal choices without a distinct behavior change need no extra checklist row. Use the existing six files and mappings, not another approval layer.

An effect not covered by the admitted scope is a scope change even when discovered during execution under the same requirement ID, file ownership or component bytes. Assess it before mutation. Amend the affected plan and increment its revision for a material change; refresh required criticism before implementing it. Ordinary implementation of the admitted behavior is not a scope amendment. Documenting an addition after execution does not retroactively authorize it. Check the final changes against the same source-derived scope before completion.

Correct faulty implementations within the authorized goal without new approval rounds. If a genuinely necessary correction materially changes the goal, interface, storage ownership, permissions or runtime failure policy beyond that authority, obtain the user's decision before accepting that expansion. Investigation and verification procedures are evidence-gathering work; they do not authorize persistent features, restrictions, automation or side effects. Safeguards already required by the request, existing contract or mandatory policy remain required; scope discipline is not permission to under-deliver.

Example traceability:
```json
{
  "requestSources": [{"id":"S1","role":"user","origin":"Current user request","text":"Preserve the requester's Slack identity"}],
  "requirements": [{"id":"R1","text":"Preserve the requester's Slack identity","sources":["S1"],"kind":"requested"}],
  "steps": [{"id":"P1","requirements":["R1"],"paths":["app/example.ts"],"change":"Carry the authenticated requester through dispatch","dependsOn":[]}],
  "checks": [{"id":"T1","requirements":["R1"],"method":"Integration test with two users","expected":"Each run retains its own requester","boundary":"Fixture test; live identity configuration still needs verification"}]
}
```

## Selection and readiness

Pass --record whenever the task already identifies a record. Relative paths resolve from --project-root, not the process working directory. The AI Development Workflow skill must always pass --record after selecting from this conversation or an explicit user path. Do not use automatic filesystem selection, even if exactly one active record exists. The underlying helper supports automatic selection for compatibility only. Multiple, malformed, incomplete or escaped records produce errors rather than silently selecting old work. Ask only when the intended record cannot be resolved from the conversation and project.

After source review and traceability are complete, fill the metadata and run:
```bash
python3 <SKILL_DIRECTORY>/scripts/finalize_plan_record.py --project-root <ROOT> --record <RECORD> --stage planned
```
Planned finalization validates plan/provenance for criticism and leaves execution not_ready.
Use --stage criticized only after substantive criticism, resolved findings, actual ready/revised
outcome and the completed additive workflowContract review/briefing data documented in
[admission metadata](workflow-contract-records.md). The finalizer validates these supplied
fields and current bindings before atomic replacement; it does not create review evidence,
publish a message, establish source freshness or grant permission.

Criticized finalization also supports a legitimate record-only Plan or Review contract.
It validates the same completed criticism, provenance, phases and public briefing without
inventing a product mutation. The result is `status: criticized`, `readiness: not_ready`,
`reviewValidated: true` and `executionAdmitted: false`. This is a completed reviewed outcome,
not an unfinished critique. A selected product-writing workflow can instead become `ready`,
but still needs separate execution admission. Never add a dummy execute phase to finalize
a planning or inspection task.

If blocked, preserve the reason and set readiness blocked; do not run the finalizer merely to clear it. Critique may be completed yet blocked. A changed plan invalidates old hashes; re-review it. The planner cannot reset a previously reviewed plan to not_requested to bypass a blocked critique.

Executor gate for actually selected and authorized product changes:
```bash
python3 <SKILL_DIRECTORY>/scripts/resolve_plan_record.py --project-root <ROOT> --record <RECORD> --execution
```
Interrupted executing/blocked work requires --resume and an explicit record. Reconcile actual changes and outcomes, clear only resolved blockers with evidence, and run finalize_plan_record.py with --resume plus --stage criticized after completed current review and the updated declared briefing. This validates current evidence while preserving interrupted status, so resolve_plan_record.py --resume can admit the same attempt. Planned-only finalization cannot admit resumed writes. Save the original admission revision/hashes and previous failures in results.md first. If the substantive plan changed, pause and re-review it before this transition. Never run two executors on the same record/worktree; record an execution owner/attempt and check for active ownership before mutation. Scripts do not implement a distributed lock.

Check hashes at admission under the exact normalization/binding rules in [admission metadata](workflow-contract-records.md). Normal execution updates checkbox state and results; changes to requirement wording, references or plan content still invalidate review. Do not rehash changed plan definitions and retroactively pretend they were originally reviewed. At interruption, first reconcile, then a reviewer refreshes readiness as appropriate. Preserve attempts and failed checks.

## Existing records and relocation

All older records remain inspectable. Execution also requires the additive
workflowContract schema and its actual current evidence. Inspect source and preserve old
review/history while adding truthful contract data to the same selected record; never
infer completion from a legacy ready flag. No bulk migration of unrelated records.

Old v1 records remain inspectable, but execution rejects absent contractVersion 2. Migration is explicit: inspect all six files and source, retain history, add missing metadata and mappings, verify root identity, then finalize after review. Do not automatically convert a legacy status into ready.

Older v2 records without request provenance remain inspectable but require a source-fidelity review before execution. Enrich only the selected record from the available original conversation, preserving revision/history; do not migrate other tasks or ask permission merely to populate available evidence. If the actual request cannot be recovered, ask for that missing context rather than labeling the agent's plan as the user's words. Refresh readiness after the review, retaining any required critique/resume gates.

After moving a project/record, verify project identity and source before updating projectRoot/recordPath. Source revision drift is not automatically fatal: inspect changed relevant files; unrelated changes are recorded and preserved. Material drift blocks implementation and requires plan correction.

## Evidence and completion

In fix-plan.md, retain the requested stages, actual deliverable and decisive completion evidence derived from the chronological user instructions. This is part of the existing reviewed plan, not an extra schema or approval layer. Structural validation cannot detect a semantically substituted deliverable: an internally valid documentation record is not evidence of implementing an adopted product checklist. Planning-only history remains preserved, but later implementation authority and clarification must govern the current work. Apply SKILL.md's execution-intent rules before readiness and completion claims.

Record each executed check: ID, exact command or manual procedure, environment, time, exit code where applicable, result and artifact reference. Label not_run, failed, passed and waived distinctly. A waiver needs explicit user authority and does not become a passed test.

Complete means every requested in-scope outcome has decisive evidence. External deployment, publication or acceptance may remain separate states when excluded from scope; do not block a completed code-only task solely for unrequested deployment. If an in-scope outcome remains unverified, use blocked and keep the checklist open.

Use status complete for done/closed; completion does not archive the conversation or make the record immutable. Any subsequent substantive user instruction amends the selected record by meaning under [source capture](standard-workflow.md#capture-before-planning), without requiring a mode or trigger phrase. Reopen affected outcomes, increment revision for material changes, invalidate readiness and preserve prior completion/history and unaffected outcomes. Append distinct requirements; revise or supersede existing ones for corrections rather than retaining contradictory executable instructions. Only an explicit fresh-task selection or a fresh legacy stage 0 creates another record; prior records remain untouched. Execution follows current user intent and pending authorization, not record status alone.

Store commands and outcomes, not credentials, private tokens or unredacted personal data.
