# Complete AI Development Workflow catalogue

Catalogue fingerprint: `a8d9edaf6c1359af93f15a718ee12522c38f01a3f489d204081283ffebf31376`

Reference material for selected work. Load relevant handlers and their prerequisites; specialist lenses inherit the chosen operation's scope.

## Public controls

| Mode | Purpose | Scope |
| --- | --- | --- |
| auto | Resolve a concrete mode and source-grounded Fast/Architect routing, then assign actual workers. | task-defined |
| plan | Delegate planning, criticize the plan and stop before product changes. | record-only |
| build | Use a specialist executor and independent plan/result review for the authorized change. | repo-write-scoped |
| review | Delegate meaningful inspection and report findings without implementing repairs. | record-only |
| loop | Repeat independent review, checklist execution and fresh review until acceptance or a genuine blocker. | repo-write-scoped |

## Six canonical worker families

The coordinator is additional. Every new task needs at least two useful actual worker contributions; profiles and capabilities are not running agents.

| Family | Instruction owner |
| --- | --- |
| Investigator | [investigator](../agents/investigator/agent.md) |
| Architect and Planner | [architect](../agents/architect/agent.md) |
| Builder | [builder](../agents/builder/agent.md) |
| UI Director | [ui-design-director](../agents/ui-design-director/agent.md) |
| Reviewer | [reviewer](../agents/reviewer/agent.md) |
| Verification Engineer | [verification-engineer](../agents/verification-engineer/agent.md) |

## All commands, including hidden compatibility commands

| ID | Option | Scope | Summary |
| --- | --- | --- | --- |
| command:G0 | [Quick Task (hidden compatibility command)](../commands/quick-task/ai-dev-quick-task.md) | repo-write-scoped | Quick change with a source log, checklist and scoped verification |
| command:GS | [Assess, plan, review and build](../agents/codebase-assessor/commands/ai-dev-codebase-assessment.md) | repo-write-scoped | Assess existing code conventions before planning and implementation |
| command:GPL | [Goal Planner — plan only](../agents/goal-planner/commands/ai-dev-goal-plan.md) | record-only | Plan goals, preconditions, dependencies and the most efficient credible sequence |
| command:GCP | [Code Goal Planner — plan only](../agents/code-goal-planner/commands/ai-dev-code-plan.md) | record-only | Plan code changes against existing owners and testable milestones |
| command:GA | [Architecture, plan and build](../agents/architect/commands/ai-dev-architecture.md) | repo-write-scoped | Consult architecture while planning, then build and test |
| command:G1 | [Standard plan and build](../commands/ai-dev-build.md) | repo-write-scoped | Plan, criticise, implement and test a normal task |
| command:GB | [Fast full build](../agents/fast-engineer/commands/ai-dev-fast-build.md) | repo-write-scoped | Complete the full scope with reuse, dependency batching and consolidated acceptance |
| command:GT | [Full test-first build](../agents/tdd-guide/commands/ai-dev-test-first.md) | repo-write-scoped | Plan and critique, then delegate test-first implementation |
| command:G7 | [Visual Fidelity (hidden compatibility command)](../agents/visual-fidelity/commands/ai-dev-visual-fidelity.md) | repo-write-scoped | Inspect existing UI, compare the target, implement and verify |
| command:GEA | [Delegate to E2E Agent (hidden compatibility command)](../agents/e2e-runner/commands/ai-dev-e2e-execute.md) | repo-write-scoped | Plan and critique, then let the E2E agent implement and test |
| command:GCA | [Delegate to Code Reviewer (hidden compatibility command)](../agents/code-reviewer/commands/ai-dev-review-execute.md) | repo-write-scoped | Use an existing plan; the code reviewer implements and tests |
| command:GR | [Build and Cleanup (hidden compatibility command)](../agents/refactor-cleaner/commands/ai-dev-cleanup.md) | repo-write-scoped | Build the requested change, then clean its affected code |
| command:GH | [AI Repository Hygiene (hidden compatibility command)](../agents/refactor-cleaner/commands/ai-dev-repo-hygiene.md) | repo-write-scoped | Organise repository files safely and repair their references |
| command:GF | [AI Feature Finalisation (hidden compatibility command)](../agents/feature-finaliser/commands/ai-dev-feature-finalise.md) | repo-write-scoped | Finalise one feature and test its exact delivery package |
| command:GC | [Build and Code Review (hidden compatibility command)](../agents/code-reviewer/commands/ai-dev-code-review.md) | repo-write-scoped | Build and test, then obtain a separate code review |
| command:GX | [AI Security Verification (hidden compatibility command)](../agents/security-verifier/commands/ai-dev-security.md) | repo-write-scoped | Test access boundaries and fix scoped security defects |
| command:GU | [AI Accessibility and Interaction QA (hidden compatibility command)](../agents/accessibility-verifier/commands/ai-dev-accessibility.md) | repo-write-scoped | Verify keyboard, focus, forms and responsive interactions |
| command:GE | [Build and E2E Tests (hidden compatibility command)](../agents/e2e-runner/commands/ai-dev-e2e-tests.md) | repo-write-scoped | Build and test, then run end-to-end verification |
| command:GJ | [AI Journey Test Automation (hidden compatibility command)](../agents/e2e-runner/commands/ai-dev-journey-tests.md) | repo-write-scoped | Build rerunnable customer and admin browser test suites |
| command:GP | [AI Performance and Resilience (hidden compatibility command)](../agents/performance-verifier/commands/ai-dev-performance.md) | repo-write-scoped | Measure performance budgets and verify failure recovery |
| command:GD | [Build and Documentation (hidden compatibility command)](../agents/doc-updater/commands/ai-dev-documentation.md) | repo-write-scoped | Build and test, then update affected documentation |
| command:G6 | [Build, Docs, E2E and Review (hidden compatibility command)](../commands/ai-dev-full-checks.md) | repo-write-scoped | Build, then update documentation, run E2E tests and review |
| command:GAS | [Codebase assessment only](../commands/stages/ai-dev-assess-only.md) | record-only | Inspect relevant code and document proven owners and conventions, without planning or implementing |
| command:GRS | [Research only](../commands/stages/ai-dev-research-only.md) | record-only | Research a technical question with source evidence and a decision-ready summary, without coding |
| command:GDA | [Design audit only](../commands/stages/ai-dev-design-audit.md) | record-only | Inspect existing UI and design tokens and document measurable gaps before proposing changes |
| command:GAA | [Architecture assessment only](../commands/stages/ai-dev-architecture-advice.md) | record-only | Review integration boundaries and architectural trade-offs without building |
| command:GDS | [Design specification only](../commands/stages/ai-dev-design-spec.md) | record-only | Write a reusable design specification from a verified UI audit without implementing it |
| command:GPP | [Plan from assessment](../commands/stages/ai-dev-plan-from-evidence.md) | record-only | Plan code changes from a verified assessment or design specification; do not review or build |
| command:GPR | [Review and refine plan](../commands/stages/ai-dev-review-plan-only.md) | record-only | Independently critique the existing plan, correct it and record execution readiness; no coding |
| command:GTF | [Write failing tests (TDD red)](../commands/stages/ai-dev-write-red-tests.md) | tests-only | Implement test cases only, show correct red failures and hand them to the TDD executor |
| command:GEX | [Execute reviewed plan](../commands/stages/ai-dev-execute-plan.md) | repo-write-scoped | Implement and test the accepted existing plan without re-planning or allocating a record |
| command:GTE | [Execute TDD plan (green)](../commands/stages/ai-dev-execute-tdd.md) | repo-write-scoped | Consume reviewed plan and demonstrated red tests; implement green/refactor and verify |
| command:GUT | [Unit and integration verification](../commands/stages/ai-dev-unit-verify-only.md) | test-output-only | Run existing unit/integration checks against delivered code without building |
| command:GVE | [End-to-end verification only](../commands/stages/ai-dev-e2e-verify-only.md) | test-output-only | Validate real customer journeys from delivered code, without repeating the build |
| command:GVR | [Independent code review only](../commands/stages/ai-dev-review-code-only.md) | record-only | Review the final implementation and test evidence without repeating its implementation |
| command:GVS | [Security verification only](../commands/stages/ai-dev-security-verify-only.md) | record-only | Check delivered changes for security defects; report findings without rebuilding |
| command:GVA | [Accessibility verification only](../commands/stages/ai-dev-a11y-verify-only.md) | record-only | Verify keyboard, focus, interaction and responsive accessibility without rewriting the UI |
| command:GVP | [Performance verification only](../commands/stages/ai-dev-performance-verify-only.md) | test-output-only | Measure performance and resilience on bounded workloads with no automatic optimisations |
| command:GVD | [Update documentation only](../commands/stages/ai-dev-update-docs-only.md) | docs-only | Update documentation from tested code under current reviewed coverage; no product rebuild |
| command:GCL | [Cleanup existing implementation](../commands/stages/ai-dev-clean-only.md) | repo-write-scoped | Make scoped, behaviour-preserving cleanup after a delivered change, not another full build |
| command:GRC | [Repository Contribution Scout](../agents/contribution-scout/commands/ai-dev-contribution-discovery.md) | record-only | Inventory an entire repository and rank evidence-backed, PR-sized contribution proposals across engineering categories; plan-only |

