# Stage artifacts and durable handoff

Apply the [workflow contract](workflow-contract.md), [record contract](record-contract.md)
and [progress announcements](progress-announcements.md). Scope, current plan criticism,
visible phases/owners and actual worker counts remain mandatory before product writes.

Each operation works within one selected task record and one assigned workspace. A public
mode or standalone starter may allocate that record once; subsequent operations reuse it.
An explicitly selected record path is authoritative. Do not choose a different record by
filesystem recency, create worker sub-records, or replace original sources with a recap.

For visual tasks, load [UI applicability](ui-routing.md) and the
[UI Design Director](../specialists/ui-design.md). Expertise never expands the assigned write
scope. See [composition](portable-composition.md) for dependencies and worker ownership.

## Atomic G evidence

Create `<record>/artifacts/` when needed. Preserve the six core record files, selected source
captures and earlier reports. Append a dated attempt or use a new attempt directory on retry.
Link actual results from `results.md`; do not mark downstream work complete from file presence.

| Artifact key | Usual evidence | Producer and required content |
| --- | --- | --- |
| `assessment` | `artifacts/assessment.md` | GAS: C IDs, paths/symbols, owners, tests, gaps and source provenance |
| `research` | `artifacts/research.md` | GRS: verified sources, versions, findings, licenses and uncertainty |
| `design_audit` | `artifacts/design-audit.md` | GDA: observed UI, tokens, component owners, screenshots and limits |
| `architecture` | `artifacts/architecture.md` | GAA: existing architecture, bounded decisions and tradeoffs |
| `design_spec` | `artifacts/design-spec.md` | GDS: scoped design, reuse, states and measurable acceptance |
| `plan` | `fix-plan.md` and `test-plan.md` | GPP/GCP/GPL: source-linked R/P/T coverage; planning is not execution |
| `plan_review` | `critique.md` and `artifacts/plan-review.md` | GPR: independent findings, dispositions, reviewed revision and hashes |
| `red_tests` | `artifacts/red-tests.md` | GTF: actual test files and the correct intentional RED failure |
| `implementation` | `artifacts/implementation.md` and `results.md` | GEX/GTE: scoped changes and actual verification outcomes |
| `unit_verification` | `artifacts/unit-verification.md` | GUT: actual commands, exits, failures and coverage limits |
| `e2e_verification` | `artifacts/e2e-verification.md` | GVE: observed journeys, assertions and browser evidence |
| `code_review` | `artifacts/code-review.md` | GVR: independent source/diff findings and evidence |
| `security_verification` | `artifacts/security-verification.md` | GVS: bounded checks and supported findings |
| `accessibility_verification` | `artifacts/accessibility-verification.md` | GVA: semantics, controls, focus and relevant interaction evidence |
| `performance_verification` | `artifacts/performance-verification.md` | GVP: named baselines, workloads, measurements and budgets |
| `documentation` | `artifacts/documentation.md` | GVD: changed docs grounded in actual behavior |
| `cleanup` | `artifacts/cleanup.md` | GCL: bounded refactor and affected checks |
| `contribution.portfolio` | Contribution reports and `portfolio.json` | GRC: inventoried repository, source-grounded candidates and validation |

Internal operations under [workflows/](../workflows/catalog.json) use their own exact artifact
keys, such as `code.plan` and `plan.review`. The catalogue explicitly normalizes the shipped
G artifact aliases for composition; this does not create, inspect or approve the actual evidence.
Read the selected instruction and real input before consuming it.

## Evidence and completion

Record the request/requirement, source version, exact output path, actual author/reviewer
identity where available, checks performed, observed results and limitations. When hashes
or plan revisions bind evidence, compute them from the actual artifacts. Never fabricate a
Git baseline, worker identity, transcript timestamp or passing test result.

Use `succeeded` only when the assigned operation really completed and its required evidence
exists. Missing source/tools, stale review, unobserved behavior or an unresolved prerequisite
means `blocked` or `failed` as appropriate. A nonzero test exit is not success except for an
explicit expected TDD RED assertion; runner/import/syntax failures are not valid RED evidence.

The real coordinator reads returned worker results and reconciles artifacts before dependent
work. No custom host completion event, queue ledger, receipt schema or `artifact.json` is
required by this portable handoff. A conversational “done” or a structurally valid JSON file
still cannot replace observed evidence.

## Mutation and review gates

Every product/test/docs writer needs current concrete plan coverage, completed criticism and
successful public-briefing admission. GPR and the internal `review-plan` operation require a
real independent critic. G0/G1/GB have no solo or self-critique exemption for writing work;
apply the concrete mode, routing and assignment requirements in [task routing](task-routing.md).
Reviewer operations stay read-only; executor operations make only admitted changes.

Source, requirements or relevant plan changes invalidate affected evidence. Preserve prior
attempts and refresh the required review instead of silently waiving it. Accepted continuing
implementation may update source under its reviewed plan, but unrelated drift requires
reconciliation. Documentation and cleanup have no exemption from the write gate.

Do not infer authorization to commit, push, deploy, send messages or perform destructive work
from completing a stage. Continue actions already authorized by the current task, and report
the actual boundary when a dependent external action remains unavailable or unapproved.
