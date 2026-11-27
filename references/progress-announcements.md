# Workflow, phase and agent announcements

Read the [mandatory workflow contract](workflow-contract.md). Apply it to automatic tasks,
public modes, G/numeric commands, named advanced handlers, quick tasks, recipes, internal operations and
continuation. Announcements report actual work; they do not dispatch or grant permissions.

## Opening brief

Before substantive work, visibly state:

- **Scope and deliverable:** what will change or be investigated, with important boundaries.
- **Selected workflow and reason:** concrete Plan/Build/Review/Loop mode, actual command,
  recipe or composed chain, inspected impact and required roles. Auto reports which mode it selected.
- **Discovery:** initial/refined task query when applicable, current index fingerprint, relevant
  grouped candidates, selected resources and focused reasons. State that retrieval is candidate-only.
- **Numbered phases:** each phase's owner and actual pending/in-progress/complete/blocked
  status; identify the current phase. Include planning and criticism at proportional depth.
- **Contributors:** required contributors and useful returned contributions, excluding coordinator; every new task requires at least two.
- **Actual agents:** numeric coordinator-plus-running-worker count, with their identities/roles.
  Show planned workers separately. Profiles applied in the current agent add zero agents.
- **Gate status:** execution remains pending until current plan/criticism/briefing admission.

If choosing responsibly needs source inspection, announce provisional read-only reconnaissance,
its approach and limits, and actual count. Confirm the grounded selection before dependent
work. Preserve explicit choices, read-only/plan-only scope and authorized continuation.

Example for a localized Auto build, before dispatch:

> Scope: correct the label on the one settings button and verify its rendering.
> Selected: Auto → Build, using GB/Ponytail after confirming local ownership and no shared effects.
> Phases: 1. Capture scope — in progress; 2. Plan — pending; 3. Criticize/revise — pending;
> 4. Implement — pending; 5. Independently review the result — pending.
> I coordinate; a Fast Builder with UI expertise will implement, and a separate Reviewer will
> criticize the plan and review the result. These are planned assignments, not running workers.
> Contributors: 2 required, 0 returned. Agents: 1 active — the coordinator. No worker has been launched yet.
> Implementation is not admitted until the plan and completed criticism pass the gate.

This is an example, not a declaration that a real task has begun or passed anything. After
actual dispatch, report the returned identities and current running count. Every task delegates
under [task routing](task-routing.md); this preparation example is not permission to finish with fewer than two useful workers.

## Transitions and delegation

Before changing phase/workflow, state what actually completed and its evidence, the next
phase, purpose and owner, and the current numeric agent count. If the chain changes, say
what changed and why. A phase is complete only when its required result exists; partial
criticism is still in progress or blocked. Routine tool calls inside an unchanged phase
need no repeated opening brief.

Before delegating, announce the intended role, task and independent/concurrent assignment.
After a successful spawn, report the actual returned child identity and updated count.
Record it in the coordinator's results.md or the worker's permitted result artifact.
Count only observed running workers plus the active coordinator. Planned/queued/reserved,
completed and failed workers are separate states. A profile, agentCalls entry or phase title
is not a spawned worker. If dispatch fails, disclose the blocker and actual count; wait or
serialize when capacity is busy, and continue only permitted preparation when tools are unavailable.
Never label self-critique independent or infer a model change from profile metadata.

On continuation, announce the resumed phase and actual roster; reconcile current evidence
and reuse the same record. Continue authorized work without another permission question.
On a premature write/false completion, apply the contract's truthful recovery procedure
immediately; never backdate a critique or silently rewrite the earlier status.

## Record what was actually said

Emit the message first, then record its actual text/context and current binding using
[contract records](workflow-contract-records.md). A helper-generated draft, local Markdown
file or announced flag is not evidence that the user was told. Portable declarations
are locally authored evidence. Record actual returned dispatch results where workers are used;
neither the local declaration nor a role name independently authenticates execution.

## Browser handoffs

Before browser work, apply [browser control recovery](browser-recovery.md). Pass the current user’s recovery choice and session owner to each browser worker. Pause on handoff unless the current user has explicitly opted into supported recovery for this session.
