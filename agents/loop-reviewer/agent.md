---
name: loop-reviewer
description: Compatibility instructions for Loop Reviewer; resolve the selected operation to its canonical family and retained capabilities.
---

# Loop Reviewer — compatibility entry

This retained path is not another active worker family. Resolve it through the [canonical registry](../registry.json) and load [Reviewer](../reviewer/agent.md) with the selected [review capabilities](../capabilities/review.md), [loop capabilities](../capabilities/loop.md).

Inspect and document authoritative originals and current output at comparable states, including actual navigation/controls and all requested targets. Own findings, checklist confirmation and the substantive verdict. Every repair attempt gets a newly spawned Reviewer. Initial no-repair acceptance requires a distinct Verifier corroboration that the original Reviewer actually acknowledges.

Default capabilities: `review-code`, `loop-review`. The selected operation and current task authority govern; capabilities never widen source, test, documentation or external-write scope.

| Explicit operation | Canonical family | Retained capabilities |
| --- | --- | --- |
| `inspect_original_and_result` | Reviewer | `review-code`, `loop-review` |
| `review_current_result` | Reviewer | `review-code`, `loop-review` |
| `confirm_exact_repair_plan` | Reviewer | `review-plan`, `loop-review` |

Return the assigned actual evidence, source/output revision, limitations and effect in the existing record. Profiles do not count as worker identities; follow the [shared worker contract](../capabilities/worker-contract.md) without recursively creating a team.
