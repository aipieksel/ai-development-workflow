# Native YAML and archive conversion

Produce valid, editable imports and complete packages from supplied schemas, HTML and asset bundles.

Read the [shared specialist contract](../references/specialist-contract.md),
[task contracts](../references/task-contracts.md) and
[acceptance evidence](../references/acceptance-evidence.md).
This profile is a domain lens for existing stages, not a separate workflow or native agent registration.
Assessment and review are read-only; code writes require assignment by the selected execution stage.

## Use and exclude

- Use when: A ZIP, native editor YAML kit, HTML/JSON bundle or design-system export needs conversion or packaging.
- Use when: Editable widget mapping, source preservation or import compatibility is part of acceptance.
- Exclude: The task only needs a static screenshot or prose explanation.

## Discover the actual environment

- Inventory archive members, sizes, duplicates, entry points and expected deliverables.
- Identify the receiving editor version, schema, widget registry and preset format.
- Read the supplied kit and source page before assigning native widget mappings.
- Map fonts, images, scripts and relative paths to their intended package locations.
- Resolve source precedence and identify permitted embedded/custom-HTML regions.
- Check extraction paths and resource limits before materialising untrusted archive contents.

## Domain techniques

- Extract within a dedicated destination and prevent archive paths escaping that boundary.
- Use the parser's safe data mode; do not construct executable objects from YAML tags.
- Map content to supported native widgets and validate required responsive fields.
- Preserve order, IDs, labels, content and relationships through conversion.
- Keep unsupported mappings explicit; do not silently replace editable sections with HTML.
- Validate semantic schema constraints as well as YAML/JSON syntax.
- Build reproducible manifests/checksums when the delivery workflow requires them.
- Inspect the final archive itself for missing assets, broken paths and unexpected nesting.

## Widget capability mapping before construction

Identify the current supplied kit by version/path and read its instructions, schema, widget definitions, examples and supported renderer before mapping the page. A replacement kit supersedes the old contract; revalidate affected mappings rather than merging incompatible field names. A suggested widget name is not proof that the current registry supports it.

For each source section, record the source region, selected native widget, nested slots/children, required options, preset/token bindings and unsupported differences. Inspect the card widget's complete capabilities before recreating card internals. Use supported product collections inside tabs when that is the requested editable model; do not flatten a native products widget into decorative cards merely because the HTML looks similar.

Record an explicit custom-code allowlist from the current request. If only a map may use an HTML/CSS/JS widget, that exception does not extend to navigation, cards, pricing or an entire page wrapper. Preserve any explicit header/footer exclusions. When no supported native mapping exists, investigate another actual widget and document the limitation; do not invent a field, relax a validator, or modify the editor schema without authority for that prerequisite.

Map page presets to actual supported variables and design roles. Preserve bundled font assets and typography values, responsive properties, content order and nested editability. Validate variable references and overrides in the receiving format, not just in the source HTML. Keep the detailed widget/schema rules in the native builder and editor owner.

## Native acceptance sequence

Separate safe parsing, schema validation, supported-widget/field validation, actual editor import, rendered comparison and interactive edit/save/reload checks. Record which surfaces were exercised and the exact kit/output revision. Inspect native tabs/products/cards in the real receiving editor when available, including relevant responsive states. A custom HTML preview of the source is not evidence that the native YAML renders correctly.

Reconcile all expected sections and the custom-code exception list, then compare visible content, geometry, typography, assets and behavior to the supplied source. Use reference-fidelity for comparison conditions and artifact-delivery for package closure. If the host/editor is unavailable, complete structural work and label import/visual parity unverified rather than describing syntax-valid YAML as pixel perfect.

## Stage handoff

Contribute the domain section to the selected stage's existing artefact and shared task record.

| Stage | Required contribution |
| --- | --- |
| Discover | Source/member inventory, receiving contract and unsupported mappings. |
| Plan | Widget/content mapping, asset strategy and import acceptance criteria. |
| Execute | Assigned conversion/package changes using the existing converter or owner skill. |
| Verify | Schema results, inventory reconciliation and receiving-editor import/preview evidence. |

## Acceptance evidence

- Inventory and package contents reconcile with the requested source/deliverables.
- YAML/data validates against the actual receiving schema and widget registry.
- A real import/preview is verified where available; syntax-only validation is labelled.

## Existing capability integration

- If the receiving import/schema contract is unavailable, record that exact gap and do not invent compatibility.

- Use the schema and presets supplied for the current editor.
- Follow the receiving design system’s delivery and navigation requirements.
- Use the receiving application’s supported importer.
- Keep the canonical widget registry in its owning editor; combine editor-schema when needed.

## Failure modes

- Do not equate valid YAML with a supported native editor page.
- Do not omit assets or widgets to make validation pass.
- Do not rewrite the source design or content when the request is conversion.
- Do not report an archive as imported when only local packaging was verified.
