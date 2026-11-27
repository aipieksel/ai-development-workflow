# Public modes

AI Development Workflow exposes one main skill with five public controls: Auto selects one
of four concrete execution modes, Plan, Build, Review or Loop. Every new task needs at least two useful contributions from distinct actual workers, excluding the coordinator,
under [task routing](task-routing.md); tiny tasks and explicit advanced controls have no solo
exemption. These controls share the
[workflow contract](workflow-contract.md), the same task evidence and the same scope/review
gates. The mode chooses the job to perform; it does not grant tools or external permissions.

## Invoke the skill

In ChatGPT, type `@`, begin typing `AI`, wait for autocomplete, and select the installed
**AI Development Workflow** entry. Then write the mode and task. The examples below show
the selected skill as `@ai-development-workflow`; typing that text without selecting an
installed autocomplete entry does not by itself attach the plugin.

```text
@ai-development-workflow auto Fix the reported save error and verify the existing flow.
@ai-development-workflow plan Plan the migration and criticize the plan before any code changes.
@ai-development-workflow build Implement the adopted migration plan and verify it.
@ai-development-workflow review Compare this page with the supplied original and report every gap.
@ai-development-workflow loop Compare the original and current work, repair the findings, and repeat independent review.
```

An attached skill plus ordinary prose defaults to Auto. A compatible local host may select
the skill with `$ai-development-workflow`. The bundled explicit router accepts the canonical
`/ai-development-workflow` prefix and bare explicit mode controls through `--text`. These
are parsing interfaces, not a promise that every host registers slash commands or autocomplete.

## Mode contracts

| Mode | Phase sequence | Product write scope | Completion |
| --- | --- | --- | --- |
| `auto` | Establish intent/impact → select and announce Plan, Build, Review or Loop → assign actual workers → follow that mode | Determined by the actual request and resolved mode | The requested outcome, with observed evidence and remaining limits; unresolved Auto cannot admit execution |
| `plan` | Capture or reuse record → investigate relevant source → plan → criticize/revise | `record-only` | A source-grounded plan and completed criticism; no product implementation |
| `build` | Capture or reuse record → plan/reconcile → criticize/revise → admit → implement → verify | `repo-write-scoped`, narrowed by the request | Authorized changes and decisive verification |
| `review` | Define scope/reference → critically plan inspection → inspect current work → report | `record-only`; authorized non-mutating checks may produce evidence | Findings, coverage and limitations; no silent repairs |
| `loop` | Independent review → checklist/plan → reviewer confirmation → execution → fresh independent review; repeat as needed | `repo-write-scoped` for the executor only | Current-revision reviewer acceptance or an explicit resumable blocker |

### Auto

Use [automatic selection](automatic-selection.md) and the shared [routing rules](task-routing.md)
to determine the concrete mode, actual outcome, scope, inspected impact and required real
assignments. Known localized Build work uses GB/Ponytail and Fast Engineer. Broad/shared
effects require Architect advice before the final plan; uncertain impact requires investigation.
Load the relevant handler/profile dependencies progressively.
Do not force every task through G1, a complete build chain, or every catalogue entry.
Research, review, planning and bounded corrections stay proportional. Selected read-only
operations do not gain repair authority from Auto. An explicit G code is an advanced choice,
not a competing public mode.

### Plan

Reuse the selected compatible record, or capture a fresh task once through the existing
record allocator. The user does not need to know a numeric creation code. Inspect enough
source to identify owners, dependencies, protected behavior and decisive checks. Write the
implementation/test plan through the actual planning worker, then actually criticize it and
resolve findings. If criticism is
blocked or incomplete, say so; do not report the Plan mode complete or execution ready.

Finalize the completed criticism with the existing record helper. A valid record-only plan
finishes as `criticized` with `reviewValidated: true`, `readiness: not_ready` and
`executionAdmitted: false`. The readiness value concerns product execution; it does not
mean the criticism is unfinished. Do not invent an execute phase to finish Plan mode.

Use an actual Architect/Planner and a distinct Reviewer. The Reviewer examines the resulting plan and evidence; a coordinator approach self-check cannot replace this contribution. Track all adopted plan/architecture/design authors and exclude them from independent criticism. Keep implementation
unauthorized until the user requests it. A reviewed plan is reusable evidence, not permission
to begin Build. A later Build request can reuse its current criticism after reconciliation.

