# 01 — Project Specification

## Executive summary
AuditForge correlates construction milestone requirements, visual site evidence, vendor documents, inventory movements, and quantity calculations. It identifies unsupported claims and discrepancies, then routes them to authorized reviewers. It is not an autonomous fraud authority or a substitute for required engineering inspection.

## Problem
Construction records are fragmented across photographs, PDFs, spreadsheets, paper challans, invoices, and stock logs. Manual comparison is slow and vulnerable to missing references, duplicate documents, unit mismatches, weak evidence provenance, and delayed approvals. AuditForge creates a common evidence model and applies deterministic checks plus AI-assisted extraction.

## Product principles
1. Evidence before assertion.
2. Reproducible arithmetic before opaque prediction.
3. Human authority for consequential decisions.
4. Explicit uncertainty and missing information.
5. Tenant isolation by design.
6. Provenance retained through extraction, normalization, correction, and review.
7. Build an end-to-end MVP before decorative breadth.

## Personas
| Persona | Primary responsibilities |
|---|---|
| Site Supervisor | Capture live site evidence via camera, link it to milestones, respond to evidence requests |
| Store In-Charge | Submit receipt/issue records, attach challans (upload or live scan), resolve inventory gaps |
| Project Auditor | Review evidence, run reconciliation, investigate findings, record decisions when designated |
| Project Manager | Monitor work and resolve blockers; approval rights must be explicit |
| Organization Administrator | Manage organization membership and assignments without bypassing audit history |
| Platform Operator | Maintain service availability; no default access to customer evidence content |

Every role is scoped by organization and, where relevant, project membership. Frontend role hiding is not a security boundary.

## MVP scope
- Supabase Auth, profile, organization/project membership and role checks.
- Projects, versioned milestones/acceptance criteria, BOQ, materials, units, approved wastage policy.
- Private evidence ingestion: live camera-only capture for site progress photos (local file upload disabled to guarantee on-site presence and fresh provenance); dual-mode ingestion (file upload and live camera scan) for vendor documents (invoices, challans, receipts); metadata, SHA-256 hash, status, history, and authorized retrieval.
- OCR/PDF extraction with human correction of uncertain fields.
- VLM candidate visual observations tied to criteria and evidence.
- Canonical material/unit normalization.
- Deterministic comparisons among purchase orders, invoices, challans, receipts, stock, issues, returns, and supported BOQ allowances.
- Explainable rule-based anomaly detection.
- Investigations, human review, clearance eligibility, reports/certificates, audit events.
- Responsive app UI and isolated 3D homepage.

## Out of scope unless separately approved
Autonomous fraud accusations/penalties; automatic engineering/regulatory certification; guaranteed exact completion percentage from images; unreviewed AI financial fields; blockchain by default; unrestricted crawling/URL fetching; bespoke VLM training; predictive scheduling without data; unsupported compliance claims.

## Functional requirements
| ID | Requirement | Acceptance evidence |
|---|---|---|
| FR-001 | Authenticate users | Valid token accepted; invalid/expired token rejected |
| FR-002 | Enforce tenant/project access | Cross-tenant tests return no data |
| FR-003 | Manage projects | Project saved under correct organization and audit event created |
| FR-004 | Version milestone criteria | Historical criteria version remains referenceable |
| FR-005 | Store BOQ with canonical units | Invalid or incompatible units rejected |
| FR-006 | Secure evidence ingestion | Live camera capture enforced for site photos; dual upload/camera options for documents; payloads validated, hashed, stored privately, audited |
| FR-007 | Track processing jobs | Status, attempts, outputs, and failures persisted |
| FR-008 | Extract document fields | Raw source, normalized candidate, provenance, uncertainty retained |
| FR-009 | Produce VLM observations | Schema-valid result references evidence and limitations |
| FR-010 | Reconcile material records | Same versioned inputs produce same calculations |
| FR-011 | Detect anomalies | Each finding has rule/version, evidence, explanation, severity |
| FR-012 | Investigate findings | Linked findings include rationale without unsupported causal claims |
| FR-013 | Record decisions | Actor, time, reason, and referenced versions preserved |
| FR-014 | Gate certificates | No issue without eligibility and authorized approval |
| FR-015 | Generate audit reports | Report reflects a versioned snapshot and is access-controlled |
| FR-016 | Preserve audit history | Sensitive mutations create append-only audit events |
| FR-017 | Responsive UI | Core workflows work on desktop/mobile |
| FR-018 | 3D homepage only | Dashboard/auth bundles exclude 3D scene code |
| FR-019 | Provider failure handling | Safe failed state and bounded retry without duplicate side effects |
| FR-020 | Trace requirements to tests | Critical requirements map to test cases |

