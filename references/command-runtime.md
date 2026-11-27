# Shared command execution

Apply the [mandatory workflow contract](workflow-contract.md) and
[progress announcements](progress-announcements.md) to every entry: public modes, G/numeric
compatibility controls, recipes and internal operations. Announce scope, phases, owners,
actual worker count and admission state before work and relevant transitions.
Apply [task routing](task-routing.md) to resolve the concrete mode and mandatory actual
assignments, including Fast Engineer for known localized builds and Architect for broad/shared
effects before the final plan. These requirements govern every command, including G0/G1/GB.

Use [public modes](public-modes.md) for `auto`, `plan`, `build`, `review` and `loop`.
Explicit G selections load their actual command file. Numeric selections load
[numeric controls](../commands/numeric-stages.md) and the selected record's relevant handler.
Plain mentions and historical quoted commands are not fresh invocations. Automatic selection
loads relevant capabilities progressively; it does not read every unrelated index entry.

## Records, sources and admission

Use [standard workflow](standard-workflow.md) for explicit legacy record/numeric semantics
and source capture, and [record contract](record-contract.md) for shared evidence and gates.
Paths in those references resolve from the main skill root. A fresh standalone G starter
allocates once using its actual preset; all later phases and workers retain that record.
Public modes handle fresh capture or selected-record reuse through their own stated contract.

Preserve the requested output boundary. Planning, assessment and review do not authorize
implementation. Numeric operations retain their requested phases, but missing universal
pre-write prerequisites must be disclosed and satisfied rather than silently waived.

For a full 0123 workflow, completed criticism of the concrete plan precedes execution. A
later code review is a separate activity. Finalize the actual reviewed plan, then run
`resolve_plan_record.py --execution --require-critique` with the exact record. Use `--resume`
only after reconciling interrupted execution. Every source/test/docs writer, including quick
corrections, documentation and cleanup, requires current criticism and a visible briefing.

## Real handoffs and ownership

Use an available named worker, or dispatch a real generic child with the complete linked
role instructions. Supply scope, project root, exact record, current request/corrections,
baseline, allowed paths, relevant input artifacts, selected lenses, tests and output destination.
Preserve the actual host's configured tools/models/permissions. Follow
[host access](chatgpt-host.md) and [browser recovery](browser-recovery.md).

Record the returned worker identity and wait for its actual result. Applying a profile in the
current agent adds no worker. Every new task needs useful contributions from at least two
distinct actual workers excluding the coordinator, including Plan, read-only and standalone
operations. Product/test/docs changes use an actual Builder and distinct independent Reviewer.
Track all substantive authors, including secondary authors and coordinator integration.
A coordinator self-check cannot replace either worker's bounded contribution. The coordinator must
not perform the assigned child's source work in parallel or silently take over after a failed
dispatch. Busy slots mean wait/serialize; unavailable dispatch is an explicit blocker.

Keep one implementation owner for overlapping changes and one generator/package owner.
Read-only consultations cannot implement. Do not recursively invoke a whole preset from an
atomic operation. Resume existing children where supported; otherwise reconcile saved state
and actual ownership before replacement. Never assume an unknown executor has stopped.
Mandatory delegation applies to the coordinator; already assigned children do not recursively
spawn workers or restart the workflow. The coordinator may integrate, package and perform
already-authorized publication of the independently accepted result.

Selected post-implementation checks run before closure. The coordinator retains final
accounting until their results arrive, and the implementation owner repairs authorized findings
after any needed plan/review update. Loop uses its stricter manager/reviewer/executor boundary.

## Continue and report

Preserve the original deliverable and dependency groups. Missing access to one dependent action
does not authorize substituting a documentation-only result for implementation. Continue useful
independent work, retain exact blockers, and reuse settled evidence. Wait for a consultation's
finished result before reviewing its dependent plan; do not revise a plan during its critique.

Keep the durable checklist synchronized with visible Markdown or an actually supported,
acknowledged host checklist surface. Report real changes, observed checks, remaining work and
delivered artifacts. Converter output or saved files alone do not prove publication.

At task start, check `workflow_log.py status --project-root <ROOT>` when a shell is available.
Optional [debug logging](debug-logging.md) is off by default. When enabled, use its shell
wrapper and actual event API; never claim it captured host actions that were not delivered.
