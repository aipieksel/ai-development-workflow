# Python automation and data pipelines

Build resumable data processing with validated inputs, explicit failures and reconciled outputs.

Read the [shared specialist contract](../references/specialist-contract.md).
This profile is a domain lens for existing stages, not a separate workflow or native agent registration.
Assessment and review are read-only; code writes require assignment by the selected execution stage.

## Use and exclude

- Use when: Python scripts, API ingestion, scraping outputs, transformations or automation pipelines are changing.
- Use when: Pagination, retries, checkpoints, data contracts or partial failure affect correctness.
- Exclude: The project has no Python/data-processing component.

## Discover the actual environment

- Read Python/runtime constraints, dependency locks and the existing execution entry point.
- Inspect representative actual input and output shapes before writing transformations.
- Map source pagination, identifiers, cursors, timezones and retry semantics.
- Identify persistence/checkpoints, downstream consumers and partial failure behaviour.
- Read pipeline schemas and the business meaning of important fields.
- Identify available fixtures and cost-sensitive external operations.

## Domain techniques

- Validate data at external boundaries and report rejected records with useful reasons.
- Use stable identifiers and explicit deduplication/idempotency rules.
- Make retries bounded and distinguish transient failures from invalid input.
- Checkpoint durable progress only after the corresponding output is safely recorded.
- Reconcile input, accepted, rejected and output counts where meaningful.
- Preserve numeric, date and null semantics rather than coercing them silently.
- Keep credentials out of logs and minimise stored source data to what the task needs.
- Retain existing tooling; use dbt/Dagster/Pydantic guidance only for actual dependencies.

## Stage handoff

Contribute the domain section to the selected stage's existing artefact and shared task record.

| Stage | Required contribution |
| --- | --- |
| Discover | Input/output examples, dependency map, failure modes and data contract. |
| Plan | Transformation rules, retry/checkpoint semantics and representative acceptance cases. |
| Execute | Assigned pipeline changes with small safe runs and preserved checkpoints. |
| Verify | Boundary, rerun and partial-failure evidence plus output reconciliation. |

## Acceptance evidence

- Representative real input produces schema-valid, reconciled output.
- Reruns, partial failures and pagination do not silently lose or duplicate data.
- Existing runtime/tooling and externally visible data contracts remain compatible.

## Existing capability integration

- Scope caution: dbt, Dagster or Pydantic AI is merely a possible tool, not an actual project dependency.

- Use the project's existing scheduler, data libraries and connector tools.
- Combine database for schema/transaction changes and content-seo for publishing data products.
- Use installed framework-specific skills when their detected stack is relevant.
- Let the shared test strategist choose meaningful assertions; no arbitrary coverage target.

## Failure modes

- Do not guess column names or response shape from a task description.
- Do not swallow errors and call the batch complete.
- Do not migrate package managers or require a hosted observability account by default.
- Do not run a full expensive dataset when a targeted sample resolves the current risk.
