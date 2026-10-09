# 07 — Security and Access Control

## Objectives and trust model
Protect tenant isolation, evidence confidentiality, quantity/financial integrity, review authority, secrets, and audit history. Assume browser requests, uploads, OCR/VLM output, and external responses may be malicious or wrong.

## Identity versus authorization
Supabase Auth establishes identity; FastAPI must cryptographically verify token signature, expiry, issuer, and applicable audience/claims using a supported method. Never merely decode a JWT. Then resolve active organization membership and project assignment from trusted records. Client-supplied roles and organization/project IDs are requests, not proof of access. Every protected route—including list, detail, preview, download, correction, review, and certificate actions—must authorize server-side. Apply scope before filtering/pagination. Use consistent 403/404 policy to avoid leaking resource existence.

## Role/permission baseline
| Action | Supervisor | Store In-Charge | Auditor | Project Manager | Org Admin |
|---|---|---|---|---|---|
| View assigned project | Yes | Yes | Yes | Yes | Organization scope |
| Upload milestone evidence | Yes | Contextual | If assigned | If assigned | Not automatically |
| Submit receipts/issues | No by default | Yes | Review/read | Explicit grant | Not automatically |
| Edit baseline/BOQ | No | No | Review only by default | Explicit grant | Policy-dependent |
| Run reconciliation | Read results | Limited | Yes | Explicit grant | Not automatically |
| Review findings | Respond to requests | Respond to inventory requests | Yes | Explicit grant | Not automatically |
| Approve clearance | No by default | No | If designated | If designated | Not automatically |
| Manage membership | No | No | No | No by default | Yes |

This is a safe default, not a universal legal policy. Implement explicit permissions; role names alone must not accidentally grant clearance authority.

## RLS and database access
Use RLS on tables accessible from the browser. Define SELECT/INSERT/UPDATE/DELETE policies separately. Derive access through authenticated identity and membership relations, never a caller-provided organization ID. Test two organizations and nested child resources. A privileged service-role connection may bypass RLS; FastAPI must still authorize every action and use least-privileged DB access where possible. Never expose a service-role key in browser code or `NEXT_PUBLIC_` variables.

## Evidence storage
Private buckets by default. Use random object keys and treat original filenames as display metadata only. Validate extension, declared/detected MIME, file signature, size, and parser result. Enforce page/pixel/expanded-size limits. Issue short-lived signed URLs only after authorization and never log full URLs. Reauthorize downloads/previews/certificates. Clean up abandoned uploads safely.

## AI/document threats
Uploaded content may contain prompt injection, hidden text, malicious links, or malformed structures. OCR/VLM output is data, not instructions. Models must not invoke privileged tools, execute SQL, alter roles, or issue certificates. Validate model output strictly. Do not automatically fetch URLs found in documents. If URL ingestion is added later, require DNS/IP validation, redirect restrictions, private-address blocking, egress controls, timeouts, allowlists where practical, and size limits to mitigate SSRF.

## API and secret controls
Use TLS, strict CORS allowlist, rate limits for uploads/AI/report generation, body-size limits, Pydantic validation, parameterized SQL, stable safe errors, correlation IDs, idempotency keys, open-redirect protection, secure cookie flags/CSRF controls where applicable, and security headers. Keep secrets in deployment secret stores; `.env.example` contains placeholders only. Rotate leaked keys immediately.

## Audit trail
Record actor, action, target, timestamp, request ID, outcome, and safe metadata for baseline edits, field corrections, membership changes, reconciliations, decisions, and certificates. Never log tokens, passwords, API keys, signed URLs, or complete documents. Make audit events append-only to normal application roles. A database table alone is not cryptographic proof of immutability; stronger tamper evidence may require restricted operations and external log export.

## Threat/control/test matrix
| Threat | Control | Test |
|---|---|---|
| Cross-tenant IDOR | Membership/project checks on every record | User A guesses User B IDs; no data returned |
| Role escalation | Server derives role from membership | Request body says `role=admin`; ignored/rejected |
| Malicious upload | Signature/type/size checks, restricted parsing | MIME spoof, oversized file, malformed PDF rejected safely |
| Prompt injection | Untrusted-content prompt, no privileged tools, schema validation | “Ignore rules” document cannot change permissions/domain state |
| SQL injection | ORM/parameterized queries | Adversarial input treated as data |
| Secret leakage | Secret scan, server-only env, log redaction | Build/log scan finds no secrets |
| Signed URL leak | Short expiry, no logging, authorization before issue | Expired URL fails; other tenant cannot obtain URL |
| Replay/duplicate | Idempotency and uniqueness constraints | Repeated request does not duplicate movement/certificate |
| Provider outage | Timeout/retry budget/safe failure | Timeout creates visible retryable job |
| False accusation | Cautious finding semantics and review | UI never equates score with proven fraud |
| Unauthorized certificate | Eligibility service and reviewer authorization | Non-approver cannot issue certificate |

## Incident response and release gate
Runbooks should cover credential leak, tenant exposure, storage exposure, provider compromise, and corrupted reconciliation. Rotate/revoke credentials, restrict access, preserve safe logs, assess impact, notify responsible owners under applicable policy, and restore from verified backups. Do not claim regulatory compliance without review. Release only after tenant isolation, role, upload, RLS, secret, and certificate authorization tests pass; disclose unresolved risks.
