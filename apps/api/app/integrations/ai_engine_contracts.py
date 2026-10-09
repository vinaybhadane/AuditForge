"""Typed contracts for Member 3 AI Engine Integration.

Per docs/08_AI_EVIDENCE_PIPELINE.md:
- Output envelope version 1.0.
- Clear confidence semantics ('calibrated', 'uncalibrated', 'not_provided').
- Limitations array acknowledging single-photo or document ambiguity.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ObservationRef(BaseModel):
    evidence_id: uuid.UUID
    page_or_frame: Optional[int] = None
    region: Optional[Dict[str, Any]] = None


class ObservationItem(BaseModel):
    observation: str
    criterion_id: Optional[uuid.UUID] = None
    evidence_refs: List[ObservationRef] = Field(default_factory=list)
    classification: str = Field(default="observed")  # observed, not_visible, inconclusive
    confidence_value: Optional[float] = None
    confidence_semantics: str = Field(default="not_provided")  # calibrated, uncalibrated, not_provided
    limitations: List[str] = Field(default_factory=list)
    requires_human_review: bool = True


class VisualAssessmentInput(BaseModel):
    job_id: uuid.UUID
    evidence_id: uuid.UUID
    project_id: uuid.UUID
    milestone_id: Optional[uuid.UUID] = None
    media_url: str
    media_type: str
    criteria_descriptions: List[Dict[str, Any]] = Field(default_factory=list)
    pipeline_version: str = "1.0"


class VisualAssessmentOutput(BaseModel):
    schema_version: str = "1.0"
    result_type: str = "visual_observation"
    observations: List[ObservationItem] = Field(default_factory=list)
    provider: Dict[str, str] = Field(default_factory=lambda: {"name": "auditforge-vlm", "model": "gemini-1.5-pro"})
    prompt_version: str = "visual-audit-v1"
    processed_at: datetime


class ExtractedFieldItem(BaseModel):
    field_name: str
    raw_value: str
    normalized_value: Optional[str] = None
    confidence: Optional[float] = None
    confidence_semantics: str = Field(default="not_provided")
    page_number: Optional[int] = None
    bounding_box: Optional[Dict[str, Any]] = None


class DocumentExtractionInput(BaseModel):
    job_id: uuid.UUID
    evidence_id: uuid.UUID
    project_id: uuid.UUID
    document_type: str  # invoice, delivery_challan, purchase_order, goods_receipt
    document_url: str
    media_type: str
    pipeline_version: str = "1.0"


class DocumentExtractionOutput(BaseModel):
    schema_version: str = "1.0"
    document_type: str
    raw_document_number: Optional[str] = None
    normalized_document_number: Optional[str] = None
    vendor_name: Optional[str] = None
    document_date: Optional[datetime] = None
    currency: str = "INR"
    total_amount: Optional[float] = None
    fields: List[ExtractedFieldItem] = Field(default_factory=list)
    provider: Dict[str, str] = Field(default_factory=lambda: {"name": "auditforge-doc", "model": "layout-parser-v1"})
    processed_at: datetime
