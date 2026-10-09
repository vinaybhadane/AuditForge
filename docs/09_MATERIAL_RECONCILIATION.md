# 09 — Material Reconciliation

## Objective and vocabulary
Provide deterministic, reproducible comparisons across BOQ expectations, purchase orders, invoices, delivery challans (ingested via digital file upload or live camera scan), goods receipts, inventory movements, issues, returns, and supported consumption estimates. Distinguish **planned**, **ordered**, **invoiced**, **challaned**, **physically received**, **issued**, **returned**, and **consumed** quantities. Purchased is not delivered; delivered is not received; issued is not necessarily consumed. Wastage allowance is project/material-specific policy, not a universal constant.

## Versioned input snapshot
Every reconciliation run records project, period/cutoff, baseline version, selected transaction IDs/versions, material mappings, unit conversions, tolerances, algorithm version, and snapshot hash/reference. Changed inputs create a new run. Historical outputs are never rewritten.

## Core calculations
Under one documented signed-movement convention:
`closing_stock = opening_stock + receipts + returns + transfer_in - issues - transfer_out + approved_adjustments`
The adjustment sign must be explicit; alternatively store all movements as signed quantities and sum them. Never mix conventions.

`remaining_order_quantity = ordered_quantity - accepted_received_quantity - valid_cancelled_quantity`
Define whether “received” means physical accepted receipt or another documented event. Do not subtract invoice quantity unless measuring invoicing specifically.

`receipt_delta = normalized_received_quantity - normalized_challaned_quantity`
Compare only after project/vendor/material/reference/unit are resolved. Partial delivery across several challans/receipts is valid.

Where a defensible policy exists:
`allowed_quantity = planned_quantity × (1 + approved_wastage_rate)`
`issue_variance = normalized_issued_quantity - allowed_quantity`
Compare the same material, scope, period, and baseline. An issue variance is not proof of consumption/diversion; consider returns and unconsumed stock.

`computed_line_total = quantity × unit_price`, followed by documented currency precision/rounding. Taxes, discounts, freight, and tax-inclusive/exclusive prices must be explicit. Never overwrite a source total to force a match.

## Worked example (illustrative demo data)
Opening cement stock 100 bags; accepted receipts 80; issues 120; returns 5; approved adjustment +2. Expected closing stock = `100 + 80 − 120 + 5 + 2 = 67 bags`. If the physical count is 60, variance is `60 − 67 = −7 bags`. This is a discrepancy under the chosen inputs/cutoff; it does not prove cause. Check timing, count, units, missing/duplicate movements, and documentation.

## Unit normalization
Keep raw quantity/unit and normalized quantity/unit. Convert only when dimensions match and conversion basis is documented. kg↔tonnes and metres↔millimetres use defined factors; boxes↔pieces require known pack size. kg↔litres requires validated material-specific density and conversion version. Reject/flag ambiguous material aliases and incompatible dimensions. Use Python `Decimal` and database `NUMERIC`.

## Matching and rules
Match in stages: trusted reference; vendor/project; material/SKU; compatible unit/date; line-level quantity; fuzzy candidate only for human review. Store match method, provenance, reviewer, and outcome. Do not merge vendors/materials from similar names alone.

| Rule | Comparison | Result | Caveat |
|---|---|---|---|
| REC-001 | PO line vs invoice | Over/under-billing candidate | Taxes, discounts, partial invoices |
| REC-002 | Challan vs accepted receipt | Delivery/receipt variance | Partial deliveries/timing |
| REC-003 | Receipts vs stock ledger | Missing/duplicate movement candidate | Must link source records |
| REC-004 | Ledger balance vs physical count | Stock variance | Same cutoff/date required |
| REC-005 | Issue vs BOQ allowance | Excess issue candidate | Issue is not consumption |
| REC-006 | Invoice/challan duplicates | Duplicate candidate | Exact vs near duplicate differ |
| REC-007 | Unit conversion | Invalid/inconclusive mapping | Never invent density/pack size |
| REC-008 | Financial arithmetic | Line/header mismatch | Tax/rounding policy explicit |

## Tolerances and corrections
Tolerance is configured per rule/unit/material/project/currency and must state absolute/relative semantics. Store the tolerance used on each run line. If none is approved, report the exact difference and policy gap. Posted stock movements are corrected with reviewed reversal and replacement records; prior runs remain immutable.

## Result contract and tests
Each line stores run/rule version, baseline/input snapshot, source references, raw/normalized values and units, formula, expected/observed/delta, tolerance, status (`matched`, `within_tolerance`, `discrepancy`, `inconclusive`, `not_applicable`), explanation, and timestamp.

Required tests: stock equation; negative stock/over-issue; partial delivery; incompatible units; ambiguous aliases; Decimal rounding; duplicate import/idempotency; reversal/replacement; changed baseline produces new run; cross-project transaction exclusion; missing evidence returns inconclusive rather than zero or fabricated match.