## Public mode contracts

| ID | Option | Scope | Summary |
| --- | --- | --- | --- |
| mode:plan | [Plan](../references/public-modes.md) | record-only | Delegate planning, criticize the plan and stop before product changes. |
| mode:build | [Build](../references/public-modes.md) | repo-write-scoped | Use a specialist executor and independent plan/result review for the authorized change. |
| mode:review | [Review](../references/public-modes.md) | record-only | Delegate meaningful inspection and report findings without implementing repairs. |
| mode:loop | [Loop — Execute and Review](../references/loop-mode.md) | repo-write-scoped | Review original and delivered work, execute the reconciled checklist, and repeat fresh independent review until accepted. |

## Internal workflow operations

| ID | Option | Scope | Summary |
| --- | --- | --- | --- |
| stage:research-technical | [Research Technical Options](../workflows/stages/research-technical.md) | record-only | Compare libraries or technical approaches with verified sources; never implement. |
| stage:discover-contributions | [Repository Contribution Scout](../workflows/stages/discover-contributions.md) | record-only | Repository-wide contribution discovery, source-grounded roadmap and PR plans (read-only). |
| stage:assess-codebase | [Assess Codebase](../workflows/stages/assess-codebase.md) | record-only | Trace relevant entry points, ownership, conventions and tests; record sources and unknowns. No application edits. |
| stage:diagnose-failure | [Diagnose Root Cause](../workflows/stages/diagnose-failure.md) | record-only | Reproduce and trace a bug or failure before any fix. Writes hypotheses, evidence, and confirmed cause. |
| stage:extract-behaviour-spec | [Extract Existing Behaviour](../workflows/stages/extract-behaviour-spec.md) | record-only | Extract observed behaviour and invariants from code, without guessing or changing application source. |
| stage:plan-goals | [Plan Goals](../workflows/stages/plan-goals.md) | record-only | Decompose authorised outcomes into dependencies, constraints and acceptance criteria; no implementation. |
| stage:design-architecture | [Consult Architecture](../workflows/stages/design-architecture.md) | record-only | Write an ADR and implementation boundaries; no source edits. |
| stage:design-ui | [Design UI](../workflows/stages/design-ui.md) | record-only | Read real design tokens and components; produce a UI specification and interaction states only. |
| stage:review-ui-spec | [Review UI Specification](../workflows/stages/review-ui-spec.md) | record-only | Check design contract for implementability, consistency, responsive behaviour and ownership; independent review. |
| stage:plan-code | [Plan Code Changes](../workflows/stages/plan-code.md) | record-only | Create file- and test-specific implementation steps, in the same record; does not execute. |
| stage:plan-tests | [Plan Tests Only](../workflows/stages/plan-tests.md) | record-only | Define assertions, fixtures and required RED/GREEN checks without writing or running tests. |
| stage:review-plan | [Review Plan](../workflows/stages/review-plan.md) | record-only | Review requirement coverage, execution feasibility and plan revision. Does not implement. |
| stage:write-red-tests | [Write Failing Tests](../workflows/stages/write-red-tests.md) | tests-only | Write tests, capture expected RED assertion, and refuse to treat infrastructure errors as RED. |
| stage:execute-plan | [Execute Approved Plan](../workflows/stages/execute-plan.md) | repo-write-scoped | Apply approved plan against current reviewed revision. Preserve scope, checkpoints and evidence. |
| stage:fix-reviewed-defects | [Fix Reviewed Defects](../workflows/stages/fix-reviewed-defects.md) | repo-write-scoped | Apply only separately authorised actionable findings; do not self-authorise scope changes. |
| stage:run-tests | [Run Tests & Validation](../workflows/stages/run-tests.md) | test-output-only | Run existing build/lint/typecheck/unit/integration commands; capture exits and logs without feature implementation. |
| stage:run-e2e | [Run End-to-End Tests](../workflows/stages/run-e2e.md) | test-output-only | Run current browser journeys and capture screenshots/traces; never run build first. |
| stage:review-code | [Review Code](../workflows/stages/review-code.md) | record-only | Review diff with evidence; reviewer cannot implement its own suggested changes. |
| stage:review-ui | [Review Visual Fidelity](../workflows/stages/review-ui.md) | record-only | Compare rendered UI to existing design or approved UI spec, with screenshot evidence. |
| stage:review-accessibility | [Review Accessibility](../workflows/stages/review-accessibility.md) | record-only | Assess keyboard, focus, semantics and responsive interaction with reproducible evidence; no automatic UI changes. |
| stage:review-security | [Review Security](../workflows/stages/review-security.md) | record-only | Bounded independent static/runtime security verification; report defects without expanding privileges. |
| stage:review-dependencies | [Review Dependency Risk](../workflows/stages/review-dependencies.md) | record-only | Review new package choices, provenance, licenses and supply-chain exposure. Does not install dependencies. |
| stage:verify-goal | [Verify Delivered Goals](../workflows/stages/verify-goal.md) | record-only | Confirm observable outcomes and requirements, rather than only counting tasks. |
| stage:update-docs | [Update Documentation](../workflows/stages/update-docs.md) | docs-only | Update affected docs from real code diff; do not rebuild source code. |
| stage:verify-docs | [Verify Documentation](../workflows/stages/verify-docs.md) | record-only | Check each documentation claim and command against actual code. |
| stage:verify-performance | [Verify Performance](../workflows/stages/verify-performance.md) | test-output-only | Verified performance evidence only. |

