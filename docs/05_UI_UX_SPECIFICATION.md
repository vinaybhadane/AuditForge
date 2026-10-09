# 05 — UI/UX Specification

## Experience architecture
There are two deliberately different experiences: (1) `/` is an interactive cinematic 3D construction-site homepage; (2) every operational page is a conventional responsive SaaS interface. Three.js must not load on auth/dashboard routes. All project/evidence/financial records require authentication and project authorization.

## Application shell
Desktop: collapsible sidebar, top bar, organization/project context selector when needed, authorized search, user menu, breadcrumbs, main content. Mobile: top bar and accessible navigation drawer. Suggested groups: Overview (Dashboard); Project controls (Projects, Milestones, BOQ); Evidence (Evidence, Documents); Materials (Inventory, Reconciliation); Audit (Investigations, Certificates, Reports); Administration (Members, Settings, permission-dependent). Navigation hiding is for usability only; API authorization remains mandatory.

## Public homepage `/`
Content order: header and brand; hero with value proposition and primary/secondary CTA; “Capture → Verify → Reconcile → Review” workflow strip; visual verification; document intelligence; material reconciliation; human review; final CTA/footer. Do not show fake partner logos, fabricated savings, unmeasured accuracy, or nonfunctional links.

The 3D scene should show a plausible multi-storey building, tower crane, columns/floors/scaffolding/materials, restrained cinematic lighting, and subtle verification motifs. Camera movement is controlled; scroll transitions must not hijack scrolling. Use a client-only dynamic import, loading poster/skeleton, static WebGL fallback, reduced-motion support, mobile scene simplification, bounded geometry/textures, and keyboard-accessible HTML controls. CTAs must work without waiting for the scene.

**Acceptance:** `/login` and `/dashboard` do not download the scene chunk; WebGL-disabled mode preserves all copy/navigation; reduced-motion disables nonessential camera motion; scene failure does not break CTA links.

## Login and session behavior
Show supported Supabase sign-in options, loading/errors, accessible labels, session expiry behavior, and password recovery only if configured. If invitation-only membership is selected, do not expose public signup. Redirect only to a safe internal destination to prevent open redirects. A user with no organization/project access sees a helpful empty/onboarding state.

## Dashboard
Show metrics only from real authorized queries: active projects, milestones awaiting review, open findings, failed processing jobs, reconciliation runs needing attention. Empty datasets show “No data yet.” Every metric links to filtered records and indicates scope/time range. States: loading, no projects, forbidden, API failure/retry, populated, stale. Do not show an unexplained risk score or fabricated data.

## Projects
List search/status/owner filters and bounded pagination. Detail tabs: overview, milestones, BOQ, evidence, inventory/reconciliation, investigations, members (permission-dependent), activity. Validate organization ownership, date order, timezone, and currency. Show baseline version and changes. Baseline/criteria/BOQ changes after a run create a new version; historical runs must not be silently rewritten.

## Milestones and acceptance criteria
List identifier, name, planned dates, status, evidence count, open findings, and review state. Detail includes versioned criteria, linked BOQ, evidence, AI observations, findings, timeline, and permitted review actions. Never infer completion percentage from photo count or uncalibrated VLM output. Required/optional/not-applicable criteria must follow documented policy.

## Evidence workspace
Filters: project, milestone, type, uploader, date, processing status, review state. Detail: source file, evidence ID, hash, upload metadata, claimed capture metadata, version, processing history, extracted fields, AI observations, linked findings, audit timeline. Clearly label uploader-supplied versus file-derived metadata. Upload flow: select project/milestone, select file, add context, validate type/size, upload with progress, confirm storage, show processing state. Failed uploads retain recoverable state. Exact hash duplicates differ from perceptual-similarity candidates.

## Documents and extraction review
Show original preview/download, extracted candidate fields, source page/span, uncertainty/confidence semantics, validation issues, and correction controls. Corrections preserve the original extraction and record reviewer, timestamp, reason, and version. Uncertain financial fields cannot silently feed authoritative reconciliation.

## Inventory and reconciliation
Differentiate receipts, issues, returns, adjustments, transfers, and stock snapshots. Show source document, material, raw and canonical units, quantities, effective date, creator, and approval state. Reconciliation requires explicit project, period, baseline version, input snapshot, and rule version. Each result shows formula, inputs, expected/observed values, delta, tolerance, status, and source links. Missing inputs yield `inconclusive`, not fabricated zeroes.

## Findings and investigations
Finding detail states rule, inputs, calculation, severity, evidence, limitations, and recommended next step. Never call an anomaly proof of fraud. Investigation links require a rationale; temporal proximity alone is not causality. Preserve finding history when dismissed/resolved.

## Human review and certificates
Review panel combines criteria, source evidence, extraction fields, reconciliation snapshots, findings, and unresolved blockers. Actions: approve, request evidence, request inspection, hold, reject, escalate—only if authorized. Consequential decisions require a reason. Disable clearance with explicit blockers. Certificate preview includes project/milestone, authorized decision, approver, timestamp, evidence/report version, certificate ID, and verification method. AI output alone cannot issue a certificate.

## Settings and shared states
Member changes are audited. Settings may configure organization, project defaults, unit/material mappings, and notification preferences. Never display secrets; show configured/not configured only. Every data page needs loading, empty, error, unauthorized, and success states. Forms have labels and server error handling; long jobs remain inspectable after navigation; toasts supplement persistent state. Display local/project timezones while storing UTC. Do not send document contents or signed URLs to analytics by default.
