# Portable workflow contract records

Apply [the workflow contract](workflow-contract.md) and [team routing](task-routing.md).
These are portable declarations, not authenticated worker/chat receipts or proof of review
quality. The host must dispatch real workers, inspect source/evidence and emit actual briefings.

## Contents

- [Location and explicit migration](#location-and-explicit-migration)
- [Selection and assignments](#selection-and-assignments)
- [Actual workers and authors](#actual-workers-and-authors)
- [Useful contributions and current results](#useful-contributions-and-current-results)
- [Criticism and bindings](#criticism-and-bindings)
- [Author, announce and admit](#author-announce-and-admit)
- [Completion validation](#completion-validation)
- [Compact G0](#compact-g0)

## Location and explicit migration

Development records retain `schema: project-development-plan/v1`, `contractVersion: 2`, their
six files, source provenance and stable R/P/T mappings. The executable `workflowContract`
object now uses **`ai-development-workflow/contract-v2`**. G0 retains its existing `request.md`
and `checklist.md`, with one `workflow-contract.json` in the same directory. A compact task
is not promoted to six files merely to satisfy staffing.

Archived v1 records and XR evidence retain their original bytes/hashes. Inspect them as history.
Active execution or completion requires explicit current reconciliation. This read-only helper
prints a proposal without editing the record, inventing contributions or admitting execution:

```bash
python3 scripts/workflow_contract.py migration-proposal --record /absolute/task/record
```

Add `--kind quick` for G0. The result contains `sourceContractHash`, `proposedContract`,
`requiredActions` and `executionAdmitted: false`. It retains the original parsed contract under
`legacyEvidence.contract` and actual roster identities/evidence, with new declarations pending.
Preserve the old record snapshot before adopting any proposal. Reconcile the actual selected
mode, aliases, operations, scope, all authors and valid outputs; obtain missing contributions and
current criticism. Never promote an old single-worker result or silently rehash its old review.
A pending template/proposal is preparation, not permission to work alone or edit product files.

## Selection and assignments

| Field | Required declaration |
| --- | --- |
| `schema` | `ai-development-workflow/contract-v2`. |
| `selection.workflow`, `reason` | Actual workflow/command/recipe/composition and source-grounded reason. |
| `selection.selectionSchema`, `discovery` | New selections use `ai-development-workflow/selection-v2` and a current `ai-development-workflow/discovery-v1` receipt. Legacy selections remain readable but require discovery reconciliation before new execution. |
| `selection.mode` | Concrete `plan`, `build`, `review` or `loop`. Auto/XR are selector/alias provenance, not unresolved execution modes. |
| `selection.originMode` | Optional selector provenance, e.g. Auto. |
| `selection.routing` | Exact inspected impact fields below. |
| `selection.uiContext` | Boolean `applicable`, `kind: none|mechanical|design|shared`, and concrete `reason`. False applies only to none. |
| `selection.verificationContext` | Boolean `required`, unique `triggers` and concrete `reason`; required is true exactly when triggers are nonempty. |
| `selection.reviewPolicy` | Independent criticism for writing/Plan and selected independent-review work. Any permitted self-check of a read-only approach does not replace two useful workers or independent corroboration. |
| `selection.phases` | Ordered `id`, `title`, `kind`, `operation`, `writeScope`, `dependsOn`, `owner`. Dependencies refer only to preceding phases. |
| `selection.delegation` | `policy: required`, concrete `reason`, nonempty source `evidence` and required assignments. |

Routing has exactly `impact`, `affectedPages`, `affectedFeatures`, `changedSharedContract`,
`architectureOrMigration`, `reason`, `evidence`. Impact is `unknown`, `small-localized`,
`standard` or `cross-cutting`. Page/feature lists identify changed outcomes/consumers rather
than all inspected files. Known-impact flags are booleans; genuinely unknown flags can be null.
Unknown impact cannot admit repair or pretend to qualify for Fast. Broad Build obtains actual
Architect advice before final planning/criticism and distinct Architect/Builder/Reviewer identities.

Verification triggers are `multiple-families`, `multiple-environments`, `specialized-measurement`,
`lifecycle`, `substantial-browser-journeys`, `independent-deliverable`. Use real acceptance needs,
not keyword matches. A trigger requires a distinct Verification Engineer's contribution. UI
classification follows [UI routing](ui-routing.md); every applicable task uses full UI expertise.

Each assignment has exactly these fields:

```json
{
  "id": "implement-change",
  "phaseId": "execute",
  "profile": "agents/builder/agent.md",
  "capabilities": ["execute-plan", "fast-build"],
  "independentFrom": [],
  "question": "Correct the scoped behavior in its existing owner and verify the preserved boundary."
}
```

IDs are unique; capabilities are nonempty unique registry IDs compatible with the resolved
family. Resolve a supported legacy profile by selected operation and explicit capability mapping.
Family is derived, not independently duplicated. The operation/write scope remains authoritative.
A capability is knowledge, not authority for extra stages, writes, installation or publication.

`independentFrom` names distinct other selected phases. Include every affected substantive
architecture/design/plan/source/integration phase. A separate bounded corroboration phase inside
a standalone operation does not claim an unrequested numeric stage ran. The primary Reviewer of
GVR/GPR stays Reviewer; the second actual Reviewer/Verifier examines a consequential claim.

For `artifacts/workflow-selection.json`, use the same current `mode`, `routing`, `uiContext`,
`verificationContext`, `delegation`, `reviewPolicy` and `phases`, alongside the catalogue's existing
selection fields/fingerprint. Do not maintain a weaker duplicate staffing definition.
The router's optional `--decision` accepts exactly `mode`, `routing`, `uiContext`, `verificationContext`.
It supplies diagnostic routing/duties, not actual worker evidence or execution admission.

The discovery receipt contains the literal initial query, optional source-refined query, current
index fingerprint, compact matched shortlist, selected IDs with reasons/instruction paths/worker
questions/acceptance criteria, and one selected-or-not-applicable disposition for every specialist
recommended by a selected recipe. It does not require full-catalogue evaluation. Paths and hashes
bind declarations but cannot prove intellectual application; record the specialist's actual effect
in its contribution and have the independent Reviewer inspect it.

New pending records declare the current selection/discovery schemas with an intentionally incomplete
receipt. Before execution admission, the gate rebuilds the authoritative packaged catalogue and
search index, reruns the recorded initial/refined query, and rejects missing, stale or inconsistent
receipts. Discovery is part of the policy/review binding: changing a reconciled query, shortlist or
selection after criticism requires current criticism and briefing bindings again. Read-only catalogue
inspection may still parse a legacy selection, but `--execution` cannot admit it until reconciliation.

## Actual workers and authors

| Field | Meaning |
| --- | --- |
| `roster.coordinatorId` | Actual coordinating identity; never also a worker. |
| `roster.workers` | Actual distinct `id`, `role`, `status: running|completed|failed`, observed spawn/result `evidence`. |
| `roster.assignments` | Exact `{assignmentId, workerId}` bindings only after observed dispatch; one binding per assignment. |
| `roster.plannedWorkers` | Queued `role`/`phaseIds`; contributes zero actual/active workers. |
| `roster.profiles` | Complete bundled profile `name` and actual applying `ownerId`; expertise adds zero agents. |
| `roster.activeAgentCount` | Exactly one coordinator plus currently running workers. Completed/failed workers add zero. |
| `progress.currentPhase` | Actual selected current phase. |
| `progress.phases` | One row per phase: `id`, `status`, `ownerId`, `authorIds`, `evidence`, `workHash`; blocked rows also explain `reason`. |
| `progress.resultRevision` | Null before stable output; then exact current source/artifact revision or manifest hash, separate from plan/work hash. |

An unlaunched future assignment stays unbound. Required assignments can run sequentially with
one free child slot; a previous worker's real completed result is retained. Do not invent actual
IDs or mark completed agents running to satisfy a count. A pending worker can be legitimate at
an earlier gate, but every due assigned operation must actually finish before dependent work.

Track **every substantive author** in each phase's `authorIds`, not just the primary owner.
Adopted architecture/UI/plan decisions and source/test/docs/integration changes include secondary
authors and coordinator authors. Raw factual evidence, ordinary critical comments or unadopted
suggestions do not automatically create downstream authorship. Authoring contributions must match
the recorded authors. Profile changes do not change identity or remove independence constraints.

Phase kinds remain `capture`, `plan`, `critique`, `execute`, `verify`, `report`, `other`.
Scopes remain `read-only`, `record-only`, `test-output-only`, `none`, `repo-write-scoped`,
`tests-only`, `docs-only`, `external-write`. The last four require actual mutation authority;
a record declaration does not grant external permission. Preparation phases cannot write product.
Statuses are `pending`, `in-progress`, `complete`, `blocked`. A completed phase needs current
bound evidence and completed prerequisites. One portable current phase can contain several
workers with disjoint assignments. Mark every actual author as that work occurs.

## Useful contributions and current results

`workflowContract.contributions` contains completed contribution rows:

```json
{
  "id": "builder-result-1",
  "assignmentId": "implement-change",
  "workerId": "actual-returned-worker-identity",
  "kind": "authoring",
  "summary": "The existing owner now implements the requested correction; adjacent behavior was checked.",
  "evidence": ["artifacts/implementation.md", "artifacts/targeted-check.log"],
  "limitations": [],
  "workHash": "CURRENT-REVIEWED-WORK-HASH",
  "artifactRevision": "EXACT-CONTRIBUTION-ARTIFACT-HASH",
  "resultRevision": null,
  "disposition": "incorporated",
  "effect": "Corrected the requested outcome while preserving the identified caller contract."
}
```

Replace example identities/hashes with actual evidence. Kinds are `authoring`, `investigation`,
`independent-review`, `verification`; dispositions are `incorporated`, `rejected`, `unresolved`.
Required `limitations` is a unique list of substantive known limits; `[]` means none are known.
Missing/placeholder limits are invalid. Describing an unmet required criterion does not waive it.
A rejected suggestion can be useful when the concrete reason/effect is recorded; unresolved
in-scope work blocks completion/publication and cannot count as a resolved second contribution.

A completed assigned phase needs a current contribution for every assignment. Incorporated
authoring workers appear in `authorIds`; non-coordinator substantive authors have actual authoring
contributions. Coordinator authorship is explicit but adds zero worker contributions. Status-only
pings, summaries without inspected evidence, failed workers and repeated identities do not count.
Runtime validation rejects structural gaps; substantive usefulness still requires real inspection.

Task completion needs at least **two distinct useful actual workers** and all required assignments
resolved. Broad Build uses distinct Architect/Builder/Reviewer; design Build uses distinct UI
Director/Builder/Reviewer; shared UI uses four; substantial verification adds a distinct Verifier.
Secondary compatible authoring duties may share a worker when these identity and independence
requirements still hold. A worker never needs its own recursive team for an already assigned duty.

Final acceptance and its required substantial-verification contributions bind `resultRevision`
to `progress.resultRevision`; the required Verifier contribution uses `kind: verification`. Required family coverage comes from a completed, resolved
contribution for that family’s actual duty, not an actor’s unrelated earlier contribution or
a future assignment. The separate Verifier must complete the selected prerequisite before
acceptance; later installation readback may remain pending until installation. Changing the
integrated output reopens affected acceptance even with an unchanged plan. A previously returned
contribution is reused only when its work and evidence remain current. Keep author checks and
independent acceptance distinct. Publication waits for exact prepared-result acceptance and due
contributions; future readback assignments run after the external action they inspect.

## Criticism and bindings

A completed `review` has `status: complete`, `decision: ready|revised`, actual `authorId` and
`reviewerId`, truthful `mode`, exact `binding`, concrete `checks`, resolved `findings` (or grounded
`noFindingsRationale`) and real report `evidence`. Its five check areas are exactly **scope,
feasibility, dependencies, verification, preservation**. Each records an actual observation and
sources. Findings have stable IDs, issue, disposition, resolution and evidence. Unfinished or
blocking findings cannot be relabeled ready by metadata changes.

For development records, insert the real criticism in `critique.md`; a pending placeholder or
risk list is insufficient. Preserve reviewed revisions. Reviewer must be independent of every
substantive author in the review subject, including adopted architecture/design/plan and integrated
work. One still-independent Reviewer may critique the plan and later accept the result.

The snapshot's `reviewBinding` covers record identity/kind, plan revision/definition/files,
critique file, declared source baseline, selected operation order/scopes/dependencies, task policy
and **preparation authorship**. Policy includes the canonical registry/instruction fingerprint and
UI/verification facts. `preparationAuthorsHash` includes all adopted plan/architecture/design
authors. Changing these is not a mere roster-display update; reconcile and review affected work.
The final-result revision is separately bound by acceptance and its required substantive verification contributions.

The `briefingBinding` covers current scope, selection, progress, roster, review and work binding.
Refresh after actual phase/worker transitions. Do not repeat substantive criticism merely because
an unchanged worker finished. Checklist hashes normalize real checkbox markers only; changed
wording/source references still invalidate the reviewed plan. Other plan files remain byte-bound.
Keep progress/output evidence in results/artifacts rather than rewriting the approved plan.

Source declarations are not automatic filesystem monitoring. The critic/executor inspect actual
source/diffs and current worker outputs. Helpers do not authenticate a chat message, worker
identity, semantic review quality, undeclared repository changes or tool permission.

## Author, announce and admit

Use the actual installed skill/project/record paths:

```bash
WORKFLOW_SKILL=/absolute/path/to/ai-development-workflow
TASK_PROJECT=/absolute/path/to/project
TASK_RECORD=/absolute/path/to/the/selected/task/record

python3 "$WORKFLOW_SKILL/scripts/workflow_contract.py" template --record "$TASK_RECORD"
```

Template output is pending. Author actual scope, original sources, R/P/T work, current source,
selection, assignments, real roster and explicit authors. A new never-reviewed plan can use
`finalize_plan_record.py --stage planned`; this reports not-ready and does not complete criticism.
A materially revised previously reviewed plan needs fresh criticism, not a reset of its history.

Perform real criticism, resolve findings and write the report. Print current bindings:

```bash
python3 "$WORKFLOW_SKILL/scripts/workflow_contract.py" snapshot --record "$TASK_RECORD"
```

Copy its exact `reviewBinding` into the completed review. Bind actual completed preparation and
contributions to the returned `workHash`; this follows actual work, not retroactive invention.
Snapshot seals appended original request sources in memory while rejecting edits/removals of
preserved sources. It does not approve the record or mutate it.

Generate the complete required public block:

```bash
python3 "$WORKFLOW_SKILL/scripts/workflow_contract.py" briefing-text --record "$TASK_RECORD"
```

**Emit that block through the actual conversation before recording its receipt.** Preserve every
nonblank line/value/order; Markdown blank lines and trailing hard-break spaces are acceptable.
Then set `briefing` to `status: declared`, `kind: portable-declaration`, exact `briefingBinding`,
actual emitted `text`, message `context`, and real `evidence`. A tool print, local draft, flag or
“I told the user” assertion is not delivery. Do not manufacture receipts.

Finalize and separately admit writing:

```bash
python3 "$WORKFLOW_SKILL/scripts/finalize_plan_record.py" \
  --project-root "$TASK_PROJECT" --record "$TASK_RECORD" --stage criticized

python3 "$WORKFLOW_SKILL/scripts/resolve_plan_record.py" \
  --project-root "$TASK_PROJECT" --record "$TASK_RECORD" --execution
```

Finalization always reports `executionAdmitted: false`. With an actual writing selection it
sets readiness ready after valid criticism. The separate execution admission is mandatory.
For record-only Plan/Review, criticized/not-ready means review complete but no authorized product
mutation; do not invent an execute phase. `--require-critique` remains compatibility syntax and
never waives criticism when omitted. Interrupted executing/blocked work uses explicit `--resume`
after real reconciliation; criticized finalization may also need `--resume`. Plain resolution,
catalogue validation, template and snapshot outputs grant no execution authority.

## Completion validation

After actual results, all authors, contributions, limitations, final-result acceptance and the
current user briefing are recorded, validate closure without changing state or granting writes:

```bash
python3 "$WORKFLOW_SKILL/scripts/workflow_contract.py" validate \
  --record "$TASK_RECORD" --completion
```

The read-only completion check requires all non-report work complete, every assigned contribution
current/resolved, required distinct identities and final-result acceptance. It is not an execution
resolver for a completed record. An unchanged status reply reuses valid evidence without a new
record or spawns. Fresh changes reopen the relevant work and obtain current admission.

## Compact G0

Use the same shared v2 team/authorship/contribution fields in the existing quick directory.
Print a pending shape with `template --kind quick --record "$TASK_RECORD" --workflow G0`.
Add positive `planRevision`, scope, declared source baseline and a compact plan:

```json
{
  "steps": [{"id": "P1", "change": "Actual scoped correction", "paths": ["actual/file.ext"], "dependsOn": []}],
  "checks": [{"id": "T1", "steps": ["P1"], "method": "Decisive check", "expected": "Requested result", "boundary": "What it establishes"}]
}
```

Every step needs a check. Existing source-to-checklist traceability remains. Snapshot/briefing
and validation commands use `--kind quick`; criticism is inline. Two distinct useful contributors,
all-author independence and current result acceptance still apply. No development finalizer or
second GB record is needed. Actual execution admission remains:

```bash
python3 "$WORKFLOW_SKILL/commands/quick-task/scripts/audit_task_record.py" "$TASK_RECORD" --execution
```

Without `--execution`, that audit is traceability-only. A failed gate leaves permitted preparation
available; it is not a request for another routine user-approval ceremony.
