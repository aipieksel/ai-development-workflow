# ChatGPT and local host access

Use the actual tools, models, storage and permissions exposed in the current session.
This package supplies workflow instructions and local helpers. It does not install a model,
browser, subagent service, computer connection, timer or background execution engine.

## Resolve the installed resources

Select the single main `ai-development-workflow` skill through the host's supported interface.
Resolve resources from that installed package or its local root. The advanced command and
role files are bundled implementation resources; their presence does not register separate
public skills. Use [advanced reference](advanced-reference.md) to locate an explicitly chosen
G/numeric handler. Do not infer missing instructions from absent launcher autocomplete.

If skill resources are exposed as text only, use the host's resource reader. When a local
helper is needed, materialize it together with its sibling imports in an authorized runtime.
Preserve the complete package layout. Python helpers require Python 3.10+ and the standard
library. If a required execution gate cannot run, retain a blocker and complete useful
preparation; do not fabricate admission or replace the gate with an assertion.

## Real workers and tools

A generic child given the complete role instructions is a real delegated worker when the
actual spawn succeeds and returns an identity. Applying a profile in the current chat adds
zero workers. Preserve the real configured model, tools and permissions. Record actual
dispatch results and wait for the worker's output. Follow [task routing](task-routing.md):
every new task has at least two distinct useful actual worker contributions, including Plan and read-only work. Writing tasks need independent criticism/result acceptance. A coordinator inspection-approach self-check is disclosed separately and cannot replace either worker. Busy slots mean wait/serialize;
unavailable dispatch blocks dependent task work. Already assigned children do not recurse.

Browser interactions, screenshots, document editing, image generation, test runs and imports
must use available supported tools. Discover their current contracts. Do not invent method
names, installed applications or successful calls. Apply [browser recovery](browser-recovery.md)
to current-user authorization and the same session. Report an actual access limitation without
asking the user to repeat permission already given.

The active roster has six canonical families. Resolve legacy paths and selected operations through `agents/registry.json`; load capabilities as knowledge, not extra worker identities. Preserve real author/acceptor separation, including secondary architecture, design and integration authors.

## Records, progress and history

Keep one durable task record in the available project workspace. Without filesystem access,
maintain an explicit task-note fallback and disclose that durable file recording is unavailable.
That fallback cannot satisfy a product execution helper that the selected workflow requires.

Show the actual checklist in ordinary Markdown. An available host checklist/plan tool may
mirror it using that tool's real schema and acknowledged result. The bundled JSON converter
does not publish a panel or establish persistence. Avoid claims about a particular custom
Tasks UI. Follow [record visibility](record-contract.md#visible-checklist-and-execution-reporting).

Capture accessible relevant messages with real locators; use null for unavailable timestamps.
`chatgpt_bridge.py` records visible messages supplied to it, and `capture_conversation.py`
works with supplied transcript files. Neither retrieves unseen chat history. A history search
hit or summary is not a complete transcript. Record actual coverage and access failures.

## Delivery and lifecycle

Session files are not automatically permanent storage. Use the actual requested destination
and verify its returned state when saving or uploading. Distinguish an artifact prepared
locally from one installed, uploaded, published or activated on the user's host.

Loop's [five-minute monitor](loop-timers.md) uses actual worker/mailbox waits first and real
timers second. A helper checkpoint is bookkeeping. Normal waits do not prove persistence
after the manager/session stops. Do not promise background progress without actual support.
