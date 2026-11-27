# Infrastructure and deployment configuration

Ground infrastructure changes in provider versions, actual state, execution mode and recovery evidence.

Read the [shared specialist contract](../references/specialist-contract.md).
This profile is a domain lens for existing stages, not a separate workflow or native agent registration.
Assessment and review are read-only; code writes require assignment by the selected execution stage.

## Use and exclude

- Use when: Server/container configuration, infrastructure as code, CI deployment or runtime operations are changing.
- Use when: Networking, secrets, storage, provisioning or service health affect the requested result.
- Exclude: The task is only application UI/content work with no infrastructure impact.

## Discover the actual environment

- Identify provider/runtime, tool versions, environment and configuration ownership.
- Read existing deployment manifests, CI workflows and state/backend conventions.
- Map resources, network boundaries, secrets references and service dependencies.
- Inspect current observable state and drift only through authorised tooling.
- Determine which validation commands are read-only and which create or alter resources.
- Read existing health checks, rollout policy and rollback/recovery process.

## Domain techniques

- Use the current infrastructure source of truth and preserve environment separation.
- Validate syntax and plans before applying meaningful changes.
- Treat Terraform test apply mode and integration fixtures as real resource operations.
- Prefer isolated mocks/plan checks when they resolve the task's present risk.
- Keep secrets in existing secret/configuration mechanisms and out of diffs/logs.
- Make provisioning and deployment reruns predictable with explicit state ownership.
- Trace CI event inputs and permissions when automation invokes coding agents.
- Check service health and dependent behaviour after an authorised rollout.

## Stage handoff

Contribute the domain section to the selected stage's existing artefact and shared task record.

| Stage | Required contribution |
| --- | --- |
| Discover | Environment/resource/dependency map and observed failure or drift evidence. |
| Plan | Configuration changes, execution mode, affected resources and recovery criteria. |
| Execute | Only assigned changes and operations covered by the current authorisation. |
| Verify | Validation/plan output and, when applied, health and recovery evidence. |

## Acceptance evidence

- Configuration validates with the detected tool/provider versions.
- Planned changes and affected resources are understood before authorised application.
- Health and recovery checks distinguish prepared, applied and verified states.

## Existing capability integration

- Scope caution: No provider/runtime access exists; prepare and validate source without claiming applied state.

- Use the existing deployment toolchain and provider-specific skills when detected.
- Use HashiCorp guidance only for relevant Terraform/Packer work.
- Combine database for persisted-data effects and migration-release for release coordination.
- Use shared security review for concrete findings rather than a new permission framework.

## Failure modes

- Do not treat the word test as proof a command cannot mutate resources.
- Do not claim deployment success from a configuration commit or local build.
- Do not create a new cloud account, provider or paid service as an incidental convenience.
- Do not disable protections or rewrite live state to hide an unexplained failure.
