# 03 — Technology Stack

## Selection principles
Choose a small, maintainable stack for a hackathon MVP with a credible growth path. “Free” does not mean unlimited: hosting, compute, storage, bandwidth, logging, and model calls may have quotas or charges. Pin compatible versions and commit lockfiles during implementation; do not pretend a package is installed before scaffold.

## Frontend
**Next.js App Router + React + strict TypeScript:** routing, server rendering, layouts, and route-level code splitting. Server components by default; client components only for browser interactions. FastAPI remains the domain backend. React + Vite is an alternative but would need more separately configured routing/server rendering.

**Tailwind CSS + accessible primitives:** design tokens and responsive layout; use shadcn/ui or an equivalent selectively. Copied component source still needs maintenance/accessibility checks. Avoid overlapping component libraries.

**React Hook Form + Zod:** form ergonomics and early validation; backend validation remains authoritative. **TanStack Query:** use where async server state, polling, caching, and invalidation justify it. **Recharts or equivalent:** accessible charts with labels, textual interpretation, and empty states.

## 3D homepage only
**Three.js + React Three Fiber + Drei:** use exclusively on `/`, isolated in a client-only dynamically imported component. Provide WebGL fallback, reduced motion, mobile geometry/texture budgets, lazy assets, and no unnecessary post-processing. Verify dashboard/auth bundles do not include the scene. A static illustration is fallback, not the default experience.

## Backend
**Python + FastAPI + Pydantic:** typed HTTP API, validation, OpenAPI, dependency injection. Async syntax does not make CPU-heavy OCR nonblocking; use worker processes for long tasks.

**SQLAlchemy 2.x + Alembic:** relational data access and recorded migrations. Keep route handlers thin, domain services testable, and transactions explicit.

**Background processing:** MVP may use a database-backed job table plus separate worker with safe atomic claiming, bounded retries, and idempotent writes. Celery + Redis is a scaling option, not a mandatory dependency. Persist job status in PostgreSQL in either case.

## Database, auth, and storage
**Supabase Auth:** identity/session provider; backend verifies tokens. Authentication does not grant project authorization.

**Supabase PostgreSQL:** authoritative operational data, constraints, indexes, snapshots, and audit history. Use RLS for any direct browser access, while retaining backend authorization.

**Supabase Storage or equivalent private object storage:** evidence and reports. Private buckets, validated uploads, safe object keys, and short-lived signed URLs are required. Check current plan limits and retention/provider terms before deployment.

## AI and document processing
**VLM adapter:** a provider such as Google Gemini can produce candidate visual observations against explicit criteria. Keep provider-specific code behind an interface; record model ID/prompt/schema versions; bound timeout, payload, retry, and cost. No provider output directly approves a milestone.

**OCR:** evaluate PaddleOCR and Tesseract against representative documents. Prefer native PDF text extraction when usable, OCR for scanned pages. PaddleOCR can require heavier runtime resources; Tesseract may need more preprocessing. Choose based on measured field accuracy and deployment constraints, not assumption.

**Pillow/OpenCV/PDF parser:** decoding, orientation, resizing, quality checks, and PDF extraction. These parsers are attack surface; enforce byte/page/pixel limits and isolate workers.

**Pandas/statistical tools:** useful for analysis but not a substitute for domain validation. Statistical anomaly models are optional and require representative historical data; deterministic rules are MVP foundation.

## Testing and quality
Pytest; a compatible frontend unit/component test runner; Playwright E2E; TypeScript strict checks; ESLint/formatting; Python lint/format/type checks; migration tests; dependency and secret scans where available. Exact tools and versions are chosen at scaffold and recorded in lockfiles.

## Cost and complexity controls
Set maximum file/model payload sizes, per-user/project rate limits, bounded retries, and usage monitoring. A clearly labeled demo fixture may be used if a provider is unavailable, but never silently display fake analysis as live AI. Avoid Kubernetes, microservices, Kafka, vector databases, blockchain, or bespoke model training until a measured need exists.
