# AI Development Workflow — Version 2

**One portable agent-development skill for planning, criticizing, building, reviewing and verifying development work.** The complete skill can be used in ChatGPT, Codex, Claude, DeepSeek, and other compatible hosts that can load its instruction bundle and provide the workers and tools required by the selected task. Describe the task, and the workflow discovers appropriate operations and expertise while preserving the original request, existing work and evidence of completion.

The five public controls are **auto**, **plan**, **build**, **review** and **loop**. Auto selects and announces one of the four concrete execution modes. **Every new task uses at least two distinct actual sub-agents with useful contributions, excluding the coordinator—even small corrections, Plan and read-only Review.** You do not need to choose among dozens of internal agents or memorize numeric commands. Advanced controls remain available and are fully documented in the [complete command, operation, role and recipe reference](references/advanced-reference.md).

## Contents

- [Start here](#start-here)
- [Five modes](#five-modes)
- [The workflow contract](#the-workflow-contract)
- [Task-aware resource discovery](#task-aware-resource-discovery)
- [Agents and UI expertise](#agents-and-ui-expertise)
- [How the workflow chooses agents](#how-the-workflow-chooses-agents)
- [Loop: Execute and Review](#loop-execute-and-review)
- [What is included](#what-is-included)
- [Records and continuation](#records-and-continuation)
- [Install the complete package](#install-the-complete-package)
- [Validate and build releases](#validate-and-build-releases)
- [Capabilities, privacy and rights](#capabilities-privacy-and-rights)
- [Support and security reports](#support-and-security-reports)

## Start here

Install or load the **complete package** through the interface supported by your host. Invocation,
autocomplete, worker dispatch and tools are host capabilities; the examples below are not promises
that every host exposes the same syntax or plugin archive format.

In ChatGPT, **type `@`, start typing `AI`, wait for autocomplete, and select the installed AI Development Workflow entry**. Then write `auto` followed by your task:

```text
@ai-development-workflow auto Fix the reported save error, preserve the existing editor behavior, and verify the result.
```

The example shows the selected skill as `@ai-development-workflow`. Typing that text without selecting the installed autocomplete entry does not itself attach a plugin. You can also attach the main skill and describe the task normally; Auto is the default.

In Codex or another compatible local `SKILL.md` host—including Claude or DeepSeek setups with an
equivalent local-skill loader—select the installed skill through that host's interface. Where the
host supports dollar-prefixed skill selection, for example:

```text
$ai-development-workflow auto Fix the reported save error and verify the existing flow.
```

The package includes a portable router for explicit controls, but actual autocomplete, slash
shortcuts, sub-agent dispatch and tools depend on the host. Loading instructions alone does not
invent unavailable worker or browser APIs. A parsed command describes work; it does not run it.

## Five modes

| Mode | What it does | Where it stops |
| --- | --- | --- |
| **auto** | Selects **Plan, Build, Review or Loop**, explains the inspected impact and route, assigns actual workers, and follows that mode. | The requested outcome or an explicit blocker. Unresolved Auto does not admit execution; audit/planning boundaries remain intact. |
| **plan** | Captures or reuses the task record, investigates relevant source, writes the plan, then criticizes and revises it. | A reviewed plan. Product code, tests and project documentation are not changed. |
| **build** | Prepares or reuses the current plan and completed criticism, implements the authorized changes, and verifies the result. | The implemented outcome with actual evidence and remaining limits. |
| **review** | Critically plans an inspection, examines the specified plan, implementation, UI or artifact, and reports findings. | Evidence and findings. It does not silently repair the reviewed work. |
| **loop** | Coordinates separate reviewer and executor workers through repeated review, checklist execution and fresh review. | Current-revision reviewer acceptance, cancellation, interruption or a real resumable blocker. |

```text
@ai-development-workflow plan Plan the account migration, criticize it, and stop before changing code.
@ai-development-workflow build Implement the adopted migration plan and run the relevant checks.
@ai-development-workflow review Compare the delivered page with the original, including navigation, tabs, buttons and responsive states.
@ai-development-workflow loop Compare the original and current implementation, repair the complete findings checklist, and repeat independent review.
```

See [public mode contracts](references/public-modes.md) for exact boundaries. **XR remains a compatibility alias for Loop.** The primary word `plan` includes capture and completed criticism; advanced numeric `1` retains its historical existing-record planning-only behavior.

## The workflow contract

Before substantive work, the agent must tell you the scope and deliverable, selected workflow and reason, numbered phases with their actual status, the owner of each phase, and the numeric count of the coordinator plus actually running workers. Required contributors, useful returned contributions, currently active agents, planned workers and applied profiles are reported separately.

The required sequence is proportional to the task:

1. **Capture scope.** Preserve the actual request, adopted corrections, relevant sources, protected behavior and acceptance criteria.
2. **Plan.** Identify existing owners, concrete changes, dependency order and decisive checks. Small corrections use a compact plan.
3. **Criticize and revise.** Examine scope, feasibility, sequencing, verification and protected behavior against the exact source and plan. Resolve material findings before implementation.
4. **Implement authorized work.** Every product, test and project-documentation writer needs current plan/criticism coverage, a visible briefing and successful execution admission.
5. **Verify and report.** Complete requirements with observed evidence. Keep failed, blocked and unverified outcomes visible.

The agent must not report a partial critique complete, use a role name as proof of a spawned agent, or mark a checklist item verified from an executor's unsupported claim. Missing criticism digits in advanced controls do not waive the gate. Reviewers report findings; the admitted implementation owner makes repairs.

Every product, test or project-documentation change has a **real Builder and a distinct independent Reviewer**. Criticism of the actual plan precedes writes, and independent acceptance of the stable integrated result precedes completion. **Plan and read-only tasks also require two useful actual contributors.** A coordinator self-check cannot supply the second worker. G0, G1 and GB have no exemption.

Independence includes every substantive author: adopted architecture/design, plans, source, tests, documentation and integration. An actor cannot switch profiles to review their own work. Ordinary critical feedback or raw fact collection does not automatically make its author a solution author. See the [routing and delegation policy](references/task-routing.md), [workflow contract](references/workflow-contract.md) and [admission records](references/workflow-contract-records.md).

These are mandatory workflow instructions backed by checks on supported admission paths. They do not install a universal interceptor around arbitrary host tools or prove the intellectual quality of criticism. The agent still has to follow the contract and inspect the actual evidence.

## Task-aware resource discovery

Before the workflow finalizes a mode, operation chain or team, it searches the packaged
`references/workflow-search-index.json`. An initial query comes from the literal request. When the
stack, owner or affected surface was initially unknown, the query is refined after reading project
instructions and relevant source. Results are bounded separately for recipes, specialists,
operations/capabilities and references, so general contract prose cannot hide domain expertise.

```bash
python3 scripts/workflow_catalog.py \
  --search "Improve a portable skill router from observed usage failures" \
  --refined-query "Python skill catalogue and package router; specialists are not selected" \
  --format json
```

Matches include scores, matched fields/terms and instruction paths. They are candidates, not
autonomous routing or permission. The agent inspects the shortlist, selects only applicable
resources, reads the selected files completely, and gives actual workers the selected specialist
instructions with concrete questions and acceptance criteria. A compact versioned receipt records
the queries, fingerprint, candidates, selections, paths and selected-recipe recommendation
dispositions. It cannot prove that a model understood the prose; independent review checks whether
the expertise materially affected the plan or result. If Python is unavailable, a compatible host
can search the shipped JSON directly with normal file tools.

## Agents and UI expertise

The active roster has **six core worker families**. Relevant capabilities and domain lenses are loaded into the actual assigned worker; the user does not need to choose internal roles.

| Core family | Useful contribution |
| --- | --- |
| **Investigator** | Source-backed research, assessment, root-cause evidence, behavior/invariant extraction and contribution discovery. |
| **Architect and Planner** | Architecture, dependency/migration decisions, implementation plans and test strategy. |
| **Builder** | Admitted implementation, Fast/Ponytail, TDD, cleanup, documentation and complete delivery preparation. |
| **UI Director** | Actual reference/state inventory, UI audits/specifications and visual/interaction direction grounded in existing owners. |
| **Reviewer** | Independent plan criticism, source/result review, coverage and substantive acceptance. |
| **Verification Engineer** | Actual tests, browser journeys, accessibility, security, performance and lifecycle evidence. |

A **profile** is an instruction body. A **worker** is a separately dispatched agent with a returned identity and real output. Two profiles on one worker still count as one worker. Thirty-eight original role paths remain mapped: two are reused core paths, and 36 are meaningful compatibility entries. The package therefore has 42 physical role files, but the active roster is six families. `agents/openai.yaml` is only skill-list metadata.

The coordinator manages scope, dependencies, assignments and one combined result. It keeps one writer per overlapping surface and one integration/package owner. Several Builders can work on separate modules or isolated checkouts, then the final Reviewer checks the integrated output and every author's contribution. The coordinator may perform already-authorized publication after acceptance.

Every selected worker receives a concrete question or output. Its contribution records inspected evidence, result, limitations, exact revision, disposition and effect on the outcome. A status ping, failed spawn, copied summary or nominal second worker does not satisfy the contract. The second worker can confirm a consequential boundary without finding a defect. Disagreements are resolved through evidence into **one** result; unresolved required work stays open.

Two contributors need not be active simultaneously. With one available child slot, complete one worker and then dispatch a different one. Completed contributions remain available without inflating the active count. Assigned children do their bounded work without recursively starting teams. Unchanged status/continuation reuses valid evidence; changed scope/results reopen affected checks. Missing real dispatch blocks dependent work honestly.

The **UI Director's complete expertise** applies automatically to layout, websites, colors, typography, spacing, components, assets, animation and visual corrections, including follow-ups such as “the spacing is still wrong.” A mechanical application of an approved local label/token can combine that expertise with the Fast Builder and Reviewer. New design decisions or reference reconstruction require a distinct UI Director contribution; shared UI also requires Architect input.

UI work inspects actual approved references, components/tokens, requested pages/states and relevant interactions. Preserve unaffected properties and verify the real rendered result. Builds, valid YAML or a small screenshot sample prove narrower facts. Existing editor kits, image tools and domain plugins retain their formats and tool ownership. The package does not use UIUX Pro Max.

All **21 domain lenses** remain: React, editor schema, WordPress/WooCommerce, WHMCS, plugins/MCP, browser extraction, native editable YAML, content/SEO, Python/data, databases, infrastructure, migration/release, realtime/native apps, reference fidelity, design systems, image direction, motion, media libraries, delivery, usage analysis and full UI design. See the [complete specialist table](references/advanced-reference.md#all-21-specialist-lenses).

## How the workflow chooses agents

Selection follows the actual request, inspected source ownership and affected consumers. A short diff or one changed file is not proof of small impact. The [complete routing matrix](references/task-routing.md#which-roles-to-assign) supplies explicit rules.

| Task evidence | Required contributors, excluding coordinator |
| --- | --- |
| Known localized implementation with no shared effects | **Fast Builder + Reviewer**, using **Build → GB / Fast full build / Ponytail**. |
| Multiple pages/features, changed shared component/service/token/API/schema or architectural/migration decisions | **Three distinct workers: Architect + Builder + Reviewer**. Advice precedes finalized planning and criticism. |
| Unknown cause, ownership or impact | **Investigator first**; evidence determines the repair team. Investigation-only completion still gets a Reviewer. |
| Planning only | **Architect/Planner + Reviewer**. Add actual fact/UI contributions when needed; no product changes. |
| Research, assessment or diagnosis only | **Investigator + Reviewer**, with an independently examined claim, omission or counterexample. |
| Standalone plan/code/spec review, including GPR/GVR | **Primary Reviewer + different Reviewer or Verification Engineer** for bounded corroboration. Primary ownership and read-only scope stay intact. |
| Verification only | **Verification Engineer + Reviewer**. Checks cannot silently repair or weaken tests. |
| Mechanical approved local UI correction | **Fast Builder with full UI expertise + UI-aware Reviewer**, checking the actual rendering. |
| Layout, palette, typography, responsive/interaction design or reference reconstruction | **UI Director + Builder + Reviewer**, with a distinct design contribution before the plan is accepted. |
| Shared UI or design-system Build | **Architect + UI Director + Builder + Reviewer**, using waves when slots are limited. |
| Multiple verification families/environments, specialized measurements, lifecycle work, substantial browser journeys or explicitly independent verification | **Add a distinct Verification Engineer**. Author-run checks remain separate evidence. |
| Documentation or packaging | **Builder with the relevant capability + Reviewer**; add independent lifecycle verification when needed. |

Changing one local button label can use Fast Build. Changing one shared header used by several pages requires Architect advice even if only one file changes. G0 retains its compact record, with the same two-worker minimum; it does not launch a second GB pipeline.

The six families combine **37 internal capability selectors** in shared instruction bodies. These are knowledge/operation selectors, not another public menu or 37 workers. Existing TDD RED/GREEN, docs-only, audit-only, check-only and mixed legacy execution boundaries survive. For example, GCA and GEA implementation goes to Builder with review/journey knowledge and separate acceptance; their old profile names cannot turn a writer into its own Reviewer.

## Loop: Execute and Review

Loop begins with **review of the existing work**. Its three roles have deliberately separate responsibilities:

| Role | Responsibility |
| --- | --- |
| Manager | Preserve context, dispatch workers, map every in-scope finding to checklist items, reconcile IDs/status/evidence references, monitor progress and maintain the checkpoint. The manager does not inspect product quality or make repairs. |
| Reviewer | Investigate the originals and current work, exercise available behavior, compare structure/visuals/function, document complete findings, confirm the derived repair plan and decide substantive acceptance. |
| Executor | Implement the admitted checklist, run appropriate checks, and return evidence for every item. Implemented items remain awaiting independent review. |

After the initial review, the manager produces the stable checklist and plan; the reviewer confirms that exact plan before the executor starts. After execution is fully accounted for, a **new reviewer with a new actual identity** examines the latest result. The process repeats until the reviewer accepts the current revision or a real blocker prevents progress. A clean initial review receives a **separate Verification Engineer’s corroboration**, bound to the same result and coverage, followed by the **original Reviewer’s acknowledgement** before acceptance. No empty executor pass is invented. If corroboration finds a defect, the existing checklist/repair cycle begins.

The manager checks the active worker every **five minutes (300 seconds)**. It uses a suitable worker/mailbox **wait tool first**, then an actual host timer if waiting is unavailable. Otherwise it reports explicitly limited active-session monitoring. A saved timestamp or bookkeeping helper is not an armed timer, and a normal wait does not prove monitoring continues after the session ends.

See [Loop mode](references/loop-mode.md), [artifact/accounting contracts](references/loop-artifacts.md) and [monitoring](references/loop-timers.md). Old `xr-*` schema identifiers and `artifacts/xr/` evidence remain intact for compatibility. If the host cannot launch required independent workers, the loop is blocked at that capability boundary; useful preparation can continue without pretending self-review is independent.

## What is included

| Capability | Included resources |
| --- | --- |
| One public skill and five modes | [SKILL.md](SKILL.md), [mode descriptors](modes/catalog.json), public mode and Auto instructions |
| 41 advanced G commands | Real [command handlers and exact launcher mappings](references/advanced-reference.md#all-41-g-commands), including full builds and atomic planning/execution/verification |
| Numeric compatibility | Supported capture/plan/criticize/execute sequences, revise/resume and conversation-time scope anchors |
| 26 internal operations | [Neutral operation catalogue](workflows/catalog.json), instruction bodies and explicit input/output/write-scope contracts |
| 10 task recipes | Reference rebuild, visual correction, design-system rollout, native YAML conversion, asset production, motion reconstruction, media-library extension, content-site delivery, artifact handoff and plugin evolution |
| 21 specialist lenses | Source-grounded domain guidance applied within selected operation scope |
| Six core worker families | Substantive canonical instruction bodies, 37 capability selectors and complete compatibility mapping for all 38 original role paths; 36 nonempty compatibility entries preserve old paths |
| Runtime helpers | Canonical family/capability resolution, routing, source-bound selection, contribution/authorship and admission checks, explicit record reconciliation, Loop corroboration/accounting and optional local diagnostics |

The [advanced reference](references/advanced-reference.md) contains every retained command, alias, phase, role expectation, prerequisite, operation, recipe expansion and specialist. The generated [workflow index](references/workflow-index.md) provides another source-derived lookup. Neither catalogue is a requirement to read every entry before a simple task.

Advanced examples after selecting the main skill:

```text
@ai-development-workflow G1 Implement the scoped change with planning, criticism and verification.
@ai-development-workflow GAS Assess the existing code and document its owners without editing it.
@ai-development-workflow GPR Independently criticize the selected plan.
@ai-development-workflow recipe visual-correction Repair the listed layout mismatches and preserve approved styling.
@ai-development-workflow 0123 Implement the adopted checklist in a new development record.
```

G controls are advanced compatibility handlers, not separate public skill registrations. Multiple G words in one string do not form a chain; ask Auto to compose the work or use separate invocations on the selected record. Removed native `stage`/`pipeline` selectors are explicitly unsupported. Help/menu shows the five ordinary modes; no editor picker or custom queue interface is installed.

## Records and continuation

Substantial tasks use one `documents/tasks/development/<record>/` directory containing:

| File | Purpose |
| --- | --- |
| `record.json` | Source provenance, scope, requirement/step/check mappings, revisions and readiness declarations |
| `checklist.md` | Stable requirement IDs and actual completion state |
| `fix-plan.md` | Concrete changes, owners, dependencies, protected behavior and decisions |
| `test-plan.md` | Decisive verification mapped to requirements |
| `critique.md` | Actual criticism, findings/dispositions and reviewed revision |
| `results.md` | Observed changes/checks, worker outcomes, delivery and remaining work |

New executable tasks use **workflow contract-v2**, including actual assignment bindings, all substantive authors, useful contributions and the exact final-result revision. Archived v1 records keep their original bytes and evidence. Actively resumed records reconcile aliases, identities, missing contributions and current criticism explicitly; an old review is never silently rehashed or treated as proof of the new policy.

Relevant source captures and operation artifacts live with the task. G0 keeps a compact quick-task record. Corrections amend the selected record, preserve original sources and unaffected outcomes, and reopen only affected work. Continue/resume reconciles actual source and worker state; it does not automatically replay every completed phase or create another task.

Show the real checklist during planning and execution, using ordinary Markdown or an actually supported and acknowledged host checklist surface. Source capture helpers work with supplied accessible messages/transcripts; they do not retrieve unseen chat history. See the [record contract](references/record-contract.md).

## Install the complete package

Use the distribution that matches your host. Preserve the complete contents; **copying only SKILL.md or agents/openai.yaml is not a complete installation**.

| Distribution | Archive layout | Use |
| --- | --- | --- |
| `ai-development-workflow-v2.0.0-plugin.zip` | Plugin metadata/artwork at the archive root; exactly one canonical skill under `skills/ai-development-workflow/` | Install/import through the plugin interface actually supported by your host. |
| `ai-development-workflow-v2.0.0-local-skill.zip` | `SKILL.md` and its complete runtime directories directly at the archive root | Extract the complete archive into a folder named `ai-development-workflow` in your local assistant's supported skill location. |
| Source checkout | Canonical skill at the repository root, with additional development/build files | Inspect, develop, test and create both exports from one source. |

Both exports include the complete canonical README/CHANGELOG, 41 command handlers, six substantive role families, shared capability bodies, meaningful legacy entries, 21 domain lenses, references, catalogues and helper dependencies. Each archive adds `PACKAGE-CONTENTS.json` listing paths, byte sizes and SHA-256 hashes of its other files. The plugin package also includes its small root entry README. These are complete fresh exports, not update overlays.

Python helpers require **Python 3.10+** and use the standard library. Browser, shell, editor/image tools, actual workers and wait/timer capabilities come from the host. Core instructions can be read without Python, but a missing required execution helper cannot be reported as a successful admission gate.

Keep task records, raw conversations, private inputs and debug logs outside the reusable installed package. The package supplies no store approval, automatic host activation or universal installation path. Verify the actual installed entry and resource access in the intended host.

## Validate and build releases

From a **source checkout**, run:

```bash
python3 -m unittest discover -s scripts/tests
python3 tools/build_release.py --check
python3 tools/build_release.py --output-dir dist
```

The builder checks required runtime contents, the six-family registry and full compatibility/capability mappings, command/operation dependencies, source links, version alignment, the single-entry plugin boundary and forbidden obsolete host plumbing before creating the archives. It verifies archive contents against source and emits package inventories. Source/package integrity checks do not prove installation or live agent/browser behavior.

`tools/`, `packaging/` and `scripts/tests/` are source-checkout development resources and are intentionally excluded from runtime exports. This README remains complete in both distributions; checkout-only commands above require the checkout rather than the installed runtime alone.

For local routing/selection inspection in either complete runtime:

```bash
python3 scripts/route_workflow.py --text '/ai-development-workflow auto Fix the scoped issue.'
python3 scripts/workflow_catalog.py --format json
```

See [optional debug logging](references/debug-logging.md) to enable local diagnostics for actual helper, shell and reported host events. Logging is **off by default**; it installs no telemetry service or background watcher.

Version `2.0.0` is the first formal Version 2 tag/release baseline. The next routine release is `2.0.1` under the [versioning policy](references/versioning-policy.md). A future GitHub release title is publication metadata, not the source version. Preparing, committing, publishing and activating a version remain distinct outcomes. See [CHANGELOG.md](CHANGELOG.md) for the complete Version 2 entry.

## Capabilities, privacy and rights

The workflow uses real available tools and current authorization. It cannot invent a missing browser, worker API, timer, private history source, upload result or installed model. Browser recovery uses the **current user's explicit session opt-in** and supported host operations; it does not transfer another owner's standing permission. See [host access](references/chatgpt-host.md) and [browser recovery](references/browser-recovery.md).

The public package contains reusable guidance, not personal chat history, private company defaults, account identifiers or task-specific permissions. Relevant private evidence stays with the task. Optional log redaction is best-effort; inspect real diagnostic contents before sharing. External tools and storage continue to operate under their own actual contracts.

The project is maintained by [aipieksel](https://github.com/aipieksel) and distributed under the included [MIT license](LICENSE). Preserve [source/permission notices](NOTICE.md) and the bundled [Ponytail](references/licenses/ponytail-MIT.txt) and [Ruflo](references/licenses/ruflo-MIT.txt) credits. Required publisher and upstream attribution remain accurate. Removing omitted integration components does not relicense them.

## Support and security reports

For bugs, feature requests and documentation questions, [open a GitHub issue](https://github.com/aipieksel/ai-development-workflow/issues). Include the package version, the host you are using, steps to reproduce the issue and relevant sanitized output. Omit private task records, conversations, credentials and account data.

For a sensitive security report, first request a private reporting route without posting exploit details or private data in the public issue. This project does not advertise a separate security email or guarantee that a private-reporting feature is enabled.
