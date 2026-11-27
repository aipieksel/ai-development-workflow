# Complete advanced reference

Version **2.0.4**. Start with the [main guide](../README.md) and
[five public modes](public-modes.md). This reference documents the complete retained command,
operation, recipe and role inventory. It is a lookup resource; Auto loads relevant instructions
progressively instead of evaluating every row for every task. The authoritative
[task routing](task-routing.md) policy applies to every entry below: choose a concrete
mode and obtain useful contributions from at least two distinct actual workers, excluding the coordinator.

## Contents

- [Exact invocation syntax](#exact-invocation-syntax)
- [Write scopes and phase meanings](#write-scopes-and-phase-meanings)
- [All 41 G commands](#all-41-g-commands)
- [Atomic command dependencies](#atomic-command-dependencies)
- [Numeric controls and continuation](#numeric-controls-and-continuation)
- [Task recipes](#task-recipes)
- [All 26 internal operations](#all-26-internal-operations)
- [All 21 specialist lenses](#all-21-specialist-lenses)
- [Six families and all 38 legacy mappings](#six-families-and-all-38-legacy-mappings)
- [Combine capabilities without duplicate work](#combine-capabilities-without-duplicate-work)
- [Records, evidence and helpers](#records-evidence-and-helpers)
- [Compatibility and retired interfaces](#compatibility-and-retired-interfaces)

## Exact invocation syntax

In ChatGPT, type `@`, start typing `AI` and select **AI Development Workflow** from autocomplete.
There is one public entry skill. Then write the mode/G control and task. Text examples show the
selected skill as `@ai-development-workflow`; typing a tag alone does not install or attach it.
Local hosts may use `$ai-development-workflow` through their supported skill interface.

The bundled router accepts the following explicit forms. These parsing interfaces do not
promise that a host separately registers every slash launcher or role name.

| Control | Accepted form | Meaning |
| --- | --- | --- |
| Default/Auto | `@ai-development-workflow auto <task>`; attached main skill plus ordinary task prose | Resolve Plan, Build, Review or Loop and assign real workers from intent and inspected impact. |
| Public modes | `plan <task>`, `build <task>`, `review <task>`, `loop <task>` after selecting the main skill | Use the five-mode contracts. Bare explicit controls are also accepted by `--text`. |
| G command | `/ai-development-workflow GAS <task>`; explicit `GAS <task>` | Select the exact named G handler. |
| Named handler | `/ai-dev-assess-only <task>`; `ai-dev-assess-only <task>` | Explicit router compatibility form for the same G command; no separate public skill required. |
| Recipe | `/ai-development-workflow recipe reference-rebuild <task>` | Main prefix required for explicit recipe syntax; Auto may also choose a recipe semantically. |
| Numeric | `/ai-development-workflow 0123 <task>`; explicit `0 1 2 3 <task>` | Legacy record phases; preserve the leading zero. |
| Loop compatibility | `XR <task>`; `/ai-dev-loop <task>`; `/ai-dev-execute-review <task>` | Canonical result is Loop. |
| Help | `/ai-development-workflow menu`; `--menu`; `help` | Ordinary help with five modes; no custom popup. |
| Continuation | `resume`; `--follow-up` with actual selected preset/mode context | Continue the same selected work and its current authorization. |

The main prefix accepts `@`, `/` or `$`, including the namespaced main form. The optional
`/aidw` shortcut is recognized by the parser; actual host composer registration is host-dependent.
Retained aliases are `GO → G0`, `ponytail → GB`, `agent-goal-planner → GPL` and
`agent-code-goal-planner → GCP`. Historical A profiles are record compatibility, not current commands.

Use `--task` for literal ordinary prose. Use `--text` only for a caller-identified explicit
control. This prevents “Go through…”, “3 columns…” or quoted old commands from becoming syntax.
Read-only intent still constrains literal prose; it is not permission to ignore “plan only.”

```bash
python3 scripts/route_workflow.py --task 'Go through this implementation and report the gaps.'
python3 scripts/route_workflow.py --text '@ai-development-workflow plan Criticize the migration plan.'
python3 scripts/route_workflow.py --text '/ai-development-workflow recipe visual-correction Fix the specified spacing.'
python3 scripts/route_workflow.py --text 'GPR Review the selected plan.'
python3 scripts/route_workflow.py --text 'resume' --selected-mode loop
```

The router prints a route description. `--schedule` prints an expected order; neither action
executes work, allocates a record, launches agents or starts monitoring.

## Write scopes and phase meanings

| Scope | Allowed surface | Boundary |
| --- | --- | --- |
| `record-only` | Selected task records and evidence | Product code, tests, configuration and project documentation remain unchanged. |
| `test-output-only` | Authorized checks and their logs/traces/results | No source or test edits to force a pass. |
| `tests-only` | Exact reviewed test files and fixtures | No production implementation. |
| `docs-only` | Exact reviewed project documentation | No production changes or invented functionality. |
| `repo-write-scoped` | Paths/behavior admitted by the current plan | The scope ceiling does not authorize every repository file. |
| `inherit-stage` | The selected operation’s scope | Specialist expertise creates no additional authority. |

Legacy phases are **0 capture/create**, **1 plan**, **2 criticize/revise**, **3 execute/verify**.
Every product writer still needs the actual current plan, completed criticism, public phase/role
briefing and successful admission. Missing phase digits cannot waive prerequisites. Task evidence
needed to plan or criticize can be written within the preparation scope.

Command tables describe duties, not already-running agents. Every new logical task needs
at least two distinct actual worker contributors, excluding the coordinator, including tiny,
Plan, Review and standalone operation invocations. The tables show command-specific duties;
the coordinator supplies any additional critic, corroborator, Architect, UI Director or
Verification Engineer required by [task routing](task-routing.md). Report required/returned
contributors separately from active workers. Capacity may be sequential.

Every source writer needs independent plan criticism and result acceptance. Record all
substantive authors, including adopted architecture/design and coordinator integration.
A change of role does not erase authorship. Read-only work keeps its scope while a second
worker contributes a bounded critique or corroboration. Bounded child assignments do not
recursively launch teams. Capability names below select instructions; they are not extra
public modes or permission to broaden the operation.

## All 41 G commands

The following 22 retained full-workflow/planning commands preserve their selected operations
and record boundaries; universal staffing and impact rules apply.
“New” means a standalone invocation allocates one record; a selected composition reuses its
shared record instead of replaying allocation. All linked files contain real command instructions.

| Code | Exact launcher and purpose | Phases / record | Agent expectation | Write scope |
| --- | --- | --- | --- | --- |
| G0 | [ai-dev-quick-task](../commands/quick-task/ai-dev-quick-task.md) — Quick Task | New record; Compact scope → plan → critique → implement → verify | Reviewer (`review-plan`, `review-code`); Builder (`execute-plan`, `fast-build`); complete the required team | `repo-write-scoped` |
| GS | [ai-dev-codebase-assessment](../agents/codebase-assessor/commands/ai-dev-codebase-assessment.md) — Assess, plan, review and build | New record; 0 → 1 → 2 → 3 | Investigator (`assess-codebase`); complete the required team | `repo-write-scoped` |
| GPL | [ai-dev-goal-plan](../agents/goal-planner/commands/ai-dev-goal-plan.md) — Goal Planner — plan only | New record; 0 → 1 | Architect and Planner (`plan-goals`); complete the required team | `record-only` |
| GCP | [ai-dev-code-plan](../agents/code-goal-planner/commands/ai-dev-code-plan.md) — Code Goal Planner — plan only | New record; 0 → 1 | Architect and Planner (`plan-code`); complete the required team | `record-only` |
| GA | [ai-dev-architecture](../agents/architect/commands/ai-dev-architecture.md) — Architecture, plan and build | New record; 0 → 1 → 2 → 3 | Architect and Planner (`design-architecture`); complete the required team | `repo-write-scoped` |
| G1 | [ai-dev-build](../commands/ai-dev-build.md) — Standard plan and build | New record; 0 → 1 → 2 → 3 | Reviewer (`review-plan`, `review-code`); Builder (`execute-plan`); complete the required team | `repo-write-scoped` |
| GB | [ai-dev-fast-build](../agents/fast-engineer/commands/ai-dev-fast-build.md) — Fast full build | New record; 0 → 1 → 2 → 3 | Reviewer (`review-plan`, `review-code`); Builder (`execute-plan`, `fast-build`); complete the required team | `repo-write-scoped` |
| GT | [ai-dev-test-first](../agents/tdd-guide/commands/ai-dev-test-first.md) — Full test-first build | New record; 0 → 1 → 2 → 3 | Builder (`execute-plan`, `tdd`); complete the required team | `repo-write-scoped` |
| G7 | [ai-dev-visual-fidelity](../agents/visual-fidelity/commands/ai-dev-visual-fidelity.md) — Visual Fidelity | New record; 0 → 1 → 2 → 3 | UI Director (`visual-fidelity`, `ui-design`); Builder (`execute-plan`, `visual-fidelity`, `ui-design`); complete the required team | `repo-write-scoped` |
| GEA | [ai-dev-e2e-execute](../agents/e2e-runner/commands/ai-dev-e2e-execute.md) — Delegate to E2E Agent | New record; 0 → 1 → 2 → delegated 3 | Builder (`execute-plan`, `run-e2e`); complete the required team | `repo-write-scoped` |
| GCA | [ai-dev-review-execute](../agents/code-reviewer/commands/ai-dev-review-execute.md) — Delegate to Code Reviewer | Existing record; 1 → 2 → delegated 3 | Builder (`execute-plan`, `review-code`); complete the required team | `repo-write-scoped` |
| GR | [ai-dev-cleanup](../agents/refactor-cleaner/commands/ai-dev-cleanup.md) — Build and Cleanup | New record; 0 → 1 → 2 → 3 | Builder (`execute-plan`, `cleanup`); complete the required team | `repo-write-scoped` |
| GH | [ai-dev-repo-hygiene](../agents/refactor-cleaner/commands/ai-dev-repo-hygiene.md) — AI Repository Hygiene | New record; 0 → 1 → 2 → 3 | Builder (`execute-plan`, `cleanup`); complete the required team | `repo-write-scoped` |
| GF | [ai-dev-feature-finalise](../agents/feature-finaliser/commands/ai-dev-feature-finalise.md) — AI Feature Finalisation | New record; 0 → 1 → 2 → 3 | Builder (`execute-plan`, `delivery`); complete the required team | `repo-write-scoped` |
| GC | [ai-dev-code-review](../agents/code-reviewer/commands/ai-dev-code-review.md) — Build and Code Review | New record; 0 → 1 → 2 → 3 | Reviewer (`review-code`); complete the required team | `repo-write-scoped` |
| GX | [ai-dev-security](../agents/security-verifier/commands/ai-dev-security.md) — AI Security Verification | New record; 0 → 1 → 2 → 3 | Builder (`execute-plan`, `review-security`); complete the required team | `repo-write-scoped` |
| GU | [ai-dev-accessibility](../agents/accessibility-verifier/commands/ai-dev-accessibility.md) — AI Accessibility and Interaction QA | New record; 0 → 1 → 2 → 3 | Builder (`execute-plan`, `review-accessibility`, `ui-design`); complete the required team | `repo-write-scoped` |
| GE | [ai-dev-e2e-tests](../agents/e2e-runner/commands/ai-dev-e2e-tests.md) — Build and E2E Tests | New record; 0 → 1 → 2 → 3 | Verification Engineer (`run-e2e`); complete the required team | `repo-write-scoped` |
| GJ | [ai-dev-journey-tests](../agents/e2e-runner/commands/ai-dev-journey-tests.md) — AI Journey Test Automation | New record; 0 → 1 → 2 → 3 | Builder (`execute-plan`, `author-e2e`, `run-e2e`); complete the required team | `repo-write-scoped; tests/fixtures/CI only` |
| GP | [ai-dev-performance](../agents/performance-verifier/commands/ai-dev-performance.md) — AI Performance and Resilience | New record; 0 → 1 → 2 → 3 | Builder (`execute-plan`, `verify-performance`); complete the required team | `repo-write-scoped` |
| GD | [ai-dev-documentation](../agents/doc-updater/commands/ai-dev-documentation.md) — Build and Documentation | New record; 0 → 1 → 2 → 3 | Builder (`update-docs`); complete the required team | `repo-write-scoped` |
| G6 | [ai-dev-full-checks](../commands/ai-dev-full-checks.md) — Build, Docs, E2E and Review | New record; 0 → 1 → 2 → 3 | Builder (`update-docs`); Verification Engineer (`run-e2e`); Reviewer (`review-code`); complete the required team | `repo-write-scoped` |

Several names are historical: **GC, GX, GU, GE, GP and GD include implementation or repairs**.
Use Review or their verification-only counterparts when the task is read-only. **GCA is an
executor assignment** resolved to Builder with execution and code-review knowledge. GVR remains independent read-only review.
G0, G1 and GB have no solo or writing self-critique exemption. Auto uses GB for known,
bounded local changes; an explicit G0 keeps its compact record. A one-file shared component
can still require Architect advice. “Fast” preserves planning, independent criticism,
complete scope and independent result acceptance.

The remaining 19 commands are bounded operations. Their prerequisites appear below.

| Code | Exact launcher and purpose | Phase / record | Agent expectation | Write scope |
| --- | --- | --- | --- | --- |
| GAS | [ai-dev-assess-only](../commands/stages/ai-dev-assess-only.md) — Codebase assessment only | New record; 0 | Investigator (`assess-codebase`); complete the required team | `record-only` |
| GRS | [ai-dev-research-only](../commands/stages/ai-dev-research-only.md) — Research only | New record; 0 | Investigator (`research-technical`); complete the required team | `record-only` |
| GDA | [ai-dev-design-audit](../commands/stages/ai-dev-design-audit.md) — Design audit only | New record; 0 | UI Director (`audit-ui`, `ui-design`); complete the required team | `record-only` |
| GAA | [ai-dev-architecture-advice](../commands/stages/ai-dev-architecture-advice.md) — Architecture assessment only | Existing record; atomic assignment | Architect and Planner (`design-architecture`); complete the required team | `record-only` |
| GDS | [ai-dev-design-spec](../commands/stages/ai-dev-design-spec.md) — Design specification only | Existing record; atomic assignment | UI Director (`design-ui`, `ui-design`); complete the required team | `record-only` |
| GPP | [ai-dev-plan-from-evidence](../commands/stages/ai-dev-plan-from-evidence.md) — Plan from assessment | Existing record; phase 1 | Architect and Planner (`plan-code`); complete the required team | `record-only` |
| GPR | [ai-dev-review-plan-only](../commands/stages/ai-dev-review-plan-only.md) — Review and refine plan | Existing record; phase 2 | Reviewer (`review-plan`); complete the required team | `record-only` |
| GTF | [ai-dev-write-red-tests](../commands/stages/ai-dev-write-red-tests.md) — Write failing tests (TDD red) | Existing record; atomic assignment | Builder (`write-red-tests`); complete the required team | `tests-only` |
| GEX | [ai-dev-execute-plan](../commands/stages/ai-dev-execute-plan.md) — Execute reviewed plan | Existing record; atomic assignment | Builder (`execute-plan`); complete the required team | `repo-write-scoped` |
| GTE | [ai-dev-execute-tdd](../commands/stages/ai-dev-execute-tdd.md) — Execute TDD plan (green) | Existing record; atomic assignment | Builder (`execute-plan`, `green-refactor`); complete the required team | `repo-write-scoped` |
| GUT | [ai-dev-unit-verify-only](../commands/stages/ai-dev-unit-verify-only.md) — Unit and integration verification | Existing record; atomic assignment | Verification Engineer (`run-tests`); complete the required team | `test-output-only` |
| GVE | [ai-dev-e2e-verify-only](../commands/stages/ai-dev-e2e-verify-only.md) — End-to-end verification only | Existing record; atomic assignment | Verification Engineer (`run-e2e`); complete the required team | `test-output-only` |
| GVR | [ai-dev-review-code-only](../commands/stages/ai-dev-review-code-only.md) — Independent code review only | Existing record; atomic assignment | Reviewer (`review-code`); complete the required team | `record-only` |
| GVS | [ai-dev-security-verify-only](../commands/stages/ai-dev-security-verify-only.md) — Security verification only | Existing record; atomic assignment | Verification Engineer (`review-security`); complete the required team | `record-only` |
| GVA | [ai-dev-a11y-verify-only](../commands/stages/ai-dev-a11y-verify-only.md) — Accessibility verification only | Existing record; atomic assignment | Verification Engineer (`review-accessibility`, `ui-design`); complete the required team | `record-only` |
| GVP | [ai-dev-performance-verify-only](../commands/stages/ai-dev-performance-verify-only.md) — Performance verification only | Existing record; atomic assignment | Verification Engineer (`verify-performance`); complete the required team | `test-output-only` |
| GVD | [ai-dev-update-docs-only](../commands/stages/ai-dev-update-docs-only.md) — Update documentation only | Existing record; atomic assignment | Builder (`update-docs`); complete the required team | `docs-only` |
| GCL | [ai-dev-clean-only](../commands/stages/ai-dev-clean-only.md) — Cleanup existing implementation | Existing record; atomic assignment | Builder (`execute-plan`, `cleanup`); complete the required team | `repo-write-scoped` |
| GRC | [ai-dev-contribution-discovery](../agents/contribution-scout/commands/ai-dev-contribution-discovery.md) — Repository Contribution Scout | New record; 0 | Investigator (`discover-contributions`); complete the required team | `record-only` |

## Atomic command dependencies

These are the artifact names declared by the G handlers. **All** inputs are required;
an **Any** list requires at least one actual matching artifact. Absence of declared inputs
does not waive source, authority, operation-plan or capability checks. Product writers also
need the actual concrete plan and completed criticism under the shared admission contract.

| Command | All inputs | Any input | Produces |
| --- | --- | --- | --- |
| GPL | — | — | `plan` |
| GCP | — | — | `plan` |
| GAS | — | — | `assessment` |
| GRS | — | — | `research` |
| GDA | — | — | `design_audit` |
| GAA | — | `assessment`, `plan` | `architecture` |
| GDS | `design_audit` | — | `design_spec` |
| GPP | — | `assessment`, `design_spec` | `plan` |
| GPR | `plan` | — | `plan_review` |
| GTF | `plan_review` | — | `red_tests` |
| GEX | `plan_review` | — | `implementation` |
| GTE | `plan_review`, `red_tests` | — | `implementation` |
| GUT | `implementation` | — | `unit_verification` |
| GVE | `implementation` | — | `e2e_verification` |
| GVR | `implementation` | — | `code_review` |
| GVS | `implementation` | — | `security_verification` |
| GVA | `implementation` | — | `accessibility_verification` |
| GVP | `implementation` | — | `performance_verification` |
| GVD | `implementation`, `plan_review` | — | `documentation` |
| GCL | `implementation`, `plan_review` | — | `cleanup` |
| GRC | — | — | `contribution.portfolio` |

The legacy metadata field named `queue` now describes these dependency declarations; it does
not supply a queue runner. The catalogue explicitly normalizes the shipped artifact aliases
for composition: assessment→assessment.report, research→research.report, design_audit→design.audit,
architecture→architecture.advice, design_spec→ui.spec, plan→code.plan, plan_review→plan.review,
red_tests→tdd.red.evidence, implementation→execution.result, unit_verification→test.results,
e2e_verification→e2e.results, code_review→review.findings, security_verification→security.review,
accessibility_verification→accessibility.review, performance_verification→performance.results,
documentation→docs.change. Normalization does not create or inspect the evidence.

GEX's plan_review input must refer to the actual current executable plan, not an unrelated
review. GTF/GTE require real intentional RED evidence where specified. GVD and GCL consume
implementation plus current reviewed coverage. Fresh review/testing of existing work can use
the corresponding internal snapshot operation instead of fabricating implementation history.

## Numeric controls and continuation

These legacy controls operate on the selected record. Public `plan` is now the complete
Plan mode, not an alias for numeric 1. Use the exact numeric control for its historical semantics.

| Control | Meaning | Creates a record? |
| --- | --- | --- |
| `0` | Capture/create a draft only; no planning or implementation | Yes, once |
| `01` | Capture and plan; no execution | Yes, once |
| `012` | Capture, plan, criticize/revise; no execution | Yes, once |
| `013` | Capture, plan, satisfy current criticism, execute/verify | Yes, once |
| `0123` | Capture, plan, criticize/revise, execute/verify | Yes, once |
| `1` | Plan or update the selected record | No |
| `2`, `criticize`, `criticise` | Criticize and correct the selected plan | No |
| `3`, `execute` | Execute after all current admission prerequisites | No |
| `12` | Plan, then criticize | No |
| `13` | Plan, satisfy current criticism, then execute | No |
| `23` | Criticize, then execute | No |
| `123` | Update the selected plan, criticize, execute | No |
| `revise`, `r` | Amend the selected plan only; preserve history | No |
| `resume` | Reconcile and continue selected interrupted work under its original scope | No |

Compact and spaced forms are equivalent: `0123` and `0 1 2 3`. Unsupported sequences include
`02`, `03`, `023`, `21`, `11`, `321` and `10`. They must not silently become another workflow.
Combining stage 0 with a leading existing-record selector is conflicting. New standalone G
starters likewise cannot silently discard an explicit existing-record selection.

For existing work, `--plan <record>` or `--record <record>` identifies the record; quote spaces.
Otherwise use the record actually selected in the conversation, not filesystem recency or a
similar older task. A chat-only plan is source evidence until a permitted capture step creates
its durable record. Public modes handle fresh capture without asking for a numeric code.

G0 uses its compact checklist record and its own admission helper. Ordinary continuation or
`resume` retains that record; development-only numeric phases cannot operate on it. Loop can
make an explicitly announced one-time promotion to a development record while preserving the
original checklist and provenance. GPL/GCP resume remains planning-only until actual implementation
is authorized. Loop continuations retain `--selected-mode loop` (legacy XR accepted); conflicting
numeric operations require an explicit intended legacy-workflow selection.

### Conversation-time anchors

```text
$ai-development-workflow 0123 11:24 PM
$ai-development-workflow 0 1 2 3 23:24
$ai-development-workflow 0123 2030-01-15 11:24 PM "check each item"
```

A time immediately after a numeric control anchors the conversation source range. It is not a
deadline or timer. Resolve the displayed local/UI timestamp and timezone from actual metadata;
apply an explicit date/quote first, then choose the latest matching user/assistant message
through the invocation. Include that message and every subsequent user/assistant message through
the invocation. Exclude automated instruction attachments and duplicate/tool events. Do not use
the nearest nonmatching time or invent unavailable timestamps. Preserve the resolved range and
later corrections; an anchor does not erase unrelated existing requirements or change record rules.
See [source and timestamp rules](standard-workflow.md#optional-conversation-start-time).

## Task recipes

All ten are portable patterns within Auto or the explicit main-prefix `recipe <id>` control.
They use internal operations, not separately installed agents. The catalogue defines the exact
ordered expansion. A bounded task may borrow a justified subset while recording what actually
ran; a full-recipe claim must cover its required steps and bindings. All recipes have a
`repo-write-scoped` ceiling, which the actual task can narrow to planning or analysis.

| Recipe ID and instructions | Purpose | Recommended specialist lenses |
| --- | --- | --- |
| `reference-rebuild` — [Rebuild from a supplied reference](../task-recipes/reference-rebuild.md) | Reconstruct supplied HTML, screenshots or extracted pages while preserving declared source details and validating the rendered result. | ui-design, reference-fidelity, browser-extraction, artifact-delivery |
| `visual-correction` — [Repair precise visual feedback](../task-recipes/visual-correction.md) | Apply itemized corrections to the current approved artifact and verify the requested delta together with protected properties. | ui-design, reference-fidelity, design-system |
| `design-system-rollout` — [Roll out shared design changes](../task-recipes/design-system-rollout.md) | Update canonical components, typography and theme presets across a declared target set, checking affected states and exported outputs. | ui-design, design-system, reference-fidelity, artifact-delivery |
| `native-yaml-conversion` — [Convert to native editable YAML](../task-recipes/native-yaml-conversion.md) | Map supplied sources to the receiving kit and real widget capabilities, then validate editable structure, assets and import/render parity. | ui-design, native-yaml-archives, editor-schema, reference-fidelity, artifact-delivery |
| `asset-production` — [Produce or edit a visual asset set](../task-recipes/asset-production.md) | Create source-aware images, SVGs or banner variants with explicit composition constraints, distinct concepts where requested and complete output reconciliation. | ui-design, image-art-direction, reference-fidelity, artifact-delivery |
| `motion-reconstruction` — [Reconstruct and verify motion](../task-recipes/motion-reconstruction.md) | Preserve or repair supplied animation and interactive behavior using an explicit sequence and observed full-cycle verification. | ui-design, motion-interaction, reference-fidelity, browser-extraction |
| `media-library-extension` — [Extend an existing media workspace](../task-recipes/media-library-extension.md) | Integrate media conversion or navigation into the current library, reusing folder identity, tree controls, drop behavior and persisted state. | media-library, editor-schema, migration-release |
| `content-site-delivery` — [Deliver a source-grounded content site](../task-recipes/content-site-delivery.md) | Reconcile requested pages and source content, reuse the approved presentation and verify routes, metadata, links and delivered artifacts. | content-seo, design-system, artifact-delivery |
| `artifact-handoff` — [Verify and deliver an artifact](../task-recipes/artifact-handoff.md) | Reconcile final source and package identity, repair in-scope delivery defects and verify the authorized destination with readback. | artifact-delivery, migration-release |
| `plugin-evolution` — [Improve a plugin from actual usage](../task-recipes/plugin-evolution.md) | Analyze available usage evidence, map current coverage, implement justified instruction or routing changes and verify the same plugin release. | usage-learning, plugins-mcp, artifact-delivery |

### Exact default operation expansions

The `stage:` prefix is omitted below for readability. These are internal chain identifiers,
not shell commands. Preserve actual prerequisite evidence when reusing or shortening a pattern.

| Recipe | Ordered operations | Extra required planning inputs |
| --- | --- | --- |
| reference-rebuild | `assess-codebase` → `design-ui` → `review-ui-spec` → `plan-code` → `review-plan` → `execute-plan` → `run-e2e` → `review-ui` → `review-accessibility` → `verify-goal` | plan-code: assessment.report, ui.spec, ui.spec.review |
| visual-correction | `assess-codebase` → `diagnose-failure` → `design-ui` → `plan-code` → `review-plan` → `execute-plan` → `review-ui` → `verify-goal` | plan-code: assessment.report, diagnosis.report, ui.spec |
| design-system-rollout | `assess-codebase` → `design-ui` → `review-ui-spec` → `plan-code` → `review-plan` → `execute-plan` → `run-tests` → `run-e2e` → `review-ui` → `review-accessibility` → `verify-goal` | plan-code: assessment.report, ui.spec, ui.spec.review |
| native-yaml-conversion | `assess-codebase` → `design-ui` → `plan-code` → `review-plan` → `execute-plan` → `run-tests` → `review-ui` → `verify-goal` | plan-code: assessment.report, ui.spec |
| asset-production | `assess-codebase` → `design-ui` → `plan-code` → `review-plan` → `execute-plan` → `review-ui` → `verify-goal` | plan-code: assessment.report, ui.spec |
| motion-reconstruction | `assess-codebase` → `extract-behaviour-spec` → `design-ui` → `plan-code` → `review-plan` → `execute-plan` → `run-e2e` → `review-ui` → `review-accessibility` → `verify-goal` | plan-code: assessment.report, behaviour.spec, ui.spec |
| media-library-extension | `assess-codebase` → `extract-behaviour-spec` → `plan-code` → `review-plan` → `execute-plan` → `run-tests` → `run-e2e` → `review-code` → `verify-goal` | plan-code: assessment.report, behaviour.spec |
| content-site-delivery | `assess-codebase` → `plan-code` → `review-plan` → `execute-plan` → `run-tests` → `run-e2e` → `verify-goal` | plan-code: assessment.report |
| artifact-handoff | `assess-codebase` → `plan-code` → `review-plan` → `execute-plan` → `run-tests` → `verify-goal` | plan-code: assessment.report |
| plugin-evolution | `research-technical` → `assess-codebase` → `extract-behaviour-spec` → `plan-code` → `review-plan` → `execute-plan` → `run-tests` → `review-code` → `update-docs` → `verify-goal` | plan-code: assessment.report, research.report, behaviour.spec |

```text
@ai-development-workflow recipe reference-rebuild Rebuild the supplied page and preserve its approved layout and interactions.
@ai-development-workflow recipe native-yaml-conversion Convert this source through the supplied editor kit and verify editability.
@ai-development-workflow recipe plugin-evolution Improve this plugin from the supplied failure evidence and verify the full package.
```

The UI director is added whenever actual visual outcomes require it, even if another recipe's
static recommended-lens list does not include it. A recipe cannot provide a missing image tool,
browser, editor schema, importer or destination permission. Use the actual owner tool/skill.

## All 26 internal operations

These operations are selected inside Auto/composition and recipes. Their full instruction
bodies live under `workflows/stages/`. Public native `stage <id>` and `pipeline <id>` invocations
are retired. Naming an operation in normal task prose can guide selection; it does not dispatch it.

| Internal ID / instruction | Role | Required inputs → outputs | Write scope |
| --- | --- | --- | --- |
| `stage:research-technical` — [Research Technical Options](../workflows/stages/research-technical.md) | [Investigator](../agents/investigator/agent.md) — `research-technical` | `request` → `research.report` | `record-only` |
| `stage:discover-contributions` — [Repository Contribution Scout](../workflows/stages/discover-contributions.md) | [Investigator](../agents/investigator/agent.md) — `discover-contributions` | `request`, `repo.snapshot` → `contribution.portfolio` | `record-only` |
| `stage:assess-codebase` — [Assess Codebase](../workflows/stages/assess-codebase.md) | [Investigator](../agents/investigator/agent.md) — `assess-codebase` | `request`, `repo.snapshot` → `assessment.report` | `record-only` |
| `stage:diagnose-failure` — [Diagnose Root Cause](../workflows/stages/diagnose-failure.md) | [Investigator](../agents/investigator/agent.md) — `diagnose-failure` | `request`, `repo.snapshot` → `diagnosis.report` | `record-only` |
| `stage:extract-behaviour-spec` — [Extract Existing Behaviour](../workflows/stages/extract-behaviour-spec.md) | [Investigator](../agents/investigator/agent.md) — `extract-behaviour-spec` | `repo.snapshot` → `behaviour.spec` | `record-only` |
| `stage:plan-goals` — [Plan Goals](../workflows/stages/plan-goals.md) | [Architect and Planner](../agents/architect/agent.md) — `plan-goals` | `request`, `repo.snapshot` → `goal.plan` | `record-only` |
| `stage:design-architecture` — [Consult Architecture](../workflows/stages/design-architecture.md) | [Architect and Planner](../agents/architect/agent.md) — `design-architecture` | `request`, `repo.snapshot` → `architecture.advice` | `record-only` |
| `stage:design-ui` — [Design UI](../workflows/stages/design-ui.md) | [UI Director](../agents/ui-design-director/agent.md) — `design-ui`, `ui-design` | `request`, `repo.snapshot` → `ui.spec` | `record-only` |
| `stage:review-ui-spec` — [Review UI Specification](../workflows/stages/review-ui-spec.md) | [Reviewer](../agents/reviewer/agent.md) — `review-ui-spec`, `ui-design` | `ui.spec`, `repo.snapshot` → `ui.spec.review` | `record-only` |
| `stage:plan-code` — [Plan Code Changes](../workflows/stages/plan-code.md) | [Architect and Planner](../agents/architect/agent.md) — `plan-code` | `request`, `repo.snapshot` → `code.plan` | `record-only` |
| `stage:plan-tests` — [Plan Tests Only](../workflows/stages/plan-tests.md) | [Architect and Planner](../agents/architect/agent.md) — `plan-tests` | `request`, `repo.snapshot` → `test.strategy` | `record-only` |
| `stage:review-plan` — [Review Plan](../workflows/stages/review-plan.md) | [Reviewer](../agents/reviewer/agent.md) — `review-plan` | `code.plan`, `request`, `repo.snapshot` → `plan.review` | `record-only` |
| `stage:write-red-tests` — [Write Failing Tests](../workflows/stages/write-red-tests.md) | [Builder](../agents/builder/agent.md) — `write-red-tests` | `code.plan`, `plan.review`, `repo.snapshot` → `tdd.red.evidence` | `tests-only` |
| `stage:execute-plan` — [Execute Approved Plan](../workflows/stages/execute-plan.md) | [Builder](../agents/builder/agent.md) — `execute-plan` | `code.plan`, `plan.review`, `repo.snapshot` → `execution.result` | `repo-write-scoped` |
| `stage:fix-reviewed-defects` — [Fix Reviewed Defects](../workflows/stages/fix-reviewed-defects.md) | [Builder](../agents/builder/agent.md) — `fix-reviewed-defects` | `code.plan`, `plan.review`, `review.findings`, `repo.snapshot` → `execution.result` | `repo-write-scoped` |
| `stage:run-tests` — [Run Tests & Validation](../workflows/stages/run-tests.md) | [Verification Engineer](../agents/verification-engineer/agent.md) — `run-tests` | `repo.snapshot` → `test.results` | `test-output-only` |
| `stage:run-e2e` — [Run End-to-End Tests](../workflows/stages/run-e2e.md) | [Verification Engineer](../agents/verification-engineer/agent.md) — `run-e2e` | `repo.snapshot` → `e2e.results` | `test-output-only` |
| `stage:review-code` — [Review Code](../workflows/stages/review-code.md) | [Reviewer](../agents/reviewer/agent.md) — `review-code` | `repo.snapshot` → `review.findings` | `record-only` |
| `stage:review-ui` — [Review Visual Fidelity](../workflows/stages/review-ui.md) | [Verification Engineer](../agents/verification-engineer/agent.md) — `review-ui`, `ui-design` | `repo.snapshot`, `ui.spec` → `ui.visual.review` | `record-only` |
| `stage:review-accessibility` — [Review Accessibility](../workflows/stages/review-accessibility.md) | [Verification Engineer](../agents/verification-engineer/agent.md) — `review-accessibility`, `ui-design` | `repo.snapshot` → `accessibility.review` | `record-only` |
| `stage:review-security` — [Review Security](../workflows/stages/review-security.md) | [Verification Engineer](../agents/verification-engineer/agent.md) — `review-security` | `repo.snapshot` → `security.review` | `record-only` |
| `stage:review-dependencies` — [Review Dependency Risk](../workflows/stages/review-dependencies.md) | [Reviewer](../agents/reviewer/agent.md) — `review-dependencies` | `repo.snapshot` → `dependency.review` | `record-only` |
| `stage:verify-goal` — [Verify Delivered Goals](../workflows/stages/verify-goal.md) | [Reviewer](../agents/reviewer/agent.md) — `verify-goal` | `request`, `repo.snapshot` → `goal.verification` | `record-only` |
| `stage:update-docs` — [Update Documentation](../workflows/stages/update-docs.md) | [Builder](../agents/builder/agent.md) — `update-docs` | `code.plan`, `plan.review`, `repo.snapshot` → `docs.change` | `docs-only` |
| `stage:verify-docs` — [Verify Documentation](../workflows/stages/verify-docs.md) | [Reviewer](../agents/reviewer/agent.md) — `verify-docs` | `repo.snapshot`, `docs.change` → `docs.verification` | `record-only` |
| `stage:verify-performance` — [Verify Performance](../workflows/stages/verify-performance.md) | [Verification Engineer](../agents/verification-engineer/agent.md) — `verify-performance` | `repo.snapshot` → `performance.results` | `test-output-only` |

Source-backed snapshot operations can inspect existing code or artifacts without inventing
an earlier implementation result. Plan/code/test writers retain their current review gate.
The operation policy assigns meaningful operations to real workers and preserves independent
review assignments. Coordinator preparation, handoff integration and authorized publication
remain legitimate work; they do not substitute for the required specialists. Removing obsolete
native-dispatch metadata does not remove GPR, Loop or selected review independence.

## All 21 specialist lenses

Lenses provide domain expertise inside a selected operation and inherit its scope. They are
not separate public modes, new build engines or automatically running workers. There is no
standalone `specialist <id>` router command. Request the expertise in prose or let Auto select it
from actual source; the coordinator records the applied `specialist:<id>` values and assigns
the corresponding complete expertise to the real operation worker. Several compatible lenses
can share one worker. A lens does not require one new worker for each keyword.

| Lens ID / instructions | When it helps |
| --- | --- |
| `specialist:react-frontend` — [React and frontend systems](../specialists/react-frontend.md) | Apply the existing workflow to React interfaces, reusable components, responsive behaviour and frontend performance. |
| `specialist:editor-schema` — [Editors, registries and persistent schemas](../specialists/editor-schema.md) | Preserve native widget models, nested editability, preset inheritance and persistent tree/configuration semantics across every editor surface. |
| `specialist:wordpress-woocommerce` — [WordPress and WooCommerce](../specialists/wordpress-woocommerce.md) | Use WordPress and commerce-specific lifecycle, data, permissions and compatibility checks. |
| `specialist:whmcs` — [WHMCS modules and client-area systems](../specialists/whmcs.md) | Assess and implement WHMCS extensions with verified hook contracts, lifecycle and account boundaries. |
| `specialist:plugins-mcp` — [Plugins, skills and MCP applications](../specialists/plugins-mcp.md) | Evolve plugin instructions, routers and tool/host contracts from evidence while preserving identity, explicit scope, compatibility and release provenance. |
| `specialist:browser-extraction` — [Browser evidence and website extraction](../specialists/browser-extraction.md) | Ground reconstruction and UI repair in identified source versions, asset dependencies and comparable rendered/interactive states. |
| `specialist:native-yaml-archives` — [Native YAML and archive conversion](../specialists/native-yaml-archives.md) | Map supplied HTML and the current kit to genuinely editable native widgets, presets and complete import packages with explicit custom-code exceptions. |
| `specialist:content-seo` — [Structured content and technical SEO](../specialists/content-seo.md) | Build and migrate source-grounded content collections with real destinations, preserved approved copy, coherent presentation and validated metadata/schema. |
| `specialist:python-data` — [Python automation and data pipelines](../specialists/python-data.md) | Build resumable data processing with validated inputs, explicit failures and reconciled outputs. |
| `specialist:database` — [Database schemas and data integrity](../specialists/database.md) | Apply engine-specific checks to migrations, queries, tenant access, locks and data compatibility. |
| `specialist:infrastructure` — [Infrastructure and deployment configuration](../specialists/infrastructure.md) | Ground infrastructure changes in provider versions, actual state, execution mode and recovery evidence. |
| `specialist:migration-release` — [Migration, recovery and release completion](../specialists/migration-release.md) | Resume interrupted work from real source and task evidence, preserve milestones and reconcile the requested repository/package/release outcome. |
| `specialist:realtime-native` — [Realtime media and native application lifecycles](../specialists/realtime-native.md) | Trace message identity, delivery/history, hidden/popout views and shared media ownership through the actual realtime or native runtime. |
| `specialist:reference-fidelity` — [Reference fidelity and precise corrections](../specialists/reference-fidelity.md) | Preserve approved source identity, constrain changes to requested deltas and verify observable results without collateral redesign. |
| `specialist:design-system` — [Shared design systems, typography and presets](../specialists/design-system.md) | Maintain canonical components, tokens, fonts, icons and saved visual presets consistently across consumers and interaction states. |
| `specialist:image-art-direction` — [Image art direction and consistent asset production](../specialists/image-art-direction.md) | Direct authorized image generation/editing with source-locked composition, consistent geometry and semantically distinct product concepts. |
| `specialist:motion-interaction` — [Motion, interactive widgets and temporal verification](../specialists/motion-interaction.md) | Model and verify meaningful animation sequences, transitions, controls and theme-dependent states over a complete relevant cycle. |
| `specialist:media-library` — [Media libraries, archive ingestion and local conversion](../specialists/media-library.md) | Extend existing media-workspace navigation, imports, storage and conversion while preserving identity, privacy and measurable fidelity. |
| `specialist:artifact-delivery` — [Artifact completeness and verified delivery](../specialists/artifact-delivery.md) | Reconcile complete deliverables, dependency closure, actual output revisions and authorized destination readback before claiming handoff. |
| `specialist:usage-learning` — [Usage evidence and workflow improvement](../specialists/usage-learning.md) | Analyze complete task evidence with deduplication and outcome limits, map demand to current capabilities and evaluate bounded plugin improvements. |
| `specialist:ui-design` — [UI Design Director](../specialists/ui-design.md) | Apply scoped visual corrections and a coherent design direction to every relevant UI task, with complete target review and evidence of visible quality. |

UI Design Director applies semantically to layout, palettes, typography, components, visual
content, image direction, motion and visual correction—not just requests containing “UI”.
It inspects the existing system, protects approved properties and demands relevant rendered
evidence. It uses project-specific approved sources; the public package contains no private
company palette or inherited owner permission. It does not incorporate UIUX Pro Max.

Native YAML and native-app lifecycle expertise remain generic domain capabilities. They do
not imply the removed editor selector/queue integration is present.

## Six families and all 38 legacy mappings

The six canonical families contain substantive worker instructions. `agents/openai.yaml`
provides main-skill display/invocation metadata; it does not implement worker behavior.
The coordinator reads the selected family's profile, complete capability instructions and
relevant domain lenses, then actually dispatches a worker with a bounded responsibility.

| Canonical family | Instructions | Typical contribution |
| --- | --- | --- |
| Investigator | [investigator](../agents/investigator/agent.md) | Evidence, ownership, root causes and existing behavior |
| Architect and Planner | [architect](../agents/architect/agent.md) | Architecture, code/goal planning and test strategy |
| Builder | [builder](../agents/builder/agent.md) | Fast/Ponytail, ordinary build, TDD, cleanup, documentation and delivery |
| UI Director | [ui-design-director](../agents/ui-design-director/agent.md) | Design direction, references, visual corrections, assets and interaction specifications |
| Reviewer | [reviewer](../agents/reviewer/agent.md) | Independent plan criticism and final acceptance |
| Verification Engineer | [verification-engineer](../agents/verification-engineer/agent.md) | Tests, browser journeys, accessibility, security, performance and delivery checks |

The registry retains **37 capability selectors**, **26 bounded operations** and **21 domain
lenses**. Its **38 original role mappings** preserve old command paths and operation semantics.
There are **42 physical role files**: six canonical bodies plus 36 nonempty compatibility
entries; the original Architect and UI Director paths are reused as canonical families.
Compatibility entries are redirects with explicit scope and capability rules, not another
38-worker roster.

The table below is a lookup for old references. Resolve **profile plus operation** using
[agents/registry.json](../agents/registry.json). An override applies only to its exact selected
operation and never grants write authority by itself. Explicit canonical assignments carry
capabilities to disambiguate generic verbs such as `consult`, `review` and `execute_and_test`.

| Original profile path | Default family and capabilities | Operation-specific overrides |
| --- | --- | --- |
| [agents/accessibility-verifier/agent.md](../agents/accessibility-verifier/agent.md) | Verification Engineer — `review-accessibility`, `ui-design` | `execute_and_test` → Builder (`execute-plan`, `review-accessibility`, `ui-design`) |
| [agents/architect/agent.md](../agents/architect/agent.md) | Architect and Planner — `design-architecture` | `consult` → Architect and Planner (`design-architecture`) |
| [agents/code-goal-planner/agent.md](../agents/code-goal-planner/agent.md) | Architect and Planner — `plan-code` | `consult` → Architect and Planner (`plan-code`) |
| [agents/code-reviewer/agent.md](../agents/code-reviewer/agent.md) | Reviewer — `review-code` | `review` → Reviewer (`review-code`); `execute_and_test` → Builder (`execute-plan`, `review-code`) |
| [agents/codebase-assessor/agent.md](../agents/codebase-assessor/agent.md) | Investigator — `assess-codebase` | — |
| [agents/contribution-scout/agent.md](../agents/contribution-scout/agent.md) | Investigator — `discover-contributions` | — |
| [agents/design-specialist/agent.md](../agents/design-specialist/agent.md) | UI Director — `audit-ui`, `design-ui`, `ui-design` | `audit_design` → UI Director (`audit-ui`, `ui-design`); `design_spec` → UI Director (`design-ui`, `ui-design`) |
| [agents/doc-updater/agent.md](../agents/doc-updater/agent.md) | Builder — `update-docs` | — |
| [agents/e2e-runner/agent.md](../agents/e2e-runner/agent.md) | Verification Engineer — `run-e2e` | `test` → Verification Engineer (`run-e2e`); `execute_and_test` → Builder (`execute-plan`, `run-e2e`) |
| [agents/fast-engineer/agent.md](../agents/fast-engineer/agent.md) | Builder — `execute-plan`, `fast-build` | — |
| [agents/feature-finaliser/agent.md](../agents/feature-finaliser/agent.md) | Builder — `execute-plan`, `delivery` | — |
| [agents/goal-planner/agent.md](../agents/goal-planner/agent.md) | Architect and Planner — `plan-goals` | `consult` → Architect and Planner (`plan-goals`) |
| [agents/implementation-executor/agent.md](../agents/implementation-executor/agent.md) | Builder — `execute-plan` | — |
| [agents/loop-executor/agent.md](../agents/loop-executor/agent.md) | Builder — `execute-plan`, `loop-execution` | `execute_checklist` → Builder (`execute-plan`, `loop-execution`) |
| [agents/loop-reviewer/agent.md](../agents/loop-reviewer/agent.md) | Reviewer — `review-code`, `loop-review` | `inspect_original_and_result` → Reviewer (`review-code`, `loop-review`); `review_current_result` → Reviewer (`review-code`, `loop-review`); `confirm_exact_repair_plan` → Reviewer (`review-plan`, `loop-review`) |
| [agents/performance-verifier/agent.md](../agents/performance-verifier/agent.md) | Verification Engineer — `verify-performance` | `execute_and_test` → Builder (`execute-plan`, `verify-performance`) |
| [agents/plan-reviewer/agent.md](../agents/plan-reviewer/agent.md) | Reviewer — `review-plan` | — |
| [agents/red-test-author/agent.md](../agents/red-test-author/agent.md) | Builder — `write-red-tests` | — |
| [agents/refactor-cleaner/agent.md](../agents/refactor-cleaner/agent.md) | Builder — `execute-plan`, `cleanup` | `cleanup` → Builder (`execute-plan`, `cleanup`); `clean_and_test` → Builder (`execute-plan`, `cleanup`) |
| [agents/researcher/agent.md](../agents/researcher/agent.md) | Investigator — `research-technical` | — |
| [agents/security-verifier/agent.md](../agents/security-verifier/agent.md) | Verification Engineer — `review-security` | `execute_and_test` → Builder (`execute-plan`, `review-security`) |
| [agents/tdd-guide/agent.md](../agents/tdd-guide/agent.md) | Builder — `execute-plan`, `tdd` | `write-red-tests` → Builder (`write-red-tests`, `tdd`); `write_red_tests` → Builder (`write-red-tests`, `tdd`) |
| [agents/tdd-implementer/agent.md](../agents/tdd-implementer/agent.md) | Builder — `execute-plan`, `green-refactor` | — |
| [agents/ui-design-director/agent.md](../agents/ui-design-director/agent.md) | UI Director — `ui-design` | `audit_design` → UI Director (`audit-ui`, `ui-design`); `design_spec` → UI Director (`design-ui`, `ui-design`); `inspect_reference` → UI Director (`visual-fidelity`, `ui-design`) |
| [agents/unit-verifier/agent.md](../agents/unit-verifier/agent.md) | Verification Engineer — `run-tests` | — |
| [agents/visual-fidelity/agent.md](../agents/visual-fidelity/agent.md) | UI Director — `visual-fidelity`, `ui-design` | `inspect_reference` → UI Director (`visual-fidelity`, `ui-design`); `execute_and_test` → Builder (`execute-plan`, `visual-fidelity`, `ui-design`); `review-ui` → Verification Engineer (`review-ui`, `visual-fidelity`, `ui-design`) |
| [workflows/agents/behaviour-spec-miner/agent.md](../workflows/agents/behaviour-spec-miner/agent.md) | Investigator — `extract-behaviour-spec` | — |
| [workflows/agents/dependency-risk-reviewer/agent.md](../workflows/agents/dependency-risk-reviewer/agent.md) | Reviewer — `review-dependencies` | — |
| [workflows/agents/doc-verifier/agent.md](../workflows/agents/doc-verifier/agent.md) | Reviewer — `verify-docs` | — |
| [workflows/agents/goal-verifier/agent.md](../workflows/agents/goal-verifier/agent.md) | Reviewer — `verify-goal` | — |
| [workflows/agents/plan-executor/agent.md](../workflows/agents/plan-executor/agent.md) | Builder — `execute-plan` | `fix-reviewed-defects` → Builder (`fix-reviewed-defects`) |
| [workflows/agents/plan-reviewer/agent.md](../workflows/agents/plan-reviewer/agent.md) | Reviewer — `review-plan` | — |
| [workflows/agents/researcher/agent.md](../workflows/agents/researcher/agent.md) | Investigator — `research-technical` | — |
| [workflows/agents/root-cause-analyst/agent.md](../workflows/agents/root-cause-analyst/agent.md) | Investigator — `diagnose-failure` | — |
| [workflows/agents/test-runner/agent.md](../workflows/agents/test-runner/agent.md) | Verification Engineer — `run-tests` | — |
| [workflows/agents/test-strategist/agent.md](../workflows/agents/test-strategist/agent.md) | Architect and Planner — `plan-tests` | — |
| [workflows/agents/ui-design-architect/agent.md](../workflows/agents/ui-design-architect/agent.md) | UI Director — `design-ui`, `ui-design` | — |
| [workflows/agents/ui-spec-reviewer/agent.md](../workflows/agents/ui-spec-reviewer/agent.md) | Reviewer — `review-ui-spec`, `ui-design` | — |

For example, the old code-reviewer execution assignment in GCA resolves to Builder, while
GVR resolves to Reviewer. The E2E execution/test-authoring commands retain their Builder
scope; verification-only GVE remains Verification Engineer. Fast, TDD, RED-only, GREEN,
visual-fidelity and Loop duties remain distinguishable. A registry lookup does not launch
workers, authenticate identities, inspect evidence or approve an action.

## Combine capabilities without duplicate work

Describe the complete outcome through Auto when possible. Composition selects useful bounded
operations, merges repeated discovery/planning/checks, applies relevant lenses and retains one
source owner for overlapping edits. Read-only reviews may run in parallel where supported;
dependent execution waits for actual review results. Two full build workflows are not a chain.

Typing `GAS GPP GPR GEX` in one command does **not** parse four stages: GAS is the control and
the remainder is its task text. Either ask Auto for the sequence or issue separate explicit
invocations against the same selected record after each dependency actually completes:

```text
@ai-development-workflow GAS Assess the existing save flow and its owners.
@ai-development-workflow GPP Plan the adopted correction from that assessment.
@ai-development-workflow GPR Independently criticize and revise that exact plan.
@ai-development-workflow GEX Implement and verify the reviewed plan.
```

Those lines are separate invocations, not one multi-command string. The original task's
authorization still governs whether a later executor may run. For test-first composition,
insert GTF after GPR and use GTE after genuine RED evidence. Add only the relevant verification
commands before closure. Do not use a full GS/GA/G1 workflow as an atomic operation.

### Focused selection evidence

A focused selection preserves the actual current catalogue fingerprint, literal request,
intent, reason, ordered chain and selected specialist IDs. It also carries the complete
[contract-v2 selection](workflow-contract-records.md): concrete `mode`, `originMode`,
impact `routing`, `uiContext` (including `kind`), `verificationContext`, ordered phases,
question-bearing capability assignments, independent review policy and two-contributor rule.
A short chain is not an exemption from staffing or phase disclosure.

`intent` accepts `implement`, `assess`, `plan`, `review`, `research` or `docs`. A public mode
is the sole chain entry; use internal operation IDs for an explicit composed chain. Optional
`existingEvidence` entries contain exactly `artifact` and `record` references to real prior
evidence that must be inspected. An optional `evaluated` array records selected/covered/
not-applicable decisions; there is no requirement to enumerate every catalogue entry.
Borrowed recipe `coveredBy` operations must follow recipe and chain order.

```bash
python3 scripts/workflow_catalog.py --format json
python3 scripts/workflow_contract.py template --record /absolute/task/record
python3 scripts/workflow_catalog.py --validate-selection /absolute/selection.json
```

The template prints pending declarations; fill them from the actual task and host results.
Validation checks IDs, dependencies, scopes, roles and selected-chain consistency. It does
not inspect evidence references, certify reasoning, launch workers or approve implementation.
The separate reviewed-record admission helper remains necessary before writes. Archived v1
records remain historical; active records require explicit reconciliation and fresh review.

## Records, evidence and helpers

Substantial work uses one `documents/tasks/development/<record>/` directory containing
`record.json`, `checklist.md`, `fix-plan.md`, `test-plan.md`, `critique.md` and `results.md`.
Relevant source captures and actual operation artifacts remain with that task. G0 uses the
compact checklist record. Follow-ups amend the selected record, preserve IDs/history and
reopen affected outcomes instead of copying a fresh plan for every correction.

The detailed [record contract](record-contract.md), [admission declarations](workflow-contract-records.md)
and [stage artifact contract](stage-artifacts.md) define sources, review bindings and completion.
The helper interfaces below are local utilities, not new chat modes or background services.

| Helper | Purpose / limit |
| --- | --- |
| [scripts/route_workflow.py](../scripts/route_workflow.py) | Parse explicit controls or preserve literal task prose; output route/schedule descriptions only. |
| [scripts/workflow_catalog.py](../scripts/workflow_catalog.py) | Read authoritative catalogue sources and validate focused selection declarations. |
| [scripts/create_plan_record.py](../scripts/create_plan_record.py) | Allocate a development record when the selected mode permits capture. |
| [scripts/finalize_plan_record.py](../scripts/finalize_plan_record.py) | Bind the declared plan/review stage to current record contents. |
| [scripts/resolve_plan_record.py](../scripts/resolve_plan_record.py) | Resolve the exact record and enforce current execution/resume admission declarations. |
| [scripts/workflow_contract.py](../scripts/workflow_contract.py) | Validate and record scope/phase/agent/criticism/public-briefing declarations. |
| [scripts/capture_conversation.py](../scripts/capture_conversation.py) | Capture/verify selected messages from supplied transcript files; does not fetch hidden chats. |
| [scripts/chatgpt_bridge.py](../scripts/chatgpt_bridge.py) | Capture/export visible message data supplied to it; cannot recover unavailable history. |
| [scripts/checklist_payload.py](../scripts/checklist_payload.py) | Convert a record/checklist to generic JSON; does not publish a host surface. |
| [scripts/acceptance_matrix.py](../scripts/acceptance_matrix.py) | Check declared target/expectation coverage and file bindings; cannot judge pixels or authenticate remote delivery. |
| [scripts/loop_checklist.py](../scripts/loop_checklist.py) | Reconcile review/checklist/execution/acceptance and monitor checkpoints; performs no scheduling or worker actions. |
| [scripts/contribution_scout.py](../scripts/contribution_scout.py) | Validate source-grounded contribution portfolio structure and bindings. |
| [scripts/workflow_log.py](../scripts/workflow_log.py) | Optional local diagnostic log, disabled by default; records only actual supplied/wrapped events. |
| [commands/quick-task/scripts/audit_task_record.py](../commands/quick-task/scripts/audit_task_record.py) | Audit the compact G0 record, including its own execution gate. |

Run a helper's `--help` for its exact current options. Python 3.10+ and the standard library
are required. Shell/application/browser access comes from the actual host and task. Missing
mandatory execution-helper capability remains a blocker; a chat note cannot claim a helper pass.

See [Loop artifacts](loop-artifacts.md) for the exact `check`, `monitor` and `timer` interfaces.
Loop checks the current worker every 300 seconds using a suitable wait first, a real timer
second and explicitly limited active-session monitoring otherwise. Old `xr-*` schemas,
`artifacts/xr/` evidence and historical 600-second checkpoint history remain intact; reconcile
the monitor to 300 seconds without rewriting earlier receipts. The helper is bookkeeping only.

Optional diagnostics are described in [debug logging](debug-logging.md). Keep logs, raw chat
exports, account identifiers and generated task records outside the reusable distribution.
Redaction is not a guarantee that arbitrary inputs contain no secrets. Sharing a report still
requires examining its actual contents and respecting the requested destination.

## Compatibility and retired interfaces

The main public surface is one skill with Auto, Plan, Build, Review and Loop. Advanced G and
numeric controls remain routed. Historical launcher aliases are parsing compatibility, not
42 separate registered skills. The generated plugin contains one canonical skill directory
with all real instruction bodies and runtime dependencies.

The editor picker, native selector/queue implementation, its manifests and public native
`stage`/`pipeline` runtime were removed from this edition. Their five former preset IDs—
`quick-safe-change`, `standard-verified-build`, `test-first-feature`, `ui-design-fidelity` and
`high-assurance-delivery`—are not accepted pipeline selectors. Their useful operation expertise
remains available through Auto and the retained neutral catalogue. Unsupported selectors must
return an explicit limitation rather than silently selecting a writing workflow.

Loop replaces XR as the primary name; XR invocation aliases and serialized evidence remain
compatible. Old records still require actual current source/review/worker reconciliation.
No profile, package, mode or validator guarantees that arbitrary host tools are unbypassable.
The supported admission paths fail closed, while actual permissions and tool execution remain
the responsibility of the host and agent following the contract.
