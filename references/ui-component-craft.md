# Component diagnosis and repair

Read only the sections relevant to the current target after establishing its visual contract.
Use these techniques to make an observed problem actionable. The current brief, approved
reference, content source and receiving kit govern; an example here is not a new design preset.
Keep findings and before/after evidence in the existing [quality review](ui-quality-review.md).

## Contents

1. [Choose the cause before the treatment](#choose-the-cause-before-the-treatment)
2. [Terminals and static code illustrations](#terminals-and-static-code-illustrations)
3. [Badges, highlighted labels and icons](#badges-highlighted-labels-and-icons)
4. [Hierarchy, density and typography](#hierarchy-density-and-typography)
5. [Vertical tabs and nested sections](#vertical-tabs-and-nested-sections)
6. [Pricing and comparisons](#pricing-and-comparisons)
7. [Palette and artwork on the destination surface](#palette-and-artwork-on-the-destination-surface)
8. [Native-widget feasibility](#native-widget-feasibility)

## Choose the cause before the treatment

Name the visual consequence before proposing a style change: for example, the label merges
with its container edge, the illustration cannot be read at its displayed size, or the main
action competes with several equally prominent elements. Identify the element and state.

Trace the cause through the actual owner: missing/shared token, incorrect native preset,
parent sizing, local override, font fallback, asset crop or the composition itself.
Do not compensate for a wrong parent constraint with scattered child offsets.

Resolve the effective cascade before diagnosing a missing inset or redundant enclosure.
Inspect all rules that match the actual element, including specificity, `:is()` selectors,
later style layers and active viewport/container conditions. A base declaration may already
be reset by a more specific component rule. Use computed styles when available; in source-only
review, cite the applicable override chain and label unresolved conditions instead of treating
base CSS values as observed padding, borders or geometry.

Choose a repair that addresses that cause and respects the task's mode. A local correction
retains the approved composition; exploration may change it. A working simple layout can
be deliberate. Explain what a proposed addition would communicate before adding it.

Make each recommendation concrete: affected owner, changed relationship, expected visible
effect, protected properties and a check capable of detecting failure. “More premium,”
“better spacing” and “add interest” are diagnoses still waiting to be made.

## Terminals and static code illustrations

**Inspect.** Identify the panel's job: a static illustration, source code, a command example,
a live terminal or a language-switching demo. Inspect the supplied content contract first.
Read the complete panel at the size it occupies beside the heading and body, then at narrow width.

**Diagnose.** Separate an undersized outer panel from tiny internal type, oversized chrome,
excessive internal empty space, a constrained parent column or a scaled-down image/SVG.
Check whether the intended text is actual readable content or part of a bitmap/illustration.
A large surrounding card does not make a small terminal inside it readable.

**Repair.** Allocate enough width to the meaningful content, adjust the internal text scale
within the approved type system, and balance header, body and inset proportions together.
Let supplied short labels form a purposeful composition; avoid a large vacant shell.
If a fixed-size visual is the cause, correct its layout or source asset rather than enlarging
unrelated section padding. When rebalancing chrome and body spacing, inspect existing viewport
and container overrides: a change that preserves desktop height can increase narrow-layout height.
Preserve intentional scroll behaviour for genuine long code.

**Protect.** Keep the illustration's actual labels, claims and role. A source that authorizes
three static labels does not authorize fabricated shell commands, version numbers, logs,
latency, deployment status or live telemetry. Do not add copy buttons or animation to make
a static illustration appear more sophisticated. Preserve existing required controls when present.

**Verify.** Inspect both the whole section and the panel at normal display size. Confirm each
required label remains readable, chrome does not dominate it, and the mobile composition has
no unintended clipping. For interactive panels, separately exercise each changed action/state.
Record the native composition or actual custom-code constraint; terminal styling alone does
not imply that executable or language-switching functionality is required.

## Badges, highlighted labels and icons

**Inspect.** Examine the actual label box, glyph bounds, baseline and adjacent content.
Check default, wrapped and relevant selected/hover states. Identify whether the label is a
standalone badge, inline highlight, a control, or an item inside a larger card.

**Diagnose.** Determine whether missing space belongs inside the colored label, between an
icon and its text, between siblings, or around the parent. A roomy card cannot compensate
for a badge whose letters touch its background edge. Check inherited line-height and display
behaviour before prescribing a new margin or changing the type size.

**Repair.** Apply insets to the label's actual owner using the appropriate shared badge/token
or native part style. Coordinate horizontal and vertical breathing room with text size and
shape. Use the component's gap/alignment controls for icon/text separation. Size icons by their
visual weight as well as their box, and align them with the intended text line or group.

**Protect.** Retain meaning, wording, semantic color and interaction. Do not turn a fact label
into a button, replace the approved icon family, or change every badge because one local
instance is wrong. When the shared owner is at fault, inspect its relevant consumers.

**Verify.** Inspect real box edges and text at the required widths, including a longer/wrapped
label where the content allows it. Confirm visible insets, intentional baseline alignment and
no collision with adjoining copy. For controls, confirm focus visibility and the actual hit area.

## Hierarchy, density and typography

**Inspect.** State the section's main message, supporting evidence and next action. Trace the
reading order through the actual heading, paragraph, visual, facts and controls. Inspect the
whole section before individual details; view the requested surrounding sections for context.

**Diagnose.** Identify which relationship is weak: everything has equal emphasis; a minor
label dominates; related items look disconnected; repeated containers conceal grouping;
empty space separates a heading from its evidence; or important content is compressed.
First confirm the actual loaded font and weight. Fallback fonts can change wraps, density
and alignment, making downstream spacing changes a misleading repair.

**Repair.** Establish clearer relative prominence with the existing type scale and spacing
system. Group related content, distinguish meaningful groups and align shared reading edges.
Adjust column proportions or text measure where allowed before shrinking all type to fit.
Use surface contrast or selective emphasis where it clarifies a role; do not decorate every
element equally. Recompose an underdeveloped section only to the extent authorized by its mode.

**Protect.** Keep complete approved headings, copy and content order unless their change is
authorized. Do not shorten copy, add invented statistics, split facts into extra cards or
insert illustrations just to fill space. Preserve deliberate quietness and compact density
when they suit the approved design and task. Avoid imposing a universal section height.

**Verify.** Compare the before/after section at matching conditions. Explain how the primary
message is easier to find or the content relationships are clearer. Check resulting wraps,
reading length, action visibility and responsive order. An absence of overflow is only one
check; it does not establish a well-composed result.

## Vertical tabs and nested sections

**Inspect.** Read the approved grouping and inspect every requested tab panel, not only the
initial panel. Distinguish the selector, panel shell, heading/card structure and nested content.
Identify content explicitly required outside the tabs and preserve that placement.

**Diagnose.** Trace uneven edges or cramped panels to selector width, nested padding, reused
card presets, unnecessary wrapper layers or different content owners. Check whether a short
panel is being stretched to imitate a long one and whether duplicated headings add false hierarchy.

**Repair.** Reuse the prescribed selector and panel composition. Make shared inner edges,
heading treatments and content insets consistent through their canonical owners. Let legitimate
content differences remain visible; change sizing only where the reference or current brief
requires it. Use the actual native nesting contract rather than flattening panels into raw HTML.

**Protect.** Keep tab count, labels, order, default selection and source-specific panel content.
Preserve working keyboard/focus behaviour and the approved narrow-screen adaptation. A visual
repair does not authorize new categories, a different navigation pattern or moving external sections.

**Verify.** Open each required panel and compare its heading, body, controls and lower edge.
Exercise changed navigation at relevant widths. For native exports, check the documented pairing
of item entries and panel hosts, preview the payload, and report editor round-trip access separately.

## Pricing and comparisons

**Inspect.** Read across adjacent plans/columns and down equivalent specification rows.
Check plan name, price, period, renewal/discount explanation, action and details as one hierarchy.
Inspect long labels, highlighted plans, outer edges and narrow-screen table behaviour.

**Diagnose.** Distinguish row misalignment from text wrapping, inconsistent content groups,
different card padding, independent heights, hidden details or a misplaced action. Check whether
emphasis helps the intended comparison or makes every column equally loud.

**Repair.** Reuse the existing pricing/table owner and align equivalent information at that
owner. Coordinate label space, content spacing and action placement without changing facts.
Apply the requested shared borders, gaps and corner treatment consistently; those choices are
project contracts, not universal pricing rules. Preserve deliberate horizontal scrolling.

**Protect.** Keep plan identities, prices, units, billing periods, qualifiers, entitlements,
button destinations and default expansion. Do not invent a “recommended” or “best value” claim.
Changing a shared presentation preset must not overwrite per-plan data or row-specific styles.

**Verify.** Compare all affected columns and shared consumers, including the first/last edges.
Confirm the price and its qualifier remain associated, equivalent rows scan coherently and
controls remain usable. Compare the actual exported state with the selected preview.

## Palette and artwork on the destination surface

**Inspect.** Place the real artwork on its actual page/hero background. Review the composition
with nearby type, borders, actions and interaction states. Inspect transparent edges and dark/light
variants at their intended display size; an isolated image preview cannot establish harmony.

**Diagnose.** Separate a palette-role conflict from excessive saturation, competing accents,
insufficient foreground separation, an incorrect asset variant or a visible compositing rectangle.
Check whether the material itself or its background is causing the clash before recoloring either.

**Repair.** Assign approved colors clear roles and use the subset that serves this composition.
Tune their relative prominence within the authorized scope. Preserve enough contrast to keep
text and meaningful visual boundaries legible. Correct the asset/crop/compositing owner when that
is the cause; a global surface change may merely move the mismatch elsewhere.

**Protect.** Retain approved brand roles, material/geometry, transparency and semantic state
colors. A request for restraint does not mean removing all color. A different project does not
inherit this project's palette. Recoloring alone does not satisfy a request for a new concept.

**Verify.** Inspect the same asset on the final surface with its actual typography and controls.
Check required default and selected states, foreground contrast, crop and edge continuity.
For motion, also inspect the complete meaningful sequence; one harmonious frame is insufficient.

## Native-widget feasibility

Read the actual kit/catalog and applicable widget references before committing to a composition.
Map the visible role to a supported widget, its documented styling owner, nesting and responsive
controls. Prefer a built-in component when it supplies the required structure and behaviour.
For container-responsive rules, retain the measuring wrapper and threshold. Use documented
scoped CSS only when native controls cannot express that condition and the task permits it.

Static terminal-like illustrations may be composed from editable text and layout primitives
when the kit supports that composition. An interactive terminal, language switcher or animated
demo may require a different widget or custom-code implementation. Determine the actual need
from the content/interaction contract; do not choose from its visual resemblance alone.

When native-only scope conflicts with the kit's supported behaviour, identify the unsupported
part and the closest native composition. Do not silently insert an HTML/CSS/JS widget, flatten
editable content into an image, or call a reduced-behaviour approximation equivalent.

Validate with the kit's real command, render the final payload, and check content and appearance
separately. A valid schema establishes permitted structure; it does not prove visual quality,
installed fonts or successful import/edit/save/reopen in the receiving editor.

## Relationship to existing rules

This first-party reference elaborates UI-001–007, UI-009–012, UI-017–018 and UI-021–022 in the
[correction playbook](ui-correction-playbook.md). It supplies diagnosis and repair techniques;
the [quality review](ui-quality-review.md) still owns coverage and observation, and
[acceptance evidence](acceptance-evidence.md) still owns the existing completion artifacts.
