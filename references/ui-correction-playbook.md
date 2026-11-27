# UI correction playbook

Apply the rules relevant to the current brief. Each rule includes an acceptance check. The [machine-readable rules](ui-correction-rules.json) use the same identifiers. Use project-specific values only when the current brief or approved design system supplies them.

## UI-001 — Define the current visual contract

**Applies to:** All visual requests.

Classify the task as exact reconstruction, bounded adaptation, exploration or local correction. Record actual target inventory, presentation source, content source, allowed changes and protected properties. Reconcile later feedback only within its subject and scope; do not promote historic requests into current commands.

**Check:** Each target has a current brief and protected properties. Styling-only work preserves supplied copy and behaviour. A rejected concept is replaced only when replacement is requested.

## UI-002 — Trace the canonical component owner and reuse it

**Applies to:** Existing interfaces and approved donor templates.

Inspect the existing UI and trace the shared component, design token, preset and data owner before editing. Reuse approved navigation, table, settings and editor primitives. Do not invent tabs, notices, CTAs or new duplicate sections when the task is a local repair.

**Check:** Shared consumers receive consistent changes. Existing navigation, controls, data ownership and complete setting inventories remain functional. Protected component structures survive scoped content patches.

## UI-003 — Separate target content from template presentation

**Applies to:** Template adaptation, SEO pages and grouped designs.

Use the approved template for layout and the correct page source for copy and facts. Preserve locked headings and wording; adapt only authorized subject-specific values. Sharing a design does not share instance copy. Detect renamed donor clones and stale donor facts.

**Check:** Every supplied heading and required content block maps to output. Each target is checked against its own source. No invented product claims, timings or replacement copy are introduced by visual polish.

## UI-004 — Assess deliberate visual quality, not merely validity

**Applies to:** Layout, banner and gallery creation or review.

Critique composition, hierarchy, proportion, visual density, content purpose and meaningful detail in every target. Distinguish broken usability from basic but underdeveloped design. When a new concept is requested, change its underlying idea and composition instead of recolouring rejected work. Simplification must retain enough meaning and interest.

**Check:** Every target has a specific quality finding or a reasoned acceptable result. Improvement proposals name affected components and actionable changes. Native editor feasibility is recorded for proposed layout changes where relevant.

## UI-005 — Use a coherent palette in its actual surface context

**Applies to:** Visual colour and material choices.

Use the current design system and a deliberate coordinated subset of colours. Inspect artwork against its real hero or page background. Preserve purposeful colour when feedback rejects playfulness; avoid an all-green or colourless overcorrection. Show requested identifying card colours in the default visible state.

**Check:** Background, artwork, accents, text and interactions are inspected together. Palettes preserve brand role and useful hierarchy. Material recolours preserve approved geometry and camera.

## UI-006 — Verify typography and font loading

**Applies to:** Any visual typography change or inherited font contract.

Use supplied font assets and canonical typography tokens across all consumers. Inspect the computed font, fallback loading, weight, size, line height, wrapping and contrast in the rendered output. Treat explicit size caps as scoped requirements.

**Check:** Actual rendered font matches the supplied asset. Headings, body, labels, buttons and terminal text form an intentional readable scale. No clipped or avoidably wrapped action labels remain at supported widths.

## UI-007 — Inspect spacing, alignment and component proportions

**Applies to:** All visual components.

Measure rendered section and card padding, row baselines, grids, icon gaps, badge insets, button spacing and terminal proportions against the actual template or current design system. Fix the whole affected family. Inherit native presets instead of adding arbitrary local overrides.

**Check:** Sibling columns and rows align intentionally. Badges and highlighted text have visible suitable insets. Cards, headings and controls are symmetrical where the design requires it. Responsive changes preserve readable proportions without clipping.

## UI-008 — Preserve and exercise real UI behaviour

**Applies to:** Interactive applications and editor tools.

