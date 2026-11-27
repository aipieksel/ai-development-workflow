# Shared design systems, typography and presets

Maintain a coherent component system across pages, states and exported artifacts without flattening approved design choices.

Read the [shared specialist contract](../references/specialist-contract.md),
[task contracts](../references/task-contracts.md) and
[acceptance evidence](../references/acceptance-evidence.md).
Apply this lens within the selected stage and its existing write boundary.

## Use and exclude

- Use for shared sections, token changes, typography systems, icon libraries, light/dark/accent modes, rebrand controls or component catalogs.
- Combine with reference-fidelity for exact corrections, motion-interaction for animated components, and editor-schema for saved configuration or preset models.
- Exclude a one-off illustration with no shared design contract. Do not introduce theme switching, a catalog or a token migration when the task only changes isolated copy.

## Resolve canonical owners

Inventory approved components, current token/preset files, font binaries and declared weights, icon assets, reference pages and consuming outputs. Identify which implementation owns each family: header/footer, tabs, cards, pricing, reviews, maps, FAQs or other actual components. Use their real names and source paths rather than assuming a fixed product catalog.

Read the current specialized design-system or page-builder skill when available. Its schema, tokens and delivery rules remain canonical. Record a source conflict and resolve it using the current task contract; do not combine incompatible historical palettes or fonts into an invented third system.

## Implement and check the system

- Map typography by semantic role: page/section/card headings, descriptions, labels, prices, navigation and code. Preserve family, weight, tracking and line height unless those properties are part of the requested change. A size adjustment is not permission to normalize every typography preset.
- Verify font files load at the intended weights and that computed styles resolve as expected. Cover long labels and the relevant desktop/tablet/mobile widths; do not declare success from a font-family declaration alone.
- Keep reusable component structure, behavior and tokens together. Roll changes through actual consumers and account for independently opened HTML exports, not just the showcase that supplies global CSS.
- Trace theme/mode/accent values into nested headers, footers, buttons, borders, icons, maps and active/hover/focus/disabled states. Distinguish semantic text/surface/border colors from a third-party logo's identity colors.
- Check card hover borders for clipping, overlap and layout shifts; check icon alignment, arrow geometry and text wrapping across sibling components. Fix the owner so shared components remain shared.
- Build an icon inventory from actual usage, including supporting feature icons and arrows. Reuse a canonical asset per meaning; a generic server symbol is not automatically appropriate for support, sales or navigation.
- Keep preview configuration controls outside the intended product composition. Preserve requested controls in the studio while making the production export render the chosen design without unsolicited badges or editor UI.
- For persistent presets, trace read, update, save, reload and export/import. A static browser page cannot silently rewrite its source JSON without a supported write capability. State the actual persistence mechanism and expose export only when required.

## Stage handoff

| Assigned stage | Concrete contribution |
| --- | --- |
| Assess/research | Component/token/font/icon ownership map and state-specific defects. |
| Plan/critique | Consumer rollout list, property-level change scope and representative state matrix. |
| Implement | Assigned canonical component/token/preset changes and affected consumer updates. |
| Review/verify | Font loading/computed-style evidence, rendered state checks and preset persistence results. |

## Acceptance evidence

Create a matrix proportional to the change: changed component families, supported modes/accents/type sets, meaningful interaction states and required viewport boundaries. Cover every affected state or explicitly record what was sampled and what remains untested. Prioritize changed combinations, contrasting surfaces, long labels and shared defaults instead of blindly generating a large Cartesian product.

Record actual source/output versions, screenshots or measurements and interaction results. For multiple outputs, reconcile the expected consumer list; showing one correct page does not prove the catalog or all exports were updated. When settings persistence is in scope, demonstrate save/reload and round-trip behavior rather than reporting that a selector exists.

## Ownership and failure modes

Use the design-system/page-builder plugin for its styles and component rules; use native YAML/preset owners for that export format. Keep commercial facts and live prices in the project's content source, not this lens.

Do not replace shared components with similar-looking local copies, recolor every logo indiscriminately, change text to conceal wrapping defects, or call a build pass visual verification. Do not publish a mockup or update a shared plugin when the current request reserves approval for that step.
