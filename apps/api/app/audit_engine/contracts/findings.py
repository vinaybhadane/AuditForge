"""Audit findings and anomaly contracts."""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class FindingCategory(str, Enum):
    EXACT_DUPLICATE = "exact_duplicate"
    DOCUMENT_DUPLICATE = "document_duplicate"
    RECONCILIATION_VARIANCE = "reconciliation_variance"
    OVER_INVOICING = "over_invoicing"
    DELIVERY_MISMATCH = "delivery_mismatch"
    EXCESS_ISSUE = "excess_issue"
    NEGATIVE_STOCK = "negative_stock"
    UNIT_INCOMPATIBILITY = "unit_incompatibility"
    TELEMETRY_ANOMALY = "telemetry_anomaly"
    MISSING_EVIDENCE = "missing_evidence"
    MODALITY_VIOLATION = "modality_violation"
    ARITHMETIC_MISMATCH = "arithmetic_mismatch"
    VISUAL_DEFECT_CANDIDATE = "visual_defect_candidate"


class FindingSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingProvenance(BaseModel):
    """Execution provenance for auditable finding traceability."""
    pipeline_version: str = "audit-pipeline-v1"
    rule_version: str = "v1"
    model_id: Optional[str] = None
    prompt_version: Optional[str] = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AnomalyFinding(BaseModel):
    """Structured audit finding.
    
    CRITICAL PRINCIPLE: An anomaly is an evidence-backed review signal,
    never an accusation of fraud or legal determination.
    """
    id: UUID = Field(default_factory=uuid4)
    rule_id: str = Field(..., description="Stable rule identifier, e.g. AN-001, REC-002")
    category: FindingCategory
    severity: FindingSeverity
    title: str = Field(..., description="Concise objective summary of the observation")
    explanation: str = Field(..., description="Auditable reasoning citing inputs and thresholds without accusatory language")
    evidence_refs: List[UUID] = Field(default_factory=list, description="IDs of linked evidence assets")
    subject_ids: List[str] = Field(default_factory=list, description="Linked entities (e.g. PO number, material code)")
    expected_value: Optional[str] = None
    observed_value: Optional[str] = None
    calculation_formula: Optional[str] = None
    tolerance_applied: Optional[str] = None
    uncertainty_notes: Optional[str] = Field(
        default=None,
        description="Explicit limitations, data gaps, or alternate explanations"
    )
    recommended_action: str = Field(..., description="Human auditor review or verification recommendation")
    provenance: FindingProvenance = Field(default_factory=FindingProvenance)
