# UI direction, audit and fidelity capabilities

Read the complete canonical [UI expertise](../../specialists/ui-design.md) and its required
correction, component-craft and rendered-review references. Apply the
[worker contract](worker-contract.md). These sections preserve design/reference knowledge across
UI Director, Builder and independent reviewer/verifier assignments; selected operation scope
still governs writes. A reference, mocked screen or source scan does not prove behavior.

## audit-ui — actual existing UI

Inspect the existing affected application first, with its components, tokens, typography, spacing,
motion, responsive states, behavior, accessibility and accessible reference. Capture the baseline
before edits and separate existing failures from missing requested behavior. Identify canonical
component/design-system owners and protected properties. Distinguish observed values from estimates
and never claim a visual audit without rendered evidence. Report functioning but underdeveloped
layout as well as defects. Save concrete gaps, measurements and source paths in the selected audit
artifact, such as `artifacts/design-audit.md`; audit does not authorize production edits.

## design-ui — an implementable specification

Consume the actual audit, request and adopted corrections. Recommend one coherent direction,
mapping every requested section to existing components/tokens, supported breakpoints, content
hierarchy, loading/error/empty/success states, interactions and accessible labels/keyboard/focus.
Preserve brand, functional controls, inherited fonts, icons and theme controls. Do not create a
replacement design system without a source-backed need and authority.

Use an existing persistent design-context sheet when available; otherwise record discovered tokens
and owners in the audit. Define permitted deviations, exact owner components and measurable
before/after acceptance. Include native-format feasibility when applicable. Repository-backed
inspiration is conceptual input with provenance/license checks, not permission to copy. Return the
selected specification (`artifacts/design-spec.md` or `UI-SPEC.md`); static mockups do not establish
functional parity. This advice is not implementation permission.

## visual-fidelity — equivalent reference and result states

Preserve the source reference unchanged. Deliver requested changes and user-approved omissions,
branding or adaptations; do not import an unrequested feature wishlist. Start with the target
application and nearest comparable controls, including open/closed states. Trace DOM/classes,
roles, attributes, imports, variants, configuration and handlers to the actual source primitive.
Interact to distinguish popover, menu, select, combobox or dialog; class names are not proof.
Observe trigger/selection, keyboard navigation, Escape/outside-click, focus return, placement,
portal and state ownership. On new pages inspect shared primitives rather than invent a baseline.

A broken capture is problem evidence, not an approved target. For tables and dashboards use
[data presentation](../visual-fidelity/references/data-presentation.md), including real aggregation,
complete query boundaries, entity rows, truthful outcomes and wrapper geometry. Do not redesign,
hide failures or treat an incomplete capture as proof of backend behavior.

Then inspect supplied HTML/assets, screenshots or the named reference state. Without external
reference, use the requested outcome and verified local pattern. Screenshots support only visible
details: image-derived measurements are estimates, not computed CSS; hidden interactions remain
unknown. Record unavailable fonts/assets/states rather than claim parity.

Inventory the whole requested surface, including below-fold and horizontal content:

- Structure: hierarchy, regions, headings, approved text, images, icons and badges.
- Controls: purpose/role, count, order, grouping, visible states and observed action outcome.
- Geometry: container/hero/sidebar and table/row/column sizes, control/icon size, alignment,
  padding, gaps, wrap, overflow, clipping and sticky behavior.
- Styling: actually loaded fonts, sizes, weights, line heights, colors, borders, radius and shadow.

Match controls by purpose/state, not counts alone. Exclude hidden responsive duplicates and nested
SVG nodes; virtualized visible rows are not dataset totals. Compare with the same browser, viewport,
zoom, theme, data and state after fonts/assets/layout settle. Label CSS-pixel coordinates and scroll
offsets. Set justified precision before editing and do not relax it to excuse mismatches.

Use `Item | Requested target | Current | Action/reuse owner | After/evidence` with present/missing/
incorrect and keep/fix/add decisions. Keep matching items without duplicating/replacing them; retain
exclusions and unavailable evidence. Return the inventory to planning and the same existing checklist.
The checklist communicates progress; it is not an extra approval ceremony.

## Builder and verification handoff

The admitted Builder configures/composes real shared primitives, handlers, tokens, icons and lifecycle
before extending an owner. A new primitive needs an evidenced gap. Preserve callers and avoid copied
lookalike markup, parallel menus/modals/state stores, hard-coded theme overrides and a new UI library.
Resolve ordinary details from local patterns; only genuinely missing essential information blocks
dependent work. Implement missing/wrong elements, then geometry/typography, then detailed styling.

The independent reviewer/verifier reopens and remeasures the actual final result and original comparable
controls. Exercise action outcomes, applicable persistence, focus/dismissal, responsive states, overflow
and console errors. Inspect screenshots and enlarged crops; use overlays without stretching/replacing
the baseline. Distinguish magnification from actual page zoom. Recheck evidence invalidated by repairs.
Report matched, mismatched, intentionally adapted and unverified items. Builds, equal counts and saved
screenshots alone do not establish fidelity; unverified required outcomes remain open.
