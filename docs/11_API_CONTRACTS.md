# 11 — API Contracts

## Conventions
Base path `/api/v1`; JSON UTF-8; IDs UUID; timestamps ISO-8601 UTC. Serialize high-precision quantities/money as decimal strings where needed and use the same convention everywhere. Lists use bounded pagination. Every protected endpoint authenticates and authorizes server-side.

## Error envelope
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request could not be processed.",
    "request_id": "correlation-id",
    "details": [{"field": "quantity", "code": "MUST_BE_POSITIVE"}]
  }
}
```
Do not expose private records or internal exceptions in `details`. Status mapping: 400 malformed request; 401 invalid/missing token; 403 forbidden; 404 absent/concealed resource; 409 state/idempotency conflict; 413 too large; 415 unsupported media; 422 schema/domain validation; 429 rate limit; 500 generic failure; 502/503 dependency/provider unavailable.

## Endpoint catalogue
| Method/path | Purpose | Minimum authorization |
|---|---|---|
| `GET /health/live` | Process liveness | Public/infrastructure-restricted |
| `GET /health/ready` | Dependency readiness | Infrastructure-restricted, safe output |
| `GET /me` | Verified profile and memberships | Authenticated |
| `GET,POST /organizations` | List/create per onboarding policy | Authenticated/eligible creator |
| `GET,PATCH /organizations/{id}` | Organization detail/update | Member/admin as defined |
| `GET,POST /organizations/{id}/members` | List/invite members | Org admin for writes |
| `PATCH /organizations/{id}/members/{membership_id}` | Change membership/role | Org admin |
| `GET,POST /projects` | List/create accessible projects | Project manager/admin for create |
| `GET,PATCH /projects/{project_id}` | Project detail/update | Assigned member/write permission |
| `GET,POST /projects/{project_id}/milestones` | List/create milestones | Read/baseline editor |
| `GET,PATCH /milestones/{milestone_id}` | Milestone detail/update | Project-scoped permission |
| `GET,POST /projects/{project_id}/boq-items` | List/create BOQ | Read/baseline editor |
| `PATCH /boq-items/{boq_item_id}` | Edit baseline item | Explicit baseline permission |
| `POST /projects/{project_id}/evidence/uploads` | Initiate secure upload | Evidence uploader |
| `POST /evidence/{id}/complete-upload` | Verify upload and queue processing | Uploader/permitted operator |
| `GET /projects/{project_id}/evidence` | List evidence | Project read |
| `GET /evidence/{id}` | Evidence metadata/results | Project read |
| `POST /evidence/{id}/process` | Queue/reprocess | Allowed operator, idempotent |
| `GET /jobs/{job_id}` | Processing status | Same tenant/project access |
| `GET /projects/{project_id}/documents` | List documents | Project read |
| `GET /documents/{id}` | Document and fields | Project read |
| `POST /documents/{id}/fields/{field_name}/corrections` | Versioned field correction | Correction permission |
| `GET,POST /projects/{id}/inventory/receipts` | List/create receipts | Store In-Charge or explicit grant |
| `GET,POST /projects/{id}/inventory/issues` | List/create issues | Store In-Charge or explicit grant |
| `POST /projects/{id}/reconciliations` | Start reconciliation | Auditor/authorized manager |
| `GET /reconciliations/{run_id}` | Immutable run and lines | Project read |
| `GET /projects/{id}/findings` | List findings | Project read |
| `GET /findings/{id}` | Finding detail | Project read |
| `POST /projects/{id}/investigations` | Open investigation | Auditor/authorized role |
| `GET,PATCH /investigations/{id}` | Read/update case | Assigned investigator/role |
| `POST /investigations/{id}/findings` | Link finding with rationale | Investigation editor |
| `POST /milestones/{id}/review-decisions` | Record human decision | Designated reviewer |
| `GET /milestones/{id}/clearance-eligibility` | Explain blockers | Project read, scoped detail |
| `POST /milestones/{id}/certificates` | Issue after eligibility checks | Designated approver only |
| `GET /certificates/{id}` | Certificate metadata | Authorized project user |
| `GET /certificates/{id}/download` | Short-lived download/stream | Authorized user |
| `GET /projects/{id}/audit-events` | Audit history | Audit permission |

## Representative requests
### Create project — `POST /api/v1/projects`
```json
{
  "organization_id": "uuid",
  "name": "Demo Residential Block",
  "project_code": "DEMO-001",
  "timezone": "Asia/Kolkata",
  "currency_code": "INR",
  "planned_start_date": "2026-10-01",
  "planned_end_date": null
}
```
Return `201` with project ID, organization, name/code, status, baseline version, timestamps. Verify actor can create in that organization.

### Initiate upload — `POST /api/v1/projects/{project_id}/evidence/uploads`
```json
{
  "filename": "column-work.jpg",
  "declared_content_type": "image/jpeg",
  "size_bytes": 2481200,
  "evidence_type": "site_photo",
  "milestone_id": "uuid",
  "source_notes": "North-east columns, inspection visit"
}
```
Return `201` with evidence ID, short-lived upload instructions, required headers, expiry, and `upload_status: initiated`. URL is secret-like; do not log it. Server generates the object key and ignores client storage paths.

### Job status — `GET /api/v1/jobs/{job_id}`
```json
{
  "id": "uuid", "status": "running", "job_type": "visual_assessment",
  "attempt_count": 1, "created_at": "2026-10-09T06:00:00Z",
  "started_at": "2026-10-09T06:00:03Z", "finished_at": null,
  "error": null, "result_available": false
}
```
Do not expose raw prompts or provider internals.

### Start reconciliation — `POST /api/v1/projects/{project_id}/reconciliations`
```json
{
  "period_start": "2026-10-01T00:00:00Z",
  "period_end": "2026-10-08T23:59:59Z",
  "baseline_version_id": "uuid",
  "scope": {"material_ids": [], "location_ids": []},
  "idempotency_key": "unique-client-key"
}
```
Return `202` with run ID/status. Capture a versioned input snapshot; do not mutate prior runs.

### Record review — `POST /api/v1/milestones/{milestone_id}/review-decisions`
```json
{
  "decision_type": "request_evidence",
  "reason": "The required east-side inspection viewpoint is missing.",
  "referenced_finding_ids": ["uuid"],
  "criteria_version": 2
}
```
Server checks reviewer permission, state, criteria version, and referenced record scope. Actor/time come from verified session, not request body.

### Issue certificate — `POST /api/v1/milestones/{milestone_id}/certificates`
```json
{
  "review_decision_id": "uuid",
  "report_format": "pdf",
  "idempotency_key": "unique-key"
}
```
Re-evaluate eligibility, verify authorized approval, snapshot evidence/reconciliation references, and reject with `CLEARANCE_BLOCKED` when blockers exist. Rendering may be asynchronous (`202`). Never trust client `approved: true`.

## Pagination, idempotency, concurrency
Use bounded `limit` (for example maximum 100) and stable/opaque cursors for changing datasets. Allowlist sort fields; never interpolate arbitrary SQL order clauses. Large exports are jobs. Bind idempotency keys to actor/scope/request hash; same key with different payload returns conflict. Use optimistic concurrency for baseline/review state changes.

## Error codes and contract testing
Use stable codes: `AUTH_REQUIRED`, `FORBIDDEN`, `RESOURCE_NOT_FOUND`, `VALIDATION_ERROR`, `STATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `UNSUPPORTED_MEDIA_TYPE`, `PAYLOAD_TOO_LARGE`, `RATE_LIMITED`, `PROVIDER_UNAVAILABLE`, `PROCESSING_FAILED`, `CLEARANCE_BLOCKED`, `INTERNAL_ERROR`. Generated OpenAPI must match semantics. Test required fields, status codes, authorization, errors, decimal serialization, pagination bounds, idempotency, and version conflicts. Update this document and tests together.
