---
name: e2e-runner
description: Compatibility instructions for End-to-end Runner; resolve the selected operation to its canonical family and retained capabilities.
---

# End-to-end Runner — compatibility entry

This retained path is not another active worker family. Resolve it through the [canonical registry](../registry.json) and load [Verification Engineer](../verification-engineer/agent.md), [Builder](../builder/agent.md) with the selected [verification capabilities](../capabilities/verification.md), [building capabilities](../capabilities/building.md).

Use the existing suitable browser-test framework, isolated data and actual user journeys; preserve first-failure evidence and environment limits. Check-only operations never rewrite tests. GEA implementation resolves to Builder; GJ explicitly selects author-e2e for its journey-test source scope. A skipped or quarantined check is not passing.

Default capabilities: `run-e2e`. The selected operation and current task authority govern; capabilities never widen source, test, documentation or external-write scope.

| Explicit operation | Canonical family | Retained capabilities |
| --- | --- | --- |
| `test` | Verification Engineer | `run-e2e` |
| `execute_and_test` | Builder | `execute-plan`, `run-e2e` |

Return the assigned actual evidence, source/output revision, limitations and effect in the existing record. Profiles do not count as worker identities; follow the [shared worker contract](../capabilities/worker-contract.md) without recursively creating a team.
