# Realtime media and native application lifecycles

Verify event-driven chat/media or native desktop behaviour in the actual supported runtime.

Read the [shared specialist contract](../references/specialist-contract.md),
[task contracts](../references/task-contracts.md) and
[acceptance evidence](../references/acceptance-evidence.md).
This profile is a domain lens for existing stages, not a separate workflow or native agent registration.
Assessment and review are read-only; code writes require assignment by the selected execution stage.

## Use and exclude

- Use when: The actual repository uses realtime chat/media, WebRTC, streaming or multi-window state.
- Use when: A native macOS application or SwiftUI/AppKit bridge is explicitly part of the task.
- Exclude: A device mentioned in conversation is only the user's computer, not the project target.
- Exclude: The task is static frontend work with no realtime or native lifecycle.

## Discover the actual environment

- Detect the actual runtime: browser/WebRTC, desktop wrapper or native SwiftUI/AppKit.
- Read package/SDK/deployment versions and supported platform constraints.
- Map message/session identity, media tracks, windows and state ownership.
- Trace connection, permission, focus, background and teardown events relevant to the change.
- Locate the actual test host and available camera/media/native capabilities.
- Record which parts can be simulated and which require a real runtime.

## Domain techniques

- Keep conversation and participant identity stable across updates and view changes.
- Separate unread counts, previews and selected-thread state to prevent accidental blanking.
- Handle reconnect, duplicate/out-of-order events and cancellation explicitly.
- Dispose subscriptions, tracks and connections at the correct owner boundary.
- Verify pop-out/pinned layouts against real state transitions, not only screenshots.
- For native code, respect SwiftUI/AppKit ownership and use narrow documented bridges.
- Check creation, update and teardown paths for native view/coordinator integrations.
- Use observable state for readiness; persistent streams need not become network-idle.

## Message and view lifecycle checks

Trace incoming/outgoing message identity, optimistic local state, delivery acknowledgement, retry, deduplication and persisted history through the actual protocol. Use stable correlation appropriate to that protocol; do not rely only on displayed text or arrival order. Exercise duplicate/out-of-order events and failed/retried sends so a successful send is visible without producing a second message.

Map conversation/participant/room identity independently of selected thread, preview, unread state and visible layout. Opening one conversation must not blank unrelated previews or erase history. Test the actual transition or timer that loses messages; merely extending an assumed timeout does not fix an ownership or persistence defect.

Separate view visibility from session lifetime. Hiding/minimizing a room or detaching a chat canvas must not terminate subscriptions required by direct messages if the task expects them to remain active. Conversely, closing the actual session should clean them up. Verify show/hide, popout/rejoin and reconnect against this ownership contract; do not keep every disposed view alive to hide a leak.

Synchronize supported settings across live views, including typography and unread-display choices, without requiring users to close/reopen unless that is an explicit runtime constraint. Preserve sender and room identities/history across the configured persistence boundary; use available data rather than inventing identity matches.

## Camera and multi-window ownership

Map each device stream, track, renderer and room consumer. Where rooms display the same camera, reuse the owned source as supported by the actual SDK and avoid unintended duplicate captures or tiles. Detaching one consumer must not stop a track still used by another; final owner teardown should release it.

Verify pinned/selected room media, camera position, stacked/side layouts and saved-reply controls in the actual main and popout views when relevant. Inspect requested and resolved media constraints, aspect ratio and rendering scale before attributing quality loss to the device. Do not claim an OBS or native-camera comparison without observing the relevant evidence.

Use synthetic or explicitly authorized test media where possible. Do not record, transmit or publish real user media as incidental testing. Distinguish lifecycle logic verified in a harness from camera permissions, device behavior and native window behavior that require a real host.

## Stage handoff

Contribute the domain section to the selected stage's existing artefact and shared task record.

| Stage | Required contribution |
| --- | --- |
| Discover | Runtime/event/resource map and reproducible lifecycle failure evidence. |
| Plan | State transitions, ownership, target-version constraints and acceptance journeys. |
| Execute | Only assigned realtime/native changes using the actual project's conventions. |
| Verify | Reconnect/teardown/multi-view results and real host evidence where available. |

## Acceptance evidence

- Relevant reconnect, teardown and multi-view state transitions are exercised.
- Media/session/window resources have clear ownership and cleanup.
- Runtime checks identify the actual platform and any unverified native capabilities.

## Existing capability integration

- Use the installed macOS build/run, window or AppKit skill only for an actual native target.
- Use browser tooling for browser behaviour and state its native-runtime limitations.
- Combine React/editor-schema where the project shares stateful UI or persisted layouts.
- Delegate accessibility, performance and visual judgement to the existing shared stages.

## Failure modes

- Do not claim a browser simulation proves native window or permission behaviour.
- Do not record, publish or stream user media as an incidental test action.
- Do not assume a selected camera or permission grant persists across device changes.
- Do not infer a native macOS project from the user's hardware profile.
