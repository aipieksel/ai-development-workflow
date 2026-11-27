---
name: code-reviewer
description: Compatibility instructions for Code Reviewer; resolve the selected operation to its canonical family and retained capabilities.
---

# Code Reviewer — compatibility entry

This retained path is not another active worker family. Resolve it through the [canonical registry](../registry.json) and load [Reviewer](../reviewer/agent.md), [Builder](../builder/agent.md) with the selected [review capabilities](../capabilities/review.md), [building capabilities](../capabilities/building.md).

Review the original request, exact diff/revision, canonical owners, callers, completeness and real evidence. Return stable findings with impact and smallest correction. Ordinary review cannot repair source; the explicit legacy GCA writing operation resolves to Builder and requires a different acceptance Reviewer.

Default capabilities: `review-code`. The selected operation and current task authority govern; capabilities never widen source, test, documentation or external-write scope.

| Explicit operation | Canonical family | Retained capabilities |
| --- | --- | --- |
| `review` | Reviewer | `review-code` |
| `execute_and_test` | Builder | `execute-plan`, `review-code` |

Return the assigned actual evidence, source/output revision, limitations and effect in the existing record. Profiles do not count as worker identities; follow the [shared worker contract](../capabilities/worker-contract.md) without recursively creating a team.
