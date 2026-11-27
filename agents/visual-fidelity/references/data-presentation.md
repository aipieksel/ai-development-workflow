# Repair data-heavy UI

Use this for tables, dashboards and a request such as “this looks wrong; diagnose and
fix it”. The defective capture is evidence of the problem, not an approved design to
reproduce. Inspect the affected live page, current source and comparable local pages;
trace the actual table/filter/detail components and data-query/aggregation owner.
With only a snapshot, repair a labelled preview and provide the production handoff;
do not claim backend behaviour or matching absent sibling pages was verified.

## Main view versus detail

Determine the user decision for each column. One entity per default row; do not render
an unbounded child list or diagnostic paragraphs inside a cell. Aggregate repeated
outcomes once per entity, show concise counts and use the existing drill-down component
for raw evidence when needed. Preserve truthful totals, warnings, permissions and data.
Don't simply CSS-hide a huge list, omit failures from a success claim or delete records.

For comparisons, keep match, mismatch, unknown/unavailable and not-compared distinct.
A successful comparison operation is not the same as a match. Zero known failures
with no comparisons is not “all matched”. Respect the actual enum and business meaning.
Label the aggregation's scope: current page/captured subset versus complete filtered
set. A LIMIT 20 child query cannot produce a truthful global count. Aggregate the full
relevant authorised set in the query/service using existing patterns, avoid join fan-out
and duplicate counting, and fetch detailed rows only when needed. Don't infer identity,
fraud or commission entitlement from browser-fingerprint matches.

## Layout and verification

Follow neighbouring pages' available content width, table treatment, filters, typography
and row density. Full width means the existing content container, not the whole window.
Use flow layout and the owning responsive wrapper; do not ship frozen extraction widths,
heights or nth-child CSS. Keep long identifiers/detail text from dictating main-row size.
Permit deliberate horizontal scrolling on narrow screens without clipping controls.

Before closure test empty, one, many, long-text, mixed-outcome, all-unknown and capped
inputs. Confirm summary counts against the source data and query boundary. Measure table
versus wrapper width, collapsed row heights, overflow and correct entity-row counts.
Test filters, sort, pagination and drill-down only where implemented; preserve their
existing contracts. Inspect screenshots at supported desktop and narrower widths.
Passing assertions alone do not establish good layout; inspect the rendered result.
