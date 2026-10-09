# AuditForge

**Every Claim. Verified by Evidence.**

AuditForge is an evidence-first construction operations auditing platform. It correlates site photographs, milestone acceptance criteria, purchase orders, invoices, delivery challans, goods receipts, stock movements, and material reconciliation. AI assists with visual observations and document extraction; deterministic rules calculate discrepancies; authorized humans make review and clearance decisions.

> AuditForge is decision support. An anomaly is not proof of fraud, and AI output is not an engineering or regulatory certification.

## Goals
- Verify milestone claims against documented criteria and available evidence.
- Extract structured information from invoices, challans, purchase orders, and receipts.
- Reconcile quantities and financial values reproducibly.
- Surface unusual consumption, duplicate documents, and inconsistent records.
- Provide evidence-linked investigations and human-reviewed clearance decisions.
- Preserve provenance, permissions, and audit history.

## Experience and stack
- `/`: premium interactive 3D construction-site homepage.
- All other routes: conventional responsive Next.js SaaS UI. Three.js must not load on dashboard/auth routes.
- Frontend: Next.js App Router, React, strict TypeScript, Tailwind CSS; React Three Fiber/Drei only for `/`.
- Backend: FastAPI, Pydantic, SQLAlchemy, Alembic.
- Auth/database/storage: Supabase Auth, PostgreSQL, private object storage.
- AI: replaceable VLM provider adapter; OCR/PDF extraction via evaluated tools such as PaddleOCR/Tesseract and native PDF text extraction.
- Testing: Pytest, frontend unit/component tests, Playwright E2E.

See `docs/03_TECH_STACK.md` for rationale and cost limitations. Free tiers may have quotas; AI usage, compute, storage, and bandwidth can incur costs.

## Repository
```text
AuditForge/
├── AGENTS.md
├── README.md
├── .env.example
└── docs/
    ├── 01_PROJECT_SPECIFICATION.md
    ├── 02_SYSTEM_ARCHITECTURE.md
    ├── 03_TECH_STACK.md
    ├── 04_DESIGN_SYSTEM.md
    ├── 05_UI_UX_SPECIFICATION.md
    ├── 06_DATABASE_SCHEMA.md
    ├── 07_SECURITY_AND_ACCESS_CONTROL.md
    ├── 08_AI_EVIDENCE_PIPELINE.md
    ├── 09_MATERIAL_RECONCILIATION.md
    ├── 10_ANOMALY_DETECTION.md
    ├── 11_API_CONTRACTS.md
    ├── 12_TESTING_AND_VALIDATION.md
    ├── 13_IMPLEMENTATION_PLAN.md
    └── 14_HACKATHON_DEMO.md
```

## Reading order
1. `AGENTS.md`, then `docs/01_PROJECT_SPECIFICATION.md`.
2. `02_SYSTEM_ARCHITECTURE.md` and `03_TECH_STACK.md`.
3. `04_DESIGN_SYSTEM.md` and `05_UI_UX_SPECIFICATION.md`.
4. `06_DATABASE_SCHEMA.md`, `07_SECURITY_AND_ACCESS_CONTROL.md`, `11_API_CONTRACTS.md`.
5. `08_AI_EVIDENCE_PIPELINE.md`, `09_MATERIAL_RECONCILIATION.md`, `10_ANOMALY_DETECTION.md`.
6. `12_TESTING_AND_VALIDATION.md`, `13_IMPLEMENTATION_PLAN.md`, `14_HACKATHON_DEMO.md`.

## Status
This pack is an engineering specification, not a claim that the application has been implemented. The implementation phase must add actual source code, migrations, tests, and verified setup commands. Sample records and illustrative metrics must be clearly labelled as demo data.

## Local setup overview
The exact commands are to be finalized after scaffold and dependency versions are selected. Prerequisites: compatible Node.js and Python runtimes, Git, and a Supabase project or local development setup.
1. Copy `.env.example` to local environment files; never commit populated secrets.
2. Configure Supabase, backend database connectivity, storage buckets, and provider keys as described in the security/deployment docs.
3. Install dependencies using committed lockfiles.
4. Apply versioned migrations.
5. Start FastAPI and Next.js separately, then run unit, integration, authorization, and E2E tests.

Do not invent package scripts before they exist. Keep this README synchronized with actual implementation.

## Security essentials
- Never expose service-role keys, database passwords, AI keys, or signing secrets to browser code.
- Keep evidence/report storage private by default.
- Verify JWTs server-side and authorize every project operation.
- Use RLS for direct database access while retaining backend authorization.
- Treat uploaded files and OCR/VLM output as untrusted.
- Keep reconciliation deterministic and decisions auditable.
