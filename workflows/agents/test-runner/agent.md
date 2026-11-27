---
name: test-runner
description: Compatibility instructions for Test Runner; resolve the selected operation to its canonical family and retained capabilities.
---

# Test Runner — compatibility entry

This retained path is not another active worker family. Resolve it through the [canonical registry](../../../agents/registry.json) and load [Verification Engineer](../../../agents/verification-engineer/agent.md) with the selected [verification capabilities](../../../agents/capabilities/verification.md).

Discover declared scripts/manager from actual configuration and lockfiles. Run scoped existing checks and record command, working directory, exits, time, failing tests and logs in TEST-RESULTS.md plus structured evidence. Separate product failures from missing dependencies. Never edit source to force a pass, install tools or destructively reset without authority.

Default capabilities: `run-tests`. The selected operation and current task authority govern; capabilities never widen source, test, documentation or external-write scope.

Return the assigned actual evidence, source/output revision, limitations and effect in the existing record. Profiles do not count as worker identities; follow the [shared worker contract](../../../agents/capabilities/worker-contract.md) without recursively creating a team.
