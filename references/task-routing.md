# Concrete modes, six families and useful teams

Apply this shared policy to Auto, explicit modes, every G/numeric control, recipe, quick task
and continuation, with the [workflow contract](workflow-contract.md). The
[registry](../agents/registry.json) owns family/capability/legacy mappings; the
[runtime policy](../scripts/task_policy.py) validates declared decisions. The host supplies
source-grounded judgment, real dispatch and inspected results.

## Select a concrete mode

Exactly five public controls remain: **auto**, **plan**, **build**, **review**, **loop**. Auto
selects one of the other four. Explicit advanced controls retain their requested phases,
inputs, record semantics and write boundaries while resolving a concrete mode.

| Intent | Mode | Boundary |
| --- | --- | --- |
| Produce or revise a plan/specification | Plan | Planning and independent criticism; stop before product edits. |
| Implement, fix, refactor, author tests or change project docs/artifacts | Build | Exact plan criticism, admission, implementation and independent acceptance. |
| Research, diagnose, assess, audit, compare or check existing work | Review | Evidence and findings; no silent repair. |
| Repeated independent review and repair until acceptance | Loop | Existing manager/executor/fresh-review cycle with five-minute monitoring. |

Investigation can be a read-only phase inside authorized Build. A finding does not authorize
repair. Preserve audit-only, Plan-only, mockup-first and no-publish limits. Do not ask the user
to select internal roles when the request and source establish the answer.

## Delegate useful work every time

Every new logical task returns contributions from **at least two distinct actual workers**,
excluding coordinator. Tiny, Plan, Review, research, verification and standalone commands have
no single-worker exemption. A role path, `agentCalls` row, planned identity, status ping,
failed dispatch, second profile on one actor or repeated summary without independent inspection
does not count. A short source-grounded no-findings report can count; finding a defect is not a quota.

The primary worker does useful work. A different worker supplies a specific independent check,
challenge or corroboration. Writing tasks have independent current plan criticism before edits
and acceptance after the stable integrated result. Plan/Review tasks obtain the second useful
contribution before reporting completion without inventing implementation or a formal stage.

Pass the original requirements/corrections, source baseline, selected record, bounded question,
allowed paths/operations, selected capability instructions, output destination and decisive checks.
Combine relevant domain lenses on actual workers; do not launch a worker for every keyword.

## Six canonical families

| Family | Owns | Scope boundary |
| --- | --- | --- |
| [Investigator](../agents/investigator/agent.md) | Research, assessment, diagnosis, behavior/invariants, contribution discovery | Source/evidence work, no automatic repair. |
| [Architect and Planner](../agents/architect/agent.md) | Architecture, goal/code/test planning, dependencies and migration order | Advice and planning. |
| [Builder](../agents/builder/agent.md) | Admitted implementation, Fast/Ponytail, TDD, cleanup, docs and delivery preparation | Only assigned product/test/docs paths; no self-acceptance. |
| [UI Director](../agents/ui-design-director/agent.md) | Actual reference inventory, UI audit/specification, visual/interaction direction | Design/advice, no competing implementation owner. |
| [Reviewer](../agents/reviewer/agent.md) | Independent plan criticism, source/outcome review, completeness and acceptance | Read-only review, independent of substantive authors. |
| [Verification Engineer](../agents/verification-engineer/agent.md) | Actual tests, browser journeys, accessibility, security, performance and lifecycle checks | Check outputs only; no fixes or weakened tests. |

Thirty-eight original role paths resolve through the registry to these families and required
capabilities. The two reused core paths plus 36 compatibility entries remain meaningful and
nonempty. They are not 38 active agents. The 21 domain lenses remain reusable knowledge.
Resolve **profile plus selected operation**, not profile name alone. GCA/GEA writes are Builder
work; review-only and check-only operations stay read-only. GJ test authoring, GTF RED-only,
GTE GREEN/refactor, GVD docs-only and GPP planning retain their distinct boundaries.

## Select the route from inspected impact

Before final routing, search the packaged task index provisionally from the literal request,
inspect project/source evidence, and refine the query when ownership, stack or affected surfaces
were initially unknown. Inspect the grouped shortlist; retrieval is candidate-only.

1. Resolve intent before speed. A quick inspection stays Plan or Review.
2. Investigate unknown cause, ownership or affected consumers before classifying/admitting repair.
3. Broad changes—multiple affected pages/features, changed shared contracts or architectural/
   migration decisions—require Architect advice before the finalized plan and criticism.
   A one-line shared setting can require this; source file count is not impact.
4. Known bounded localized Build uses [GB/Fast/Ponytail](../agents/fast-engineer/commands/ai-dev-fast-build.md),
   with Builder's complete `fast-build` capability plus independent Reviewer. Fast reduces
   repeated reading/work, never contributors or gates.
5. Preserve explicit controls. G0 remains compact; applying Fast there does not allocate a
   second GB record. Explicit GB/G0/G1 cannot waive broad-impact advice or independent review.
6. Select UI and substantial-verification duties from inspected outcomes and exact acceptance.
   Do not guess these facts from keyword lists or report a descriptor as real dispatch.

## Which roles to assign

