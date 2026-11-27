# React and frontend systems

Apply the existing workflow to React interfaces, reusable components, responsive behaviour and frontend performance.

Read the [shared specialist contract](../references/specialist-contract.md).
This profile is a domain lens for existing stages, not a separate workflow or native agent registration.
Assessment and review are read-only; code writes require assignment by the selected execution stage.

## Use and exclude

- Use when: React or Next.js components, application routes, state-driven UI or frontend regressions are in scope.
- Use when: Shared design tokens, component APIs or rendering performance affect the requested change.
- Exclude: The task is only static content conversion with no React runtime.

## Discover the actual environment

- Read package and lockfiles for React, framework, router and build-tool versions.
- Find route entry points, shared components, tokens and the actual source of UI state.
- Map data fetching, loading/error states and client/server boundaries only where relevant.
- Inspect the supplied reference and current rendered behaviour before proposing layout changes.
- Identify existing lint, type, component and browser checks and their realistic cost.
- Record who owns each affected component and which routes reuse it.

## Domain techniques

- Preserve the established component API; extract shared behaviour when reuse is demonstrated.
- Keep transient UI state local and durable settings in the existing persistence owner.
- Trace stale closures, subscriptions and derived state before adding effects or memoisation.
- Apply performance changes to measured bottlenecks; avoid blanket caching and memoisation.
- Gate framework-specific APIs on installed versions, especially React 19 and server features.
- Check loading, empty, error, disabled and narrow-screen states for changed interactions.
- Use existing typography and spacing tokens; approved copy and assets remain the reference.
- Exercise theme/accent propagation through shared header, footer and component boundaries.

## Stage handoff

Contribute the domain section to the selected stage's existing artefact and shared task record.

| Stage | Required contribution |
| --- | --- |
| Discover | Component/state map, affected routes and reproduction evidence in the existing assessment. |
| Plan | Owned files, component contract, state transitions and observable acceptance criteria. |
| Execute | Only assigned implementation changes, with meaningful checkpoints and scoped checks. |
| Verify | Interaction results and relevant build/type output; delegate visual, a11y and performance gates. |

## Acceptance evidence

- Affected user journeys work at the required viewport and theme states.
- State and component ownership match the existing architecture.
- Relevant build, type and interaction evidence is recorded; visual review is separate.

## Existing capability integration

- Scope caution: An installed design-system skill owns the detailed visual contract; use it alongside this lens.

- Use the installed frontend builder/testing or React guidance when the environment exposes it.
- Use the user's design-system builder for supplied tokens, page kits and shared section contracts.
- Keep editor import/export invariants in the editor-schema lens when both apply.
- Use existing visual-fidelity and accessibility agents for those reviews instead of duplicating them.

## Failure modes

- Do not replace an accepted widget to solve a local palette or animation defect.
- Do not introduce new font scales, component variants or UI controls without task evidence.
- Do not call a compile pass proof of rendering, interaction or persistence.
- Do not assume Next.js, server rendering or a particular state library from the word React.
