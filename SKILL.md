---
name: ai-development-workflow
description: Create, plan, criticize, revise, or execute project development work in one skill. Use 0123 for a new record and all stages; 123 updates and executes the selected existing record. Only stage 0 creates a record. Other modes include 0, 01, 012, 013, 1, 2, 3, 12, 13, 23, revise and resume.
---

# AI Development Workflow

Only stage 0 creates and selects a new task record. All subsequent stages and follow-up changes use the selected record, including after completion. Before deriving or revising the plan, preserve the selected source messages in that record and reconcile its individual commitments as described below. Read references/record-contract.md and the references for the requested stages. Apply the selection and mode rules below when a stage reference provides a different default. See README.md for usage examples.

The user's request and corrections remain authoritative, not the agent's plan. Every behavior-changing clause must follow from the cited request or an evidenced necessary implementation detail; citing a whole message does not authorize additional clauses. Review scope before improving the design. Apply this to all proposed work and its effects, including behavior introduced around unchanged components, data or processes. Features, defaults, dependencies, transformations, side effects and operational rules do not become authorized because they improve the design or fit an existing requirement ID. Use the behavioral scope review in references/record-contract.md during planning, criticism, execution changes and completion.

## Invocation

The skill's canonical name is `ai-development-workflow`. In the Codex composer, type `/aidw` and press Tab; the composer resolves that shortcut to the attached `ai-development-workflow` skill. Do not treat plain `@aidw` or `$aidw` text as a skill attachment. The canonical dollar invocation is `$ai-development-workflow`.

After resolving the shortcut, append the mode and request. Examples: `/aidw` + Tab, then `0123 add a report command`; `01` for a new checklist/plan; `123` to update, review and execute the selected existing record; `revise add retry handling`; or `3 --plan "documents/tasks/development/<record>"`.

| Mode | Stages |
|---|---|
| 0 | Create and select a new draft record only |
| 01 | Create a record, then build its checklist and plan |
| 012 | Create, plan, then criticize |
| 013 | Create, plan, then execute |
| 0123 | Create, plan, criticize, then execute |
| 1 or plan | Build or update the selected record's checklist and plan |
| 2 or criticize | Criticize and correct the existing plan |
| 3 or execute | Execute the existing ready plan |
| 12 | Plan, then criticize |
| 13 | Plan, then execute |
| 23 | Criticize, then execute |
| 123 | Update the selected existing record's plan, criticize, then execute |
| revise or r | Apply requested changes to the existing plan only |
| resume | Resume interrupted execution of the active plan |

Accept the listed digit sequences compactly or space-separated: `0123` and `0 1 2 3` are identical; `123` and `1 2 3` are identical. Preserve the leading zero, never parse the mode as an integer. Accept `aidw`-prefixed and slash-prefixed equivalents after this skill is selected, including `aidw0123` and `/0123`. Natural-language requests may select stages 1-3, revise or resume, but cannot silently add stage 0: a request for a new record without 0 requires asking the user to include 0. Without a mode, follow an unambiguous non-creation stage request; otherwise default to stage 1 on the selected record. Never infer execution from a bare skill mention. Unsupported orders, repeated stages, and `02`, `03`, or `023` require clarification; do not silently insert planning or drop zero. Stage 0 may run alone or precede a sequence starting with 1.

## Select the plan

### Optional conversation start time

Accept a start time immediately after the mode, such as `0123 11:24 PM` or `0 1 2 3 23:24`. An optional ISO date and short identifying quote can disambiguate: `0123 2026-09-10 11:24 PM "for every widget"`. This is a conversation scope anchor, not a deadline, schedule or additional stage. A time embedded in ordinary task prose is not automatically an anchor.

- Resolve the anchor before creating or editing any record. Match the timestamp displayed for a user or assistant message in this conversation, using the user's confirmed local/UI timezone. When history stores UTC timestamps, convert them with the applicable date/timezone; never match raw UTC to local clock text or use tool-event times as message times. Use 12-hour AM/PM or 24-hour notation as supplied. Do not assume the current date for a time-only anchor.
- Read timestamped conversation history through the invocation and match the supplied local clock time at its stated precision. Apply any supplied date/quote or explicit role/message locator first. If multiple actual user/assistant messages match, select the most recent matching message in conversation order, including across dates or within the same minute. This is the default tie-breaker, not ambiguity requiring clarification. Exclude automated instruction/context attachments, tool events and duplicate event copies from anchor candidates. Never select a message after the invocation or the nearest nonmatching time. No match, uncertain timezone, unavailable timestamp metadata or incomplete history that prevents reliable identification requires one concise clarification; a summary alone does not prove the boundary.
- The range includes the matched message and every subsequent user/assistant message through the invocation, in conversation order. Freeze the endpoint at that invocation, not at when tools finish. Read the whole range; if portions cannot be recovered, ask for the missing content rather than silently using only the newest visible messages. Apply later explicit user corrections normally, recording them as appended sources rather than silently extending the original range.
- Derive new work and individual issue checkpoints from the relevant requirements and findings in that range. Earlier messages remain context for constraints, authority and understanding references; they do not automatically add deliverables. If the range explicitly adopts an earlier list or says "all issues above", recover that referenced material and identify the inclusion, or clarify what is meant. Assistant findings remain context, not independent permission for suggested features.
- State the resolved start date/time/timezone, message quote/locator and inclusive endpoint briefly, then proceed without another approval when unambiguous. Preserve the range in fix-plan.md and the complete conversation archive below, plus requestSources with their actual roles and locators. Stage 0 alone captures history and the boundary but leaves its scaffold draft/not_ready.
- A time anchor does not imply stage 0, change record selection, waive review or authorize deletion of existing requirements. On `123` without 0, use the selected record and reconcile the ranged changes while preserving unrelated requirements/history. Without an anchor, use the existing relevance-based conversation scope; do not invent a time boundary.

