# Task-specific composition guide

Read the relevant workflow entries, selected handlers and their actual dependencies. These are
recommendations for composing a proportional chain, not keyword routing rules or commands to
run blindly. Keep existing evidence and user scope authoritative. Here “diagnose”, “behaviour”,
“visual review”, “goal verify” and “dependency review” refer to bounded internal operations in
the neutral catalogue and [composition guide](portable-composition.md).
First apply [task routing](task-routing.md): resolve the concrete mode, delegate actual work,
use GB/Fast Engineer for known localized builds, and obtain Architect advice before the final
plan for broad/shared effects. These rules take precedence over abbreviated examples below.

## Portable task recipes

The [portable recipe catalogue](../task-recipes/catalog.json) supplies explicit reusable
patterns for the work below. Automatic selection loads a relevant recipe and its operation/profile
dependencies when the actual task needs them; unrelated entries need no evaluation. The user
does not need to choose a code. `/ai-development-workflow recipe <id>` describes
a portable chain without dispatching workers. Read [task contracts](task-contracts.md)
and preserve the current user's scope when adapting it.

Automatic selection first searches the packaged resource index, provisionally from the request
and then with inspected project evidence when needed. A returned recipe is a candidate, not a
decision. If selected, each recommended lens receives a focused selected or not-applicable
disposition and every chosen instruction body is read and assigned concretely.

| Recipe ID | Use it for | Decisive addition to the existing workflow |
|---|---|---|
| `reference-rebuild` | Supplied screenshot, HTML, extracted ZIP or approved page | Source inventory, protected composition, real component reuse, matched render comparison |
| `visual-correction` | Named defects or repeated dissatisfaction with existing output | Exact delta ledger, protected neighbors, current baseline, observable before/after result |
| `design-system-rollout` | Shared components, font sets, modes, accents and presets | Canonical token/component owner and explicit nested-state/caller coverage |
| `native-yaml-conversion` | HTML/design to editable native YAML | Current kit and widget capability map, card/product/tab composition, explicit code exceptions, real round trip |
| `asset-production` | Product image edits, compositions and constrained variant sets | Reference identity, angle/baseline/spacing constraints, allowed variation axes, every output inspected |
| `motion-reconstruction` | Animated heroes, demos, tabs and interactive widgets | Actual source logic, sequence and complete-cycle timing/transition evidence |
| `media-library-extension` | New media/icon workflows inside an existing application | Shared navigation/tree/drop/state owners, metadata/persistence, conversion fidelity and privacy |
| `content-site-delivery` | Source-grounded pages, content migrations and SEO implementation | Current facts and content inventory, approved shared sections, valid links/schema, rendered deliverables |
| `artifact-handoff` | Complete files, imports, packages, destinations and release mismatch | Final revision and asset closure, actual destination readback, separate preparation/delivery states |
| `plugin-evolution` | Improve plugins/skills from actual usage or defects | Complete evidence coverage, deduplication, sanitized behavior cases, compatible saved release |

Do not stack two complete recipes. Borrow their useful atomic operations once, retain the
review dependency, and combine specialist lenses within real assignments. Small corrections
keep an explicitly selected G0 record while using the required Fast Engineer and reviewers;
ordinary localized Auto builds use GB. Review-only tasks stay read-only; a missing renderer is an evidence limit,
not permission to invent results. Recipes do not supersede a companion plugin's native
schema, theme/preset, importer or image-tool contract.

## General composition patterns

