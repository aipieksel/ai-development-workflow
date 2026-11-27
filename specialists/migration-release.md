# Migration, recovery and release completion

Reconcile previous work, preserve checkpoints and finish authorised repository/release tasks with evidence.

Read the [shared specialist contract](../references/specialist-contract.md),
[task contracts](../references/task-contracts.md) and
[acceptance evidence](../references/acceptance-evidence.md).
This profile is a domain lens for existing stages, not a separate workflow or native agent registration.
Assessment and review are read-only; code writes require assignment by the selected execution stage.

## Use and exclude

- Use when: The task resumes a stalled build, migrates systems, recovers missing work or completes a release.
- Use when: Local files, branches, commits, remote repositories or packaged versions disagree.
- Exclude: There is no migration/release/recovery scope and a normal implementation stage suffices.

## Discover the actual environment

- Resolve the intended repository/release identity and current source before changing anything.
- Inspect worktree status, branches, commits, remotes and relevant untracked artefacts.
- Read available task records, migration lists and prior evidence; record retrieval gaps.
- Compare old/new behaviour and classify completed, partial and missing work.
- Inspect CI status and logs for the relevant revision rather than a nearby run.
- Identify who owns current changes and where recoverable checkpoints exist.

## Domain techniques

- Preserve unrelated or uncommitted work before planning integration.
- Use an isolated worktree when it reduces collision without hiding the intended source.
- Build a source-to-destination feature/file mapping for substantive migrations.
- Commit authorised significant milestones with focused scope and recorded verification.
- Distinguish committed locally from pushed remotely and verify the destination revision.
- Resolve conflicts using source behaviour and intent rather than blanket file replacement.
- Diagnose CI environment/billing/access failures separately from source defects.
- Package and inspect the actual deliverable; verify installation/deployment only when performed.

## Recovery and milestone contract

Resume the selected task record and reconcile its requirements with actual files, branches, commits, packages and remote state. A previous chat saying work finished is a lead, not proof. Mark each requirement complete, partial, missing, superseded or blocked with its source evidence; preserve the user's latest corrections and original scope across thread handoffs.

Before integrating, identify the intended baseline and ownership of outstanding changes. A request to consolidate work does not justify deleting unrelated branches, resetting a dirty tree or force-pushing. Resolve conflicts from required behavior and relevant history. For extension migrations, keep functionality in the extension where the current architecture supports it and document the native prerequisites that genuinely remain.

For authorized implementation, checkpoint coherent milestones before lengthy later phases or environment transitions. Use meaningful source/control changes, not empty commits; record the revision, relevant verification and next unresolved item. Do not commit credentials or unrelated artifacts. Include private user media only when the requested deliverable and repository audience authorize it. If remote push is unavailable, preserve local work and report the precise boundary.

On recovery, compare the remote target revision and package/deployment provenance, not a nearby timestamp. Distinguish source defects from quota, billing, access and environment failures using actual error evidence. Never infer a billing cause merely because a job did not run.

A handoff should identify the current task record, source revision, completed scope, outstanding checks, intended target and exact next action. Do not recreate an entire workflow when existing valid artifacts and review evidence can be reused. Changes after a check invalidate its affected revision-bound evidence.

## Stage handoff

Contribute the domain section to the selected stage's existing artefact and shared task record.

| Stage | Required contribution |
| --- | --- |
| Discover | Reconciliation table with source evidence, current state and outstanding items. |
| Plan | Recovery/integration sequence, owned changes and concrete completion criteria. |
| Execute | Assigned missing work and authorised checkpoints/release operations. |
| Verify | Relevant tests, clean integration state, remote/package evidence and remaining blockers. |

## Acceptance evidence

- Built, local, committed, pushed, packaged and deployed states are reconciled.
- Authorised significant milestones are preserved without overwriting unrelated work.
- Remaining failures are supported by exact logs/state, not assumptions.

## Existing capability integration

- If the current request is assessment only, retain read-only scope even when an unfinished release is found.

- Use existing repository and plugin release workflows rather than creating competing destinations.
- Combine plugins-mcp for plugin releases and relevant existing platform owners for migrations.
- Use CI tools exposed in the session before assuming a local CLI or account.
- Keep the shared record current so the next run can resume without repeating discovery.

## Failure modes

- Do not claim lost work exists merely because a prior chat said it was built.
- Do not reset, clean or force-push unrelated changes to simplify recovery.
- Do not infer payment details from a generic failed check.
- Do not report success when only the source build, not the requested delivery, finished.
