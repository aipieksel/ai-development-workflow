# WHMCS modules and client-area systems

Assess and implement WHMCS extensions with verified hook contracts, lifecycle and account boundaries.

Read the [shared specialist contract](../references/specialist-contract.md).
This profile is a domain lens for existing stages, not a separate workflow or native agent registration.
Assessment and review are read-only; code writes require assignment by the selected execution stage.

## Use and exclude

- Use when: The task changes a WHMCS addon, hook, client-area template, API integration or account workflow.
- Use when: Rate limits, billing/account behaviour or module lifecycle depends on WHMCS.
- Exclude: The task affects only WordPress/WooCommerce or generic PHP, with no WHMCS integration.
- Exclude: Only marketing-page copy changes and no WHMCS integration is affected.

## Discover the actual environment

- Identify the running/target WHMCS and PHP versions and the relevant module type.
- Locate module functions, hooks, client/admin dispatchers, templates and database access.
- Verify hook names, arguments and return behaviour against current official documentation.
- Trace the actual request path, including public endpoints and alternate entry points.
- Read schema changes and module activation/deactivation behaviour before altering storage.
- Identify available local/staging fixtures and distinguish them from production access.

## Domain techniques

- Follow the existing module bootstrap and naming conventions; avoid host-core modifications.
- Keep client identity, administrator permissions and cross-account access checks explicit.
- Define rate-limit key, window, clock and storage semantics before implementing counters.
- Check concurrent requests and multiple workers when shared limits or idempotency matter.
- Avoid account enumeration and record only the diagnostics needed for the task.
- Use supported database APIs and output escaping in the module's actual template context.
- Keep migration and activation operations repeatable and scoped to owned data.
- Inspect official examples as structural references and recheck their age and version fit.

## Stage handoff

Contribute the domain section to the selected stage's existing artefact and shared task record.

| Stage | Required contribution |
| --- | --- |
| Discover | Request/hook map, version evidence and observed behaviour in the assessment. |
| Plan | Policy boundaries, storage decisions and concrete success/failure cases. |
| Execute | Assigned module/hook/template changes with targeted local or staging checks. |
| Verify | Real hook evidence where available; denied, repeated and concurrent request results. |

## Acceptance evidence

- The relevant hook/module executes on the declared host version.
- Account and admin boundaries are exercised with permitted and denied cases.
- Repeat requests, concurrency and upgrade behaviour match the requested policy.

## Existing capability integration

- Use current WHMCS documentation as the contract for host hooks and module behaviour.
- Combine database for schema/locking work and the existing security stage for account risks.
- Use React or frontend guidance only for the client-area UI technology actually present.
- Follow the existing deployment process; a source change is not a claim of live installation.

## Failure modes

- Do not invent a hook because its name sounds plausible.
- Do not use WordPress capability/nonces as if WHMCS supplied the same APIs.
- Do not vendor the old sample without resolving its root-licence/file-header inconsistency.
- Do not call a per-process counter a distributed rate limit.
