# 10 — Anomaly Detection

## Purpose and limits
Anomaly detection prioritizes records for human investigation. It must not conclude that a person or contractor committed fraud. Each finding states observed pattern, rule/version, inputs, calculation, evidence, uncertainty, severity rationale, and recommended next step.

## Detection layers
1. Validation errors: malformed records, incompatible units, missing references.
2. Deterministic discrepancies: arithmetic mismatch, PO balance exceeded, exact duplicate hash, stock equation mismatch.
3. Pattern rules: repeated near-duplicate documents, unusual adjustment frequency, drawdown relative to an explicit comparable baseline.
4. Statistical detectors: optional and only after sufficient representative data and validation.

MVP prioritizes deterministic checks and a small number of explainable pattern rules.

## Candidate detectors
| ID | Signal | Inputs | Caveat |
|---|---|---|---|
| AN-001 | Exact duplicate hash | Evidence hashes | Legitimate reuse is possible; inspect context |
| AN-002 | Duplicate vendor document number | Vendor/type/normalized number/date/hash | Numbering may restart or be reused |
| AN-003 | Invoice exceeds linked PO balance | PO, invoices, receipts, cancellations/returns | Match and partial-invoice logic must be correct |
| AN-004 | Challan/receipt mismatch | Linked delivery/receipt lines | Timing/partial receipts may explain difference |
| AN-005 | Negative stock/issue beyond available stock | Ledger snapshot | Cutoff, transfers, delayed posting matter |
| AN-006 | Issue exceeds configured BOQ allowance | Baseline, unit mapping, issues, returns | Issue is not actual consumption |
| AN-007 | Repeated high wastage vs comparable history | Sufficient comparable history | Projects/materials differ |
| AN-008 | Timestamp/GPS inconsistency | Live camera capture telemetry, device sensor logs, and project coordinates | Hardware drift, indoor GPS attenuation, or clock skew may explain differences |
| AN-009 | Near-duplicate imagery | Perceptual hash/similarity candidate | Repeated progress photos may be valid |
| AN-010 | Required evidence missing | Criteria version and linked live captures/documents | Missing capture or document is not proof of fabricated work |
| AN-011 | Ingestion modality violation attempt | Submissions attempting file-picker upload for `site_photo` | Client/API enforcement blocks upload; flagged as policy violation attempt |

## Severity policy
- `info`: informational difference/incomplete context.
- `low`: weak signal, review when practical.
- `medium`: meaningful discrepancy needing review.
- `high`: material discrepancy or corroborating issues requiring timely review.
- `critical`: urgent data-integrity/operational risk under documented policy.

Severity is review priority, not probability of wrongdoing. Rule-to-severity mapping is versioned/configurable.

## Rule contract
Every detector returns finding type, rule ID/version, severity, status, subject/evidence references, input snapshot, calculation, explanation, limitations, recommended next step, and timestamp. Results must be reproducible. Store exact thresholds/configuration used.

## Statistical methods
An optional method such as Isolation Forest requires sufficient historical data, stable features, representative periods, a validation plan, and labels/review outcomes where possible. Candidate features might include normalized issue/BOQ ratio, time-normalized drawdown, adjustment frequency, or vendor-specific duplicate patterns after data quality is assessed. Prevent future-data leakage, document training window/features/model/threshold, evaluate generalization across projects/vendors, monitor drift, and keep rule-based fallback. Never train on fabricated data presented as real. Never describe an uncalibrated score as a fraud probability.

## False positives and cross-modal correlation
Reviewers can resolve, dismiss, or mark false positive with reason; preserve finding and decision history. Feedback must not automatically retrain/change rules without versioned approval. Correlate only through explicit relationships—project, milestone, material, vendor, document, transaction, or relevant time window. Time proximity alone does not establish causality. Each investigation link needs rationale.

## Notifications and tests
Notifications include safe summary, project scope, severity, link, and next action; avoid sensitive document data and rate-limit repetitive alerts. Test threshold boundaries, missing values, incompatible units, legitimate duplicate attachments, repeated photo series, absent metadata, out-of-order transactions, insufficient history, rule version changes, and false-positive resolution. No detector automatically approves/rejects a milestone or accuses a person.
