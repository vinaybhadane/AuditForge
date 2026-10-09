import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ExtractedFieldCorrectionRequest(BaseModel):
    normalized_value: str = Field(..., min_length=1)
    correction_reason: str = Field(..., min_length=5, max_length=500)


class ExtractedFieldResponse(BaseModel):
    id: uuid.UUID
    field_name: str
    raw_value: str
    normalized_value: Optional[str] = None
    confidence: Optional[float] = None
    confidence_semantics: str
    page_number: Optional[int] = None
    bounding_box: Optional[Dict[str, Any]] = None
    version: int
    review_status: str
    corrected_by: Optional[uuid.UUID] = None
    correction_reason: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentResponse(BaseModel):
    id: uuid.UUID
    evidence_id: uuid.UUID
    project_id: uuid.UUID
    document_type: str
    raw_document_number: Optional[str] = None
    normalized_document_number: Optional[str] = None
    vendor_name: Optional[str] = None
    document_date: Optional[datetime] = None
    currency: str
    total_amount: Optional[Decimal] = None
    processing_status: str
    created_at: datetime
    extracted_fields: List[ExtractedFieldResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}
