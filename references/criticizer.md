# Project Development Plan Criticizer

Apply the [mandatory workflow contract](workflow-contract.md) and [admission metadata](workflow-contract-records.md). Record real author/reviewer identities, self versus independent criticism, completed checks, findings/dispositions and exact review bindings. Pending placeholders and outcome flags are insufficient.

Under [task routing](task-routing.md), every product/test/docs change has an actual independent
critic, including G0/G1/GB. Confirm the concrete mode, source-grounded impact, required actual
assignments and completed pre-plan Architect advice when broad/shared effects apply. A read-only
approach self-check does not replace either of its two useful actual contributors or a selected independent review. Check every substantive author, including secondary contributions and adopted advice, rather than only the primary owner.

Critique and revise the selected task record only. Do not fix application code. Preserve the original goal, previous findings, executed evidence and current user authorization.

When explicitly requested with planner/executor, run after planning and before execution, passing the same record path without another process question. Do not start other task/planning workflows.

Apply the selected command’s hooks from its command file; see [shared execution](command-runtime.md).

## Workflow

1. Read record-contract.md and select the exact supplied or preceding record. Always pass the conversation-selected record explicitly to resolve_plan_record.py --project-root <ROOT> --record <RECORD>. Multiple active records require context-based resolution or one concise question, not newest-record guessing.
2. Read all six files, applicable project instructions, relevant source/diff and supporting evidence. A plan's assertions are not source proof. For partially implemented work, inspect actual changes; do not infer success from checked boxes.
   Read the selected sources for this review and relevant retained constraints; independently reconcile in-scope issues against their checkpoints and specific tests. A parent R/P/T match is insufficient when a child commitment has no decisive assertion. Restore omitted checkpoints before admitting execution; copying the whole transcript alone does not establish coverage.
3. Check scope before completeness: first derive the authorized outcomes and constraints from the actual selected conversation, without adopting the plan's requested/necessary labels. Apply the contract's behavioral scope review to every R/P/T change, including added clauses and effects around unchanged components or data. Identify its supporting phrase or test its necessity against evidence and a narrower solution. A whole-message citation, existing R ID or claimed safeguard is not a scope finding. Remove unwarranted additions and restore lost constraints before improving the design. Then investigate source-backed diagnosis, paths, dependencies, conventions, permissions, sequencing/recovery and decisive verification.
   Also check for under-delivery: an older planning-only instruction must not cancel a later authorized stage 3. Reject changing implementation outcomes into "specify/document future work" unless that is the user's current deliverable. Verify the stages/deliverable/completion evidence in fix-plan.md against the chronological request and any clarification that continued the invocation. Scope protection must not become a reason to remove authorized implementation.
4. Append findings in critique.md with stable F ID, severity, source/requirement, concrete defect and likely impact, affected R/P/T section, smallest correction and disposition: fixed_in_plan, rejected_with_reason or unresolved. Substantiate the review with the concrete material behavior changes and their authority, reusing the plan's scope delta where accurate. A blanket "no additions" or "all requirements trace to S1" is insufficient. Resolve conflicts between the narrative, source, plan, diff and results; a ready flag or successful helper cannot override missing or contradictory review evidence. “Fixed in plan” never means application code fixed.
5. Correct checklist.md, fix-plan.md, test-plan.md and metadata mappings, never the preserved source text. Update the short scope delta in fix-plan.md and report added/removed behavior in critique.md (or explicitly none). Each accepted addition must trace to user authority or an evidenced necessary detail. Record rejected/optional findings outside executable mappings; do not let optional work block the original task. Preserve historical findings and dated review rounds. Removing an unrequested expansion or fixing an in-scope defect needs no new approval. If a necessary correction would materially expand authorized scope, keep that decision blocked pending the user; do not silently accept it.
6. Increment planRevision for substantive plan changes. Record critiqueOutcome ready (no material revision), revised (corrections incorporated), or blocked. Set reviewedPlanRevision to the actual reviewed revision only after the final cross-check.
7. Recheck original source → R → P → T in both directions, including unchanged behavior and deferred phases. Account for all material added effects, not just validation or approval mechanisms; check that the critic's own corrections also pass the same scope review. Claims about unchanged files do not settle behavioral scope. For ready/revised, finalize with --stage criticized only after completing the substantive review; pending text, unsupported declarations and unresolved contradictions cannot be finalized as reviewed. For unresolved blockers, retain them and set status criticized, readiness blocked, critiqueOutcome blocked.
   Reconcile every relevant itemized conversation finding with its checklist checkpoint and disposition. An omitted item, a misleadingly merged item, or an optional suggestion silently promoted into executable work is a scope defect even when all existing R/P/T references are valid.
   Explicitly reconcile the user's bullets, numbered items, checkboxes and nested children under the record contract's user-list coverage check, including items in the invocation itself. When corrections change the checklist, publish the updated Tasks panel if available and acknowledged; otherwise show the updated Markdown checklist in a progress message. Preserve its actual verification state.
8. If work was executing, do not race an active executor. Coordinate/confirm it has stopped before changing the record. Preserve results and reconcile changed checklist evidence; do not mark unexecuted revised steps complete.

## Review discipline

Prioritise scope, reuse, tests that can detect failure and unsafe side effects.
Scale depth to risk; preferences and hypothetical future improvements are nonblocking.
After material changes, re-review affected findings rather than reopening settled work
without evidence. Keep one critique.md; no numeric self-confidence gate or new approval
ceremony. Self-critique is not independent review.

## Completion

Report concrete findings and corrections, rejected points, unresolved blockers, exact record path, and whether the revised plan passes the execution gate. Include or publish the revised checklist when changed; plan corrections do not mark implementation outcomes complete. Do not execute it unless the user also requested execution.

## Contract and tooling

Read record-contract.md before operating. The helper validates metadata, files, mappings, dependencies and readiness hashes; it cannot establish factual correctness or permission. Follow applicable project policy and the current user's scope. Use the authorized available browser only for browser-visible claims; an unavailable preferred browser does not justify claiming visual verification.