### Record selection

Interpret every subsequent user message by meaning, not trigger phrases. Any new requirement, change, defect report, correction, constraint, acceptance criterion or answer affecting the work automatically amends the selected record, during execution or after completion. No mention of the plan or repeated mode is required. Only a fresh invocation containing 0 creates another record; never replay an earlier 0. Explicit selection of another existing record still applies.

Append distinct new issues; revise affected checkpoints for corrections, removals or replacements, preserving IDs, history and unaffected work. Do not leave superseded requirements executable. Capture new sources once, update affected implementation/test mappings and refresh material review. Questions seeking explanation, status requests and hypothetical ideas alone are not implementation requirements; mixed messages still contribute their actual requested changes.

Preserve pending authorized stages across amendments; do not reset a pending 0123 to planning because a follow-up lacks a mode. A natural-language request to fix or implement work authorizes execution after review on the same record, including after completion. A plan-only request authorizes planning only; an explicit pause or no-execution instruction governs. These semantic follow-up rules take precedence over the bare-mode default above.

1. With stage 0, create one new dated record and select it, even if another record is open or complete. Leave earlier records untouched. Derive the new task from current relevant requests, corrections and findings; do not copy an old checklist or replay completed work. Pass this exact new record through every following stage. `0123` creates one record, not four. If 0 is combined with `--plan`/`--record` or an instruction to modify an existing record, ask whether to create new or reuse; never silently discard either instruction. An explicitly identified source plan may seed a new record, but must not be modified.
2. Without 0, an explicit `--plan <path>`, `--record <path>`, or unambiguous record path overrides conversation context. Resolve quoted paths with spaces correctly. A Markdown file inside a record identifies its containing record. Otherwise use the record most recently selected, created or explicitly adopted in this conversation. Completed records remain selectable for changes. Do not choose an older record merely because its topic seems more relevant, search other chats, or choose by filesystem recency.
3. A chat-only or standalone plan can supply source material, but materializing it into a six-file record requires stage 0. Without 0, do not invoke the allocator or create a directory even when a plan is available only in chat. Ask for an existing record or an invocation including 0. Preserve the source when authorized to materialize it; missing evidence remains explicit. A context summary is not proof of unseen checks or details.
4. Without 0, if no record is selected/available, ask which existing record to use or ask the user to start with 0. An unavailable explicit path is a blocker, not permission to choose or create another record. If selection is genuinely ambiguous, ask one concise question. With 0 and a clear current task, do not ask which old record to use.
5. State the selected task and path briefly. Always supply that exact path to helper scripts. Resolve the actual project root independently; never infer it from a staging folder. Missing source access remains an explicit limitation.

## Run stages

### Capture before planning

Select messages simply: with a supplied time, start at the most recent matching message, including it and everything after it through the invocation. Without a time, use the last few messages discussing current changes, problems or fixes, not the entire task history or a fixed message count. "Your last message" means that message; "your last message and what I said before it" means that recent exchange. Include the invocation and its corrections. Do not ask for a timestamp when this selection is clear.

Before deriving requirements, save only those selected messages to `conversation.json` inside the record, preserving their order, roles, timestamps, locators and full contents. Completeness means all selected messages, not all history. Older context can inform constraints without being copied or becoming new work. Recover missing selected messages, not unrelated history. Exclude automated instruction attachments, compaction summaries, hidden reasoning and tool-output dumps; redact secrets explicitly. Read referenced attachments separately and preserve their locators.

Use the bundled capture helper for Codex JSONL sources. Select the relevant messages first; the helper preserves and verifies that selection:
`python3 <SKILL_DIRECTORY>/scripts/capture_conversation.py --source <ROLLOUT> --thread-id <ID> --start-line <FIRST_MESSAGE_LINE> --end-line <INVOCATION_LINE> --output <RECORD>/conversation.json`
Use `--message-lines <N> <N> ...` for selected recent messages, or `--last-assistant` for "your last message"; the invocation is included automatically. For a time anchor use `--start-time "12:04 PM" --timezone Africa/Johannesburg` (and `--date YYYY-MM-DD` only when supplied), with the search boundaries covering available messages through the invocation. Pass `--exclude-lines <N> ...` for identified automated attachments and compaction summaries; exclusions are applied before selection. The helper selects the latest matching time, preserves exact selected payloads and refuses overwrite. Run the same command with `--verify`. Relevance and identification of automated messages remain agent judgments, not text-prefix guesses. Never widen the selection to suit the helper. For non-JSONL or redacted sources, verify selected contents against original locators and state the verification boundary.

