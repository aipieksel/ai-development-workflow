# Extend an existing media workspace

Integrate media conversion or navigation into the current library, reusing folder identity, tree controls, drop behavior and persisted state.

Read [the shared portable recipe contract](README.md) first. Use the authoritative expansion and recommended lenses in [catalog.json](catalog.json); adapt them to the current task and actual tools.

## Integrate into the existing workspace

Read the current library tree, category tabs, folder/file identities, canvas controls, metadata, persistence and drag/drop handlers. A quoted standalone brief does not override a later instruction to integrate into the existing app. Use the actual shared sidebar and interaction primitives; conversion settings belong in the established control surface, not a new competing sidebar by default.

Map folder drops, individual files, default destinations, duplicate filenames, nested paths, selected item, favorites and sort/group state. Preserve original user assets and keep imports separate from code publication. Determine which metadata is actually available; do not label everything undated when created/modified values exist.

## Exercise user journeys

Test drop into every supported surface, folder creation, default grouping, automatic conversion where requested, selection-to-canvas navigation, sorting, favorites and save/reload. Test a representative malformed or unsupported input and interrupted processing. Compare source/output quality with meaningful media fixtures; an SVG extension alone does not prove editable vector geometry or scalable fidelity.

Verify state ownership and async cancellation so navigation does not lose results or duplicate work. Use current repository policy for checkpoints when authorized, and report source, saved data, package and deployment status separately.
