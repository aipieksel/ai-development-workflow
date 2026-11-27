# Visual quality review and complete target coverage

## Establish the expected set

Read the real source inventory and current request. Enumerate each requested page/layout/component,
asset variant and required state. Preserve stable IDs. Treat a stated approximate count as a clue;
resolve the actual count from the files. Examples such as one poor terminal or badge are diagnostic
seeds for an all-layout review, not permission to inspect only those examples.

Use the existing task record and [acceptance evidence](acceptance-evidence.md). Record the expected
set before repair, so a failed target cannot disappear from the denominator. Keep a compact correction
table for a single local edit; do not impose a batch manifest on a trivial repair.

## Inspect the actual output

Open every requested target in the relevant browser, native application, editor renderer or image viewer.
Inspect full-size readable content, relevant below-fold regions and hidden panels. A contact sheet is a
navigation aid. Inspect affected desktop, intermediate and small viewport behaviour according to the
current target contract, including intentional internal table scrolling. Load actual fonts and assets.
Observe full meaningful animation cycles and changed transitions where motion is in scope.

Keep source and output comparable: revision, viewport, zoom, data, theme, font, selected tab and timing.
Measure geometry from the runtime where available; label screenshot estimates as estimates. Confirm
that the page being reviewed is the actual final output rather than a stale preview. Use available
authorized browser/rendering capabilities and the kit's real tools; do not invent unavailable commands.

## Review working layouts as critically as broken ones

| Dimension | Concrete inspection |
|---|---|
| Purpose and hierarchy | Is the main idea and next action clear? Do heading, copy and visual reinforce it? |
| Composition and density | Are relationships deliberate, proportions balanced and useful detail sufficient? Is empty space serving the composition? |
| Spacing and alignment | Check real outer/inner padding, highlighted-text insets, card gaps, baselines, icons, button groups and sibling edges. |
| Typography | Confirm loaded family, weights, scale, line-height, wrapping, line length and readable labels/terminal output. |
| Palette and surfaces | Inspect foreground, background, artwork, borders and hover/focus/selected states together. Use a coherent subset of approved colours. |
| Components | A terminal needs believable proportions and readable task-appropriate content; a badge needs padding; a comparison needs scannable aligned information. |
| Assets and identity | Check correct source/variant, crop, edges, transparency, geometry, material, persona traits and destination-surface harmony. |
| Behaviour and access | Exercise changed actions, keyboard/focus, pending/error/empty states, overflow and persistence. Remove duplicate focus rings without removing focus visibility. |
| Native feasibility | Map each proposal to actual supported widget types, fields, nested structure and presets in the supplied kit. |
| Export and delivery | Verify selected copy/palette/settings survive the actual native/standalone export and intended opening context. |

A clean build, valid YAML or absence of clipping does not establish deliberate design quality. Identify
underdeveloped but working layouts, repetitive default compositions, weak hierarchy, oversized empty
areas, cramped meaningful content and decorative detail with no purpose. Each recommendation must
explain a concrete visual change and its effect. Respect approved simplicity and reconstruction targets;
quality improvement does not authorize new copy, extra features or a different brand.

Use [component diagnosis and repair](ui-component-craft.md) for the affected component family.
Name the actual owner and cause before prescribing a treatment; measure the visible relationship
that should change. Preserve deliberately simple work and source-only illustrations.

## Record findings in the existing evidence artifacts

For each target retain these fields in its review table or linked observation:

`Target ID | Output/source revision | Viewport/state | Observed issue | Functional severity |
Improvement potential | Concrete change | Protected properties | Native mapping/feasibility |
Evidence | Recheck state`

Functional severity can be blocking, major, minor or none. Improvement potential is a separate judgment
of how much a composition can benefit: high, medium, low or already deliberate. Explain both from
observations. Avoid arbitrary self-awarded quality scores. A target with no blocking defects still
needs a reasoned quality assessment. Native feasibility is not applicable to non-editor work; if the
kit is missing, record the mapping as unresolved instead of inventing widget support.

When multiple observations share a cause, link a family finding while keeping every target's inspection
and result visible. Report all requested issues; prioritization may order the report, not omit less
urgent targets. Clearly distinguish a user's reported defect from a defect independently observed now.
Historical labels such as B13/M04 do not establish exact geometry without their source visuals.

## Repair and verify

For authorized changes, fix the canonical owner with the smallest complete scoped change. Recheck every
affected target and protected neighbour required by the contract, including shared consumers. Verify
that the original complaint is observably resolved and that changes did not remove approved details.
For audit-only work, deliver the complete actionable findings and native feasibility without editing.

State requested, inspected, repaired, rechecked, unresolved and delivered counts separately. Every
required target/state needs current evidence; unobserved or inaccessible results remain blocked or
not-run. A sampled inspection must never become an exhaustive visual claim. Do not call the result
perfect, user-approved or fully verified when any requested outcome remains unobserved.