Preserve existing archives and requestSources as history. For a substantive follow-up, capture only newly selected messages not already saved, in a uniquely named snapshot; reuse existing locators for unchanged sources. Do not create another snapshot merely for a resume or repeated invocation with no new scope. In fix-plan.md, identify the sources for the current amendment and the retained requirements it affects. Read those sources and relevant existing constraints, not every historical snapshot on every pass or after compaction. Do not race another executor to amend its record.

Keep one stable checkpoint per distinct in-scope issue, requirement or constraint, with source locators and decisive implementation/test coverage. Preserve separate assertions for distinct accepted details even when steps/tests are shared. Merge duplicates with their source links. Briefly explain exclusions only for plausible requested work that was rejected, deferred, superseded or already resolved; incidental discussion needs no checklist row. Assistant suggestions and external reports are evidence, not authority by themselves. Check both omissions and unauthorized additions against the selected messages. Hashes, counts and valid links alone do not establish semantic correctness.

### Preserve execution intent

Resolve authorization chronologically. An earlier "plan first", "think before implementation" or audit-only instruction governs that earlier phase; a later explicit invocation containing 3 authorizes implementation of the adopted work after planning/review. A reply clarifying record identity or source checklist continues the pending invocation, even when it does not repeat the mode. Preserve the requested stages and underlying deliverable across clarification, handoff and compaction; do not reset them from older source text.

For an adopted implementation checklist, stage 3 means performing and verifying its in-scope work, not merely writing, reviewing, linking or validating the checklist. Do not rewrite "implement X" as "specify/retain a future acceptance item for X", or put application implementation out of scope, to satisfy an earlier planning-only instruction. Before finalizing readiness and again before execution, state the requested stages, actual deliverable, and evidence that will demonstrate that deliverable in fix-plan.md. Compare these with the latest user authority, not just the record's internally consistent mappings.

A genuinely documentation-only request still executes as documentation; mode 3 does not invent product work. An explicit current "do not implement" or "checklist only" constraint is not overridden by inference. If current instructions genuinely conflict about the deliverable, ask one targeted question before changing it. Do not ask again merely because the user previously requested planning first or clarified which record to use. Record completion requires evidence for the authorized deliverable, not a substituted paperwork task. If a record was wrongly closed on that basis, preserve the old report, correct the scope and reopen the same selected record for fresh review.

- Creation (0): verify the real project root and applicable instructions, then run `python3 <SKILL_DIRECTORY>/scripts/create_plan_record.py --project-root <ROOT> --title "<TASK>"` exactly once. Select the returned path and capture the source conversation. Stage 0 alone leaves the scaffold draft/not_ready; it does not build the checklist, finalize readiness, criticize or execute. Continue with stage 1 only if requested. The allocator is not a mode router; do not call it from stage 1 or other modes lacking 0.
- Planning: follow references/planner.md.
- Criticism: follow references/criticizer.md.
- Execution/resumption: follow references/executor.md. Always use the shared resolver with `--execution`; resumption additionally requires `--resume` and the explicit record.
- Revision: follow references/planner.md against the selected existing record. Apply the user's requested changes; preserve unrelated requirements, stable IDs, original creation date, findings and execution history. Append a concise dated change rationale to fix-plan.md; update affected R/P/T mappings and checks. Increment planRevision for substantive edits and invalidate prior readiness. Re-review changed source assumptions. A previously criticized plan needs fresh criticism before execution; do not reset critique history to bypass it. Revision alone never changes application code. For an interrupted implementation reconcile actual work and preserve evidence before changing planned steps; do not race an active executor.

For requested changes to a completed record, reopen that same record for planning/review, preserve its prior completion evidence, and reopen only affected checklist outcomes and checks. Revision alone does not authorize execution; requested execution can proceed after fresh review. Never leave a changed record marked complete or reuse its old readiness hashes.

Run only requested stages, in their defined order, without repeatedly asking permission already supplied by the invocation. Blocked planning may still proceed to requested criticism to investigate and correct issues. Execution requires resolved blockers, a ready record, current source evidence and actual user authority. If a previously criticized plan needs renewed review in mode 13, perform the necessary review and explain why; never bypass a stale critique gate. No mode independently authorizes deployment, external messages or destructive actions.

## Handoff

Keep using the selected record until stage 0 creates another or the user explicitly selects a different existing record. Report its path, revision, completed stages, substantive changes, actual verification and remaining blockers. Successful verified execution closes that record using status complete; no separate closed status or automatic chat archival is needed. If execution is interrupted or any required outcome is unverified, keep it executing/blocked, not complete. Distinguish plan corrections from implemented changes.
