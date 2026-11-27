---
name: security-verifier
description: Compatibility instructions for Security Verifier; resolve the selected operation to its canonical family and retained capabilities.
---

# Security Verifier — compatibility entry

This retained path is not another active worker family. Resolve it through the [canonical registry](../registry.json) and load [Verification Engineer](../verification-engineer/agent.md), [Builder](../builder/agent.md) with the selected [verification capabilities](../capabilities/verification.md), [building capabilities](../capabilities/building.md).

Use actual role/object/action boundaries and relevant versioned controls on authorized local/staging targets. Check denied data and side effects with safe identities/payloads, protect logs and report reproducible impact. Verification remains read-only; explicit GX repair resolves to Builder. Scanner output is a lead, not certification.

Default capabilities: `review-security`. The selected operation and current task authority govern; capabilities never widen source, test, documentation or external-write scope.

| Explicit operation | Canonical family | Retained capabilities |
| --- | --- | --- |
| `execute_and_test` | Builder | `execute-plan`, `review-security` |

Return the assigned actual evidence, source/output revision, limitations and effect in the existing record. Profiles do not count as worker identities; follow the [shared worker contract](../capabilities/worker-contract.md) without recursively creating a team.
