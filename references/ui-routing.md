# Automatic UI expertise and team selection

## Decide from the requested outcome

Assess the complete current task, adopted corrections, source and selected record. Apply
`specialist:ui-design` whenever the outcome creates, changes, assesses or repairs presentation,
interaction design, visual quality or visual assets. Apply it alongside relevant stack/format
knowledge, including follow-ups such as “the spacing is still wrong.” An ordinary attached
skill and explicit Auto use the same rule.

| Outcome | Relevant knowledge |
| --- | --- |
| Layouts, websites, sections, cards, tables, dashboards and navigation | UI design plus the actual frontend/platform owner. |
| Colors, palettes, typography, spacing, alignment, proportions and icons | UI design; design-system for shared owners; reference-fidelity for approved baselines. |
| Visual audit, critique or improvement proposal | UI knowledge within the selected read-only/Plan scope. |
| Native YAML, HTML/template conversion or editor presentation | UI plus native-yaml/editor-schema and the receiving kit. |
| Hero/CTA artwork, renders, image variants or reference-image corrections | UI plus image-art-direction/reference-fidelity and actual image tools. |
| Animation, demos, tabs/carousels and transitions | UI plus motion-interaction; inspect complete temporal behavior. |
| Filters, controls, focus, state, accessibility or feedback | UI plus the actual interaction/state owner. |

Pure backend/data/infrastructure work without a visible outcome is not UI work. Quoted old
requests, a color word in data or a frontend directory alone prove no applicability. Policy
work about UI does not itself authorize a website redesign. Image-only work uses actual image
inspection; native desktop work uses its real runtime rather than an invented browser.

## Classify the design contribution

Every v2 task declares actual UI facts:

```json
{
  "applicable": true,
  "kind": "design",
  "reason": "The requested correction changes layout and responsive navigation behavior."
}
```

| `kind` | Meaning | Required staffing |
| --- | --- | --- |
| `none` | No requested visual/interaction outcome; `applicable` is false. | The task's nonvisual team; no invented UI work. |
| `mechanical` | Apply an existing approved local label, token or component without new design decisions. | UI-capable Fast Builder and independent UI-aware Reviewer for Build. |
| `design` | Decide layout, palette, type, responsiveness, interaction or reference reconstruction. | Distinct UI Director before accepted planning; Builder and Reviewer for Build. |
| `shared` | Change shared UI/design-system decisions or consumer contracts. | Architect and UI Director plus Builder/Reviewer for Build, using waves if needed. |

The kind is an inspected fact, not a keyword classifier or speed waiver. New design cannot be
labeled mechanical to omit the UI Director. Shared UI cannot be classified local just because
one file changes. UI-only Plan/Review obtains useful design and independent criticism/corroboration
without adding a Builder or product writes.

## Carry complete expertise into actual work

Read [the full UI expertise](../specialists/ui-design.md), [UI Director](../agents/ui-design-director/agent.md)
and relevant capability instructions. Pass complete applicable knowledge to actual design,
implementation and independent review workers. Declare `ui-design` on their assignments and
record actual assignment-to-worker bindings and contributions. A specialist catalogue row,
profile name or summary alone proves no dispatch.

A separate UI Director is required for design/shared work, with the real source/reference/state
brief before the affected plan and criticism. Mechanical work may combine UI expertise with
Builder; rendered acceptance remains independent. Relevant operations remain authoritative:

- Audit/review/research: inspect and report, no repairs.
- Plan/specification: implementable direction and measurable acceptance, no build.
- Mockup-first: deliver the agreed mockup and preserve its implementation boundary.
- Authorized Build: implement the admitted scope and independently check its visual result.
- Help/no-task/status: preserve current selection; a policy pointer starts no invented task.

Inspect approved references, existing tokens/components, requested pages, viewports and states.
Verify actual rendering and relevant interactions. Record what remains unverified; markup,
schema and build success cannot establish visual parity. Domain kits/editor/image tools keep
their real ownership. Respect explicit current user exclusions through truthful scope/policy
reconciliation rather than falsely declaring non-UI applicability or pretending a gate passed.

## Selection, validation and continuation

Select `specialist:ui-design` when applicable. Existing explicit visual operations require it;
a false/omitted applicability field cannot waive their knowledge requirement. Legacy evaluated
rows may remain source evidence, but active v2 records need the full current declaration.
Record substantive UI authors in `authorIds`; they cannot independently criticize their adopted
specification or accept the resulting design by changing profiles.

The router describes required duties from supplied `uiContext` and verification facts. It does
not render, dispatch or inspect the request itself. Source/capability changes affect catalogue
and policy fingerprints. Reconcile affected pending work while preserving current verified
outcomes. Use [task routing](task-routing.md), [contract records](workflow-contract-records.md)
and real rendered evidence to complete the task.
