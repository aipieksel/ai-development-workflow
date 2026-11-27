# Editors, registries and persistent schemas

Protect editable document models, widget registries, settings, history and import/export compatibility.

Read the [shared specialist contract](../references/specialist-contract.md),
[task contracts](../references/task-contracts.md) and
[acceptance evidence](../references/acceptance-evidence.md).
This profile is a domain lens for existing stages, not a separate workflow or native agent registration.
Assessment and review are read-only; code writes require assignment by the selected execution stage.

## Use and exclude

- Use when: A visual editor, page builder, structured tree, widget registry or saved workspace is changing.
- Use when: Document schemas, settings persistence, selection, undo/redo or import/export contracts are involved.
- Exclude: The page is a static presentation with no editable document model.

## Discover the actual environment

- Identify the canonical document model, widget registry and schema/version declarations.
- Trace how registry entries drive rendering, settings, inspector controls and export.
- Locate persistence, migration, history, selection and clipboard ownership.
- Read representative saved documents, including older versions and nested structures.
- Check framework and validator versions before choosing schema features.
- Map the requested change to the precise owner rather than parallel shadow models.

## Domain techniques

- Keep one canonical representation and explicit adapters at import/export boundaries.
- Preserve stable IDs, parent-child relationships, ordering and references through edits.
- Validate external documents before applying them; report unsupported fields and versions.
- Define migration defaults deliberately and preserve unknown data when the contract requires it.
- Treat undo/redo, detach/attach, duplicate and reorder as document operations with invariants.
- Synchronise visible controls with the supported schema instead of exposing inert settings.
- Use schema fixtures and round trips to verify meaningful compatibility risks.
- Separate preview-only controls from exported product content and persisted document data.

## Preset and reusable-widget integrity

Trace every changed option across its canonical schema/registry, inspector control, renderer, default value, persistence and export/import adapter. For cards with nested widgets, verify slot ownership, parent/child identity, order, alignment, duplicate/reorder and supported nesting constraints. A renderer-only capability or an inert inspector setting is an incomplete feature.

Keep global presets, per-section overrides and preview-only controls distinct. Determine whether a change inherits a default or writes an override; reset must restore the intended inheritance. Switching typography should preserve the chosen system's weight, tracking and line height except for explicit overrides. Theme changes must reach nested widgets rather than only their outer wrapper.

For saved selections, test change, save, reload, export and reimport against representative documents. Inspect real storage behavior: local browser persistence is not a rewrite of a static JSON source file, and a downloaded export does not mean a server accepted an update. Apply migrations only within the authorized document scope and retain older document behavior according to the compatibility contract.

When a new library category or panel is added, reuse existing tree/selection/folder operations instead of creating a shadow model. Combine media-library for archive and conversion behavior. Preserve stable IDs through renaming, moving and duplicates; update references deliberately rather than resetting user data to clear errors.

## Precise acceptance additions

Record before/after document examples and the actual schema version used by each checked surface. Assert supported semantic equivalence after round trips, not necessarily byte equality if the format intentionally normalizes serialization. Verify malformed/unsupported input diagnostics without silently dropping content. Keep rejected fields visible in diagnostic evidence and never weaken validation to accept an unsupported widget.

## Stage handoff

Contribute the domain section to the selected stage's existing artefact and shared task record.

| Stage | Required contribution |
| --- | --- |
| Discover | Registry/renderer/persistence map and compatibility risks in the assessment. |
| Plan | Schema delta, migration policy, ownership and before/after document examples. |
| Execute | Assigned schema, adapter and UI changes; migrate only the authorised document scope. |
| Verify | Round-trip, save/reload and targeted history/selection results using representative fixtures. |

## Acceptance evidence

- Edit-save-reload-export-import preserves supported semantics and stable identity.
- Registry, inspector and renderer agree on supported fields and defaults.
- Existing documents survive migration; malformed inputs fail with useful diagnostics.

## Existing capability integration

- Scope caution: A native YAML converter owns mapping rules; combine lenses rather than invent another registry.

- Read the native editor kit or exported schema supplied with the task before mapping widgets.
- Use native-yaml-archives for package boundaries and React specialists for renderer state.
- Use the existing design-system and importer plugins for their supported widget conventions.
- Contribute to the shared stage record; do not introduce a second task or queue ledger.

## Failure modes

- Do not maintain separate handwritten registries for the inspector and renderer.
- Do not silently drop unsupported content or flatten editable widgets into embedded HTML.
- Do not reset saved workspaces to make a new schema appear to work.
- Do not infer a passing importer from valid JSON/YAML syntax alone.
