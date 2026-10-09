import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class GoodsReceiptLineCreate(BaseModel):
    material_code: str = Field(..., max_length=100)
    quantity: Decimal = Field(..., gt=0)
    unit: str = Field(..., max_length=20)
    challan_reference: Optional[str] = None
    condition_notes: Optional[str] = None


class GoodsReceiptCreate(BaseModel):
    receipt_number: str = Field(..., min_length=2, max_length=100)
    receipt_date: date
    store_location_id: Optional[uuid.UUID] = None
    source_evidence_id: Optional[uuid.UUID] = None
    lines: List[GoodsReceiptLineCreate] = Field(..., min_length=1)


class GoodsReceiptLineResponse(BaseModel):
    id: uuid.UUID
    material_code: str
    quantity: Decimal
    unit: str
    challan_reference: Optional[str] = None
    condition_notes: Optional[str] = None

    model_config = {"from_attributes": True}


class GoodsReceiptResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    receipt_number: str
    receipt_date: date
    status: str
    lines: List[GoodsReceiptLineResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class StockMovementCreate(BaseModel):
    material_code: str = Field(..., max_length=100)
    location_id: Optional[uuid.UUID] = None
    movement_type: str = Field(
        ...,
        pattern=r"^(opening_balance|receipt|issue|return|adjustment|transfer_in|transfer_out|reversal)$",
    )
    quantity: Decimal = Field(..., description="Quantity following documented signed movement conventions")
    unit: str = Field(..., max_length=20)
    effective_date: date
    source_reference: Optional[str] = None
    source_evidence_id: Optional[uuid.UUID] = None
    notes: Optional[str] = None


class StockMovementResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    material_code: str
    movement_type: str
    quantity: Decimal
    unit: str
    effective_date: date
    source_reference: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
