# Architecture and planning capabilities

Apply the [worker contract](worker-contract.md). These operations produce advice or plans,
not application code, tests, dependency installs, deployment or new worker teams. The
coordinator saves the selected record and routes the real artifact through independent
criticism. Use the actual project model, conventions and evidence; no automatic SPARC/Ruflo
CLI, swarm setup, persistent memory system or new task schema.

## design-architecture — the smallest coherent change

Inspect affected components, canonical owners, callers, dependencies, data flow and constraints.
Actual advice must precede the finalized plan for multiple pages/features, shared contracts,
architecture or migration decisions; one edited file does not establish local impact.
Recommend the smallest design meeting the whole request. Explain material tradeoffs,
affected modules/interfaces, migration/cutover order, failure recovery and verification.
Consider actual security boundaries, stored data, observability, scale and compatibility.
Do not use broad consultation as permission for a redesign. Use the project's existing
decision-record format when requested and state essential uncertainty.

## plan-goals — outcomes, preconditions and effects

Establish current and goal states, verified constraints and the gap. Decompose the goal into
actions with preconditions, effects, dependencies and decisive success criteria. Identify
shared prerequisites that unlock dependent work. Compare credible paths by effort, risk and
dependency cost; label estimates rather than invent measurements. A* is appropriate only
for an actual finite state model, not a claim that prose proves global optimality.

Return one sequence and `Action | Preconditions | Effect/deliverable | Dependencies |
Cost/risk | Success check`. Preserve the entire requested goal; a prerequisite is not a
substitute deliverable. Check that each precondition exists or is produced earlier, break
cycles and separate independent reads from overlapping writes. Name material non-goals,
recovery/replanning triggers and future observe/orient/decide/act checkpoints. Do not execute
that loop during a planning-only operation or invent product requirements and tools.

## plan-code — source-backed implementation milestones

Read the selected request, existing record and nearest maintained analogous features. Apply
useful GOAP/SPARC lenses inside one plan: specification and invariants; nonobvious algorithms
or state transitions; existing architecture and seams; dependency-ordered refinement/checks;
and final integration/deliverable acceptance. These are thinking aids, not five new pipelines.

Trace real files/symbols, callers, registry keys, build inputs, configuration, exports, tests
and fixtures. Distinguish capabilities already present, minimal additive extension and the
consumers that must migrate. Prefer extending a verified owner over creating a parallel one.
Use `Milestone | Existing files/symbols | Change/effect | Preconditions/dependencies |
Test/expected result`. Group shared-root-cause or mechanical work instead of planning each
file separately. Include integration checkpoints and deduplicated customer/admin acceptance
where those roles exist; account for delivery manifests, settings and tests as well as code.

Every dependency needs evidence and every requested outcome a check capable of failing.
Account for data, permission and lifecycle risks and a practical recovery path. Use actual
project coverage/performance budgets; never import an example's 80% target or promise timing,
throughput or zero downtime without evidence. Missing input blocks only dependent milestones.
Return the plan with source bindings, protected properties and remaining uncertainty. Under
an explicit plan-only command, implementation has not run; a broader authorized Build can
continue through its existing criticism/admission without creating another pipeline.

## plan-tests — evidence that detects the failure

Translate requested behavior and current evidence into a matrix of path, fixture,
precondition, assertion, false-negative risk, environment and failure interpretation.
Separate unit, integration, contract, browser/E2E and manual checks. For TDD, identify the
intended RED condition and distinguish it from syntax, compilation or infrastructure failure;
GREEN must demonstrate the feature. Use project thresholds, not arbitrary coverage targets.
This operation does not author tests or source. Preserve actual test owner and package manager
and state unavailable environments before promising coverage.