## Portable task recipes — adapt to current scope

| ID | Option | Scope | Summary |
| --- | --- | --- | --- |
| recipe:reference-rebuild | [Rebuild from a supplied reference](../task-recipes/reference-rebuild.md) | repo-write-scoped | Reconstruct supplied HTML, screenshots or extracted pages while preserving declared source details and validating the rendered result. |
| recipe:visual-correction | [Repair precise visual feedback](../task-recipes/visual-correction.md) | repo-write-scoped | Apply itemized corrections to the current approved artifact and verify the requested delta together with protected properties. |
| recipe:design-system-rollout | [Roll out shared design changes](../task-recipes/design-system-rollout.md) | repo-write-scoped | Update canonical components, typography and theme presets across a declared target set, checking affected states and exported outputs. |
| recipe:native-yaml-conversion | [Convert to native editable YAML](../task-recipes/native-yaml-conversion.md) | repo-write-scoped | Map supplied sources to the receiving kit and real widget capabilities, then validate editable structure, assets and import/render parity. |
| recipe:asset-production | [Produce or edit a visual asset set](../task-recipes/asset-production.md) | repo-write-scoped | Create source-aware images, SVGs or banner variants with explicit composition constraints, distinct concepts where requested and complete output reconciliation. |
| recipe:motion-reconstruction | [Reconstruct and verify motion](../task-recipes/motion-reconstruction.md) | repo-write-scoped | Preserve or repair supplied animation and interactive behavior using an explicit sequence and observed full-cycle verification. |
| recipe:media-library-extension | [Extend an existing media workspace](../task-recipes/media-library-extension.md) | repo-write-scoped | Integrate media conversion or navigation into the current library, reusing folder identity, tree controls, drop behavior and persisted state. |
| recipe:content-site-delivery | [Deliver a source-grounded content site](../task-recipes/content-site-delivery.md) | repo-write-scoped | Reconcile requested pages and source content, reuse the approved presentation and verify routes, metadata, links and delivered artifacts. |
| recipe:artifact-handoff | [Verify and deliver an artifact](../task-recipes/artifact-handoff.md) | repo-write-scoped | Reconcile final source and package identity, repair in-scope delivery defects and verify the authorized destination with readback. |
| recipe:plugin-evolution | [Improve a plugin from actual usage](../task-recipes/plugin-evolution.md) | repo-write-scoped | Analyze available usage evidence, map current coverage, implement justified instruction or routing changes and verify the same plugin release. |

## Specialist instruction profiles

| ID | Option | Scope | Summary |
| --- | --- | --- | --- |
| specialist:react-frontend | [React and frontend systems](../specialists/react-frontend.md) | inherit-stage | Apply the existing workflow to React interfaces, reusable components, responsive behaviour and frontend performance. |
| specialist:editor-schema | [Editors, registries and persistent schemas](../specialists/editor-schema.md) | inherit-stage | Preserve native widget models, nested editability, preset inheritance and persistent tree/configuration semantics across every editor surface. |
| specialist:wordpress-woocommerce | [WordPress and WooCommerce](../specialists/wordpress-woocommerce.md) | inherit-stage | Use WordPress and commerce-specific lifecycle, data, permissions and compatibility checks. |
| specialist:whmcs | [WHMCS modules and client-area systems](../specialists/whmcs.md) | inherit-stage | Assess and implement WHMCS extensions with verified hook contracts, lifecycle and account boundaries. |
| specialist:plugins-mcp | [Plugins, skills and MCP applications](../specialists/plugins-mcp.md) | inherit-stage | Evolve plugin instructions, routers and tool/host contracts from evidence while preserving identity, explicit scope, compatibility and release provenance. |
| specialist:browser-extraction | [Browser evidence and website extraction](../specialists/browser-extraction.md) | inherit-stage | Ground reconstruction and UI repair in identified source versions, asset dependencies and comparable rendered/interactive states. |
| specialist:native-yaml-archives | [Native YAML and archive conversion](../specialists/native-yaml-archives.md) | inherit-stage | Map supplied HTML and the current kit to genuinely editable native widgets, presets and complete import packages with explicit custom-code exceptions. |
| specialist:content-seo | [Structured content and technical SEO](../specialists/content-seo.md) | inherit-stage | Build and migrate source-grounded content collections with real destinations, preserved approved copy, coherent presentation and validated metadata/schema. |
| specialist:python-data | [Python automation and data pipelines](../specialists/python-data.md) | inherit-stage | Build resumable data processing with validated inputs, explicit failures and reconciled outputs. |
| specialist:database | [Database schemas and data integrity](../specialists/database.md) | inherit-stage | Apply engine-specific checks to migrations, queries, tenant access, locks and data compatibility. |
| specialist:infrastructure | [Infrastructure and deployment configuration](../specialists/infrastructure.md) | inherit-stage | Ground infrastructure changes in provider versions, actual state, execution mode and recovery evidence. |
| specialist:migration-release | [Migration, recovery and release completion](../specialists/migration-release.md) | inherit-stage | Resume interrupted work from real source and task evidence, preserve milestones and reconcile the requested repository/package/release outcome. |
| specialist:realtime-native | [Realtime media and native application lifecycles](../specialists/realtime-native.md) | inherit-stage | Trace message identity, delivery/history, hidden/popout views and shared media ownership through the actual realtime or native runtime. |
| specialist:reference-fidelity | [Reference fidelity and precise corrections](../specialists/reference-fidelity.md) | inherit-stage | Preserve approved source identity, constrain changes to requested deltas and verify observable results without collateral redesign. |
| specialist:design-system | [Shared design systems, typography and presets](../specialists/design-system.md) | inherit-stage | Maintain canonical components, tokens, fonts, icons and saved visual presets consistently across consumers and interaction states. |
| specialist:image-art-direction | [Image art direction and consistent asset production](../specialists/image-art-direction.md) | inherit-stage | Direct authorized image generation/editing with source-locked composition, consistent geometry and semantically distinct product concepts. |
| specialist:motion-interaction | [Motion, interactive widgets and temporal verification](../specialists/motion-interaction.md) | inherit-stage | Model and verify meaningful animation sequences, transitions, controls and theme-dependent states over a complete relevant cycle. |
| specialist:media-library | [Media libraries, archive ingestion and local conversion](../specialists/media-library.md) | inherit-stage | Extend existing media-workspace navigation, imports, storage and conversion while preserving identity, privacy and measurable fidelity. |
| specialist:artifact-delivery | [Artifact completeness and verified delivery](../specialists/artifact-delivery.md) | inherit-stage | Reconcile complete deliverables, dependency closure, actual output revisions and authorized destination readback before claiming handoff. |
| specialist:usage-learning | [Usage evidence and workflow improvement](../specialists/usage-learning.md) | inherit-stage | Analyze complete task evidence with deduplication and outcome limits, map demand to current capabilities and evaluate bounded plugin improvements. |
| specialist:ui-design | [UI Design Director](../specialists/ui-design.md) | inherit-stage | Apply scoped visual corrections and a coherent design direction to every relevant UI task, with complete target review and evidence of visible quality. |

## Dependencies and recipe expansions

