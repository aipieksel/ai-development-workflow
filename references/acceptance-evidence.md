# Acceptance evidence and delivery completeness

## Use the right proof

An acceptance matrix makes each requested outcome, target and state visible. Keep it in the
existing record. It supplements the plan, critique and actual tools; it does not approve work,
replace domain validation or establish visual quality. A small reversible fix can use the
short correction table in [task contracts](task-contracts.md) without JSON.

For batches, repeated corrections, conversions or multi-state work, capture the expected
requirements, output IDs and check IDs **before implementation**. Reconcile them with the
actual user request and source inventory. Keep that expectation file with the reviewed plan.
Do not reduce expectations, change tolerances or delete failed states to make a pass.
Amend it only for a real scope correction, preserving the previous revision and evidence.

## Two small artifacts

Use `artifacts/acceptance-expectations.json` for the declared contract and
`artifacts/acceptance-matrix.json` for observed results. These are evidence artifacts in the
same task record, not a second record schema. The read-only [validator](../scripts/acceptance_matrix.py)
requires both. Check exact identifiers, not merely equal totals.

The expectations object contains:

| Field | Meaning |
|---|---|
| `schema` | `ai-development-workflow/acceptance-expectations/v1` |
| `requirements` | Every relevant stable R ID; complete-mode use with `--record` requires exact agreement with the current selected record |
| `outputs` | Every expected output with unique `id`, `requirements`, `kind`, `deliveryRequired` and either local `path` or external `locator` |
| `checks` | Every required check/state with unique `id`, `requirements`, `kind`, `criterion`, output `targets`, and optional string `dimensions` |

Check kinds are `source`, `visual`, `interaction`, `motion`, `roundtrip`, `content`, `package`,
`delivery`, `compatibility`, `privacy`, `test`, and `correction`. Dimensions can name viewport,
theme, font, interaction or timeline point. Enumerate every required state; an aggregate
“all themes passed” row hides coverage unless its underlying evidence reconciles the set.

The results object contains schema `ai-development-workflow/acceptance-matrix/v1`, plus
exactly the expected `outputs` and `checks` IDs. Each output has `id`, `status`, and its actual
`revision` when prepared. Each check has `id`, `status`, `targets`, `evidence`, and an `observed`
result for a pass. Target bindings repeat the verified output ID and revision; external
bindings also name the exact locator. This lets the helper reject an old check against a
new artifact, even when someone has refreshed the output's own hash.

Use `passed`, `failed`, `blocked` or `not-run` for checks. Use `pending`, `prepared`, `delivered`
or `blocked` for outputs. A waiver or omitted state is not a pass. Local file evidence has
`path` and `sha256`; paths are canonical, relative to the declared workspace root, with no
symlinks or traversal. Hash actual bytes after the check. Do not use the manifest as evidence
for itself. A file hash proves identity, not that an observation in the file is true.

### Local output example

This is the shape of one expected target and check; preserve the rest of the declared set:

```json
{
  "schema": "ai-development-workflow/acceptance-expectations/v1",
  "requirements": ["R1"],
  "outputs": [{
    "id": "hero", "requirements": ["R1"], "kind": "local",
    "path": "output/hero.html", "deliveryRequired": false
  }],
  "checks": [{
    "id": "hero-light", "requirements": ["R1"], "kind": "visual",
    "criterion": "Requested shadow is removed; approved layout, type and controls remain.",
    "targets": ["hero"], "dimensions": {"theme": "light", "viewport": "1280x800"}
  }]
}
```

The result's local output revision is the current file's SHA-256. The passing check must bind
that same revision and reference actual review evidence. Set `deliveryRequired: true` if
upload/publication is part of the task; a prepared file alone then cannot complete it. A
`delivered` output must name a `deliveryCheck` whose expected kind is `delivery`, whose
targets include that output and whose actual result passed against its current revision.

## Remote and generated outputs

External output expectations use an exact known `locator` instead of a local path, and
`deliveryRequired: true`. The actual output uses the observed release/version/receipt identity
as `revision`. Save the actual provider/tool response privately in the task evidence. Normalize
only its identity into a small JSON receipt:

```json
{
  "target": "exact provider target or artifact locator",
  "revision": "actual observed revision",
  "status": "verified",
  "source": {"path": "artifacts/provider-response.json", "sha256": "actual SHA-256"}
}
```

The output's `receipt` is an evidence reference (`path`, `sha256`) to that receipt file.
The helper checks target/version agreement and the retained response's bytes. A person or
agent must still inspect the original response and the authorized destination. This is not
a signed host receipt and does not authenticate the provider. Preserve relevant safe fields;
never retain credentials or signed transfer URLs merely to satisfy this helper.

Use actual image-generation tool/host output identities and existing delivery evidence when
available. Do not download, reconstruct or re-upload a generated image just for this matrix.
If no usable host receipt/version is exposed, use the normal observed tool result and report
that the structured external check was not run; the optional helper does not invent IDs or
override the host's generated-image handling. No URLs are fetched by the validator.

## Run and interpret

```bash
python3 <skill>/scripts/acceptance_matrix.py \
  --root <workspace> \
  --expectations <record>/artifacts/acceptance-expectations.json \
  --matrix <record>/artifacts/acceptance-matrix.json \
  --record <record>/record.json \
  --complete
```

Paths to the manifests/record must remain under the supplied root. Omit `--complete` for
progress validation; the helper then never reports completion. Omit `--record` only when
there is no development record (such as the existing G0 checklist path), and retain the
`declared-expectations-only` coverage boundary in the result. With `--record`, the requirement
sets must match. Neither mode reads the original conversation or judges its semantic coverage.

Exit 0 means the requested structural check passed; exit 2 means it failed. Complete mode
requires every declared check passed with nonempty current evidence, every expected output
prepared or delivered, and required delivery verified. Zero-file analysis tasks are supported
with an empty output list and requirement checks referencing real analysis evidence.

An external publication may be blocked while local implementation is verified. Keep those
statuses separate and continue available work. Never turn a green matrix into “pixel perfect,”
“all users verified,” “installed,” “deployed” or “accepted” without the corresponding proof.
