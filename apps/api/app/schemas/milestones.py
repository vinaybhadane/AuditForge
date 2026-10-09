import uuid
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AcceptanceCriterionCreate(BaseModel):
    criterion_code: str = Field(..., max_length=50)
    description: str
    required_evidence_types: str = Field(..., description="Comma-separated e.g. site_photo,delivery_challan")
    verification_method: str = Field(default="visual_assessment")
    is_required: bool = True


class AcceptanceCriterionResponse(BaseModel):
    id: uuid.UUID
    milestone_id: uuid.UUID
    version: int
    criterion_code: str
    description: str
    required_evidence_types: str
    verification_method: str
    is_required: bool
    is_active: bool

    model_config = {"from_attributes": True}


class MilestoneCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None


class MilestoneUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None


class MilestoneResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    code: str
    name: str
    description: Optional[str] = None
    status: str
    criteria_version: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ReviewDecisionCreate(BaseModel):
    decision_type: str = Field(
        ...,
        pattern=r"^(approve|request_evidence|request_inspection|hold|reject|escalate)$",
        description="Review decision type"
    )
    reason: str = Field(..., min_length=5)
    referenced_finding_ids: Optional[List[str]] = Field(default_factory=list)
    criteria_version: int = Field(default=1)


class ReviewDecisionResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    milestone_id: uuid.UUID
    decision_type: str
    reason: str
    reviewer_id: uuid.UUID
    criteria_version: int
    referenced_finding_ids: Optional[List[str]] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ClearanceEligibilityResponse(BaseModel):
    milestone_id: uuid.UUID
    is_eligible: bool
    status: str
    blockers: List[str]
    unresolved_discrepancies: int
    open_critical_findings: int
    verified_evidence_count: int
    latest_decision: Optional[str] = None


class CertificateIssueRequest(BaseModel):
    review_decision_id: uuid.UUID
    report_format: str = Field(default="pdf", pattern=r"^(pdf|json)$")
    idempotency_key: str = Field(..., min_length=8, max_length=128)


class CertificateResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    milestone_id: uuid.UUID
    certificate_number: str
    decision_id: uuid.UUID
    report_object_key: str
    snapshot_hash: str
    version: int
    status: str
    issued_by: uuid.UUID
    issued_at: datetime

    model_config = {"from_attributes": True}
