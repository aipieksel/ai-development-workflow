# Change Request Traceability

Prevent requirements from disappearing between a user's request and implementation. Preserve the source request first, make every action traceable to it, and keep the durable and visible checklists synchronized through completion.

## Internal reference

For visual outcomes, follow [UI applicability](../../references/ui-routing.md) and read the
[UI Design Director](../../specialists/ui-design.md). Pass the complete profile to this quick
task's actual assigned worker and retain its existing checklist. Keep a local correction proportional, preserve approved properties and perform
the relevant rendered check; do not replace G0 with a larger pipeline.

Use this bundled workflow for G0/GO and the Quick Task entry, not as a separate skill.
Every quick task follows [task routing](../../references/task-routing.md): announce a
concrete mode and dispatch a real worker. Read-only requests need a short visible
operation plan and criticism plus a meaningful specialist inspection; they do not create
a write-task record or authorize implementation. Resolve scripts and references relative to
the directory containing this file. Do not look up a globally installed task-checklist.

## Visible checklist contract

`checklist.md` is the durable source of truth. Show its initial state before implementation,
then additions, meaningful text/status changes and the final verified state in ordinary
Markdown. Use stable R IDs and preserve source links. A supported host checklist tool may
mirror the same work through its documented schema and actual acknowledgment.

Read [checklist presentation](references/checklist-ui-surfaces.md) for stable IDs, local
payload conversion and actual host boundaries. The bundled `scripts/checklist_payload.py`
requires Python 3.10+ and prints generic JSON; it does not publish a panel.

- A missing or failed optional mirror means the complete Markdown list remains the visible
  surface. Never substitute a promise, item count or file link for the actual checklist.
- Keep at most one item in progress. Mark complete only after the work and required checks
  passed and the durable checkbox reflects that evidence.
- Update the durable file first and the visible state in the same work interval. Preserve
  stable list/item IDs, unresolved items and reasons throughout amendments and final handoff.

## Context-only invocation mode

When G0/GO or the Quick Task entry is invoked with no substantive instructions in
the same message, treat that invocation as a control command. It selects this
workflow; it is not the subject of the request record or checklist.

1. Find the most recent point where the agent completed a task and gave its
   completion handoff. Use that handoff as the boundary anchor, then collect
   every related user and assistant message from that point through the bare
   invocation. Include the immediately preceding explanation, the user message
   it answered, earlier related corrections and follow-ups, and directly
   referenced issue artifacts needed to preserve the complete context.
2. Exclude the bare skill invocation from the semantic task scope. Record it
   only as evidence that the user requested this workflow.
3. Create the same extensive source record that would have been created if the
   user had pasted that issue corpus alongside the invocation. Preserve all
   concrete defects, symptoms, affected surfaces, missing behavior, unresolved
   questions, proposed corrections, constraints, examples, acceptance criteria,
   and verification expectations.
4. If the source-corpus boundary, intended outcome, repository, record path, or
   any requirement is uncertain, stop and ask the user. This is a hard gate:
   do not infer, silently choose, or convert uncertainty into an assumption.
   Do not invent optional scope, responsive targets, implementation choices, or
   "helpful" interpretations. Do not create artificial ambiguity when the
   source already states an operationally complete requirement.
5. Do not cross into an older completed task or unrelated conversation. If the
   last completion boundary, relationship of intervening messages, or existence
   of an unresolved issue is uncertain, ask the user before creating the record.
   If there is no issue-bearing conversation after the completion handoff, ask
   what should be converted into a checklist.

### Checklist semantic target

Derive the primary checklist from the underlying issues in the source corpus,
not from the latest meta-request to document, summarize, or create a checklist.

- Give every underlying defect, missing behavior, requested correction,
  unresolved question requiring investigation, constraint, acceptance
  criterion, and verification need one or more explicit checklist items.
- Do not substitute meta-work such as "document the request", "create the
  checklist", "inspect the source", or "report the document path" for the
  underlying remediation work.
- Add necessary preparation, source preservation, documentation, and reporting
  items only as secondary workflow items after the complete issue-remediation
  checklist. Clearly label agent-added necessities.
- Before implementation, perform this semantic self-check: if every checkbox
  could be completed while the underlying defects remain unfixed or the
  underlying questions remain unresolved, reject and rebuild the checklist.

Read `references/context-only-invocation.md` when this mode is triggered. It
contains the issue-corpus selection procedure and a regression example based on
the demonstrated Page Audit failure.

## Record the request before implementation

