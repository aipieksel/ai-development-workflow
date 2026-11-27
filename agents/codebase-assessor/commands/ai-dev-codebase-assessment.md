---
{
  "command": "GS",
  "launcher": "ai-dev-codebase-assessment",
  "order": 1,
  "phase": "Assessment",
  "label": "Assess, plan, review and build",
  "stages": "0123",
  "recordKind": "development",
  "createsRecord": true,
  "agentCalls": [
    {
      "agent": "investigator",
      "when": "after_0_before_1",
      "operation": "assess_codebase",
      "capabilities": [
        "assess-codebase"
      ]
    }
  ],
  "summary": "Assess existing code conventions before planning and implementation",
  "requires": [
    "subagent"
  ],
  "effects": "Scoped implementation and verification; no automatic deployment.",
  "pickerVisible": true,
  "kind": "pipeline"
}
---

# AI Codebase Assessment — GS

Follow the [shared execution rules](../../../references/command-runtime.md) for records,
stages, scope, progress, handoffs and optional logging. Load only this command’s
linked references and selected agent profiles.

Run **0 → assessment → 1 → 2 → 3**. The assessment is before planning, not a
post-hoc justification. Call [codebase-assessor](../agent.md)
as a real read-only worker. Under [task routing](../../../references/task-routing.md),
the coordinator retains scope and record ownership, obtains any required Architect advice
before the final plan, assigns independent plan criticism and delegates implementation to
a real execution specialist. Obtain independent result acceptance before closure.

1. After stage 0 and source capture, supply scope, project root and the exact record.
   Wait for actual findings before drafting implementation steps. Preserve the
   returned report verbatim in `requestSources` as `id: CA1`, `role: context`, with
   its actual result locator as `origin`. Seal `requestHashes` with the existing
   `seal_request_sources` helper before planning; summarise its C-ID contract in
   fix-plan.md without replacing the original report or creating another record.
2. In stage 1, derive P steps and T checks from the request and applicable C IDs.
   Name existing owners to reuse. Verified local conventions govern over generic
   examples; user scope and enforced project policy still apply.
3. In stage 2, compare each material change and its tests with CA1 and sourced addenda.
   Record conflicts and F-ID dispositions in critique.md. Prefer fixing the plan.
   Never rewrite CA1 to clear a conflict: append sourced CA2, CA3, etc. only for
   corrected findings, changed requirements or changed source evidence. Re-review;
   unresolved material conflicts remain in blockers. Finalise ready/revised only
   after conformity or an evidenced authorised exception.
4. Stage 3 requires the assessment and current criticism. Follow the admitted
   conventions, recheck relevant source assumptions and test existing callers.
   Material drift returns affected work to assessment/review on the same record.
   Reconcile the final diff with the contract and evidence before closure.

The resolver rejects GS without CA1 or a current critique. A planned finalisation
validates structure, not execution admission or semantic correctness. Keep routine
handoffs internal. Assessment-only or planning-only instructions stop at that
boundary. Missing real agent capability leaves assessment pending, not fabricated.

**Advanced command classification:** This is a **complete pipeline**, not a standalone stage. For bounded composition, use the atomic handlers in `commands/stages/` or the internal operation catalogue. The selected operations and record semantics are preserved; the shared mode, delegation and impact rules govern staffing.

Before task work and each workflow/stage or agent transition, follow [progress announcements](../../../references/progress-announcements.md).

## Team contract

Resolve the selected operation through the six-family registry and [task routing](../../../references/task-routing.md). Every new logical task returns useful, current contributions from at least two different actual workers, excluding the coordinator. Preserve this command’s inputs, phases and write scope. The coordinator supplies any missing independent criticism/corroboration and result acceptance without inventing a second implementation pipeline. Already assigned children perform their bounded assignment without recursively spawning teams.
