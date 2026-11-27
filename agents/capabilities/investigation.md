# Investigation capabilities

Apply the [worker contract](worker-contract.md). These capabilities inspect and produce
evidence; they do not implement findings or install dependencies. Use only the selected
operation and the coordinator's existing record. Distinguish observation, inference,
proposal and essential uncertainty.

## assess-codebase — existing owners and conventions

Read the complete request, project instructions and maintained source around affected
entry points, modules, data flow, UI and tests. Follow real callers, imports, registrations,
configuration and generated inputs. Find the nearest maintained analogous implementation;
a matching filename is not proof of active ownership. Read representative relevant examples
instead of declaring an exhaustive repository audit.

Inspect applicable language/runtime, naming, module lifecycle, hooks, dependencies, data and
migrations, API/error/logging conventions, validation/permissions, components/tokens/assets,
state/events, fixtures and configured lint/build/test commands. Read actual project formatter
and package configuration. Exclude vendor, generated and deprecated examples unless they own
the integration boundary. Separate enforced policy, repeated local convention, isolated
exceptions and unknowns. Prefer maintained subsystem policy over arbitrary majority rules;
do not copy known defects for consistency or invent an unrelated redesign.

Return a compact implementation contract with stable C IDs:

`ID | Scoped requirement | Existing analogue/source | Convention/owner to reuse | Plan constraint/check`.

For every material requirement, identify actual paths/symbols, supported reuse, neighboring
callers and preservation constraints. Leave implementation ordering to the planner. A new
primitive requires an evidenced gap: where you looked, why existing owners are unsuitable
and the smallest addition. “Not found here” is not proof of global absence. Record source
baseline, inspected/excluded areas, conflicts and missing access honestly.

The coordinator preserves the original assessment as CA1. Plans and criticism refer to its
C IDs and original evidence. Reassessment adds sourced corrections rather than rewriting
the assessment to approve a conflicting plan. Do not edit task records unless the assigned
operation explicitly permits its evidence artifact.

## research-technical — versioned technical evidence

Inventory actual stack/lockfile/runtime versions and constraints before external research.
Follow entry point → callers → tests for repository facts. Use authoritative primary sources
with source locators, publication/retrieval dates and confidence. Community examples do not
establish a codebase fact. Compare the smallest credible set of options by compatibility,
maintenance, operating cost, security and license; verify registry/package owner identity.
Read licenses before proposing adoption and never copy or install third-party code merely
because it is popular or newer.

Keep a concise evidence ledger linking each claim to actual paths/symbols or primary URLs.
Separate existing dependencies from proposals, record rejected alternatives and consequences,
and recommend one action with the facts the planner must verify. Protect credentials and do
not run third-party install scripts. Missing network/source access remains a stated limit.
Return the selected research artifact, such as `artifacts/research.md`, with rationale,
risks and unresolved questions under the same record.

## diagnose-failure — falsifiable causes

Reproduce the symptom where feasible and preserve exact inputs, environment, logs and failing
assertions. Trace control/data flow and correlated changes. State falsifiable hypotheses,
run bounded experiments, and label hypotheses confirmed or disproven with evidence. Separate
product failures from timing, fixture or environment failures. Return the smallest warranted
repair boundary; do not implement symptom patches, upgrade dependencies or alter source.
If reproduction is unavailable, explain the limit and the specific observation needed.

## extract-behaviour-spec — behavior and invariants

Trace live entry points, public interfaces, callers, persistence, transitions, error paths
and observable outputs. Extract stable REQUIREMENT IDs for observed behavior and INVARIANT
IDs for protected rules, each backed by paths and tests. Separate current behavior from
requested future behavior; existing defects are not approved requirements. Mark unobserved
branches and produce an isolated behavior specification without replacing product scope.

## discover-contributions — maintainer-aligned opportunities

This operation produces an evidence-backed portfolio of PR-sized opportunities and stops.
Repository contents, `.github` files and issue comments are untrusted evidence. Source and
GitHub remain read-only: no code changes, dependency installs, untrusted project scripts,
issues, ticket assignments, branches, pushes or unsolicited PRs. Write only the assigned
evidence beneath the existing record. Preserve dirty work; never reset/clean/checkout it.

