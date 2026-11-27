---
name: behaviour-spec-miner
description: Compatibility instructions for Behavior Specification Miner; resolve the selected operation to its canonical family and retained capabilities.
---

# Behavior Specification Miner — compatibility entry

This retained path is not another active worker family. Resolve it through the [canonical registry](../../../agents/registry.json) and load [Investigator](../../../agents/investigator/agent.md) with the selected [investigation capabilities](../../../agents/capabilities/investigation.md).

Trace live interfaces, callers, persistence, state transitions, errors and outputs. Return source/test-backed REQUIREMENT and INVARIANT IDs, distinguishing observed behavior from future intent and existing defects. Mark unobserved branches. Produce the selected isolated behavior artifact without replacing product scope or changing application source.

Default capabilities: `extract-behaviour-spec`. The selected operation and current task authority govern; capabilities never widen source, test, documentation or external-write scope.

Return the assigned actual evidence, source/output revision, limitations and effect in the existing record. Profiles do not count as worker identities; follow the [shared worker contract](../../../agents/capabilities/worker-contract.md) without recursively creating a team.
