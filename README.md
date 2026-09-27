# AI Development Workflow

Maintained by [aipieksel](https://github.com/aipieksel). Upstream credits and licenses remain with their respective authors.

AI Development Workflow is a Codex skill for carrying a software task from a request through a durable plan, critical review, implementation, and evidence-backed completion. It keeps the original request, checklist, plan, critique, and results together in one task record so later corrections can amend the same work without losing its history.

Choose the stages you need when invoking the skill. `0123` starts a new record and carries it through execution; later calls can plan, review, execute, revise, or resume the selected record. The skill checks that the plan matches the user's request before code changes and that completion is supported by actual verification. It does not grant permission to publish or deploy.

| Stage | Action |
| --- | --- |
| 0 | Create and select a new draft record |
| 1 | Build or update its checklist and implementation/test plan |
| 2 | Criticize and correct the plan against the original request |
| 3 | Execute, verify, and complete the record when every outcome is proven |

## Examples

```text
$ai-development-workflow 0123
$ai-development-workflow 0 1 2 3
$ai-development-workflow 01 Plan the issues from our latest discussion.
$ai-development-workflow 123
$ai-development-workflow 12
$ai-development-workflow 3 --plan "documents/tasks/development/<record>"
$ai-development-workflow revise Preserve explicit inheritance resets.
$ai-development-workflow resume
```

`0123` and `0 1 2 3` create one record and run all stages. `123` updates, reviews and executes the selected existing record. `01` creates and plans; `012` also reviews without executing; `013` creates, plans and executes with any required review gates intact. `0` alone allocates the draft and captures its source history, without planning or execution. `1`, `2`, `3`, `12`, `13`, `23`, `123`, `revise` and `resume` never create records.

The Codex composer shortcut is `/aidw` followed by Tab, then the mode. Keep the leading zero. `02`, `03`, `023`, reordered or repeated stages are not supported. Combining 0 with an existing-record selector is conflicting and requires clarification. A standalone/chat-only plan needs 0 to become a durable record; its source is preserved.

## Checklist And Lifecycle

### Start From A Message Time

```text
$ai-development-workflow 0123 11:24 PM
$ai-development-workflow 0 1 2 3 23:24
$ai-development-workflow 0123 2026-09-10 11:24 PM "for every widget"
```

The time immediately after the mode means: start with the message at that displayed local/UI time, include it and all subsequent messages through this invocation. It is not a deadline or schedule. Add a date or short quote when needed. Matching uses message timestamps converted to your confirmed local/UI timezone, not raw UTC or tool-event times.

If multiple messages match that time, use the most recent matching user/assistant message through the invocation, including across dates or within the same minute. Apply any supplied date, quote or explicit message selector first. Include that selected message and every subsequent message through the invocation; do not ask merely because there are multiple matches. Automated context attachments and duplicate/tool events are not anchor candidates. Ask only when no match exists or the timestamps/timezone/history cannot establish the range reliably. Never substitute the nearest nonmatching time or silently omit missing messages. Report the resolved range and record it in fix-plan.md with source provenance in record.json.

Earlier discussion supplies constraints and context, not automatic extra deliverables. Explicit references to earlier lists are followed and recorded. Later user corrections still apply. Each relevant listed issue in scope receives an individual checkpoint; assistant suggestions do not become authority merely by falling inside the range.

The anchor does not change lifecycle rules: `0123 11:24 PM` creates a new record; `123 11:24 PM` updates the selected existing record without erasing unrelated requirements. Without a time, scope remains relevance-based rather than limited to a fixed number of messages.

### Findings And Completion

With a time, start at the most recent matching message, including it and everything after it through the invocation. Without a time, use the last few messages about current changes, problems or fixes, not the entire task history or a fixed message count. "Your last message" means that message; "your last message and what I said before it" means that recent exchange. Include the invocation and its corrections. Do not ask for a timestamp when that selection is clear.

Before planning, save only those selected messages in `conversation.json` inside the plan folder, preserving order, timestamps, roles and full contents. Older context can inform constraints without being copied or becoming new work. Recover missing selected messages, not unrelated history. Capture new substantive follow-up messages only; reuse existing sources for resumes and unchanged scope. Preserve earlier evidence without routinely rereading it all. Redact secrets; exclude automated instruction attachments, compaction summaries, tool-output dumps and hidden reasoning.

The bundled `scripts/capture_conversation.py` supports exact `--message-lines`, `--last-assistant`, and latest local-time matching with `--start-time`/`--timezone`. Identified automated messages are omitted using `--exclude-lines`. The invocation is retained. Use `--verify` to check the exact selected payloads against the source. The agent still judges relevance and identifies automated content; capture verification does not prove understanding.

The checklist keeps one checkpoint per distinct in-scope issue or constraint, including accepted details with their own assertions. Merge duplicates with source links. Briefly explain exclusions of plausible requested work; incidental discussion needs no administrative row. Criticism reads the selected sources and relevant retained constraints to catch omissions. Execution and completion require evidence for each accepted child outcome. Copying history is necessary evidence, not a substitute for this coverage check.

An earlier "plan first" instruction does not cancel a later `0123`/`123` request to implement the adopted work. Clarifying which record or source checklist to use retains the pending stages. For an implementation checklist, stage 3 performs the work, not just documents it. The reviewed plan records the stages, actual deliverable and completion evidence so criticism/execution can reject that substitution. Genuine documentation-only requests remain documentation-only; current conflicting instructions require clarification. Missing provider/live permissions remain limited to dependent actions, not an excuse to stop independent authorized development or mark unfinished work complete.

Every subsequent instruction is interpreted by meaning, not a trigger phrase. New requirements, changes, defects, corrections, constraints and acceptance criteria automatically amend the selected record without mentioning the plan or repeating a mode. Append new issues; revise existing checkpoints for corrections, removals or replacements, preserving history and unaffected work. Only a fresh invocation containing 0 creates another record; explicit selection of another existing record still applies. Questions or hypothetical ideas alone do not become implementation requirements.

Continue pending authorized stages after reviewing affected changes. A natural-language fix/implementation request authorizes execution on the same record, even after completion; a plan-only request or explicit pause does not. Capture new substantive sources once and reuse existing locators; preserve older archives without rereading them all.

The selected record remains selected until 0 creates another or you explicitly select a different one. Completed records can be reopened for changes, preserving history and requiring fresh review of affected work. A new record does not close or alter an older one. Execution marks a record `complete` only with decisive evidence; incomplete or interrupted work remains open/blocked. Completion does not archive the Codex task.

Records live under the project's `documents/tasks/development/` directory and contain `record.json`, `checklist.md`, `fix-plan.md`, `test-plan.md`, `critique.md` and `results.md`. Stage instructions are in SKILL.md and references/record-contract.md. Source hashes and valid mappings do not prove semantic correctness or authorize scope expansion. No mode independently authorizes deployment or external/destructive actions.

### Scope Across All Stages

Planning links each behavior-changing clause to the supporting request phrase or evidence of necessity. Criticism independently checks those claims against the request and concrete before/after effects, including behavior added around unchanged components, documents or data. Execution applies the same review before a new material change and at completion; keeping an existing requirement ID does not authorize additional behavior. Unsupported extras are removed while authorized work continues. The shared contract defines this review using the existing files and fields; ordinary implementation choices need no extra approval round.

## Validation

Run from this skill directory with Python 3.10 or newer:

```sh
python3 -m unittest discover -s scripts/tests
```

The helper tests cover allocation, preservation, provenance, review and resume gates. Mode selection is performed by the agent following SKILL.md, not by a numeric-mode CLI parser; test passing alone does not prove conversational routing or application outcomes.

For changes to scope handling, also use `scripts/tests/scope-review-cases.json` for a behavioral evaluation. Give the evaluator the applicable stage instructions and each case's input without its `expected` answer. Compare its actual decisions, retained work and next action with the expectations; do not count phrase matching, valid references or helper success as semantic correctness. These cases exercise planning, criticism, execution drift, indirect effects, necessary implementation details and later user authorization.

## Installation and rights

Copy this entire folder into your assistant's supported skill directory, preserving `SKILL.md`, scripts, references, examples and templates. Python 3.10+ is required for the Python helpers. Host autocomplete and tool availability depend on the installed assistant. Keep generated project/task records and private conversations outside the shared skill package. This package is licensed under [MIT](LICENSE).
