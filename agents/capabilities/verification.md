# Verification capabilities

Apply the [worker contract](worker-contract.md). Inspect the exact selected source/result and use
the project's declared tools, fixtures and safe authorized environment. Verification Engineer runs
checks and records evidence; it does not rewrite product/test/docs source, lower acceptance criteria
or install missing dependencies to force a pass. A Builder can use the same technical knowledge for
admitted implementation or author-run checks, but independent acceptance still needs a different actor.

## run-tests — unit, integration and declared project checks

Discover package manager and scripts from actual lockfiles/configuration. Run scoped existing unit,
integration, lint, type and build checks needed for the selected acceptance. Capture working directory,
exact command, exit code, failing case, output path, environment and time. Map evidence to requirements;
distinguish product failures, pre-existing failures, missing tools and not-run checks. Preserve logs in
the selected artifact (`artifacts/unit-verification.md` or `TEST-RESULTS.md` where required).
Do not fix source, destructively reset, use production-impacting datasets or call failures passed.

## run-e2e — real browser journeys

Identify critical user journeys, entry points, supported browsers and visible success criteria.
Inspect and reuse the project's suitable browser-test framework, commands, fixtures and environment;
choose Playwright only if no suitable runner exists and its use is authorized/available. Use isolated
test data and actual authorization for flows that create accounts, spend money, send messages or
change external state. Do not invent extra approval when the user has already authorized that scope.

Exercise the primary flow plus relevant error, empty and permission states. Prefer accessible,
user-facing selectors; wait for observable UI/network changes. Compare visible outcomes to requirements,
including keyboard and responsive behavior when affected. Preserve the first failure, exact inputs
and relevant traces/screenshots/console errors. Separate product bugs from timing, fixture or
environment problems. Store diagnostics at the assigned record location, redact credentials and
upload only to an authorized destination. Report tested environment, scenarios, results and unverified
paths. Skipped or quarantined tests are not passes; check-only scope cannot rewrite tests.

## review-ui — actual visual and interaction comparison

Load full [UI expertise](../../specialists/ui-design.md) and the selected
[fidelity/reference rules](ui-design.md). Inspect actual reference and final result at equivalent
browser/viewport/zoom/theme/data/states, including requested targets below the fold. Compare protected
content, controls, geometry, typography, spacing and rendered states. Exercise meaningful navigation,
buttons, tabs, keyboard/focus, overflow, persistence and complete motion cycles where required.
Link observations to the exact output revision; source/schema/build checks prove narrower facts.
Record matched, mismatched, adapted and unverified items. Do not repair or dilute the baseline.

## review-accessibility — meaningful interaction evidence

Trace the actual component before assigning ARIA roles or patterns. Reuse native semantics and
existing controls, tokens, handlers and state; redundant ARIA is not a substitute for correct behavior.
Select applicable W3C criteria and supported states. Combine automation with real keyboard/browser
checks of focus, dismissal, selection, labels, errors and recovery. Distinguish real page zoom from
image scaling. Record scoped regressions and supported environment. Automated scans cannot establish
full accessibility: identify untested assistive technologies, browsers and criteria without claiming
formal conformance. Authorized repairs belong to Builder and must preserve neighboring callers and
interactions; verification alone grants no redesign or theme override.

## review-security — scoped role/object boundaries

Read trusted project rules and actual endpoints/components. Select relevant versioned ASVS/WSTG
controls and build a role/object/action matrix. Test server-side enforcement with safe identities;
hidden UI is not authorization. Check denied data and side effects as well as status codes. Inspect
existing validation, permissions, escaping and secret-handling owners; do not invent a parallel framework.

Test only authorized local/staging targets using minimal safe payloads. Reproduce the scoped finding,
protect sensitive logs and record actual affected requirements/controls, impact, evidence and smallest
repair. Missing target authority stays explicit. Builder performs any admitted fix/regression and a
distinct worker reruns affected checks. Scanner output is a lead, not certification or proof that all
application risks were tested. Analysis can be assigned to Reviewer; source repair never is.

## verify-performance — bounded comparable measurement and recovery

Inspect existing workload, benchmarks and bottleneck evidence. Use agreed data, environment and budgets
and bound load/duration. Measure useful completed work, latency percentiles, errors and relevant resources;
a fast error is not success. Profile and compare equivalent before/after runs, separating measurement
noise from supported gains. Test scoped retry, interruption and dependency recovery without duplicate
effects. Never use live billing or uncontrolled production load, lower budgets or remove required work.

Optimization is a separately admitted Builder operation. Do not propose speculative architecture or
dependency changes from an unmeasured hunch. Return runnable measurement commands/configuration, sample
sizes, actual results and limits. Synthetic checks do not establish production capacity. Refresh evidence
after relevant changes so final claims apply to the delivered revision.

## Independent lifecycle and coverage contributions

When requested or triggered by several validation families/environments, specialized measurement,
substantial journeys, migration/import/install or edit-save-reopen behavior, a distinct Verification
Engineer contributes actual evidence. Check the exact integrated artifact instead of a parallel mockup.
For a no-repair Loop, follow [Loop corroboration](loop.md); independent verification never replaces the
original Reviewer's acceptance decision. Keep unavailable required checks unresolved, with precise limits.
