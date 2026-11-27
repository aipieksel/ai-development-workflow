# Bounded operation policy

This policy applies when the coordinator selects an internal operation from
[the catalogue](catalog.json). Read the operation's instruction body and assigned role.
Operation scope overrides a profile's broader full-workflow description. The catalogue is
shared source for Auto and recipes; it is not a native queue or a set of public skill entries.

Apply the [workflow contract](../references/workflow-contract.md) and
[progress announcements](../references/progress-announcements.md). Show actual scope,
ordered phases/owners, current phase, real running-worker count and admission status.
Use proportional planning and criticism even for record-only work. Profiles add no workers.
The coordinator applies [task routing](../references/task-routing.md) for the concrete mode,
mandatory assignments and Fast/Architect precedence. A child already assigned this operation
does not restart that workflow or recursively spawn workers to satisfy the same rule.

## Bounded assignments

1. Perform only the selected operation. Do not recursively launch G workflows, replay 0123
   or turn a review into implementation. The coordinator owns the already authorized chain.
2. Read actual supplied sources and input artifacts before relying on them. Missing inputs
   remain blocked unless the coordinator provides authorized prerequisite work. Do not infer
   completed evidence from a filename, a role description or an earlier unverified claim.
3. Use the exact selected task record and assigned output path. Do not allocate another record.
   Retain previous attempts, stable findings, requirements and evidence references.
4. Apply the operation's `writeScope`. `record-only` permits task evidence; `test-output-only`
   permits authorized checks/logs; `tests-only` and `docs-only` permit only reviewed changes in
   those surfaces; `repo-write-scoped` remains bounded by the current concrete plan.
5. Every product/test/docs writer requires captured authority, current reviewed plan coverage,
   completed criticism, visible briefing and successful actual execution admission. A missing
   or false catalogue Boolean cannot waive that shared gate.
6. Preserve one implementation owner for overlapping work and one generation/package owner.
   A reviewer does not repair its target. Findings authorize no new source changes by themselves.
7. Use available tools and actual returned results. Never invent browser execution, worker
   identities, source baselines, timestamps, permissions, test exits or external delivery.

## Independence and roles

An operation descriptor does not launch a worker. The coordinator must actually assign the
meaningful task operations to at least two distinct actual worker contributors, excluding the coordinator, including tiny, Plan, Review and standalone operation tasks. Supply the complete profile,
scope and evidence; record actual dispatch and ownership. The coordinator may prepare records,
coordinate, integrate, package and perform authorized publication without replacing the
assigned specialist. Keep one writer for overlapping source changes.

The `review-plan`, `review-ui-spec`, `review-code`, `review-ui`, `review-security`,
`review-accessibility`, `review-dependencies`, `verify-goal` and `verify-docs` operations are
independent review assignments when selected as such: use a real reviewer distinct from the
author/executor of the reviewed work. GPR and Loop always retain their independent review
requirements. A required reviewer cannot be simulated by giving the current agent another name.
Every product/test/docs change, including G0/G1/GB, needs actual independent plan criticism and
result acceptance. Read-only work needs a second worker for bounded criticism or corroboration within its selected scope. Track all substantive authors, including secondary authors, adopted advice and coordinator integration; no author may accept their own output after changing profiles. Each contribution records evidence, limitations, disposition and its effect on the combined result. Missing dispatch or required
independence blocks dependent work; busy capacity calls for waiting/serialization, not a waiver.

For source assessment, preserve source-backed C IDs. Planning roles produce plans only.
For TDD, the selected RED or strategy assignment limits the full RED/GREEN/REFACTOR profile.
Verification and documentation roles perform only their selected operation rather than building
first. Read-only current-work operations must not fabricate prior implementation artifacts.

## Evidence and outcomes

Save a readable report under the same record's `artifacts/` using the assigned attempt path.
Record actual input paths/revisions and hashes where needed, checks performed, source/output
identity, role/actual worker identity, findings, status and limitations. Link it from results.
No special host receipt, queue ledger or invented lifecycle event is required.

Test/performance evidence includes exact commands or actions, environment, actual numeric exits
where available and original logs. Browser assertions need observed outcomes. A failed check
blocks its acceptance except for a correctly identified intentional TDD RED assertion.

Review reports contain stable finding IDs, concrete evidence, severity/impact and dispositions.
Plan criticism covers scope, feasibility, sequencing, verification and protected behavior,
with actual findings or a grounded no-findings rationale. Bind it to the exact plan revision.
Blocked or unresolved findings cannot be promoted to approval by an executor or manager.

Use `succeeded`, `blocked` or `failed` for the real operation outcome. The coordinator reads
the returned result and relevant evidence before proceeding. Structural helper validation does
not prove semantic correctness, identity authenticity or live tool execution.

## UI and browser work

Assess [UI applicability](../references/ui-routing.md). Visual outcomes load the
[UI Design Director](../specialists/ui-design.md) inside the selected operation and scope.
Preserve component owners, approved tokens/content and required rendered/interaction evidence.

Every browser assignment includes [browser recovery](../references/browser-recovery.md), the
current session owner and the current user's actual recovery choice. Supported recovery under
existing authorization does not require repeat permission; missing tools remain a real blocker.
