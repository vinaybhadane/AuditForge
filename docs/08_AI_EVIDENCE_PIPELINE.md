# 08 — AI Evidence Pipeline

## Purpose and trust model
The pipeline converts source evidence into structured, reviewable candidate observations. It does not autonomously determine fraud, legal liability, exact physical completion, or clearance. Deterministic business rules remain authoritative for arithmetic and eligibility.

## Pipeline stages
1. **Ingestion & modality validation:** authenticate, authorize, check modality constraints (site progress photos must originate from authenticated live camera capture; vendor documents accept direct file upload or live camera scan), check media type/size/signature, store privately.
2. **Registration:** assign evidence ID, object key, hash, ingestion mode (`live_capture` vs `file_upload`), capture telemetry (device capture timestamp, optional geolocation), submitter, project/milestone, timestamps.
3. **Classification:** live site photo frame, digital PDF document, scanned invoice/challan/receipt image, PO, or unknown.
4. **Quality:** corrupt/blurred/low-resolution image, blank/unreadable PDF, excessive pages/pixels.
5. **Duplicate checks:** exact hash; optional perceptual similarity candidate. Similarity is not proof of fraud.
6. **Extraction:** native PDF text where usable, OCR fallback for scanned pages, bounded metadata extraction.
7. **Structured parsing:** candidate fields with page/source spans where possible.
8. **Visual assessment:** compare visible features to explicit milestone criteria.
9. **Normalization:** map materials, units, dates, vendors, and identifiers while preserving raw values.
10. **Deterministic validation:** arithmetic, references, allowed units, duplicate IDs, required fields.
11. **Reconciliation:** calculate supported quantity/financial relationships from versioned snapshots.
12. **Anomaly detection:** deterministic rules first; statistical methods only if justified.
13. **Correlation:** link findings through explicit project/milestone/vendor/material/transaction relationships.
14. **Human review:** confirm, correct, request evidence/inspection, hold, reject, dismiss with reasons.
15. **Audit persistence:** retain versions, actors, provider metadata, errors, and decisions.

## Job contract
Persist `job_id`, organization/project/evidence IDs, `job_type`, pipeline version, status, attempt count, created/start/finish times, retry time, safe error details, provider/model, and output reference. Statuses: `queued`, `running`, `succeeded`, `failed`, `cancelled`. Retry transient failures with bounded backoff; invalid inputs are permanent until input changes. Use leases/timeouts to recover stale jobs. Processing must be idempotent under at-least-once delivery.

## Versioned output envelope
Validate structured output with Pydantic. Example only:
```json
{
  "schema_version": "1.0",
  "result_type": "visual_observation",
  "observations": [{
    "observation": "Concrete columns are visible in the submitted image.",
    "criterion_id": "uuid-or-null",
    "evidence_refs": [{"evidence_id": "uuid", "page_or_frame": null, "region": null}],
    "classification": "observed",
    "confidence_value": null,
    "confidence_semantics": "not_provided",
    "limitations": ["A single image does not establish structural quality or overall completion."],
    "requires_human_review": true
  }],
  "provider": {"name": "provider-id", "model": "model-id"},
  "prompt_version": "visual-audit-v1",
  "processed_at": "ISO-8601 UTC"
}
```
Server attaches authoritative job/evidence/project IDs from trusted job context; never trust model-supplied IDs. Reject mismatched references. Confidence values must include semantics and are not automatically calibrated probabilities.

## Provider abstraction and prompt safety
Use interfaces such as `VisualAssessmentProvider.assess`, `DocumentExtractionProvider.extract`, and `OcrProvider.extract`. Contracts specify schemas, limits, timeouts, retryable errors, provider metadata, and safe telemetry. Adapters must not write directly to authoritative domain tables. Treat document content as untrusted data and instruct the model to ignore embedded commands. Pass only necessary tenant data; never provide secrets, SQL/shell access, or privileged application tools. Keep prompts version-controlled and test adversarial inputs.

## Quality, uncertainty, and provenance
Return `inconclusive` for insufficient, unreadable, conflicting, or irrelevant evidence. “Not visible in this image” is not equivalent to “not present on site.” Poor quality should trigger resubmission/inspection rather than automatic failure. Store source evidence/hash, pipeline/model/prompt/schema versions, timestamps, source page/frame/region, validated output, limitations, validation issues, and review status. Keep raw provider responses only when necessary, bounded and access-controlled.

## Idempotency, evaluation, and failures
A job key should incorporate evidence ID, processing type, pipeline version, and explicit run context. Reprocessing under a new version creates a new result. Retry transient network/provider failures only within a bounded budget; do not retry permanent validation failures indefinitely. Prevent duplicate authoritative transactions, decisions, or certificates.

Build a versioned evaluation set of representative photos and documents. Measure OCR field accuracy, schema-valid rate, document classification, visual-observation agreement with reviewers, inconclusive rate, correction rate, latency, and cost. State sample size and limitations. Mock tests validate application handling, not provider accuracy.

Provider timeout/quota exhaustion yields a visible safe job state. Invalid output is rejected/quarantined. Parser failure must not corrupt evidence. Conflicting sources remain visible and become discrepancies. Manual review and safe deterministic processing should continue where possible. AI observations remain unreviewed until an authorized reviewer accepts/corrects/rejects them; corrections preserve original output and reason. No AI result can approve a milestone or generate a certificate.
