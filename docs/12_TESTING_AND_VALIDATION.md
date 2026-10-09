# 12 — Testing and Validation

## Quality goals
Prove the core workflow is correct, secure, reproducible, and honest about uncertainty. UI snapshots alone are insufficient. Highest-risk areas are cross-tenant access, quantity arithmetic, unsupported AI conclusions, duplicate side effects, and unauthorized clearance.

## Test layers
- **Unit:** unit conversions, stock balances, invoice arithmetic, matching normalization, severity rules, eligibility, state transitions, Pydantic schemas. Use deterministic fixtures and `Decimal`.
- **API integration:** FastAPI routes against isolated test DB/schema; verify models, transactions, errors, pagination, idempotency, authorization.
- **Database:** clean/upgrade migrations, constraints, FKs, RLS, uniqueness, tenant integrity, audit history.
- **AI/OCR adapters:** mock providers for deterministic handling tests; opt-in real-provider smoke tests separately. Test malformed JSON, missing fields, mismatched IDs, timeout, quota, unsafe output. Mock tests do not establish provider accuracy.
- **Frontend:** forms, role-dependent actions, loading/empty/error states, keyboard navigation, evidence review, distinction between AI and verified facts.
- **E2E:** Playwright core journey with isolated test identities/data, desktop/mobile viewports, and WebGL fallback.
- **Security:** cross-tenant IDOR, role escalation, malicious uploads, expired signed URLs, CORS, secret scan, certificate authorization.

## Requirements-to-tests traceability
| Requirement | Test ID | Scenario | Expected result |
|---|---|---|---|
| FR-001 | AUTH-001 | Missing/expired/invalid token | Safe rejection |
| FR-002 | AUTHZ-001 | Org A requests Org B project | No data returned |
| FR-002 | AUTHZ-002 | Client submits `role=admin` | Membership-derived role prevails |
| FR-006 | FILE-001 | JPEG MIME with invalid bytes | Rejected/quarantined |
| FR-006 | FILE-002 | Size/page/pixel limit exceeded | Stable safe error |
| FR-006 | FILE-003 | File upload attempted for `site_photo` | Rejected with 422 `INVALID_INGESTION_SOURCE` |
| FR-006 | FILE-004 | Live camera capture for `site_photo` | Accepted with capture telemetry; processing queued |
| FR-006 | FILE-005 | File upload for document (`invoice`/`challan`) | Accepted; OCR processing queued |
| FR-006 | FILE-006 | Live camera scan for document (`invoice`/`challan`) | Accepted with capture telemetry; OCR processing queued |
| FR-007 | JOB-001 | Provider timeout | Visible job failure/retry state |
| FR-008 | OCR-001 | Uncertain field/total mismatch | Candidate flagged, not silently accepted |
| FR-009 | VLM-001 | Malformed model JSON | Rejected; no authoritative mutation |
| FR-009 | VLM-002 | Model invents another evidence ID | Context ID is trusted; mismatch rejected |
| FR-010 | REC-001 | Stock equation with all movement types | Exact Decimal result |
| FR-010 | REC-002 | kg→litre without density | Rejected/inconclusive |
| FR-010 | REC-003 | Repeated idempotent request | No duplicate side effects |
| FR-010 | REC-004 | Baseline changes | Old run unchanged; new run references new baseline |
| FR-011 | ANOM-001 | Legitimate duplicate attachment | Candidate duplicate, not fraud conclusion |
| FR-012 | INV-001 | Findings share timestamp only | Link rationale required; no causal claim |
| FR-013 | REVIEW-001 | Unauthorized approval attempt | Rejected and safely audited |
| FR-014 | CERT-001 | No eligible approval | `CLEARANCE_BLOCKED`; no certificate |
| FR-014 | CERT-002 | Duplicate issuance retry | No duplicate certificate |
| FR-018 | WEB-001 | Load dashboard | No landing scene chunk loaded |
| FR-018 | WEB-002 | WebGL unavailable | Static fallback/CTAs work |

## Calculation vectors
Stock: opening 100, receipts 80, issues 120, returns 5, approved adjustment +2 → expected 67. Physical count 60 → variance −7. Explanation states discrepancy, not cause.

Invoice: 12.5 × 40.00 = 500.00 before tax/discount. A source total of 510.00 must trigger mismatch or explicit tax/fee reconciliation, never silent overwrite.

Unit compatibility: tonne→kg permitted with defined factor; boxes→pieces only with approved pack size; kg→litres blocked unless validated material-specific density and conversion version exist.

## Authorization matrix
For each role, test read/list/create/update/delete or equivalent actions on projects, milestones, evidence, inventory, reconciliation, findings, decisions, certificates. Include allowed and denied cases, inactive/removed memberships, expired tokens, unassigned projects, nested cross-organization IDs, and direct storage access attempts.

## AI evaluation
Maintain versioned representative photos/documents with expected annotations and reviewer outcomes where rights allow. Measure field-level OCR accuracy, schema-valid rate, visual-observation agreement, inconclusive rate, correction rate, latency, and cost. Report dataset size and limits. Never claim measured accuracy from mocks alone.

## UI/accessibility
Keyboard-only flows through login, live camera capture (viewfinder activation, shutter trigger, preview/retake, confirm), document intake (file drag-and-drop or camera scan), review, and decision; visible focus; camera permission denied/granted states; correct labels; contrast; reduced motion; accessible async status; mobile tables/dialogs; preserved input after recoverable errors; 3D canvas has text alternative and never traps focus.

## Resilience and CI
Test large-but-allowed files, long PDFs, concurrent jobs, provider latency, database/storage outages, retry storms, rate limits, stale worker recovery, and failure recovery. CI gates should include formatting, lint, types, unit/API tests, migration checks, frontend tests, secret/dependency scans, and targeted E2E smoke. Provider-dependent tests may run separately if costly/flaky.

## Release checklist
Core journey passes; tenant isolation and certificate permissions pass; migrations reviewed; no secrets in source/build; private storage and upload limits verified; AI uncertainty UI checked; calculations reproduce exactly; dashboard excludes Three.js; logs redact tokens/signed URLs; known gaps/costs disclosed.