- **command:GPL** — produces: code.plan
- **command:GCP** — produces: code.plan
- **command:GAS** — produces: assessment.report
- **command:GRS** — produces: research.report
- **command:GDA** — produces: design.audit
- **command:GAA** — needs one: assessment.report, code.plan; produces: architecture.advice
- **command:GDS** — needs all: design.audit; produces: ui.spec
- **command:GPP** — needs one: assessment.report, ui.spec; produces: code.plan
- **command:GPR** — needs all: code.plan; produces: plan.review
- **command:GTF** — needs all: plan.review; produces: tdd.red.evidence
- **command:GEX** — needs all: plan.review; ordinary-agent additional inputs: code.plan; produces: execution.result
- **command:GTE** — needs all: plan.review, tdd.red.evidence; ordinary-agent additional inputs: code.plan; produces: execution.result
- **command:GUT** — needs all: execution.result; produces: test.results
- **command:GVE** — needs all: execution.result; produces: e2e.results
- **command:GVR** — needs all: execution.result; produces: review.findings
- **command:GVS** — needs all: execution.result; produces: security.review
- **command:GVA** — needs all: execution.result; produces: accessibility.review
- **command:GVP** — needs all: execution.result; produces: performance.results
- **command:GVD** — needs all: execution.result, plan.review; produces: docs.change
- **command:GCL** — needs all: execution.result, plan.review; produces: cleanup
- **command:GRC** — produces: contribution.portfolio
- **mode:plan** — needs all: request, repo.snapshot; produces: code.plan, plan.review
- **mode:build** — needs all: request, repo.snapshot; produces: code.plan, plan.review, execution.result, test.results
- **mode:review** — needs all: request, repo.snapshot; produces: review.findings
- **stage:research-technical** — needs all: request; produces: research.report
- **stage:discover-contributions** — needs all: request, repo.snapshot; produces: contribution.portfolio
- **stage:assess-codebase** — needs all: request, repo.snapshot; produces: assessment.report
- **stage:diagnose-failure** — needs all: request, repo.snapshot; produces: diagnosis.report
- **stage:extract-behaviour-spec** — needs all: repo.snapshot; produces: behaviour.spec
- **stage:plan-goals** — needs all: request, repo.snapshot; produces: goal.plan
- **stage:design-architecture** — needs all: request, repo.snapshot; produces: architecture.advice
- **stage:design-ui** — needs all: request, repo.snapshot; produces: ui.spec
- **stage:review-ui-spec** — needs all: ui.spec, repo.snapshot; produces: ui.spec.review
- **stage:plan-code** — needs all: request, repo.snapshot; produces: code.plan
- **stage:plan-tests** — needs all: request, repo.snapshot; produces: test.strategy
- **stage:review-plan** — needs all: code.plan, request, repo.snapshot; produces: plan.review
- **stage:write-red-tests** — needs all: code.plan, plan.review, repo.snapshot; produces: tdd.red.evidence
- **stage:execute-plan** — needs all: code.plan, plan.review, repo.snapshot; produces: execution.result
- **stage:fix-reviewed-defects** — needs all: code.plan, plan.review, review.findings, repo.snapshot; produces: execution.result
- **stage:run-tests** — needs all: repo.snapshot; produces: test.results
- **stage:run-e2e** — needs all: repo.snapshot; produces: e2e.results
- **stage:review-code** — needs all: repo.snapshot; produces: review.findings
- **stage:review-ui** — needs all: repo.snapshot, ui.spec; produces: ui.visual.review
- **stage:review-accessibility** — needs all: repo.snapshot; produces: accessibility.review
- **stage:review-security** — needs all: repo.snapshot; produces: security.review
- **stage:review-dependencies** — needs all: repo.snapshot; produces: dependency.review
- **stage:verify-goal** — needs all: request, repo.snapshot; produces: goal.verification
- **stage:update-docs** — needs all: code.plan, plan.review, repo.snapshot; produces: docs.change
- **stage:verify-docs** — needs all: repo.snapshot, docs.change; produces: docs.verification
- **stage:verify-performance** — needs all: repo.snapshot; produces: performance.results
- **recipe:reference-rebuild** — stage:assess-codebase → stage:design-ui → stage:review-ui-spec → stage:plan-code → stage:review-plan → stage:execute-plan → stage:run-e2e → stage:review-ui → stage:review-accessibility → stage:verify-goal; additional recipe inputs: {"stage:plan-code": ["assessment.report", "ui.spec", "ui.spec.review"]}; recommended lenses: specialist:ui-design, specialist:reference-fidelity, specialist:browser-extraction, specialist:artifact-delivery
- **recipe:visual-correction** — stage:assess-codebase → stage:diagnose-failure → stage:design-ui → stage:plan-code → stage:review-plan → stage:execute-plan → stage:review-ui → stage:verify-goal; additional recipe inputs: {"stage:plan-code": ["assessment.report", "diagnosis.report", "ui.spec"]}; recommended lenses: specialist:ui-design, specialist:reference-fidelity, specialist:design-system
- **recipe:design-system-rollout** — stage:assess-codebase → stage:design-ui → stage:review-ui-spec → stage:plan-code → stage:review-plan → stage:execute-plan → stage:run-tests → stage:run-e2e → stage:review-ui → stage:review-accessibility → stage:verify-goal; additional recipe inputs: {"stage:plan-code": ["assessment.report", "ui.spec", "ui.spec.review"]}; recommended lenses: specialist:ui-design, specialist:design-system, specialist:reference-fidelity, specialist:artifact-delivery
- **recipe:native-yaml-conversion** — stage:assess-codebase → stage:design-ui → stage:plan-code → stage:review-plan → stage:execute-plan → stage:run-tests → stage:review-ui → stage:verify-goal; additional recipe inputs: {"stage:plan-code": ["assessment.report", "ui.spec"]}; recommended lenses: specialist:ui-design, specialist:native-yaml-archives, specialist:editor-schema, specialist:reference-fidelity, specialist:artifact-delivery
- **recipe:asset-production** — stage:assess-codebase → stage:design-ui → stage:plan-code → stage:review-plan → stage:execute-plan → stage:review-ui → stage:verify-goal; additional recipe inputs: {"stage:plan-code": ["assessment.report", "ui.spec"]}; recommended lenses: specialist:ui-design, specialist:image-art-direction, specialist:reference-fidelity, specialist:artifact-delivery
- **recipe:motion-reconstruction** — stage:assess-codebase → stage:extract-behaviour-spec → stage:design-ui → stage:plan-code → stage:review-plan → stage:execute-plan → stage:run-e2e → stage:review-ui → stage:review-accessibility → stage:verify-goal; additional recipe inputs: {"stage:plan-code": ["assessment.report", "behaviour.spec", "ui.spec"]}; recommended lenses: specialist:ui-design, specialist:motion-interaction, specialist:reference-fidelity, specialist:browser-extraction
- **recipe:media-library-extension** — stage:assess-codebase → stage:extract-behaviour-spec → stage:plan-code → stage:review-plan → stage:execute-plan → stage:run-tests → stage:run-e2e → stage:review-code → stage:verify-goal; additional recipe inputs: {"stage:plan-code": ["assessment.report", "behaviour.spec"]}; recommended lenses: specialist:media-library, specialist:editor-schema, specialist:migration-release
- **recipe:content-site-delivery** — stage:assess-codebase → stage:plan-code → stage:review-plan → stage:execute-plan → stage:run-tests → stage:run-e2e → stage:verify-goal; additional recipe inputs: {"stage:plan-code": ["assessment.report"]}; recommended lenses: specialist:content-seo, specialist:design-system, specialist:artifact-delivery
- **recipe:artifact-handoff** — stage:assess-codebase → stage:plan-code → stage:review-plan → stage:execute-plan → stage:run-tests → stage:verify-goal; additional recipe inputs: {"stage:plan-code": ["assessment.report"]}; recommended lenses: specialist:artifact-delivery, specialist:migration-release
- **recipe:plugin-evolution** — stage:research-technical → stage:assess-codebase → stage:extract-behaviour-spec → stage:plan-code → stage:review-plan → stage:execute-plan → stage:run-tests → stage:review-code → stage:update-docs → stage:verify-goal; additional recipe inputs: {"stage:plan-code": ["assessment.report", "research.report", "behaviour.spec"]}; recommended lenses: specialist:usage-learning, specialist:plugins-mcp, specialist:artifact-delivery

