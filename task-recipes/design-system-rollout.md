# Roll out shared design changes

Update canonical components, typography and theme presets across a declared target set, checking affected states and exported outputs.

Read [the shared portable recipe contract](README.md) first. Use the authoritative expansion and recommended lenses in [catalog.json](catalog.json); adapt them to the current task and actual tools.

## Find the canonical system

Inventory the real component registry, shared section files, typography presets, color/mode/accent model, font assets, exported templates and all requested consuming pages. Read the owner design-system skill and its actual API. Use the approved preset rather than approximating its numeric values or copying component markup into parallel owners.

Separate requested token changes from properties to preserve. Typography includes family, weight, size, line height and tracking. Identify nested controls, active/hover/focus states, maps, icons, review graphics and calls to action that consume the changed tokens. Define a bounded coverage matrix across affected components and supported presets/modes/accents; disclose unsampled combinations rather than claiming exhaustive coverage.

## Propagate and verify

Change the canonical owner and verify representative consumers plus every specifically named exception. Check long headings, mobile wrapping, clipping and font loading. Exercise switches in both directions, save/reload where settings persist, and inspect canvas/preview/export parity when applicable. Keep native widgets and original approved interactions intact.

Open standalone exported sections and final pages with their packaged relative assets. Reconcile every requested target as changed or verified unchanged, with its own evidence. A demo page using the new tokens does not prove all consumers were updated.
