# 13 — Implementation Plan

## Delivery strategy
Build a thin complete audit journey early, then deepen subsystems. Do not build every dashboard screen before authorization, data model, and evidence flow work. Each phase ends with a demonstrable result, tests, and updated docs.

## Phase 0 — Workspace/specification audit
Inspect repository, dependencies, environment files, and docs. Validate naming/status/API/schema consistency; list unresolved decisions; choose compatible exact versions at scaffold. **Gate:** critical security/domain contracts consistent; no claims of implementation before code exists.

## Phase 1 — Monorepo and quality baseline
Create Next.js frontend and FastAPI backend. Configure strict TypeScript, Python lint/format/type checks, lockfiles, test runners, environment loading, structured logging, health endpoints, and CI basics. **Gate:** both services start separately; tests/checks run; no secrets committed.

## Phase 2 — Supabase, schema, authorization
Configure Auth; implement organization/membership/project/audit migrations; verify JWT; implement tenant/project authorization and RLS for direct access. **Gate:** two test organizations isolated; role tests pass; clean migrations succeed.

## Phase 3 — Projects, milestones, baseline, BOQ
CRUD projects, milestones, versioned acceptance criteria, units/materials/BOQ, baseline snapshots, permission-aware UI. **Gate:** demo project can be configured; invalid units/quantities rejected; history preserved.

## Phase 4 — Secure evidence ingestion
Private storage; client camera capture module (`getUserMedia` viewfinder, environment-facing stream, capture trigger, retake/confirm) for milestone site photos with local file upload disabled; dual-mode intake (file upload and live camera scan) for vendor documents (invoices, challans, POs, receipts); ingestion initiation/completion, signature/type/size validation, capture telemetry recording (client timestamp, optional geolocation), SHA-256, evidence list/detail, job table/worker skeleton, authorized download. **Gate:** valid evidence stored/traced; site photos strictly require live camera capture; vendor documents accept file upload or live camera scan; file uploads for site photos rejected; cross-tenant access denied; failure recovery works.

## Phase 5 — OCR/document review
PDF text extraction, OCR adapter, invoice/challan schemas, source provenance, arithmetic checks, versioned correction workflow. **Gate:** candidate fields visible; uncertain values flagged; corrections preserve raw extraction; parser failure does not corrupt evidence.

## Phase 6 — VLM visual assessment
Provider adapter, prompt/schema versions, criterion-grounded assessment, validated observations, inconclusive path, reviewer UI, timeout/quota handling. **Gate:** provider output links to evidence/criteria; invalid output rejected; no auto-clearance.

## Phase 7 — Material reconciliation
Canonical materials, unit conversion, PO/delivery/receipt/stock/issue flows, deterministic rules, immutable snapshots and result lines. **Gate:** worked calculations pass; changed baseline creates new run; incompatible units blocked; every discrepancy reproducible.

## Phase 8 — Anomalies and investigations
Implement deterministic rules, finding list/detail, explicit evidence links, case workflow/activity. **Gate:** findings show inputs/rule/severity/caveats/next steps; false positives can be dismissed with reason; no unsupported fraud claim.

## Phase 9 — Human review and certificates
Review state machine, eligibility service, report snapshot/rendering, certificate versioning/access/revocation history. **Gate:** unauthorized decision blocked; missing blockers prevent issue; valid approval generates report; retries idempotent.

## Phase 10 — 3D homepage
Isolated client-only scene, dynamic import, responsive variants, fallback/reduced motion, performance budget, SEO metadata, working CTAs. **Gate:** scene only on `/`; auth/dashboard exclude Three.js; fallback works; no unsupported marketing claims.

## Phase 11 — Hardening and demo
Run full tests, threat review, accessibility, dependency/secret scans, migration review, deployment setup, labeled demo fixtures, and failure rehearsal. **Gate:** complete vertical slice works; release checklist passes; costs/limitations documented.

## Recommended first vertical slice
1. Sign in as test user.
2. Create/select demo project and milestone.
3. Capture live on-site photo for milestone; upload or live-scan challan document.
4. Extract and review fields.
5. Enter a small set of stock movements.
6. Run deterministic reconciliation.
7. Inspect the finding.
8. Record authorized review.
9. Generate report only if eligibility passes.

## Coding-agent protocol
At each phase inspect current files; state plan/dependencies/risks; implement only that phase; run exact checks; report actual outcomes; update docs; list remaining gaps. Compiling screens alone is not phase completion.

## Risk register
- Provider cost/quota: payload caps, rate limits, retry budgets, monitoring, manual fallback.
- OCR errors: uncertainty and correction workflow, representative evaluation set.
- False positives: explainable rules, cautious wording, human disposition.
- Scope creep: preserve MVP and defer optional models/queues/analytics.
- Security: authorization first, cross-tenant tests early, private storage.
- 3D performance: route isolation, reduced geometry, static fallback, bundle checks.
- Demo instability: preflight credentials, labeled fixtures, honest fallback.
