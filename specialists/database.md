# Database schemas and data integrity

Apply engine-specific checks to migrations, queries, tenant access, locks and data compatibility.

Read the [shared specialist contract](../references/specialist-contract.md).
This profile is a domain lens for existing stages, not a separate workflow or native agent registration.
Assessment and review are read-only; code writes require assignment by the selected execution stage.

## Use and exclude

- Use when: SQL/schema changes, query behaviour, data access rules or database performance are in scope.
- Use when: A migration, import, restore or concurrency issue can affect persisted data.
- Exclude: The change is purely presentational and does not alter data access.

## Discover the actual environment

- Determine the database engine/version, ORM/query layer and migration owner.
- Inspect relevant tables, constraints, indexes and representative data safely.
- Map callers, transactions, tenant boundaries and downstream consumers.
- Identify lock/traffic sensitivity and the target environment for any operation.
- Read existing migration conventions and backup/recovery expectations.
- Capture baseline query/plan evidence when performance is the stated problem.

## Domain techniques

- Prefer compatible staged migrations when consumers cannot switch atomically.
- State defaults, nullability, backfill and rollback implications explicitly.
- Use parameterised queries and the engine's supported access-control mechanisms.
- Check tenant/role visibility with both allowed and denied cases.
- Inspect execution plans and representative cardinality before adding indexes.
- Keep transaction boundaries, uniqueness and idempotency aligned with the operation.
- Account for locks and resource use in backfills or large imports.
- Do not apply Postgres RLS or SQL syntax to MySQL/MariaDB by analogy.

## Stage handoff

Contribute the domain section to the selected stage's existing artefact and shared task record.

| Stage | Required contribution |
| --- | --- |
| Discover | Schema/caller/access map and baseline evidence relevant to the request. |
| Plan | Migration sequence, invariants, concurrency risks and recovery steps. |
| Execute | Assigned schema/query changes in the authorised environment only. |
| Verify | Migration/constraint/access results and relevant query-plan or concurrency evidence. |

## Acceptance evidence

- Schema/query changes match the detected engine and migration tooling.
- Data invariants, access boundaries and relevant concurrency behaviour hold.
- Migration and rollback/recovery evidence is appropriate to the authorised environment.

## Existing capability integration

- Scope caution: Postgres-specific guidance does not match the actual database engine.

- Use Supabase/Postgres guidance only when that engine is detected.
- Use WordPress/WooCommerce or WHMCS data APIs when the host owns the storage contract.
- Use the native database connector or existing project tooling when available.
- Coordinate with infrastructure for deployment timing and shared security for access findings.

## Failure modes

- Do not confuse a generated migration file with an applied or verified migration.
- Do not run destructive data operations under a read-only review stage.
- Do not remove constraints or disable access controls to make tests pass.
- Do not infer production performance from an empty development database.
