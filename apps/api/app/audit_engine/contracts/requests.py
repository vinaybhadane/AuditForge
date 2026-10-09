"""AuditEngine request contract models."""

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.audit_engine.contracts.evidence import EvidencePayload


class AcceptanceCriterion(BaseModel):
    """Milestone acceptance criterion against which evidence is evaluated."""
    criterion_id: UUID = Field(default_factory=uuid4)
    criterion_code: str
    description: str
    required_evidence_type: str = "site_photo"
    verification_method: str = "visual_inspection"
    is_mandatory: bool = True


class POLineItem(BaseModel):
    material_code: str
    description: str
    ordered_quantity: Decimal
    unit: str
    unit_price: Decimal
    line_total: Decimal


class PurchaseOrderPayload(BaseModel):
    po_id: UUID = Field(default_factory=uuid4)
    po_number: str
    vendor_name: str
    vendor_id: Optional[str] = None
    currency: str = "INR"
    order_date: Optional[date] = None
    lines: List[POLineItem] = Field(default_factory=list)


class ChallanLineItem(BaseModel):
    material_code: str
    description: str
    challaned_quantity: Decimal
    unit: str
    po_line_reference: Optional[str] = None


class DeliveryChallanPayload(BaseModel):
    challan_id: UUID = Field(default_factory=uuid4)
    challan_number: str
    po_number: Optional[str] = None
    vendor_name: str
    delivery_date: Optional[date] = None
    evidence_id: Optional[UUID] = None
    lines: List[ChallanLineItem] = Field(default_factory=list)


class GoodsReceiptLineItem(BaseModel):
    material_code: str
    received_quantity: Decimal
    unit: str
    condition_status: str = "good"


class GoodsReceiptPayload(BaseModel):
    receipt_id: UUID = Field(default_factory=uuid4)
    receipt_number: str
    challan_number: Optional[str] = None
    receipt_date: Optional[date] = None
    evidence_id: Optional[UUID] = None
    lines: List[GoodsReceiptLineItem] = Field(default_factory=list)


class BOQItemPayload(BaseModel):
    boq_item_id: UUID = Field(default_factory=uuid4)
    item_code: str
    description: str
    material_code: str
    planned_quantity: Decimal
    unit: str
    approved_wastage_rate: Decimal = Decimal("0.05")  # e.g. 5%
    milestone_id: Optional[UUID] = None


class StockMovementPayload(BaseModel):
    movement_id: UUID = Field(default_factory=uuid4)
    material_code: str
    movement_type: str  # opening_balance, receipt, issue, return, adjustment, transfer_in, transfer_out
    quantity: Decimal
    unit: str
    effective_date: datetime
    source_reference: Optional[str] = None


class AnalysisOptions(BaseModel):
    run_ocr_extraction: bool = True
    run_reconciliation: bool = True
    run_visual_assessment: bool = True
    run_anomaly_detection: bool = True
    quantity_tolerance_pct: Decimal = Decimal("0.01")
    financial_tolerance_abs: Decimal = Decimal("1.00")


class AuditEngineRequest(BaseModel):
    """Comprehensive input payload for an AuditEngine processing execution."""
    schema_version: str = "1.0"
    job_id: UUID = Field(default_factory=uuid4)
    project_id: UUID
    milestone_id: Optional[UUID] = None
    acceptance_criteria: List[AcceptanceCriterion] = Field(default_factory=list)
    evidence_items: List[EvidencePayload] = Field(default_factory=list)
    boq_items: List[BOQItemPayload] = Field(default_factory=list)
    purchase_orders: List[PurchaseOrderPayload] = Field(default_factory=list)
    delivery_challans: List[DeliveryChallanPayload] = Field(default_factory=list)
    goods_receipts: List[GoodsReceiptPayload] = Field(default_factory=list)
    stock_movements: List[StockMovementPayload] = Field(default_factory=list)
    physical_count: Optional[Decimal] = None
    physical_count_unit: Optional[str] = None
    options: AnalysisOptions = Field(default_factory=AnalysisOptions)