## Non-functional requirements
| ID | Requirement | Verification |
|---|---|---|
| NFR-001 | Tenant isolation | Negative authorization suite |
| NFR-002 | No browser secrets | Source/build secret scan |
| NFR-003 | Reproducible financial math | Decimal-based test vectors |
| NFR-004 | UI distinguishes AI from verified facts | UX review |
| NFR-005 | Async jobs do not block API requests | Job submission/polling integration test |
| NFR-006 | Ingestion limits enforced | Live capture stream and document upload boundary/malformed file tests |
| NFR-007 | Audit history retained | Correction and decision history tests |
| NFR-008 | Accessible core flows | Keyboard, focus, labels, contrast tests |
| NFR-009 | 3D fallback/reduced motion | WebGL-off and reduced-motion checks |
| NFR-010 | Replaceable providers | Adapter contract tests |
| NFR-011 | Observable failures | Structured logs, correlation IDs, health checks |
| NFR-012 | Bounded cost exposure | File/model limits, rate limits, retry budgets |

Set performance SLAs only after measuring the actual deployment and dataset.

## Core journeys
**Project setup:** admin creates project, assigns members, defines baseline, criteria, BOQ, units, and wastage policy. Baseline changes create a new version.

**Visual evidence:** supervisor captures live on-site photo using device camera (pre-existing image file upload disabled for site evidence to enforce on-site presence and fresh provenance), selects milestone, reviews live capture metadata (capture timestamp, optional device geolocation), and submits. The backend validates/stores it and queues quality checks and VLM assessment. Results are candidate observations awaiting review; inconclusive is valid.

**Document processing:** store user uploads invoice/challan (PDF/image file) or uses live camera capture to scan physical paper documents on arrival. OCR extracts candidate fields; arithmetic/reference validation runs; original values and uncertainty remain visible. Corrections are attributed and versioned before affecting authoritative reconciliation.

**Reconciliation:** auditor selects period, baseline, and input snapshot. Deterministic rules compare order, delivery, receipt, ledger, BOQ, and supported issue data. Findings cite source records and formulas.

**Review/clearance:** auditor requests evidence/inspection, holds/rejects, or records an authorized approval. Certificates are available only after eligibility checks and designated human approval.

## Domain vocabulary
- **Evidence asset:** source file plus immutable identity/hash/metadata/access rules.
- **Extracted field:** candidate OCR/PDF value, not automatically authoritative.
- **Normalized value:** canonical value with mapping/conversion provenance.
- **Verified fact:** confirmed through the defined review/trusted-record process.
- **AI observation:** model-generated description with evidence and limitations.
- **Calculated discrepancy:** reproducible result from versioned inputs/rule.
- **Anomaly finding:** signal for review, not an accusation.
- **Investigation:** human-managed case combining related evidence/findings.
- **Clearance decision:** authorized outcome under configured policy.

## Success metrics
Instrument upload processing success, field correction rate, review time, reproducible discrepancy count, false-positive review rate, job failures, authorization coverage, and end-to-end completion. Set baselines/targets before claiming improvements.

## Assumptions and acceptance gate
One organization may own many projects; project assignments are required. Supabase Auth is the initial identity provider. AI providers may have quotas/costs. Units, wastage, approval roles, and certificate rules require project configuration. Jurisdiction-specific legal/tax/construction standards are not assumed. MVP passes only when a test project can upload evidence, extract a document with provenance, run deterministic reconciliation, record authorized review, and generate a report/certificate only after eligibility. Demo data must be labelled.