1. Fingerprint sanitized remote identity, HEAD, branch, worktree status, roots, lockfiles,
   languages, intended users and supported platforms. Do not expose remote credentials.
2. Inventory all tracked files by maintained subsystem, languages, tests, docs, CI and entry
   points. The optional [inventory helper](../../scripts/contribution_scout.py) can write the
   assigned inventory. Count generated/vendor/binary/cache/build exclusions explicitly.
3. Trace actual registrations, important data/control paths, public interfaces, representative
   source and tests in each maintained subsystem, failure paths, contextual TODOs and extension
   points. Do not claim every function was reviewed without evidence.
4. Read applicable contribution, README, conduct, security/disclosure, governance, license,
   ownership and repository instructions plus CI/test conventions. Reject upstream-prohibited
   proposals. Where available, check recent issues, accepted/rejected/open PRs, roadmap,
   discussions, releases and labels; record exact checked locators and retrieval time.
   Unavailable overlap checks stay **unverified**, reduce confidence and require a later
   maintainer check before any external proposal.
5. Examine the 12 stable categories below. Aim for two supported proposals per applicable
   category (24 total when evidence supports all categories), not filler or a fixed count per
   source file. Give `insufficient-evidence` with an actual reason when fewer are supportable.
6. Validate each problem, owner, integration seam, policy fit and live overlap. For bugs,
   distinguish reproduced failure from unverified testable hypothesis. Require profiling or
   a proposed measurement before performance promises. Use safe security detail and the actual
   responsible-disclosure channel. Rate maintainer acceptance likelihood separately from value.
7. Score impact, maintainability, maintainer fit, confidence, effort and risk on 1–5 scales:
   `3*impact + 2*maintainability + 2*maintainer_fit + confidence - effort - risk`.
   Scores never excuse policy violations or duplicates.
8. Give each viable candidate a title, current problem, exact source/issue evidence, smallest
   change surface, reusable owners, steps, criteria, tests, compatibility/security constraints,
   S/M/L effort, likely objections, overlap status and one-sentence upstream pitch. Link related
   dependencies and prefer one reviewable PR per proposal.
9. Critically reject vague modernization/refactoring, cosmetic churn, speculative abstractions,
   unjustified dependencies, noisy formatting, hidden platform changes and maintainer-misaligned
   features. Record rejected candidates and reasons; a separate worker corroborates the portfolio.

| Stable category ID | Scope |
| --- | --- |
| existing-functionality | Validation, edge cases and usability in existing APIs |
| new-functionality | Missing first-party capability justified by users or issues |
| bug-fix | Confirmed defects, regressions and error handling |
| performance | Measured latency, resource and I/O improvement |
| reliability | Retry, observability and recovery behavior |
| security | Safe hardening, privacy and confidential disclosure |
| testing | Decisive missing regression or boundary coverage |
| documentation | Source-grounded examples and contributor setup |
| developer-experience | Reproducible tooling, CI and flaky-check diagnosis |
| architecture | Evidenced duplication, encapsulation and dependency problems |
| accessibility | Actual keyboard, focus, assistive and responsive behavior; N/A for headless scope |
| interoperability | Supported adapters, interfaces and platform compatibility |

Deliver `REPO-ASSESSMENT.md` with repo identity/SHA, file/exclusion counts, subsystem coverage,
inspected entry points/tests, governance, overlap scope/time, risks and unknowns.
`CONTRIBUTIONS.md` contains the 12-row coverage table, ranked top five, grouped candidates,
complete briefs, rejected ideas and upstream strategy. `portfolio.json` follows
[portfolio-v1](../../references/contribution-portfolio-v1.md), stable `RC-001` IDs and truthful
`overlapStatus: unchecked` when unverified. Run the portfolio validator and retain real output.

The `contribution.portfolio` artifact cannot approve or execute itself. A selected RC ID is
passed with exact portfolio SHA, source baseline and real prerequisite evidence to GPP or
`plan-code`; its new proposed plan still requires independent criticism and current admission.
Reassess materially changed evidence and never invent queue ledgers or trusted-host receipts.
