# Composable operations and workflow templates

The default main-skill invocation selects a proportional chain from the actual task, then reads the relevant handlers, profiles and prerequisites. It does not require a full-index evaluation. Explicit standalone choices preserve their boundaries. See [automatic selection](automatic-selection.md).

A **stage** completes one narrowly defined operation and writes durable evidence in the existing task record. A **complete workflow** performs its own end-to-end sequence internally; do not insert that whole workflow as an atomic operation alongside another build chain.

## Discover (read-only, except the task record)

- `GRC` — **Repository Contribution Scout**: inventory a cloned repository, inspect its architecture and maintainer priorities, then rank PR-sized contributions by category with source evidence; no code edits, issue creation or PR submission. **Use before deciding what to contribute to an unfamiliar upstream project.**

- `GAS` — **Codebase assessment only**: inspect the relevant repository, document existing owners/rules and create an assessment artifact. Does NOT plan/build. **Use before planning unfamiliar code.**
- `GRS` — **Research only**: investigate public library/project/implementation options and source evidence; no code changes. **Use when technology choices require verified information.**
- `GDA` — **Design audit**: inspect actual UI, design system, component ownership and measured gaps; no UI changes. **Use before a redesign.**
- `GAA` — **Architecture advice**: read-only trade-offs/integration boundaries against an existing assessment/plan. **Use when system design is a real decision.**

## Plan and review (no application code edits)

- `GPL` — Goal Planner: goals/dependencies/sequence, plan-only, starts a task record. Best for roadmap planning.
- `GCP` — Code Goal Planner: implementation plan grounded in existing source, plan-only, starts a task record. **Use when no separate assessment is needed.**
- `GPP` — Plan from assessment/design evidence; reuses the record created by GAS/GDA. **Use after assessment; avoids repeating discovery.**
- `GDS` — Design spec from GDA audit, with components, tokens and responsive behaviours. **Use to plan UI without building.**
- `GPR` — Independent **plan** review/critique, fixes R/P/T plan and readiness; no code. **Use before execution.**

## Execute (changes tests or production code)

- `GTF` — Write meaningful failing tests only: TDD **RED**; intentionally failing feature assertions plus evidence, no application edits.
- `GEX` — Execute **existing reviewed plan**; no new plan or record allocation. **Use to continue from GPR.**
- `GTE` — TDD **GREEN** executor: consume GTF red tests and current plan review, change product code and rerun checks.

## Verify (existing implementation; do not implement fixes)

- `GUT` — Run scoped unit/integration/lint/type/build checks.
- `GVE` — End-to-end browser/customer journey verification.
- `GVR` — Independent post-implementation code review.
- `GVS` — Security checks on scoped change.
- `GVA` — Keyboard, focus and responsive accessibility checks.
- `GVP` — Performance budgets and failure recovery measurements.

## Finish (after implementation)

- `GVD` — Documentation-only updater; reuse doc-updater agent.
- `GCL` — Scoped, behaviour-preserving cleanup (requires test reruns).

## Complete pipelines (standalone choices or templates for automatic composition)

For an explicit pipeline, run that pipeline once. For automatic composition, expand its useful operations, combine complementary stages and deduplicate before executing. Never nest full pipeline commands inside an atomic chain.

- `G1` Standard: capture → plan → critique → implement/test.
- `GS` Assessed: capture → assess → plan → critique → implement/test.
- `GA` Architecture: capture → architecture consultation → plan → critique → implement/test.
- `GT` Full test-first: capture → plan → critique → TDD agent writes RED, GREEN, refactors/tests in one build.
- `GB` Fast build: reuse/dependency batching and consolidated acceptance under full-scope constraint.

Legacy specialized complete workflows (`G6`, `G7`, `GC`, `GE`, `GD`, `GH` etc.) remain supported by their existing G codes and actual handler instructions. The public help surface presents the five primary modes: Auto, Plan, Build, Review and Loop. It is ordinary help, not a custom manual picker. The [advanced reference](advanced-reference.md) documents all retained commands and their exact dependencies. Do not confuse `GVD` (docs only) with `GD` (build + docs) or `GVE` (E2E verify only) with `GE` (build + E2E).

Use the [stage artifact contract](stage-artifacts.md), [neutral operation catalogue](../workflows/catalog.json) and [operation policy](../workflows/operation-policy.md) for same-record evidence and bounded handoffs. No bundled native queue or public native `stage`/`pipeline` runtime is required or supplied.