## Portable recipe selection

Adapt these starting patterns to actual scope and evidence. Expand selected operations in dependency order and preserve read-only and continuation boundaries. Recommended lenses do not assert running agents.

### recipe:reference-rebuild

Reconstruct supplied HTML, screenshots or extracted pages while preserving declared source details and validating the rendered result.

**Use when:**

- A supplied page, extraction or screenshot defines the requested visual and interaction target.

**Avoid when:**

- The user asks for open-ended concept exploration without an existing target.

### recipe:visual-correction

Apply itemized corrections to the current approved artifact and verify the requested delta together with protected properties.

**Use when:**

- The user identifies incorrect geometry, typography, content, component states or unintended changes to approved work.

**Avoid when:**

- There is no visual artifact or reference; use the actual domain diagnosis instead.

### recipe:design-system-rollout

Update canonical components, typography and theme presets across a declared target set, checking affected states and exported outputs.

**Use when:**

- Changes to shared components, fonts, modes, accents or presets must propagate across pages or an editor catalogue.

**Avoid when:**

- Only one self-contained image is being edited and no shared design system is involved.

### recipe:native-yaml-conversion

Map supplied sources to the receiving kit and real widget capabilities, then validate editable structure, assets and import/render parity.

**Use when:**

- The requested deliverable is a native editor YAML page, template or preset based on supplied content and a schema/kit.

**Avoid when:**

- The user wants an ordinary HTML page or screenshot without native editor compatibility.

### recipe:asset-production

Create source-aware images, SVGs or banner variants with explicit composition constraints, distinct concepts where requested and complete output reconciliation.

**Use when:**

- The task produces or edits images, product compositions, SVG conversions or a constrained set of banner concepts.

**Avoid when:**

- The actual problem is application lifecycle or UI state rather than the visual assets themselves.

### recipe:motion-reconstruction

Preserve or repair supplied animation and interactive behavior using an explicit sequence and observed full-cycle verification.

**Use when:**

- Animation, tabs, maps, terminals, timing, transitions or interactive controls are part of the requested target.

**Avoid when:**

- Only a static still image is requested and no motion behavior is involved.

### recipe:media-library-extension

Integrate media conversion or navigation into the current library, reusing folder identity, tree controls, drop behavior and persisted state.

**Use when:**

- An existing media, HTML or icon library gains import, conversion, sorting, favorites, canvas or folder functionality.

**Avoid when:**

- The task is a standalone image edit with no persistent application integration.

### recipe:content-site-delivery

Reconcile requested pages and source content, reuse the approved presentation and verify routes, metadata, links and delivered artifacts.

**Use when:**

- A help centre, product/page collection, Markdown site or content migration must preserve source facts and complete target coverage.

**Avoid when:**

- The request is strategy or information architecture advice only; retain the corresponding read-only scope.

### recipe:artifact-handoff

Reconcile final source and package identity, repair in-scope delivery defects and verify the authorized destination with readback.

**Use when:**

- A requested file, archive, export or release is missing, stale, incomplete, unstyled or not available at its authorized destination.

**Avoid when:**

- No artifact or delivery outcome is requested; do not invent publication or storage work.

### recipe:plugin-evolution

Analyze available usage evidence, map current coverage, implement justified instruction or routing changes and verify the same plugin release.

**Use when:**

- The user asks to improve a plugin, skill catalogue or agent workflow using usage histories, concrete failures or exported requests.

**Avoid when:**

- The user invokes an existing plugin to perform unrelated work, or asks only for a usage analysis without implementation.

## Specialist selection and acceptance

### specialist:react-frontend

Apply the existing workflow to React interfaces, reusable components, responsive behaviour and frontend performance.

**Use when:**

- React or Next.js components, application routes, state-driven UI or frontend regressions are in scope.
- Shared design tokens, component APIs or rendering performance affect the requested change.

**Avoid when:**

- The task is only static content conversion with no React runtime.

**Acceptance evidence:**

- Affected user journeys work at the required viewport and theme states.
- State and component ownership match the existing architecture.
- Relevant build, type and interaction evidence is recorded; visual review is separate.

Profile: `specialists/react-frontend.md`.

### specialist:editor-schema

Preserve native widget models, nested editability, preset inheritance and persistent tree/configuration semantics across every editor surface.

**Use when:**

- A visual editor, page builder, structured tree, widget registry or saved workspace is changing.
- Document schemas, settings persistence, selection, undo/redo or import/export contracts are involved.

**Avoid when:**

- The page is a static presentation with no editable document model.

**Acceptance evidence:**

- Registry, inspector, renderer and export agree on each supported field and default.
- Edit-save-reload-export-import preserves nested relationships, stable identity and intended preset overrides.
- Existing documents survive migration; unsupported fields and malformed input remain visible in diagnostics.

Profile: `specialists/editor-schema.md`.

### specialist:wordpress-woocommerce

Use WordPress and commerce-specific lifecycle, data, permissions and compatibility checks.

**Use when:**

- A WordPress theme, plugin, block, REST integration or WooCommerce extension is in scope.
- Content storage, custom checkout/order behaviour or PHP/JavaScript integration depends on WordPress.

**Avoid when:**

- Only WHMCS is affected; there is no WordPress/WooCommerce component or integration.
- The project has no WordPress runtime or compatibility requirement.

**Acceptance evidence:**

- The changed extension loads and behaves on the declared WordPress/PHP/WooCommerce versions.
- Relevant authorised and unauthorised requests behave correctly.
- Lifecycle and data changes preserve existing site/store behaviour and intended data.

Profile: `specialists/wordpress-woocommerce.md`.

### specialist:whmcs

Assess and implement WHMCS extensions with verified hook contracts, lifecycle and account boundaries.

**Use when:**

- The task changes a WHMCS addon, hook, client-area template, API integration or account workflow.
- Rate limits, billing/account behaviour or module lifecycle depends on WHMCS.

**Avoid when:**

- The task affects only WordPress/WooCommerce or generic PHP, with no WHMCS integration.
- Only marketing-page copy changes and no WHMCS integration is affected.

**Acceptance evidence:**

- The relevant hook/module executes on the declared host version.
- Account and admin boundaries are exercised with permitted and denied cases.
- Repeat requests, concurrency and upgrade behaviour match the requested policy.

Profile: `specialists/whmcs.md`.

### specialist:plugins-mcp

Evolve plugin instructions, routers and tool/host contracts from evidence while preserving identity, explicit scope, compatibility and release provenance.

