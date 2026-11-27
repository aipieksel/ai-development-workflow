# Motion, interactive widgets and temporal verification

Reconstruct or refine meaningful animation sequences and interactions, then verify them over time in their actual visual context.

Read the [shared specialist contract](../references/specialist-contract.md),
[task contracts](../references/task-contracts.md) and
[acceptance evidence](../references/acceptance-evidence.md).
Use the assigned stage's existing artifact and write boundary.

## Use and exclude

- Use for animated hero widgets, terminal sequences, maps, carousels, tab cycles, transitions, playback controls or state-dependent visual defects.
- Combine design-system for palette/type coverage, reference-fidelity for supplied logic, and the actual frontend/runtime specialist for implementation.
- Exclude static imagery or backend streaming with no animation problem; realtime session/resource ownership belongs to realtime-native.

## Model behavior before changing it

Read the supplied JavaScript/CSS and observe the current behavior with available browser tools. Identify the state machine, event/timer ownership, startup state, sequence order, transitions, dwell times, repeat behavior and user overrides. Separate animation duration, reading time and interval between scenes: a single speed slider may not correctly control all three.

List each target widget and the message its motion should communicate. Examples include work progressing, a terminal session advancing, containers starting or selected content changing. Decorative floating does not substitute for the requested behavior. Match product-specific labels/assets to the actual subject without inventing live metrics.

## Implement and observe

- Preserve the supplied logic and accepted visual structure when the task asks for adaptation or repair. A color-palette example is not permission to replace its recipient's animations.
- Fix transitions at the actual state/layout boundary. Check jumps, flashes, reflow, briefly unreadable states, clipping and height changes, including the loop back to the start.
- Balance legible typing, useful state dwell and noticeable movement. Use the requested timing or observed reference; do not blindly speed up or slow down every widget together.
- Verify tabs and automatic sequences stay synchronized. Manual navigation, pause/restart and speed changes should not leave duplicate timers, skipped states or an obsolete active label.
- Keep configuration controls in the requested preview/studio surface rather than cluttering the final banner. Hiding controls must not silently disable the animation or change its layout contract.
- Apply themes to the animated states as well as the initial frame. Verify foreground contrast on highlighted nodes, active tabs, terminal surfaces, maps and layered illustrations.
- Respect existing accessibility and reduced-motion behavior; preserve meaning and usable controls when motion is reduced. Do not introduce flashing to make a barely visible effect more noticeable.
- Distinguish illustrative network/performance animation from measured telemetry. An animation's speed is not evidence of actual latency, throughput or deployment duration.

## Stage handoff

| Assigned stage | Concrete contribution |
| --- | --- |
| Assess/research | Target/timeline inventory, observed temporal defects and reproducible trigger/state. |
| Plan/critique | Sequence/state contract, retained logic and runtime observation cases. |
| Implement | Assigned animation/interaction fixes with clear event and timer ownership. |
| Review/verify | Complete-cycle observations, control/state checks and any unobserved paths. |

## Acceptance evidence

Observe at least one complete relevant cycle, including the loop boundary, for changed sequences. Exercise relevant manual controls and alternative modes. For long sequences, record timestamped state checkpoints and transition observations using supported tools; do not claim full-cycle review from a few sampled stills. Verify a hidden/remounted widget or repeated initialization when its lifecycle changed.

Record the output revision, viewport/theme, sequence or events observed, timing findings and actual result. Use recordings where available and useful; otherwise record observed state transitions honestly. Screenshots support layout/contrast findings but cannot establish smoothness, pacing or control behavior by themselves. A structural acceptance-matrix pass cannot establish temporal quality.

## Ownership and failure modes

Use available browser/testing skills under their current host contract. Do not assume arbitrary browser evaluation, recording, access to user sessions or a native runtime. A missing runtime leaves temporal behavior unverified even if code and unit checks pass.

Do not replace meaningful content with generic motion, remove an animation to obtain a stable screenshot, simulate a live benchmark, or treat a build pass as an animation review. Recheck affected timelines after implementation fixes; keep accepted widgets unchanged unless the shared cause requires a documented update.
