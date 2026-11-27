# Reference fidelity and precise corrections

Reconstruct or improve supplied work while preserving its approved identity and checking the exact requested change.

Read the [shared specialist contract](../references/specialist-contract.md),
[task contracts](../references/task-contracts.md) and
[acceptance evidence](../references/acceptance-evidence.md).
This is a lens on the assigned stage. Assessment/review remains read-only; a repair needs an implementation assignment.

## Use and exclude

- Use for a rebuild from HTML, screenshots, an extraction or another approved artifact; for a narrowly specified visual correction; or for repeated feedback that prior work changed the wrong things.
- Combine with the actual format/runtime owner: a browser page, native YAML editor and raster image require different implementation and comparison tools.
- Exclude a purely functional change with no reference or preservation requirement. Do not turn an explicitly exploratory brief into a pixel-matching assignment.

## Establish the comparison contract

Identify the exact reference file/version and output being changed. Read the current request and corrections alongside the relevant original source; older accepted content is an invariant unless the current request changes it. Record unavailable references rather than silently choosing a similar-looking file.

Use the task's transformation mode: reconstruct, adapt, explore, correct, integrate or analyze. For each affected target, record the permitted delta and retained properties. Examples of distinct properties are object shape, arrangement, copy, typography, animation logic, color and export format. Permission to change one does not imply permission to change all of them.

For a correction list, retain one identifiable item per requested fix. Map it to the owner, observed defect, intended outcome and verification surface. Mark approved items to preserve. A short correction can use a few lines in the existing record; do not require a second planning document merely to adjust one property.

## Work from evidence

- Inspect the actual baseline before editing. For a UI, capture route, viewport, mode, font readiness, scroll position and relevant control state. For an image, inspect dimensions, composition, orientation, edges and transparent regions using supported tools.
- Trace the cause to the shared component/token/asset when applicable. Do not mask a common defect with inconsistent page-specific patches.
- Use reference assets, text and logic when their reuse is requested. Recreating an approximate terminal, logo, card or animation is not equivalent to reusing the supplied one.
- For variants, enumerate expected targets and the allowed variation axes. Genuine concept exploration needs distinct concepts; reference-locked variants keep the chosen composition and vary only authorized properties.
- Make the smallest coherent change that satisfies the accepted requirements. When a dependency must change, explain the dependency and expand the plan's affected checks rather than quietly broadening the redesign.
- Compare the changed output to both its source and its pre-change state. Confirm an observable improvement on the named defect and check retained properties for regressions.
- Continue the same task record on feedback. Reopen affected findings and checks; preserve valid evidence for unchanged work and invalidate evidence for changed revisions.

## Stage handoff

| Assigned stage | Concrete contribution |
| --- | --- |
| Assess/research | Reference inventory, source identities and an annotated discrepancy list with unknowns. |
| Plan/critique | Allowed deltas, protected properties, target ownership and comparable before/after checks. |
| Implement | Assigned corrections against the approved source, with target-level change notes. |
| Review/verify | Each correction's observed result, retained-property checks and any unresolved mismatch. |

## Acceptance evidence

Every requested target reconciles with a changed, retained or explicitly blocked disposition. Evidence identifies the actual output revision it checked and the comparison conditions. Check geometry, content, styling and behavior separately where they matter: a screenshot cannot prove a button or animation works, and a parsed DOM cannot prove visual parity.

Use a supported image/render comparison when exactness is claimed. Document renderer, dimensions, alignment and any tolerance; a subjective score or a screenshot's existence is not a pixel-equality result. If no renderer/reference is available, report which structural checks passed and leave visual parity unverified. The optional acceptance-matrix validator checks declared coverage and revision bindings; it cannot judge similarity or authenticate a review.

## Ownership and failure modes

Use the current design-system, image, native-YAML, browser or importer skill for its detailed rules. This lens does not authorize changing those plugins or bypassing their host capabilities. Ask for missing source only when necessary after completing useful independent work.

Do not silently replace a reference, delete a difficult target, regenerate an approved base merely for convenience, or claim that an unchanged preview proves a correction. A newly generated picture is not evidence that approved pixels were preserved. Keep proof files out of the product UI unless requested.