**Use when:**

- A plugin, skill catalogue, command router, MCP server or ChatGPT app is being built or changed.
- Tool descriptors, manifests, widget bridges or native-host contracts affect the requested behaviour.

**Avoid when:**

- The task only invokes an existing plugin to perform unrelated application work.
- No plugin, tool or host integration is in the actual scope.

**Acceptance evidence:**

- Catalogue entries, handler paths and portable/native route semantics resolve consistently, including preserved explicit invocations.
- Changes retain identity, scope, prompts, configurations and assets outside the authorized delta; private usage history is excluded.
- Realistic behavior and clean-package checks are recorded separately from guarded release/read-back and untested host activation.

Profile: `specialists/plugins-mcp.md`.

### specialist:browser-extraction

Ground reconstruction and UI repair in identified source versions, asset dependencies and comparable rendered/interactive states.

**Use when:**

- The task extracts, rebuilds or diagnoses an existing website or browser interface.
- Saved HTML/assets, screenshots, live page behaviour or browser-only failures are evidence.

**Avoid when:**

- The task is a public factual lookup with no need to interact with a page.
- A native application is the target and the available browser cannot observe it.

**Acceptance evidence:**

- Page/state/asset inventory identifies exact sources, output revisions and inaccessible targets.
- Source and output are compared under recorded viewport/theme/font/control conditions.
- Affected interactions and standalone exports are exercised; still screenshots do not stand in for motion or native-editor evidence.

Profile: `specialists/browser-extraction.md`.

### specialist:native-yaml-archives

Map supplied HTML and the current kit to genuinely editable native widgets, presets and complete import packages with explicit custom-code exceptions.

**Use when:**

- A supplied native YAML kit or receiving editor contract governs conversion of HTML, design-system sections or structured bundles.
- Editable cards/products/tabs, preset variables, custom-code restrictions or archive/import compatibility are acceptance requirements.

**Avoid when:**

- Only a static screenshot or prose explanation is needed.
- No receiving schema/import contract can be obtained; report the gap before claiming compatible native output.

**Acceptance evidence:**

- The current kit and every requested section reconcile with a supported widget/field/capability mapping.
- Custom HTML stays inside the explicit exception allowlist; presets, assets and nested editability are preserved.
- Parsing, schema checks, actual editor import and rendered parity are reported as separate evidence levels.

Profile: `specialists/native-yaml-archives.md`.

### specialist:content-seo

Build and migrate source-grounded content collections with real destinations, preserved approved copy, coherent presentation and validated metadata/schema.

**Use when:**

- Markdown/MDX content, seo.yaml/schema.yaml, article migrations or generated service pages are in scope.
- Canonical URLs, sitemaps, redirects, internal links or structured-data output are affected.

**Avoid when:**

- The task requests only general marketing strategy with no implementation or content artefact.

**Acceptance evidence:**

- Every requested content item maps to a produced destination or explicit exception; absent content is not invented to fill navigation.
- Approved headings, code, assets and required content variants survive conversion and agree with visible output.
- Metadata/schema/internal links validate against current content and canonical routes without unsupported product or ranking claims.

Profile: `specialists/content-seo.md`.

### specialist:python-data

Build resumable data processing with validated inputs, explicit failures and reconciled outputs.

**Use when:**

- Python scripts, API ingestion, scraping outputs, transformations or automation pipelines are changing.
- Pagination, retries, checkpoints, data contracts or partial failure affect correctness.

**Avoid when:**

- The project has no Python/data-processing component.

**Acceptance evidence:**

- Representative real input produces schema-valid, reconciled output.
- Reruns, partial failures and pagination do not silently lose or duplicate data.
- Existing runtime/tooling and externally visible data contracts remain compatible.

Profile: `specialists/python-data.md`.

### specialist:database

Apply engine-specific checks to migrations, queries, tenant access, locks and data compatibility.

**Use when:**

- SQL/schema changes, query behaviour, data access rules or database performance are in scope.
- A migration, import, restore or concurrency issue can affect persisted data.

**Avoid when:**

- The change is purely presentational and does not alter data access.

**Acceptance evidence:**

- Schema/query changes match the detected engine and migration tooling.
- Data invariants, access boundaries and relevant concurrency behaviour hold.
- Migration and rollback/recovery evidence is appropriate to the authorised environment.

Profile: `specialists/database.md`.

### specialist:infrastructure

Ground infrastructure changes in provider versions, actual state, execution mode and recovery evidence.

**Use when:**

- Server/container configuration, infrastructure as code, CI deployment or runtime operations are changing.
- Networking, secrets, storage, provisioning or service health affect the requested result.

**Avoid when:**

- The task is only application UI/content work with no infrastructure impact.

**Acceptance evidence:**

- Configuration validates with the detected tool/provider versions.
- Planned changes and affected resources are understood before authorised application.
- Health and recovery checks distinguish prepared, applied and verified states.

Profile: `specialists/infrastructure.md`.

### specialist:migration-release

Resume interrupted work from real source and task evidence, preserve milestones and reconcile the requested repository/package/release outcome.

**Use when:**

- The task resumes a stalled build, migrates systems, recovers missing work or completes a release.
- Local files, branches, commits, remote repositories or packaged versions disagree.

**Avoid when:**

- There is no migration/release/recovery scope and a normal implementation stage suffices.

**Acceptance evidence:**

- Task scope is reconciled against actual local, committed, pushed, packaged and deployed revisions.
- Authorized significant milestones and next actions are preserved without erasing unrelated work or publishing user media beyond the authorized deliverable and audience.
- Remote/package/readback evidence and remaining source, access or environment failures are distinguished explicitly.

Profile: `specialists/migration-release.md`.

### specialist:realtime-native

Trace message identity, delivery/history, hidden/popout views and shared media ownership through the actual realtime or native runtime.

**Use when:**

- The actual repository uses realtime chat/media, WebRTC, streaming or multi-window state.
- A native macOS application or SwiftUI/AppKit bridge is explicitly part of the task.

**Avoid when:**

- A device mentioned in conversation is only the user's computer, not the project target.
- The task is static frontend work with no realtime or native lifecycle.

**Acceptance evidence:**

- Duplicate/retried/reordered messages, acknowledgements, previews and persisted history behave across relevant view/session transitions.
- Hidden/popout views retain required subscriptions and shared camera/media owners release resources only at the correct boundary.
- Live settings, layout and reconnect/teardown checks identify what ran in a real host versus a simulation.

Profile: `specialists/realtime-native.md`.

### specialist:reference-fidelity

Preserve approved source identity, constrain changes to requested deltas and verify observable results without collateral redesign.

**Use when:**

- The task reconstructs or adapts supplied HTML, images, screenshots or approved artifacts.
- Specific corrections, reference-locked variants or repeated complaints require an item-level delta and preservation checks.

**Avoid when:**

- No reference/preservation requirement affects the change.
- The user explicitly requests free exploration; do not impose pixel matching without a source contract.

**Acceptance evidence:**

- Every correction/target maps to its exact source, allowed change and protected properties.
- Comparable before/after evidence shows the named delta and checks retained properties against regression.
- Exactness claims state the actual renderer, conditions and comparison result; unavailable visual evidence remains unverified.

Profile: `specialists/reference-fidelity.md`.

### specialist:design-system

Maintain canonical components, tokens, fonts, icons and saved visual presets consistently across consumers and interaction states.