| Task and evidence | Start with | Compose the remaining useful operations | Domain specialists and decisive evidence |
|---|---|---|---|
| Small, well-understood reversible fix | Inspect actual owner/consumers; GB/Fast Engineer (preserve an explicit G0 record) | Compact plan → independent critique → actual execution worker → focused check → independent result review | Relevant lens; actual changed behaviour; no solo exemption |
| Unfamiliar substantial build | GAS; GRS for uncertain technical choices | GPP → GPR → GEX → GUT → GVR; goal verify and GVD when material | Stack-matched specialists; requested end-to-end outcomes |
| Bug, regression or silent failure | GAS + diagnose | GPP → GPR → GTF/GTE when a meaningful regression test fits, otherwise GEX → affected verification → GVR | Version/runtime identity, reproduced cause and repaired path |
| React UI or application state | GAS; GDA when rendered UI is involved | GDS if design changes → GPP → GPR → GEX → GUT/GVE → GVA/visual review as relevant | React; editor/schema for persisted editor models; interaction and state parity |
| Editable page/widget/import/export defect | GAS + diagnose + existing schema inventory | GDA/GDS if visual contract changes → GPP → GPR → GEX → round-trip/output verification → GVR | Editor/schema + native YAML/archive; canonical registry, nested content and unknown fields preserved |
| Source-faithful website or screenshot reconstruction | Full source/asset inventory + GDA | GDS → GPP → GPR → GEX → GVE → visual review → GVA | Native YAML/archive + browser extraction as needed; use existing page-builder/importer owners |
| WordPress/WooCommerce feature or issue | GAS + installed WP/PHP/plugin versions | Diagnose for bug → GPP → GPR → GEX → GUT/GVE → scoped GVS | WP/Woo; hooks, capabilities/nonces, data preservation and actual supported runtime |
| WHMCS, billing or external invoice integration | GAS + API/data/security contract | GRS for current docs → GPP → GPR → GEX → integration tests → GVS → GVR | WHMCS + data/database as needed; tenant/account separation, idempotency, pagination and manual-flow preservation |
| AI plugin, skill or MCP update | GAS + catalogue/tool/packaging inventory + GRS | GAA when integration changes → GPP → GPR → GEX → routing/schema tests → GVR; dependency review if sources change → GVD | Plugins/MCP; stable identity, permissions, explicit routing and saved release readback |
| Browser extension, extraction or download issue | Installed reproduction + GAS + diagnose | GPP → GPR → GEX → browser/storage/ZIP verification → GVR | Browser extraction + migration/release; selected/captured/exported counts, assets, interactions and interrupted-download recovery |
| Help centre, Markdown/MDX or content migration | Source/status/route inventory + GAS | GPP → GPR → GEX → parser/schema/link/route checks → rendered samples → goal verify | Content/SEO + native YAML/archive if relevant; exact counts, seo.yaml/schema.yaml and approved copy |
| Python/API pipeline, importer or automation | Real input and contract inventory + GAS | GRS only for unknown APIs → GPP → GPR → GEX → pagination/retry/idempotency/checkpoint tests → GVR | Python/data; partial failures, dedupe keys, missing IDs and reconciled output counts |
| SQL schema or database migration | GAS + engine/version/data ownership | Required Architect advice → GPP → GPR → reviewed migration → GUT + scoped GVS/GVP | Database; supported engine, lock/query evidence, tenant boundaries and reversible rollout |
| Infrastructure, deployment or CI failure | GAS + diagnose + current environment | GPP → GPR → scoped implementation → plan/validation → authorised apply/release → readback | Infrastructure + migration/release; test commands may mutate resources, inspect before execution |
| Stalled task, missing commits or release mismatch | Git/source/record reconciliation + behaviour parity | Resume current reviewed plan; repair only outstanding work → relevant tests → package/install/push evidence as authorised | Migration/release + actual domain lens; preserve uncommitted work and don't equate merge with publication |
| Realtime chat/video, dictation or local/native runtime | Runtime/lifecycle identity + diagnose | GAA only for actual boundary changes → GPP → GPR → GEX → lifecycle/retry/media verification → GVP as relevant | Realtime/native; reconnect, cancellation, device/permission changes, persisted recovery and observable readiness |
| Assessment, research, planning or review only | Relevant GAS/GRS/GRC/GDA/GAA or explicit stage | Stop at requested boundary; planning can include GPP/GPR; review may include GVR/GVS/GVA/GVP | No implementation, deployment or hidden fix stage |
| Documentation-only update | Existing code/diff and GVD | Verify documentation against actual source/commands | Content/SEO only if its artefacts are affected; no code rebuild by default |

## Combination examples

- A React help-centre migration can combine assessed-build, behaviour-parity and content
  verification: GAS → behaviour → GPP → GPR → GEX → GUT → GVE → goal verify → GVD.
  Apply React, content/SEO and migration/release; add editor/schema only if an editor model
  is actually involved.
- A WHMCS password-reset rate-limit repair combines diagnosis, tested implementation and
  security: GAS → diagnose → GPP → GPR → GTF → GTE → GUT → GVS → GVR. Verify allowed and
  denied attempts, account/IP policy, time windows and concurrency in the real installed version.
- An HTML/ZIP-to-native-YAML import combines source fidelity and schema contracts:
  GDA + source inventory → GDS → GPP → GPR → GEX → import/round-trip tests → visual review.
  The current native-YAML and design-system plugins own their native component rules.
- An automatic-router plugin update combines assessment, research, architecture and contract
  verification: GAS + GRS → GAA → GPP → GPR → GEX → GUT → GVR → GVD, followed by an
  authorised release and source readback. Test explicit command preservation and no-task handling.

These examples do not confer publication, deployment, deletion, purchasing or communication
authority. Use the current request and existing permissions. Do not import private histories
or project secrets into the reusable plugin.
