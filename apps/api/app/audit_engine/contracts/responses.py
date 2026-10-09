"""AuditEngine response contract models."""

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.audit_engine.contracts.findings import AnomalyFinding


class EngineStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings"
    FAILED = "failed"


class ExtractedField(BaseModel):
    field_name: str
    raw_value: Optional[str] = None
    normalized_value: Optional[Any] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    extraction_method: str = "native_pdf"  # native_pdf, ocr, regex, model
    is_uncertain: bool = False
    notes: Optional[str] = None


class ExtractedRecord(BaseModel):
    evidence_id: UUID
    document_type: str
    document_number: Optional[str] = None
    vendor_name: Optional[str] = None
    document_date: Optional[str] = None
    fields: Dict[str, ExtractedField] = Field(default_factory=dict)
    line_items: List[Dict[str, Any]] = Field(default_factory=list)


class ReconciliationStatus(str, Enum):
    MATCHED = "matched"
    WITHIN_TOLERANCE = "within_tolerance"
    DISCREPANCY = "discrepancy"
    INCONCLUSIVE = "inconclusive"


class ReconciliationLineResult(BaseModel):
    rule_code: str
    material_code: str
    expected_value: Decimal
    observed_value: Decimal
    delta: Decimal
    unit: str
    tolerance_applied: Decimal
    status: ReconciliationStatus
    formula_code: str
    explanation: str
    source_refs: List[str] = Field(default_factory=list)


class ReconciliationResult(BaseModel):
    calculated_closing_stock: Decimal
    opening_stock: Decimal
    receipts_total: Decimal
    issues_total: Decimal
    returns_total: Decimal
    adjustments_total: Decimal
    variance_with_physical_count: Optional[Decimal] = None
    lines: List[ReconciliationLineResult] = Field(default_factory=list)


class VisualObservation(BaseModel):
    observation_id: str
    evidence_id: UUID
    criterion_id: Optional[UUID] = None
    observation: str
    classification: str = "observed"  # observed, partially_observed, not_visible, inconclusive
    confidence: Optional[float] = None
    limitations: List[str] = Field(default_factory=list)
    requires_human_review: bool = True


class VisualAssessmentResult(BaseModel):
    observations: List[VisualObservation] = Field(default_factory=list)
    provider_name: str = "GeminiVLM"
    model_id: str = "gemini-1.5-pro"
    prompt_version: str = "visual-audit-v1"


class EvidenceCorrelationLink(BaseModel):
    source_type: str
    source_id: str
    target_type: str
    target_id: str
    relationship: str
    rationale: str


class ProcessingMetadata(BaseModel):
    pipeline_version: str = "audit-pipeline-v1"
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    finish_time: Optional[datetime] = None
    duration_ms: int = 0
    stages_executed: List[str] = Field(default_factory=list)


class AuditEngineResponse(BaseModel):
    """Authoritative response produced by the AuditEngine."""
    schema_version: str = "1.0"
    job_id: UUID
    status: EngineStatus
    findings: List[AnomalyFinding] = Field(default_factory=list)
    extracted_records: List[ExtractedRecord] = Field(default_factory=list)
    reconciliation_result: Optional[ReconciliationResult] = None
    visual_assessments: List[VisualAssessmentResult] = Field(default_factory=list)
    correlation_links: List[EvidenceCorrelationLink] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    metadata: ProcessingMetadata = Field(default_factory=ProcessingMetadata)