**Use when:**

- Shared sections, design tokens, typography systems, icon libraries or component catalogs change.
- Theme/accent/font controls, per-section overrides or reusable HTML exports need consistent styling and persistence.

**Avoid when:**

- An isolated illustration has no shared system or consumer contract.
- The task changes only local copy and does not need new theme/catalog infrastructure.

**Acceptance evidence:**

- Changed component families and consumers reconcile with canonical owners and the expected rollout inventory.
- Font loading/computed styles and relevant mode/accent/type/interaction/viewport states are actually checked.
- Preset change/save/reload/export behavior and standalone component dependencies match their declared contract.

Profile: `specialists/design-system.md`.

### specialist:image-art-direction

Direct authorized image generation/editing with source-locked composition, consistent geometry and semantically distinct product concepts.

**Use when:**

- Product renders, hero/CTA imagery, consistent asset families or precise reference-image edits are requested.
- Multiple image concepts or variants need shared-base invariants, meaningful differences and a reconciled output set.

**Avoid when:**

- An exact chart/technical diagram needs deterministic geometry or factual data.
- The task implements raster-to-vector conversion rather than generating/editing visual art.

**Acceptance evidence:**

- Requested assets, dimensions, backgrounds and individual/sheet output forms reconcile with the target matrix.
- Reference and output inspection checks geometry, orientation, edges, material detail, composition and protected properties.
- Actual image-tool identity/evidence and any fidelity limits are reported without claiming unsupported pixel preservation.

Profile: `specialists/image-art-direction.md`.

### specialist:motion-interaction

Model and verify meaningful animation sequences, transitions, controls and theme-dependent states over a complete relevant cycle.

**Use when:**

- Animated hero widgets, terminals, maps, carousels, tab cycles or transition defects are in scope.
- Pacing, flashing, jumping, barely visible state changes, playback controls or preview clutter affect the requested result.

**Avoid when:**

- The target is static imagery with no temporal behavior.
- Only realtime session/resource ownership is involved; use realtime-native.

**Acceptance evidence:**

- Changed timelines, startup/loop states and relevant controls are observed in the actual supported runtime.
- Timing, layout stability, readability and theme states are checked separately from static appearance.
- Evidence records output revision and observed cycles; screenshots/builds do not imply temporal verification.

Profile: `specialists/motion-interaction.md`.

### specialist:media-library

Extend existing media-workspace navigation, imports, storage and conversion while preserving identity, privacy and measurable fidelity.

**Use when:**

- An HTML/image/icon library, nested ZIP importer, media tree/gallery or large asset workflow changes.
- Local conversion, native-pixel comparison, source/preview mapping or media loading performance is a requirement.

**Avoid when:**

- The task creates visual art rather than library/conversion behavior.
- A simple one-file export does not involve app integration, ingestion or asset lifecycle.

**Acceptance evidence:**

- New categories reuse intended shell/tree/import lifecycles and survive reload/navigation/export alongside existing ones.
- Requested/imported/duplicate/failed targets reconcile and nested resource links remain valid.
- Fidelity/performance/local-only claims are supported by appropriate real comparisons and observations, with actual transport limits stated.

Profile: `specialists/media-library.md`.

### specialist:artifact-delivery

Reconcile complete deliverables, dependency closure, actual output revisions and authorized destination readback before claiming handoff.

**Use when:**

- Multi-file packages, standalone components, archives, asset sets or saved catalog revisions must be delivered.
- Import, upload, publication or stale-output complaints require exact target/version and completeness evidence.

**Avoid when:**

- The task is explanation-only with no artifact or delivery requirement.
- A format owner still needs to validate the content; packaging alone cannot replace that work.

**Acceptance evidence:**

- Final artifacts and dependency closure reconcile with the independent requested inventory.
- Standalone/opening or clean-extraction checks run in the intended receiving context.
- Saved/uploaded/published/observed states identify the same verified output revision, with readback gaps and provider-authenticity limits explicit.

Profile: `specialists/artifact-delivery.md`.

### specialist:usage-learning

Analyze complete task evidence with deduplication and outcome limits, map demand to current capabilities and evaluate bounded plugin improvements.

**Use when:**

- Usage exports, agent traces or repeated feedback are supplied to improve plugins, skills, routers or workflows.
- Existing-versus-missing capability analysis and prioritized evidence-grounded instruction changes are requested.

**Avoid when:**

- The request is ordinary task execution or one local correction already owned by a domain stage.
- Unrelated personal-history discovery is not needed or authorized for the current request.

**Acceptance evidence:**

- All available requested records reconcile with row-level analysis, duplicate/omission handling and reproducible denominators.
- Changes map concrete demand to existing/refined/new capability owners while preserving current scope and compatibility.
- Sanitized realistic evaluation and private-data exclusion are verified separately from release/host activation.

Profile: `specialists/usage-learning.md`.

### specialist:ui-design

Apply scoped visual corrections and a coherent design direction to every relevant UI task, with complete target review and evidence of visible quality.

**Use when:**

- The actual request creates, changes, reconstructs, reviews or improves a user-visible layout, design, typography, palette, spacing, component presentation, visual asset or motion.
- A contextual follow-up asks for visual improvement or corrects prior output, including brief feedback without explicit UI keywords.
- A mixed engineering task changes user-facing presentation; apply this lens only to the relevant part and preserve the selected stage boundary.

**Avoid when:**

- The actual task is nonvisual backend, data, infrastructure or source analysis; incidental UI vocabulary does not establish visual scope.
- Only a selector or a bare invocation with no recoverable task context is present; identify the actual task before assigning work.

**Acceptance evidence:**

- Current task, approved source, permitted changes, protected properties and canonical component/token owners determine the design contract before edits.
- Every explicitly requested target is visually inspected with its own disposition, defects and improvement opportunities; a sample never becomes an exhaustive review claim.
- Rendered appearance, relevant interactions and motion are checked against the actual output revision; structural validation alone is not proof of visual quality.
- Native editor work maps to supported kit widgets and authorized exceptions, while project preferences and historical numeric examples remain scoped to their actual context.

Profile: `specialists/ui-design.md`.

Authoritative references: [references/ui-routing.md](../references/ui-routing.md), [references/ui-correction-playbook.md](../references/ui-correction-playbook.md), [references/ui-correction-rules.json](../references/ui-correction-rules.json), [references/ui-quality-review.md](../references/ui-quality-review.md), [agents/ui-design-director/agent.md](../agents/ui-design-director/agent.md), [references/ui-component-craft.md](../references/ui-component-craft.md).

## Existing profile inventory

Six core families are active roster choices. Compatibility entries preserve old paths and operation boundaries; domain lenses add knowledge. None proves running workers.