Review the actual user journey and expected state ownership. Controls must perform their stated action; focus must not retarget unrelated sessions or files. Test meaningful changed behaviour, including empty and populated states, rather than relying on a screenshot.

**Check:** Filters, density controls, folders, panels, modal controls and actions operate correctly. Disabled background work actually stops when that is the requirement. Focus and navigation do not unexpectedly mutate unrelated views or state.

## UI-009 — Reconcile every requested target and state

**Applies to:** All batch, family, gallery and multi-state requests.

Build the actual inventory from supplied files and requested targets. Treat user examples as diagnostic examples, not a reduced scope. Review every included layout and relevant hidden panel, palette, default state, viewport and exported variant. Deduplicate by content and intended identity; retain distinct requested variants.

**Check:** A per-ID matrix reconciles requested, inspected, repaired, blocked and delivered items. Each tab and FAQ panel is inspected where requested. Contact sheets support full-size review and do not replace it. The target count comes from evidence; an approximate historic number is not hardcoded.

## UI-010 — Perform rendered visual critique and report its limits

**Applies to:** Visual implementation and visual audit.

Open the actual final output in an available authorized rendering environment. Inspect desktop and mobile plus relevant interactions and full animation cycles. Record named defects, repair authorized defects, and rerun affected checks. Separate schema, source, screenshot, temporal and destination-import evidence.

**Check:** Evidence records target ID, output revision, viewport/state and observation. A successful build or validator is never reported as proof of visual quality. Blocked rendering is explicitly marked unverified; no fabricated screenshots or checks. Review-only requests remain review-only.

## UI-011 — Maintain native editor editability

**Applies to:** Tasks whose receiving format is native YAML or another editor schema.

Read the authoritative kit and approved native template. Map content to supported widgets, nesting and presets. Honor native-only requirements and only specifically authorized custom-code exceptions. Proposed improvements must describe a real supported widget composition.

**Check:** All generated widget types and properties pass the supplied validator. The complete content inventory is represented. Forbidden custom-code widgets are absent. A source HTML lookalike cannot substitute for a native editable payload.

## UI-012 — Preview the actual import payload and verify round trips

**Applies to:** Native editor deliverables.

Generate or verify HTML from the final native payload and provide it before user import when requested. Compare its source, hierarchy, content and rendered state with the supplied references. When access exists, verify import, editing, saving and reopening; otherwise state which parts remain untested.

**Check:** Each target has an independently openable matching preview. Preview and native export identify the same revision. Large previews are split only when the task or practical limits require it. Syntax, schema, render and receiving-editor checks are separately reported.

## UI-013 — Use the correct asset and preserve reference identity

**Applies to:** Image, icon, animation and archived visual retrieval.

Identify the exact source artifact, variant and latest applicable revision before work. Inspect references; keep approved silhouette, geometry, pose, angle, composition and content outside the requested change. Find real existing-site icons where required. Do not substitute a still, renamed image or unrelated gallery for a requested animation.

**Check:** Retrieved assets contain the requested concepts and variants. CAD remains genuine drawing rather than a desaturated photograph. Recolour-only output preserves other protected properties. Mismatches are described instead of asserting unsupported perfect fidelity.

## UI-014 — Inspect production image quality and compositing

**Applies to:** Raster, CAD and render assets.

Inspect full-size outputs on their actual destination surface. Check edges, transparency, clipped reflections, geometry, materials, illumination and transitions. Register CAD and realistic layers using fixed landmarks. Preserve source originals and separately requested variants.

**Check:** No visible rectangle, pasted cutout or clipped reflection breaks the intended compositing. Material and geometry match the authorized reference. Exported resolution and real detail are inspected, not inferred from file dimensions.

## UI-015 — Preserve persona traits and natural anatomy

**Applies to:** Requested persona or people imagery only.

Follow supplied persona prompts and reference traits while creating original brand-appropriate compositions. Inspect hands, pose, faces, texture and nearby callouts at display size and high zoom. Apply no-people or no-pointing constraints only to their named asset set.

