# 14 — Hackathon Demo and Evaluation

## Objective
Demonstrate a complete construction audit workflow, not disconnected screens: evidence capture, AI-assisted interpretation, deterministic reconciliation, explainable finding, and authorized human decision. All fixture records must be labelled **Demo Data**. Do not claim synthetic records are real or invent accuracy/savings.

## Suggested 5–7 minute narrative
1. **Problem (30–45 sec):** fragmented photos/documents cause slow checks and missed discrepancies.
2. **Entry (20 sec):** show the cinematic 3D homepage and enter the app.
3. **Baseline (40 sec):** show a fictional project, milestone criteria, and BOQ.
4. **Evidence (60 sec):** capture a live camera photo for a construction site milestone (highlighting that file-picker upload is disabled to enforce live site presence) and upload/live-scan a delivery challan; explain evidence ID, capture modality, private storage, and processing state.
5. **AI (60 sec):** show a criterion-linked VLM observation and OCR candidate fields with source references; point out uncertainty/review requirement.
6. **Reconciliation (60 sec):** run deterministic material calculation and show formula, inputs, units, tolerance, and discrepancy.
7. **Investigation (45 sec):** link relevant findings without asserting unsupported causality.
8. **Decision (45 sec):** auditor requests evidence/inspection or records an authorized decision; show blockers preventing clearance.
9. **Close (20 sec):** emphasize traceability, deterministic math, and accountable review.

## Fictional scenario
Use a project such as **Northstar Residential Block — Demo** and a milestone such as “Level 2 structural columns — demo milestone.” Clearly label contractors/vendors/documents as synthetic. Criteria can require specific viewpoints, visible work for a designated area, and an inspection record. Do not claim a photograph verifies concealed reinforcement or structural quality.

## Material example
Opening stock 100 bags; receipts 80; issues 120; returns 5; approved adjustment +2; calculated closing stock 67. Demo physical count 60 gives −7 variance relative to the calculated balance. Explain that this is a discrepancy under the chosen cutoff/input records, not proof of cause. Review timing, count, units, transactions, and documentation.

## Fixture requirements
- Fictional organization/project and supervisor/store/auditor test users.
- Two or three milestones with versioned criteria.
- Small BOQ with explicit units/wastage policy.
- Rights-cleared or synthetic site images.
- Sample invoice/challan documents.
- Receipts/issues/returns/adjustments with expected arithmetic.
- Duplicate-document candidate and missing-evidence finding.
- Expected reconciliation assertions/JSON.

Keep fixtures separate from production code. Never include secrets or production data. If a recorded/mock output is fallback, label it “Illustrative fixture result — not live model analysis.” Do not silently fake provider output in a live AI demo.

## Success criteria
- Demo user can sign in.
- Project/milestone baseline is visible/versioned.
- Evidence ingestion is validated and private (live camera enforced for site photos; file upload or live camera scan for documents).
- Processing state and provenance are visible.
- OCR/VLM output is structured and marked as candidate observation.
- Reconciliation reproduces expected result exactly.
- Finding includes sources, calculation, limitations, and next step.
- Role permissions block unauthorized review/certificate actions.
- Human decision is recorded in audit history.
- Report/certificate is issued only when eligibility passes.
- Homepage fallback and app navigation work if 3D fails.

## Pre-demo checklist
**Environment:** frontend/backend URLs, CORS, Auth redirects, migrations, private storage, provider credentials, worker, and role membership verified. Secrets remain outside source control.

**Data:** reset only dedicated demo environment; verify fixtures/calculations; label synthetic data; exclude personal/confidential records.

**Reliability:** test provider timeout/quota fallback, manual fallback labels, navigation without remote 3D assets, and duplicate-request safety.

**Narrative:** explain AI limitations, show an inconclusive case, and avoid unsupported claims of fraud, legal validity, compliance, accuracy, or savings.

## Proposed internal rubric
| Dimension | Evidence to demonstrate |
|---|---|
| Problem relevance | Clear construction leakage/schedule-drift pain point |
| Architecture | UI/API/storage/AI/worker separation and tenant security |
| Multimodal intelligence | Source-linked VLM observations and OCR with uncertainty |
| Reconciliation | Reproducible formulas, unit checks, provenance |
| Anomaly quality | Explainable rules and review workflow |
| Product experience | Premium 3D homepage plus efficient conventional dashboard |
| Trust | Human decision gate, history, private evidence |
| Reliability | Processing states, retries, provider failure path |
| Demo quality | Working vertical slice and honest claims |

This is a proposed internal rubric, not an official hackathon rubric unless the organizer confirms it.

## Likely judge questions
- **Why VLM?** Flexible criterion-grounded observations, with uncertainty and human review.
- **How prevent hallucinations?** Constrained prompts, schema validation, source references, domain checks, review; hallucinations are not claimed eliminated.
- **How calculate consumption?** Distinguish order/delivery/receipt/issue/return/stock; actual consumption may need further measurement.
- **Can metadata prove tampering?** No, inconsistencies are signals.
- **Is anomaly score fraud probability?** No unless separately calibrated and validated.
- **Why not blockchain?** Access controls, hashes, versioning, and audit logs address MVP provenance; blockchain is not required for core arithmetic.
- **What if AI fails?** Visible failure/pending state or explicitly labeled fixture; deterministic/manual workflow continues where safe.
- **Why disable image file upload for site photos?** Site progress verification requires proof of real-time physical presence on site. Allowing gallery/disk image uploads enables recycling old photos, uploading stock imagery, or faking milestone progress. Requiring in-app live camera capture establishes real-time capture provenance and timestamp/device telemetry. For vendor documents (invoices, challans), both digital file upload and live camera scanning remain enabled because documents are frequently received as digital PDFs or physical paper slips.
- **How prevent unauthorized access?** Verified JWT, membership/project checks, private storage, RLS where applicable, cross-tenant tests.

## After the event
Capture feedback, failed tests, provider costs, field correction rates, reviewer disagreement, false positives, and usability issues. Prioritize evidence-backed improvements; keep future features behind acceptance criteria.
