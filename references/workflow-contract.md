# Mandatory workflow contract

Apply this contract to **every invocation**: automatic selection, explicit G/numeric commands,
public modes, named advanced handlers, quick tasks, recipes, internal operations, corrections and continuation.
It governs all roles and takes precedence over older plugin wording that permits omitted
planning, criticism, real delegation or announcements. Apply the authoritative
[task routing policy](task-routing.md): every task resolves Plan, Build, Review or Loop and
requires useful contributions from at least two distinct actual workers, excluding coordinator. Auto is the selector. A selected command retains its requested outcome
and write scope; it cannot waive these prerequisites. Do not ask the user to repeat this contract.

## Contents

- [Open with the actual contract](#open-with-the-actual-contract)
- [Plan and criticize before work](#plan-and-criticize-before-work)
- [Admit product changes](#admit-product-changes)
- [Report phases and real agents](#report-phases-and-real-agents)
- [Reuse and invalidate evidence](#reuse-and-invalidate-evidence)
- [Recover truthfully](#recover-truthfully)
- [Enforcement boundary](#enforcement-boundary)

## Open with the actual contract

Before substantive task work, send the user a concise visible brief containing:

1. **Scope:** requested outcome, intended deliverable and important boundaries/protected behavior.
2. **Selection:** concrete mode, chosen workflow/recipe or composed chain, inspected impact
   and the reason the required roles fit. Auto must report the concrete mode it selected.
3. **Phases:** numbered, ordered phases with actual statuses and the current phase.
4. **Owners:** actual or planned worker assignment for each task phase; distinguish any
   coordinator self-check of a read-only approach from required independent criticism.
5. **Agents:** required/returned contributor counts and numeric count of the coordinator plus actually running workers. List planned
   workers separately. Applied specialist profiles are expertise and add zero agents.
6. **Admission:** implementation is pending until the current plan, completed criticism and
   declared briefing satisfy their admission checks. Never announce a gate passed before it did.

Use [progress announcements](progress-announcements.md) for messages and transitions.
If the workspace or suitable workflow is unknown, first announce provisional read-only
reconnaissance, its narrow approach and limitations, and actual agent count. Inspect only what
is needed to identify the owners and ground the scope/plan. Then confirm the selected chain
before dependent work. This exception permits no product change and no silent full assessment.

## Plan and criticize before work

Every task has captured scope, a proportional plan and actual criticism of that plan. The
depth follows the job; the prerequisites do not disappear because a task looks easy.

| Requested work | Required preparation | Preserved boundary |
| --- | --- | --- |
| Build, fix, test authoring, cleanup or project documentation | Concrete changes, owners, dependency order, protected behavior and decisive checks; completed criticism of that exact plan before writes | Only authorized product/test/docs changes |
| G0 quick correction | Compact scope, steps/checks, actual execution worker, independent criticism/result review and briefing in its existing quick record | No automatic six-file promotion or second GB record; no solo exemption |
| Research, assessment, review, verification or planning only | Brief operation plan and criticism of its assumptions, source access, coverage and limits; may be recorded in the existing brief/evidence | No application implementation or fabricated build history |
| Continuation with exact current evidence | Reconcile source and completed work, reuse the valid plan/criticism, publish the current phase/roster | No needless allocation or replay of completed phases |

Task-record and evidence writes needed to capture, plan, criticize and record outcomes are
allowed within their assigned scope before product admission. They are not project-documentation
implementation. Advanced planning-only operations such as numeric 1/01, GPL or GCP may stop with the
implementation critique pending; they still critically check their planning approach and report
that product execution is not admitted. The primary Plan mode includes completed criticism of
the resulting plan before it reports completion. No planning-only mode authorizes product edits.

Criticism must examine the actual source and exact proposed changes: scope authority,
feasibility, dependency order, verification, and protected behavior. Record concrete findings
and their dispositions, or a grounded explanation of why no material finding remains. Resolve
blocking findings and review the corrected plan. A risk list, an unfinished self-check, a
nonempty critique file or a `ready` flag alone is insufficient.

Every new logical task has at least two useful actual worker contributions, including Plan, read-only and standalone operations. Every product/test/docs writer, including G0/G1/GB, is a real execution specialist and needs
a distinct real critic of the current plan and independent acceptance of the result. A role
name or coordinator self-critique cannot satisfy these duties. Read-only tasks obtain a primary contribution and a distinct consequential corroboration within the selected operation. Coordinator inspection-approach self-checks do not replace either worker. Architect advice for broad/shared impact must
finish before final plan completion and criticism. Preserve Loop's stronger fresh-reviewer
requirements: its reviewer confirms the repair plan and owns substantive acceptance; its
manager only coordinates and reconciles accounting.

## Admit product changes

Before the first product source, test or project-documentation write, and before resumed
writes after interruption, require all of the following:

- Original request/corrections and scope are captured in the selected record.
- Concrete plan and verification coverage match the authorized outcome and current source.
- A concrete mode, source-grounded routing decision and required delegation assignments are
  declared; started worker phases have actual non-coordinator owners and applied profiles.
- Required Architect advice is complete before the affected final plan and criticism; unknown
  impact cannot masquerade as a localized fast build.
- Completed, revision-bound criticism has no unresolved blocker and covers the selected
  mutation operations, scopes and dependency order.
- Scope, workflow, phases/owners and actual agent count have been visibly communicated.
- The current declared briefing and review bindings pass the applicable admission helper.
- The executor has actually reconciled relevant source/diff, permissions and other writers.
- Every adopted architecture/design/plan author participates in the independence check; final acceptance excludes every source/test/docs/integration author and binds the final stable result.

The coordinator may integrate, package and perform already-authorized publication after
specialist execution and independent acceptance. This does not authorize taking over the
assigned implementation silently. Required workers may run sequentially; unavailable dispatch
blocks dependent task work. Children execute their existing bounded assignment without
recursively creating another mandatory worker chain.

For a development record, use [record gates](record-contract.md) and
`scripts/resolve_plan_record.py --execution` with the exact project/record. Criticism is
mandatory even without `--require-critique`; that compatibility flag cannot relax admission.
For interrupted execution use the documented explicit `--resume` flow.
For G0, use its shared compact contract and
`commands/quick-task/scripts/audit_task_record.py <record> --execution`.
A plain record resolve, traceability audit, router descriptor or planned finalization grants
no execution admission. Where the required helper cannot run, keep product execution blocked
and complete permitted preparation; do not invent a pass or an alternative bypass.

Numeric `013`, `13`, `3`, direct executors, GVD documentation and GCL cleanup retain their
requested operations. Announce and fulfill missing capture/plan/criticism prerequisites before
writes, or reuse their exact valid coverage. Never silently interpret a missing digit as a
waiver. Do not turn a read-only or plan-only request into a build.

All selected product-writing operations require the current reviewed plan; a missing catalogue
Boolean cannot disable the gate. Repair authorization identifies permitted findings and does
not replace criticism of the concrete repair. Continuing writes remain bound to the same
authorized work definition; material unrelated drift requires renewed planning and criticism.

## Report phases and real agents

Statuses mean **pending**, **in progress**, **complete**, or **blocked** based on evidence.
Do not mark a partial critique complete, or combine “implement and verify” into a completed
phase while verification is missing. Before a transition, state the completed phase and its
actual result, the next phase and owner, and the current numeric agent count.

Before delegation, announce the proposed assignment; only after a successful spawn report it
as launched using the real returned identity. Keep coordinator/current agent, running workers,
completed/failed workers, planned workers, and applied profiles distinct. Queued stages,
reserved identities and `agentCalls` metadata are not running agents. If dispatch fails,
report the real count and fallback. Required independence cannot be simulated by renaming
the current agent. Routine tools within an unchanged phase need no repeated opening brief.

Record the actual public briefing after emitting it, including its text/context and current
bindings. Producing text in a helper or writing a local file is not publishing it to the user.
Never manufacture an announcement receipt. Follow the same rule for completion statements.

Before completion, every required assignment has a useful current contribution with result, inspected evidence, limitations, revision, disposition and effect on synthesis. At least two different workers qualify. Unresolved in-scope obligations remain open. Before publication, required preceding contributions and independent acceptance of the exact prepared result must exist; post-install checks still follow installation.

## Reuse and invalidate evidence

Preserve one task record, original messages, stable requirement IDs and prior evidence. New execution uses contract-v2. Archived v1 records remain byte-identical; active reconciliation preserves old receipts and actual identities and obtains missing current evidence instead of silently rehashing criticism.
Changed requirements, plan definitions, relevant source assumptions, or selected mutation
operations/scopes/order need reconciliation and renewed criticism of affected work. An exact
unchanged current plan may be reused. A source description/hash in portable metadata records
the declared baseline; the executor and critic must inspect actual source and diffs. Do not
claim the portable validator automatically detects changed repository bytes.

Phase progress, agent completion and roster changes require an updated public briefing;
they do not alone invalidate a stable reviewed work definition. Keep these bindings separate.
Do not rehash ordinary execution checkmarks and call that a fresh review. Preserve original
admission evidence and follow documented continuation/reconciliation rules.

## Recover truthfully

If a product change happened before admission, or a phase was falsely reported complete:

1. Stop further product writes and correct the user-facing status immediately.
2. Identify the incomplete gate and actual premature change; preserve its diff and chronology.
3. Reconcile the current source, original scope and any interrupted worker.
4. Finish a real plan/criticism against that state, publish corrected phases/count and readmit.
5. Keep the earlier breach and correction in the record. Completing missing paperwork later
   does not make the earlier write compliant. Never backdate approval or erase evidence.

Continue already authorized work after the valid gate passes; this contract adds no routine
permission ceremony. An unresolved real blocker remains visible and cannot be checked off.

## Enforcement boundary

Portable helpers validate required declarations, file hashes, revision bindings and structural
consistency. They cannot authenticate chat delivery, worker identity, source freshness or the
intellectual quality of criticism. Actual host tool permissions and supported operations still
govern execution. Save the real public message and actual dispatch results; do not invent receipts.

This package makes its instructions mandatory and its supported admission paths fail closed.
It does not install a host interceptor or stop an arbitrary source-writing tool invoked outside
those paths. Report that boundary accurately. A model-authored `announced: true` is a local
declaration, not independent proof that the user received the message.
