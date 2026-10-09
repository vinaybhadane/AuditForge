# 04 — Design System

## Brand character
AuditForge should feel precise, trustworthy, engineered, calm, and premium. Avoid cartoon construction graphics, excessive gradients, neon dashboards, random glassmorphism, and generic AI-template styling. Visual design should reinforce traceability and accountable decisions.

## Initial color tokens
| Token | Hex | Use |
|---|---|---|
| `brand-950` | `#101B2D` | Deep hero/nav surfaces |
| `brand-800` | `#1C3555` | Headings/navigation |
| `brand-700` | `#24527A` | Primary actions |
| `brand-600` | `#2D6FA3` | Links/focus accents |
| `signal-amber` | `#E9A23B` | Construction accent/pending review |
| `signal-teal` | `#1C8C83` | Verified state where semantically valid |
| `danger-700` | `#B42318` | Critical discrepancy/destructive action |
| `warning-700` | `#9A6700` | Warning/review needed |
| `success-700` | `#18794E` | Approved state |
| `surface-0` | `#FFFFFF` | Primary surface |
| `surface-50` | `#F7F9FC` | Page background |
| `surface-100` | `#EEF2F7` | Secondary surface |
| `border` | `#D7DEE8` | Dividers |
| `text-primary` | `#172334` | Main text |
| `text-secondary` | `#536276` | Supporting text |

These are starting tokens; validate rendered contrast against WCAG AA. Never communicate state by color alone: include text and/or icon. Dark theme is optional and must not delay accessible core flows.

## Typography and spacing
Use a legible modern sans-serif with system fallback. Initial hierarchy: hero 48–72 px desktop with responsive clamp; page title 28–36 px; section title 20–24 px; body 14–16 px; dense table body 13–14 px only if still readable; metadata 12–13 px after contrast check. Use tabular numerals for quantities, money, and dates. Base spacing scale is 4 px: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80.

## Surfaces and components
- Cards: 12–16 px radius, subtle border, restrained shadow.
- Inputs/buttons: 8–10 px radius, clear hover/pressed/disabled states, visible focus.
- Primary action: one dominant action per context. Destructive actions require confirmation.
- Forms: visible labels, helper text, field errors, summary errors for complex forms, preserve input after recoverable errors.
- Tables: useful sorting, explicit empty/loading/error states, pagination, accessible row actions; mobile layout must retain access to all important fields.
- Live Capture Viewfinder (site progress photos): camera viewport with environment/rear stream default, real-time capture trigger, retake/confirm dialog, permission failure state, and live capture telemetry indicators (capture timestamp, optional location accuracy badge). Pre-existing image file upload is disabled for site evidence to enforce presence and freshness.
- Document Intake Interface (invoices, challans, receipts): dual-mode modal/panel featuring "Upload File" (drag-and-drop for PDF/images) and "Camera Scan" (in-app live document capture for physical slips).
- Evidence viewer: evidence ID, ingestion mode badge (`Live Capture` vs `File Upload`), file type, submitter/capture timestamp, checksum status, metadata caveats, milestone link, processing state, AI observations, extracted fields, version history, and authorized download action.
- Charts: state period, units, source, interpretation; avoid 3D charts and misleading axes; never fabricate empty-state metrics.

## Status language
| Status | UI wording |
|---|---|
| AI-generated | “AI observation — review required” |
| Verified/approved | “Verified” / “Approved” only after defined process |
| Pending | “Queued”, “Pending review”, etc. |
| Inconclusive | Explain what is missing or uncertain |
| Discrepancy | Show calculation and evidence links |
| Failed | Safe reason and recovery action |

Never use “fraud detected” as a generic anomaly label. Severity is review priority, not probability of wrongdoing.

## Motion and 3D art direction
Core UI transitions are short and purposeful. Honor `prefers-reduced-motion`; never delay critical actions for animation. The landing scene should show a plausible multi-storey structure, tower crane, structural grid, restrained construction materials, cinematic but legible lighting, and subtle verification motifs. Place copy over a readable overlay. Avoid fake claims/metrics and visually impossible scene geometry where practical.

## Accessibility and responsive design
Target WCAG AA contrast; keyboard navigation; visible focus; semantic headings/landmarks; labels and accessible names; announced async statuses; text alternatives for charts and 3D. Provide reduced-motion and WebGL fallback. Verify narrow mobile, large mobile, tablet, laptop, and wide desktop. Dashboard sidebar may become a drawer; tables may scroll or become record cards but must not hide critical fields.

## Acceptance checklist
- Homepage is cinematic but navigation remains usable without WebGL.
- App pages are calm, efficient, and consistent.
- AI observations cannot be mistaken for verified facts.
- Error, empty, loading, permission, and inconclusive states exist.
- Keyboard focus and contrast are visible.
- No chart presents invented data as live project results.
