# AuditForge — Agent Engineering Rules

## Mission and source of truth
AuditForge is an evidence-first construction audit platform. It assesses milestone evidence, extracts vendor-document data, reconciles material flows, identifies anomalies, and supports authorized human decisions. It is decision support—not an autonomous fraud judge, engineering certifier, or substitute for required inspections. Read `README.md` and relevant `docs/` specifications before changing code. If documents conflict, stop, describe the conflict, resolve it explicitly, and update every affected specification before implementation.

## Non-negotiable architecture
- Frontend: Next.js App Router, React, strict TypeScript, Tailwind CSS.
- Public `/` is the only 3D experience. Three.js, React Three Fiber, and Drei must be dynamically loaded only by a client-only landing scene. Never import the scene from a shared/root/dashboard layout.
- All auth, dashboard, project, milestone, evidence, document, inventory, reconciliation, investigation, certificate, report, and settings pages use conventional accessible responsive UI.
- Backend: Python + FastAPI, Pydantic schemas, SQLAlchemy, Alembic migrations.
- Identity: Supabase Auth. Database: Supabase PostgreSQL. Storage: private-by-default object storage.
- Verify JWTs server-side and separately authorize organization/project access on every protected request.
- AI providers are replaceable adapters. Raw model output cannot directly change authoritative records or issue certificates.
- Reconciliation arithmetic is deterministic, versioned, and reproducible. AI may extract or describe; it does not override ledger math.
- Long-running work is asynchronous and has persisted job status, retries, and safe failure states.

## Product integrity
1. Keep verified facts, source-extracted fields, normalized values, calculated discrepancies, AI observations, and unverified suspicions distinct.
2. An anomaly is a review signal, not proof of fraud.
3. GPS/timestamp inconsistencies are signals, not proof of tampering.
4. SHA-256 can detect changes relative to a known hash; it does not establish original authenticity.
5. One photograph generally cannot establish exact completion percentage or hidden construction quality.
6. Never equate purchased, delivered, received, issued, and consumed quantities.
7. A clearance certificate requires documented eligibility checks and an authorized human decision. AI confidence alone cannot clear a milestone.
8. Never invent accuracy, savings, users, certifications, or demo results.

## Code and domain rules
- Keep route handlers thin; business logic belongs in testable service/domain modules.
- Use typed request/response schemas, explicit enums, stable IDs, and stable error codes.
- Use UTC timestamps in storage and explicit timezone conversion at UI boundaries.
- Use `Decimal` and PostgreSQL `NUMERIC` for authoritative financial/quantity calculations.
- Parameterize queries; validate inputs; redact tokens, signed URLs, secrets, document contents, and private storage paths from logs.
- Keep modules cohesive and use dependency injection rather than global mutable state.
- Do not use frontend-only route guards as security controls.

## Security
- Verify JWT signature, issuer, expiry, and relevant claims with a supported method; never merely decode a token.
- Resolve organization/project access from trusted membership records. Never trust a client-supplied role or organization ID as proof of access.
- Never expose service-role keys, database credentials, signing secrets, or AI keys in browser code or `NEXT_PUBLIC_` variables.
- Keep evidence buckets private. Validate file extension, declared and detected MIME, signature, size, and parser behavior. Use random object keys.
- Treat uploaded documents, OCR output, VLM output, and external provider responses as untrusted data. Defend against prompt injection and malformed/oversized files.
- Do not fetch arbitrary URLs found in documents. Any URL-ingestion feature requires a separately reviewed SSRF-safe design.
- Rate-limit expensive operations and make retries idempotent. Never weaken authorization or tests merely to pass a build.

## Database and AI
- Every schema change is a reviewed migration. Test fresh installation and upgrade behavior.
- Preserve provenance/history for evidence, extracted fields, corrections, reconciliation runs, decisions, and certificates.
- Use RLS for any direct client-to-database access, but still enforce backend authorization. A service-role connection may bypass RLS.
- Store provider/model IDs, prompt/pipeline/schema versions, input evidence references, timestamps, validated output, and safe error details.
- Reject/quarantine invalid structured model output. Model output may create candidate observations, never clearance decisions.
- Do not call a score a calibrated probability unless it has been calibrated and evaluated.

## Testing and definition of done
Every task includes relevant unit, integration, authorization, failure, and UI/E2E tests. Test tenant isolation, malformed files, invalid units, provider failures, idempotency, and certificate authorization. A task is done only when code, tests, types/lint, migrations, security checks, docs, and failure handling align. Report actual commands/results; never claim unrun tests passed.

## 3D performance
Use server components by default. Isolate Three.js/R3F in a client-only dynamically imported landing component. Provide loading state, WebGL fallback, reduced-motion support, mobile adaptation, accessible text/CTAs, and bounded geometry/textures. Verify dashboard/auth route bundles do not load Three.js.

## Documentation workflow
API changes update `11_API_CONTRACTS.md`; schema changes update `06_DATABASE_SCHEMA.md`; access changes update `07_SECURITY_AND_ACCESS_CONTROL.md`; calculation changes update `09_MATERIAL_RECONCILIATION.md`; AI output changes update `08_AI_EVIDENCE_PIPELINE.md`. Update dependent tests, `README.md`, and `.env.example` together.

## Execution protocol
Inspect the workspace before changing it. Implement one vertical slice at a time. Before a phase, identify scope/dependencies/risks; after it, run relevant checks, list changed files, report exact results, update docs, and disclose remaining gaps. Prefer a working end-to-end flow over many disconnected mock screens.
