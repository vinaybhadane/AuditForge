"""Evidence correlation and traceability graph."""

from typing import List

from app.audit_engine.contracts.findings import AnomalyFinding
from app.audit_engine.contracts.requests import AuditEngineRequest
from app.audit_engine.contracts.responses import (
    EvidenceCorrelationLink,
    ExtractedRecord,
    ReconciliationResult,
)


def build_evidence_correlation_links(
    request: AuditEngineRequest,
    extracted_records: List[ExtractedRecord],
    reconciliation: ReconciliationResult,
    findings: List[AnomalyFinding],
) -> List[EvidenceCorrelationLink]:
    """Build auditable traceability links across documents, orders, receipts, and findings."""
    links: List[EvidenceCorrelationLink] = []

    # 1. Invoice -> Purchase Order Link
    for rec in extracted_records:
        if rec.document_type == "invoice":
            po_ref = rec.fields.get("po_reference")
            if po_ref and po_ref.normalized_value:
                links.append(
                    EvidenceCorrelationLink(
                        source_type="invoice",
                        source_id=str(rec.document_number or rec.evidence_id),
                        target_type="purchase_order",
                        target_id=str(po_ref.normalized_value),
                        relationship="references_purchase_order",
                        rationale=f"Invoice cites purchase order reference '{po_ref.normalized_value}'.",
                    )
                )

    # 2. Challan -> Purchase Order & Receipt Links
    for ch in request.delivery_challans:
        if ch.po_number:
            links.append(
                EvidenceCorrelationLink(
                    source_type="delivery_challan",
                    source_id=ch.challan_number,
                    target_type="purchase_order",
                    target_id=ch.po_number,
                    relationship="fulfills_order",
                    rationale=f"Challan references PO '{ch.po_number}'.",
                )
            )

    for r in request.goods_receipts:
        if r.challan_number:
            links.append(
                EvidenceCorrelationLink(
                    source_type="goods_receipt",
                    source_id=r.receipt_number,
                    target_type="delivery_challan",
                    target_id=r.challan_number,
                    relationship="verifies_delivery",
                    rationale=f"Goods receipt acknowledges delivery of challan '{r.challan_number}'.",
                )
            )

    # 3. Finding -> Evidence & Subject Links
    for f in findings:
        for ev_id in f.evidence_refs:
            links.append(
                EvidenceCorrelationLink(
                    source_type="anomaly_finding",
                    source_id=str(f.id),
                    target_type="evidence_asset",
                    target_id=str(ev_id),
                    relationship="supported_by_evidence",
                    rationale=f"Finding '{f.title}' cites evidence '{ev_id}'.",
                )
            )

    return links