**Check:** Every person matches the applicable persona reference. Hands, joints, body balance and facial rendering appear natural. Callouts and imagery relate to the target page. People-only and text/no-text variants remain complete.

## UI-016 — Make motion communicate a meaningful sequence

**Applies to:** Animated visual widgets and transitions.

Model the intended request, response, action or transformation before animating. Preserve approved geometry and paths; avoid arbitrary moving blocks. Verify startup, stages, readable holds, pacing, loop/stop behaviour, controls and a complete cycle. Timing belongs to its asset and latest scoped instruction.

**Check:** API/MCP or other semantic motion communicates the actual intended relationship. Markers stay on paths and layers remain registered. The requested playable format is delivered. Source sequence revisions do not become global duration or looping defaults.

## UI-017 — Keep shared design, instance copy and persisted state distinct

**Applies to:** Configurable studios and reusable design families.

Trace shared design choices separately from per-page content and per-item selections. Group design changes must preserve page-specific copy. Persist choices in the intended store, restore them on reopen and reflect them in previews and exports. Restore requested presets and individual editing.

**Check:** Group and individual changes affect only the expected owners. Save/reload recovers the selected values. Each copy preset populates all its intended fields. A download-to-desktop is not called server persistence.

## UI-018 — Verify export parity, isolation and dependency closure

**Applies to:** HTML/CSS/JS widgets, native wrappers and asset packages.

Export exactly the selected content, palette and enabled controls in the required format. Remove disabled presentation controls and unused palette definitions from source when required. Scope widget markup, CSS and runtime to a unique root. Reconcile standalone and bulk exports with previews and the requested inventory.

**Check:** Two widgets mounted together do not interfere. Individual and bulk downloads reproduce selected appearance and behaviour. Required native wrappers use their inherited presets. Requested source stripping is verified across HTML, CSS and JavaScript.

## UI-019 — Deliver the correct complete openable artifact

**Applies to:** Any visual handoff or download.

Check the actual archive and final openable files, not just local generation. Match the agreed destination and revision. Provide complete packages and page mappings when required; repair broken delivery. Do not replace a requested single ZIP with unexplained fragments or silently omit variants.

**Check:** Archive integrity, inventory and relative dependencies pass clean extraction checks. The actual recipient-facing link works when verification is available. Delivery limits are explicit and are not called successful downloads. Every promised artifact maps to the inspected revision.

## UI-020 — Preserve assets during cleanup and deduplication

**Applies to:** Media libraries and asset cleanup.

Determine duplication using actual content and relevant metadata, not filename equality. Preserve distinct variants and originals. For an authorized cleanup, create the required verified backup and use reversible organization where possible.

**Check:** Different files sharing a name remain distinct. Removal or hiding behaviour matches the current request. Backup and duplicate decisions are reviewable before destructive changes.

## UI-021 — Keep information architecture deliberate

**Applies to:** Existing pages, tables and editor workspaces.

Respect the requested hierarchy, section placement, navigation, table row structure and content grouping. Remove redundant content where authorized without dropping retained sections. Keep tasks and controls near the content they govern; avoid implementation jargon and unexplained controls.

**Check:** Parent/child rows have consistent useful information and clear indentation. Required stack sections stay outside tabs where specified. Omitted sections leave no empty placeholders. Body-link audits exclude chrome when that is the scope.

## UI-022 — Turn corrections into scoped regression checks

**Applies to:** Any follow-up visual correction.

Amend the current task record with the defect, affected family, protected properties and acceptance evidence. Recheck the same issue over the full authorized family. Preserve rejected/approved state and latest scoped decisions, but do not count repeated excerpts as independent failures.

**Check:** Named examples generate relevant family-wide checks. Rechecks are focused on actual risk and current scope. Unknown reference details are reopened or explicitly unresolved. A user-confirmed rejection is not treated as accepted work.