1. Perform only the minimal read-only inspection needed to identify the workspace root and record location. Do not begin implementation or make another state-changing change.
2. Store every new record under `<workspace-root>/docs/tasks/checklist/<five-digit-id>-<YYYY-MM-DD>-<short-slug>/`. Never create task-checklist records under `.codex`, and do not silently use a hidden or alternate fallback. If the workspace root or confirmed docs location is unavailable or unwritable, ask the user and wait.
3. Allocate the directory with `scripts/next_task_record.py <workspace-root> <short-slug>`. The helper scans existing record directories, uses `00001` when none exist, otherwise uses the highest numeric ID plus one, zero-pads to at least five digits, uses the current local date, creates the directory atomically, and refuses collisions. Do not calculate or create a competing ID by hand when the helper is available.
4. In `request.md`, create a `Goal` section and a `Source instructions` section containing the complete change request verbatim. Include any earlier user-supplied content that the request incorporates by reference, such as “this,” “that,” or “it.” In context-only invocation mode, preserve the complete multi-message issue corpus selected by that mode, not merely the bare invocation or final message.
5. Split the source at natural boundaries into clear topical sections with stable identifiers such as `S1` and `S1.1`. Do not paraphrase, summarize, condense, silently correct, merge, weaken, omit, replace, or reorder the user's wording. Preserve repetition, emphasis, examples, constraints, acceptance criteria, and intent.
6. Do not add an unconfirmed interpretation, assumption, inferred scope, or suggested requirement. When one is genuinely required to continue, ask the user and wait. After the user answers, record the confirmed decision in a separately labelled `User-confirmed clarifications` section and trace it like any other source instruction. Agent-added implementation necessities are allowed only when they do not choose product behavior or expand scope, and must be labelled as such.
7. Add a `Coverage map` accounting for every part of the source request by stable section/item ID. Leave no source instruction unaccounted for. Cover parent and nested instructions. Heading-only groups need no extra task. For non-actionable context, use `- S2: context-only — <reason>`; never exempt requested work.
8. After creating `checklist.md`, keep `request.md` append-only. If the user adds or corrects instructions, append a dated addendum with new stable IDs and update the coverage map and checklist before continuing implementation.

## Build the line-referenced checklist

Create `checklist.md` only after `request.md` is complete.

- Convert every actionable source item into one or more explicit Markdown checkboxes.
- Include every actionable item in user-supplied bullets, numbered lists, nested
  lists, and checklists, including later messages; preserve non-actionable
  context in the source record and coverage map.
- Prefix each checkbox label with a unique stable ID such as `R1`, `R2`.
  Preserve IDs across renames, reordering, and status changes; append new IDs
  without renumbering existing items. Give older anonymous items IDs once before
  their first publication. R IDs identify tasks; S IDs still identify sources.
- Use `[ ]` for pending, `[~]` for in progress, `[x]` for verified completion,
  and `[!]` for blocked. In-progress and blocked items are still unfinished.
- Do not combine items when doing so could hide a requirement, constraint, example, verification condition, deliverable, or dependency.
- End every checkbox with the exact `request.md` section/item IDs and physical line range that requires it, for example `(source: request.md S2.1, lines 18-22)`.
- Include preparation, implementation, verification, and delivery/reporting items when the source requires them. Give each acceptance criterion or requested verification its own checkbox.
- Preserve the user's stated or implied order. Record dependencies explicitly.
- Check bidirectional coverage: every source item must appear in at least one checklist reference, and every checklist item must trace to the source or be labelled as an agent-added implementation necessity.

## Surface the checklist before implementation

1. Tell the user that `request.md` and `checklist.md` are ready, provide both paths, and say
   planning/criticism is in progress. Do not announce implementation until admission passes.
2. Publish the checklist using the visible checklist contract before implementation.
3. After acknowledged publication, direct the user to the Tasks panel. Otherwise
   explain that the panel was not updated and paste the complete Markdown
   checklist before implementation.

## Compact plan, criticism and admission

Read the [mandatory workflow contract](../../references/workflow-contract.md) and
[contract records](../../references/workflow-contract-records.md). In the selected quick task record,
add <task-record-dir>/workflow-contract.json with scope, compact concrete plan/checks, exact request/checklist
bindings, completed criticism and a declared public briefing. The template starts pending.
For writes, assign a real independent plan critic before admission, a real execution
specialist and independent result review before completion, even for one-line changes.
Use Builder with `fast-build` for a known local write; obtain Architect advice first for broad/shared
impact. Preserve this compact record throughout. Every new logical task, including read-only work,
needs useful contributions from at least two distinct actual workers excluding the coordinator.
Read-only inspection uses a primary specialist and a distinct critic/corroborator within the
selected scope. A coordinator approach self-check does not count as either contribution.
Record findings, evidence, limitations, disposition and effect on the combined result. Track all
substantive authors and exclude them from independent acceptance. Show required/returned
contributors separately from the actual active-worker count.

Before any product write, emit the current scope/workflow, ordered phases/owners, status and
numeric running-agent count, then record that actual briefing. Run:

```bash
python3 <quick-task-directory>/scripts/audit_task_record.py <task-record-dir> --execution
```

Only passing execution admission permits the already authorized changes. A plain audit,
checklist publication or pending criticism is insufficient. On continuation reconcile actual
source and evidence, refresh stale criticism/briefing, then pass the same gate.

## Keep execution traceable

- Keep `checklist.md` and the visible checklist synchronized throughout the task.
- Add newly discovered necessities without deleting original items or losing source references, and clearly label agent-added necessities.
- Do not declare the task complete while an item is incomplete, skipped, unverified, or untraceable.
- Report blockers and explicitly identify every unchecked item.
- At final handoff, publish the final verified state so checked-off items and
  remaining work are visible. On unavailable or failed publication, show the
  actual Markdown checklist with its current markers and explain the failure.

## Traceability inspection helper

When you create or update a task record and local shell execution is available,
run the audit helper before final delivery:

```bash
python3 '<checklist-reference-dir>/scripts/audit_task_record.py' '<task-record-dir>'
```

Without --execution this is inspection only, not permission to mutate. The helper checks
files, IDs, section/line references and coverage using the
publisher's checklist parser. It reports progress counts, not proof of semantic
correctness or passed tests.