| Profile path | Type | Label | Used by |
| --- | --- | --- | --- |
| agents/accessibility-verifier/agent.md | compatibility-profile | Accessibility Verifier | Inventory only |
| agents/architect/agent.md | core-family | Architect | command:GPL, command:GCP, command:GA, command:GAA, command:GPP, stage:plan-goals, stage:design-architecture, stage:plan-code, stage:plan-tests |
| agents/builder/agent.md | core-family | Builder | command:G0, command:G1, command:GB, command:GT, command:G7, command:GEA, command:GCA, command:GR, command:GH, command:GF, command:GX, command:GU, command:GJ, command:GP, command:GD, command:G6, command:GTF, command:GEX, command:GTE, command:GVD, command:GCL, mode:loop, stage:write-red-tests, stage:execute-plan, stage:fix-reviewed-defects, stage:update-docs |
| agents/code-goal-planner/agent.md | compatibility-profile | Code Goal Planner | Inventory only |
| agents/code-reviewer/agent.md | compatibility-profile | Code Reviewer | Inventory only |
| agents/codebase-assessor/agent.md | compatibility-profile | Codebase Assessor | Inventory only |
| agents/contribution-scout/agent.md | compatibility-profile | Contribution Scout | Inventory only |
| agents/design-specialist/agent.md | compatibility-profile | Design Specialist | Inventory only |
| agents/doc-updater/agent.md | compatibility-profile | Doc Updater | Inventory only |
| agents/e2e-runner/agent.md | compatibility-profile | E2E Runner | Inventory only |
| agents/fast-engineer/agent.md | compatibility-profile | Fast Engineer | Inventory only |
| agents/feature-finaliser/agent.md | compatibility-profile | Feature Finaliser | Inventory only |
| agents/goal-planner/agent.md | compatibility-profile | Goal Planner | Inventory only |
| agents/implementation-executor/agent.md | compatibility-profile | Implementation Executor | Inventory only |
| agents/investigator/agent.md | core-family | Investigator | command:GS, command:GAS, command:GRS, command:GRC, stage:research-technical, stage:discover-contributions, stage:assess-codebase, stage:diagnose-failure, stage:extract-behaviour-spec |
| agents/loop-executor/agent.md | compatibility-profile | Loop Executor | Inventory only |
| agents/loop-reviewer/agent.md | compatibility-profile | Loop Reviewer | Inventory only |
| agents/performance-verifier/agent.md | compatibility-profile | Performance Verifier | Inventory only |
| agents/plan-reviewer/agent.md | compatibility-profile | Plan Reviewer | Inventory only |
| agents/red-test-author/agent.md | compatibility-profile | Red Test Author | Inventory only |
| agents/refactor-cleaner/agent.md | compatibility-profile | Refactor Cleaner | Inventory only |
| agents/researcher/agent.md | compatibility-profile | Researcher | Inventory only |
| agents/reviewer/agent.md | core-family | Reviewer | command:G0, command:G1, command:GB, command:GC, command:G6, command:GPR, command:GVR, mode:loop, stage:review-ui-spec, stage:review-plan, stage:review-code, stage:review-dependencies, stage:verify-goal, stage:verify-docs |
| agents/security-verifier/agent.md | compatibility-profile | Security Verifier | Inventory only |
| agents/tdd-guide/agent.md | compatibility-profile | Tdd Guide | Inventory only |
| agents/tdd-implementer/agent.md | compatibility-profile | Tdd Implementer | Inventory only |
| agents/ui-design-director/agent.md | core-family | Ui Design Director | command:G7, command:GDA, command:GDS, stage:design-ui |
| agents/unit-verifier/agent.md | compatibility-profile | Unit Verifier | Inventory only |
| agents/verification-engineer/agent.md | core-family | Verification Engineer | command:GE, command:G6, command:GUT, command:GVE, command:GVS, command:GVA, command:GVP, mode:loop, stage:run-tests, stage:run-e2e, stage:review-ui, stage:review-accessibility, stage:review-security, stage:verify-performance |
| agents/visual-fidelity/agent.md | compatibility-profile | Visual Fidelity | Inventory only |
| specialists/artifact-delivery.md | domain-lens | Artifact completeness and verified delivery | specialist:artifact-delivery |
| specialists/browser-extraction.md | domain-lens | Browser evidence and website extraction | specialist:browser-extraction |
| specialists/content-seo.md | domain-lens | Structured content and technical SEO | specialist:content-seo |
| specialists/database.md | domain-lens | Database schemas and data integrity | specialist:database |
| specialists/design-system.md | domain-lens | Shared design systems, typography and presets | specialist:design-system |
| specialists/editor-schema.md | domain-lens | Editors, registries and persistent schemas | specialist:editor-schema |
| specialists/image-art-direction.md | domain-lens | Image art direction and consistent asset production | specialist:image-art-direction |
| specialists/infrastructure.md | domain-lens | Infrastructure and deployment configuration | specialist:infrastructure |
| specialists/media-library.md | domain-lens | Media libraries, archive ingestion and local conversion | specialist:media-library |
| specialists/migration-release.md | domain-lens | Migration, recovery and release completion | specialist:migration-release |
| specialists/motion-interaction.md | domain-lens | Motion, interactive widgets and temporal verification | specialist:motion-interaction |
| specialists/native-yaml-archives.md | domain-lens | Native YAML and archive conversion | specialist:native-yaml-archives |
| specialists/plugins-mcp.md | domain-lens | Plugins, skills and MCP applications | specialist:plugins-mcp |
| specialists/python-data.md | domain-lens | Python automation and data pipelines | specialist:python-data |
| specialists/react-frontend.md | domain-lens | React and frontend systems | specialist:react-frontend |
| specialists/realtime-native.md | domain-lens | Realtime media and native application lifecycles | specialist:realtime-native |
| specialists/reference-fidelity.md | domain-lens | Reference fidelity and precise corrections | specialist:reference-fidelity |
| specialists/ui-design.md | domain-lens | UI Design Director | specialist:ui-design |
| specialists/usage-learning.md | domain-lens | Usage evidence and workflow improvement | specialist:usage-learning |
| specialists/whmcs.md | domain-lens | WHMCS modules and client-area systems | specialist:whmcs |
| specialists/wordpress-woocommerce.md | domain-lens | WordPress and WooCommerce | specialist:wordpress-woocommerce |
| workflows/agents/behaviour-spec-miner/agent.md | compatibility-profile | Behaviour Spec Miner | Inventory only |
| workflows/agents/dependency-risk-reviewer/agent.md | compatibility-profile | Dependency Risk Reviewer | Inventory only |
| workflows/agents/doc-verifier/agent.md | compatibility-profile | Doc Verifier | Inventory only |
| workflows/agents/goal-verifier/agent.md | compatibility-profile | Goal Verifier | Inventory only |
| workflows/agents/plan-executor/agent.md | compatibility-profile | Plan Executor | Inventory only |
| workflows/agents/plan-reviewer/agent.md | compatibility-profile | Plan Reviewer | Inventory only |
| workflows/agents/researcher/agent.md | compatibility-profile | Researcher | Inventory only |
| workflows/agents/root-cause-analyst/agent.md | compatibility-profile | Root Cause Analyst | Inventory only |
| workflows/agents/test-runner/agent.md | compatibility-profile | Test Runner | Inventory only |
| workflows/agents/test-strategist/agent.md | compatibility-profile | Test Strategist | Inventory only |
| workflows/agents/ui-design-architect/agent.md | compatibility-profile | Ui Design Architect | Inventory only |
| workflows/agents/ui-spec-reviewer/agent.md | compatibility-profile | Ui Spec Reviewer | Inventory only |

## Validation limits

- Structural selection validation only; the host must judge relevance and proportionality.
- No execution, scheduling, agent spawn, host installation, or source mutation is performed.
- Evidence references are not opened or authenticated; actual record, review, approval, and revision gates still apply.
- A valid selection does not prove independent review, passing tests, completed work, or executed proof files.
