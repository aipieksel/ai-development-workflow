# Artifact completeness and verified delivery

Finish the requested handoff with the actual files, identities and destination intact, and distinguish preparation from successful delivery.

Read the [shared specialist contract](../references/specialist-contract.md),
[task contracts](../references/task-contracts.md) and
[acceptance evidence](../references/acceptance-evidence.md).
Apply this lens to the selected stage; a review assignment does not grant publication authority.

## Use and exclude

- Use for a multi-file deliverable, self-contained HTML/components, asset bundles, ZIP handoffs, saved catalog revisions, import/publish requests or reports of stale/missing output.
- Combine the format owner with migration-release for repository/release tasks and media-library for large imports. Delivery is not a substitute for validating the underlying content.
- Exclude a simple explanation with no artifact or delivery requirement. Do not manufacture a ZIP, upload or release merely because this lens is available.

## Define what must arrive

Resolve expected target IDs, names, formats, counts, output form and destination from the task contract. Record source identity/version and intended replacement/backup behavior. Distinguish a preview, editable source, individual assets, archive and deployed artifact; one does not automatically satisfy another.

Inventory actual dependencies: CSS, scripts, fonts, images, relative paths, imported modules, schema files or generated assets. Identify whether the required artifact is standalone or depends on a declared runtime. Inspect current available storage/upload/release capabilities and limits before selecting a transfer plan.

## Package and verify

- Assemble only the intended deliverable contents in the requested layout. Inspect the final archive, not just its staging folder, for missing/duplicate files, accidental nesting and unrelated private material.
- Open standalone pages and reusable component exports in their intended context. Verify relative resources and fonts resolve independently; a component styled only by its surrounding studio is not a verified standalone export.
- For code/tool packages, check transitive runtime imports and run the advertised command from a clean extracted location when that is the compatibility claim. Separate optional integration tests that require a declared external core.
- Preserve requested originals or backups before replacing an existing target. Keep existing site/plugin/account identities and audiences; do not create a replacement project to bypass a failed update.
- Save or publish through the owning provider's supported workflow using the verified target and current revision where available. Do not reinterpret a file-upload request as public publication or communication to other people.
- Use resumable parts or another supported transport when actual limits require it. Record which parts arrived, failed or remain pending; preparing a part does not mean the destination accepted it.
- Read back the changed target or inspect returned version/content evidence when the provider supports it. Reconcile the exact delivered identity with the output that was verified. If readback is unavailable, report saved/uploaded separately from verified.

## Stage handoff

| Assigned stage | Concrete contribution |
| --- | --- |
| Assess/research | Expected deliverables, dependency closure, destination identities and capability limits. |
| Plan/critique | Artifact layout, replacement/backups, verification context and authorized delivery steps. |
| Implement | Assigned packaging and authorized saves/uploads/releases with actual results. |
| Review/verify | Final archive/opening checks, revision-bound receipts/readback and reconciliation of all targets. |

## Acceptance evidence

For local outputs, record actual paths and content revisions/checksums when required. For remote/generated outputs, retain the real returned identity and version/event information plus available successful tool/readback evidence; do not invent a remote content hash. A saved note or receipt's hash protects its bytes but cannot authenticate its claims.

Use the optional `scripts/acceptance_matrix.py` only as described by acceptance-evidence.md: it is read-only structural validation of the declared inventory and evidence bindings. Coverage of a real task needs the independent expected requirements/targets, and visual or provider authenticity remains outside its proof. A current output invalidates checks bound to its older revision.

When the host displays and saves generated images automatically, follow that host contract. Do not download or reconstruct them solely to create local packaging evidence. A separate image archive is work only when the task requests it or another authorized deliverable requires it.

## Completion language

Report the requested result with a working artifact/provider link according to the host's rules, a concise account of the important changes, and material unverified requirements. Keep statuses precise: prepared, locally verified, saved/uploaded, published/deployed and observed in the destination. Do not call all of them complete because the first one passed.

Do not substitute screenshots for editable source, an old file for the new revision, a contact sheet for requested individual images, or a successful build for an unperformed deployment. Resolve required missing outputs before optional polish.