Counts below exclude coordinator and describe contributors over the task, not simultaneous slots.

| Task | Required team | Expansion and preserved scope |
| --- | --- | --- |
| Small known localized Build | Fast Builder + Reviewer | Existing GB route; compact G0 stays compact. |
| Plan only | Architect/Planner + Reviewer | Add Investigator for unresolved facts or UI Director for material design. No build. |
| Research, assessment or diagnosis only | Investigator + Reviewer | Independently check a consequential claim, omission or counterexample. |
| Standalone code/plan/spec review, including GVR/GPR | Primary Reviewer + different Reviewer or Verifier | Verifier checks an executable/rendered claim; otherwise second Reviewer checks a bounded claim. Preserve primary owner and selected operation. |
| Check-only work | Verification Engineer + Reviewer | Independently check coverage and interpretation; no repairs. |
| Unknown impact inside authorized repair | Investigator first, then Builder + Reviewer | Reuse compatible investigation/execution identity where useful; add Architect if broad impact emerges. |
| Shared/multiple-page/feature or architectural Build | Distinct Architect + Builder + Reviewer | Advice before finalized plan/criticism. Track secondary authors too. |
| Mechanical local UI label/token/component application | Fast Builder with full UI expertise + UI-aware Reviewer | Existing approved design, actual rendered check. |
| New layout/palette/type/responsive/interaction design or reconstruction | Distinct UI Director + Builder + Reviewer | Actual design/state brief before accepted planning. UI Plan/Review adds no Builder. |
| Shared UI/design-system Build | Distinct Architect + UI Director + Builder + Reviewer | Shared-consumer and visual contracts; use sequential waves. |
| Substantial validation | Add distinct Verification Engineer | Multiple check families/environments, specialized measurement, lifecycle, substantial browser journeys, or explicit independent verification. |
| Documentation/package work | Builder with relevant capability + Reviewer | Add Verifier for installation/runtime/lifecycle claims. Publication follows accepted output. |

Extra Builders need nonoverlapping ownership or isolated checkouts and one integrator. A second
Reviewer must examine actual evidence, not merely endorse the first. Do not manufacture findings,
repairs or wider scope to justify workers. Use the complete [UI applicability](ui-routing.md)
and [domain specialist](specialist-contract.md) instructions where relevant.

## Independence, contribution and synthesis

Independence follows actual identity and all substantive authorship. Adopted architecture,
UI specifications and plans cannot be independently criticized by their authors. Source, test,
docs and integration authors cannot accept the resulting work. Include secondary contributors;
changing a role label does not remove authorship. Ordinary criticism/raw factual collection
is not automatically adopted solution authorship. A Reviewer that writes the solution becomes
an author and needs another acceptor. One independent Reviewer may critique and later accept.

Maintain the normal task's compact ledger, with each actual assignment/worker, concrete result,
inspected evidence, limitations, current work/artifact/result revision, disposition and effect.
Use `incorporated`, `rejected` with a reason, or `unresolved`; unresolved in-scope work blocks
completion. Empty limitations means no known material limit, not unexamined coverage.
The coordinator reconciles evidence into one result. Disagreement is resolved through sources
and the responsible owner/reviewer, not majority voting or several competing final answers.

Acceptance covers the stable integrated output. A changed output revision reopens affected
acceptance even when the plan remains valid. Author-run checks are useful evidence and remain
separate from independent acceptance. No publication before required current contributions and
acceptance; post-install readback naturally follows the installation it checks.

## Capacity and continuation

Two useful contributors need not run concurrently. If one child slot is available, complete A,
release it and dispatch different B. Report required contributors, useful returned contributors
and active agents separately. Active count is coordinator plus workers actually running;
completed/failed/queued workers add zero. Preserve real spawn/result receipts. Missing dispatch
blocks dependent work, with permitted preparation and an honest checkpoint.

Assigned children perform their bounded duty without recursively creating teams. Reuse valid
completed evidence for unchanged continuation/status. Changed scope, source/result, adopted
choices or stale contributions reopen affected work. Do not start new tasks for status questions.

New executable records use [contract-v2](workflow-contract-records.md). Preserve archived v1
bytes; actively resumed records reconcile canonical aliases, actual IDs, all authors and missing
contributions explicitly. Do not silently rehash old criticism or promote old single-worker work.

Loop keeps manager-only accounting, sole repair executor and fresh Reviewer after each execution.
A clean initial review requires independent Verifier corroboration and original Reviewer
acknowledgement before acceptance, without an empty executor pass. Preserve the five-minute
wait-first/timer-second protocol and supported user/browser control.

Portable helpers check declarations, structure and revision bindings. They cannot authenticate
workers, judge all prose quality, inspect undeclared source drift or intercept arbitrary host tools.
Actual dispatch, meaningful work and substantive independent checking remain required host actions.

## Countercheck timing

For Review, research and check-only completion, the second worker examines the primary
inspection’s actual result after that result exists. A critique of the coordinator’s approach
before inspection cannot replace the result countercheck. Plan may use criticism of the
completed actual plan. This is a bounded duty inside the selected operation, not new write
authority or a claim that an unselected numeric stage ran.