This primary `plan` mode differs from advanced numeric `1` and planning starters `01`,
GPL and GCP. Those retain their narrower historical phase semantics; see the
[advanced reference](advanced-reference.md#numeric-controls-and-continuation).

### Build

Build expresses implementation intent within the user's stated scope. Reuse an exact
current reviewed plan when available; otherwise complete capture, planning and criticism.
Disclose missing prerequisites and satisfy them before product, test or project-documentation
writes. Apply the real record admission helper; a route descriptor is not admission.

The actual execution specialist performs the work and verifies acceptance criteria. A distinct
real critic reviews the concrete plan before writes, and independent result review precedes
completion. The coordinator reconciles
every requirement. Disjoint assignments may run concurrently when useful; overlapping source,
generation and packaging have one owner. Independent reviewers stay read-only. Build does not
automatically publish, deploy, send messages, install missing services or change permissions.

### Review

Review is an inspection of the specified existing work, its requirements and available
references. Prepare and critically check the inspection approach first: source identity,
coverage, expected behavior, useful tools, and what the evidence can establish. Then examine
actual files, changes, artifacts or available page/document behavior. For a visual comparison,
inspect the original and current result under equivalent relevant conditions.

Assign at least two distinct actual contributors. Investigation uses Investigator plus Reviewer; check-only uses Verification Engineer plus Reviewer. Standalone Reviewer-led work retains its primary Reviewer and receives a different Reviewer or Verifier for a bounded consequential countercheck. Inspect real evidence and combine the findings without repairs or unselected formal stages. Coordinator self-checks and profile names do not replace either contribution.

Choose current-work operations such as code review, UI review, accessibility, security,
documentation verification or tests according to scope. Inspect real input artifacts. Do not
invent `implementation` or `execution.result` evidence merely to unlock an atomic G command
whose prerequisite the task never produced. An artifact path, screenshot or prior agent claim
is evidence to investigate, not a passing review.

Report stable finding IDs, source/requirement, affected target, evidence, severity/impact,
suggested scoped correction and acceptance check. Distinguish confirmed defects, permitted
differences, optional suggestions and unverified coverage. Do not edit the reviewed product,
tests, configuration or documentation. Later authorized Build or Loop can consume the findings.

### Loop

Read [Loop — Execute and Review](loop-mode.md), its [artifact contract](loop-artifacts.md)
and [monitoring protocol](loop-timers.md). The manager coordinates and reconciles checklist
accounting. A real reviewer inspects originals and results, confirms the derived repair plan
and decides acceptance. A real executor implements the admitted checklist. A fresh reviewer
with a new identity checks each completed round. A clean initial review receives separate Verification Engineer corroboration and the original Reviewer’s acknowledgement before acceptance, without an empty repair pass. Keep dependent phases sequential.

Monitor the active worker every **300 seconds**. A suitable worker/mailbox wait is preferred;
a real host timer is the fallback. A saved deadline or local helper does not schedule a wake.
If neither is available, report active-session monitoring limits. Missing independent-worker
support blocks the independent loop; useful preparation may continue, but manager role-play
cannot replace it. `XR` remains an invocation alias. Legacy `xr-*` schemas and checkpoint
paths remain unchanged so earlier evidence and hash chains can be read truthfully.

## Explicit controls, literal prose and help

```bash
python3 scripts/route_workflow.py --text 'plan Criticize a migration plan without changing code.'
python3 scripts/route_workflow.py --text '/ai-development-workflow build Implement the reviewed change.'
python3 scripts/route_workflow.py --task 'Plan only: explain the options for this save flow.'
```

Use `--task` for an attached skill's ordinary task body. It preserves literal text such as
“Go through these files”, “3 columns” and “Plan only” as prose; semantic scope still governs
the selected work. Use `--text` only when the caller has identified an explicit control.
Router output describes the route; it does not execute phases or launch workers.

`menu` and `--menu` request a small ordinary help response containing the five primary modes
and a link to advanced documentation. The package supplies no editor popup, model picker,
native queue or custom ChatGPT UI. Native `stage <id>` and `pipeline <id>` selectors are
retired; report that boundary rather than falling through to a write-capable route.

## Continuation and conflicts

Continue the same record and reconcile the latest request, source, worker status and evidence.
Retain the selected mode when it is still applicable; a planning-only continuation stays
planning-only. A new explicit implementation request can move the same work into Build or
Loop after current review. Corrections reopen affected outcomes and preserve prior history.

Current explicit boundaries prevail. A conflicting request such as “loop, but do not change
anything” needs its intent resolved; never use the mode name to erase the boundary. Ask only
for a material unresolved decision or missing source that available context cannot supply.
