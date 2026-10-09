"""Synthetic demo fixtures for Northstar Residential Block demonstration."""

from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.audit_engine.contracts.evidence import (
    CaptureTelemetry,
    EvidencePayload,
    EvidenceType,
    IngestionSource,
)
from app.audit_engine.contracts.requests import (
    AcceptanceCriterion,
    AnalysisOptions,
    AuditEngineRequest,
    BOQItemPayload,
    ChallanLineItem,
    DeliveryChallanPayload,
    GoodsReceiptLineItem,
    GoodsReceiptPayload,
    POLineItem,
    PurchaseOrderPayload,
    StockMovementPayload,
)

# Demo Project Constants
DEMO_PROJECT_ID = UUID("11111111-1111-1111-1111-111111111111")
DEMO_MILESTONE_ID = UUID("22222222-2222-2222-2222-222222222222")


def build_synthetic_demo_request() -> AuditEngineRequest:
    """Build the canonical Northstar Residential Block hackathon demo scenario (docs/14_HACKATHON_DEMO.md).
    
    Worked example:
    - Opening stock: 100 bags cement
    - Receipts: 80 bags
    - Issues: 120 bags
    - Returns: 5 bags
    - Approved adjustment: +2 bags
    - Expected closing stock: 100 + 80 - 120 + 5 + 2 = 67 bags
    - Physical count: 60 bags -> Discrepancy of -7 bags
    
    Also includes:
    - 1 invoice with total arithmetic discrepancy
    - 1 delivery challan with partial receipt mismatch
    - 1 live camera captured site photo
    """
    job_id = uuid4()
    site_photo_id = uuid4()
    invoice_id = uuid4()
    challan_id = uuid4()

    # Milestone Criteria
    criteria = [
        AcceptanceCriterion(
            criterion_id=uuid4(),
            criterion_code="CRIT-COL-01",
            description="Level 2 structural columns cast and concrete formwork stripped.",
            required_evidence_type="site_photo",
        ),
        AcceptanceCriterion(
            criterion_id=uuid4(),
            criterion_code="CRIT-COL-02",
            description="Rebar starter bars visible for Level 3 slab tie-in.",
            required_evidence_type="site_photo",
        ),
    ]

    # Minimal valid 1x1 JPEG byte stream for photo fixture with capture telemetry
    synthetic_jpeg = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xbf\x00\xff\xd9"

    evidence_items = [
        # 1. Site Progress Photo (strictly live camera capture)
        EvidencePayload(
            evidence_id=site_photo_id,
            evidence_type=EvidenceType.SITE_PHOTO,
            ingestion_source=IngestionSource.LIVE_CAPTURE,
            filename="site_level2_columns.jpg",
            declared_content_type="image/jpeg",
            content_bytes=synthetic_jpeg,
            size_bytes=len(synthetic_jpeg),
            capture_telemetry=CaptureTelemetry(
                captured_at=datetime.now(timezone.utc),
                device_client="AuditForge Web Viewfinder v1",
                camera_facing="environment",
                latitude=19.0760,
                longitude=72.8777,
                accuracy_meters=8.5,
            ),
            source_notes="North-east structural column inspection live capture",
        ),
        # 2. Vendor Invoice (PDF file upload)
        EvidencePayload(
            evidence_id=invoice_id,
            evidence_type=EvidenceType.INVOICE,
            ingestion_source=IngestionSource.FILE_UPLOAD,
            filename="invoice_inv_1092.pdf",
            declared_content_type="application/pdf",
            content_bytes=b"%PDF-1.4\n1 0 obj\n<< /Length 120 >>\nstream\n(Invoice No: INV-1092\nVendor: Ultratech Cement Ltd\nDate: 2026-10-02\nPO Ref: PO-2026-088\nOPC 53 Cement - 100 bags @ 380 = 38000\nTotal Amount: 38000) Tj\nendstream\nendobj\n",
            size_bytes=240,
        ),
        # 3. Delivery Challan (physical paper live camera scan)
        EvidencePayload(
            evidence_id=challan_id,
            evidence_type=EvidenceType.DELIVERY_CHALLAN,
            ingestion_source=IngestionSource.LIVE_CAPTURE,
            filename="challan_ch_440.pdf",
            declared_content_type="application/pdf",
            content_bytes=b"%PDF-1.4\n1 0 obj\n<< /Length 120 >>\nstream\n(Challan No: DC-440\nVendor: Ultratech Cement Ltd\nDate: 2026-10-03\nPO Ref: PO-2026-088\nOPC 53 Grade Cement - 80 bags) Tj\nendstream\nendobj\n",
            size_bytes=230,
            capture_telemetry=CaptureTelemetry(
                captured_at=datetime.now(timezone.utc),
                device_client="AuditForge Document Scanner v1",
            ),
        ),
    ]

    # Purchase Order (200 bags ordered)
    pos = [
        PurchaseOrderPayload(
            po_id=uuid4(),
            po_number="PO-2026-088",
            vendor_name="Ultratech Cement Ltd",
            lines=[
                POLineItem(
                    material_code="CEMENT-OPC-53",
                    description="OPC 53 Grade Cement",
                    ordered_quantity=Decimal("200"),
                    unit="bag",
                    unit_price=Decimal("380.00"),
                    line_total=Decimal("76000.00"),
                )
            ],
        )
    ]

    # Delivery Challan (states 80 bags dispatched)
    challans = [
        DeliveryChallanPayload(
            challan_id=challan_id,
            challan_number="DC-440",
            po_number="PO-2026-088",
            vendor_name="Ultratech Cement Ltd",
            lines=[
                ChallanLineItem(
                    material_code="CEMENT-OPC-53",
                    description="OPC 53 Grade Cement",
                    challaned_quantity=Decimal("80"),
                    unit="bag",
                )
            ],
        )
    ]

    # Goods Receipts (only 75 bags accepted into physical store -> 5 bag delta)
    receipts = [
        GoodsReceiptPayload(
            receipt_id=uuid4(),
            receipt_number="GR-701",
            challan_number="DC-440",
            lines=[
                GoodsReceiptLineItem(
                    material_code="CEMENT-OPC-53",
                    received_quantity=Decimal("75"),
                    unit="bag",
                )
            ],
        )
    ]

    # BOQ Item (planned 100 bags with 5% wastage -> 105 allowed)
    boqs = [
        BOQItemPayload(
            boq_item_id=uuid4(),
            item_code="BOQ-CIV-04",
            description="Column Concreting M25 Grade",
            material_code="CEMENT-OPC-53",
            planned_quantity=Decimal("100"),
            unit="bag",
            approved_wastage_rate=Decimal("0.05"),
        )
    ]

    # Stock Movements matching worked example
    # Opening: 100, Receipts: 80, Issues: 120, Returns: 5, Adjustment: +2 -> Expected: 67
    now = datetime.now(timezone.utc)
    movements = [
        StockMovementPayload(
            movement_id=uuid4(),
            material_code="CEMENT-OPC-53",
            movement_type="opening_balance",
            quantity=Decimal("100"),
            unit="bag",
            effective_date=now,
        ),
        StockMovementPayload(
            movement_id=uuid4(),
            material_code="CEMENT-OPC-53",
            movement_type="receipt",
            quantity=Decimal("80"),
            unit="bag",
            effective_date=now,
        ),
        StockMovementPayload(
            movement_id=uuid4(),
            material_code="CEMENT-OPC-53",
            movement_type="issue",
            quantity=Decimal("120"),
            unit="bag",
            effective_date=now,
        ),
        StockMovementPayload(
            movement_id=uuid4(),
            material_code="CEMENT-OPC-53",
            movement_type="return",
            quantity=Decimal("5"),
            unit="bag",
            effective_date=now,
        ),
        StockMovementPayload(
            movement_id=uuid4(),
            material_code="CEMENT-OPC-53",
            movement_type="adjustment",
            quantity=Decimal("2"),
            unit="bag",
            effective_date=now,
        ),
    ]

    return AuditEngineRequest(
        job_id=job_id,
        project_id=DEMO_PROJECT_ID,
        milestone_id=DEMO_MILESTONE_ID,
        acceptance_criteria=criteria,
        evidence_items=evidence_items,
        boq_items=boqs,
        purchase_orders=pos,
        delivery_challans=challans,
        goods_receipts=receipts,
        stock_movements=movements,
        physical_count=Decimal("60"),
        physical_count_unit="bag",
        options=AnalysisOptions(
            run_ocr_extraction=True,
            run_reconciliation=True,
            run_visual_assessment=True,
            run_anomaly_detection=True,
        ),
    )
