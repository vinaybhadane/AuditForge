import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class InvestigationCreate(BaseModel):
    case_number: str = Field(..., min_length=2, max_length=50)
    title: str = Field(..., min_length=3, max_length=255)
    summary: str = Field(..., min_length=5)
    severity: str = Field(default="medium", pattern=r"^(info|low|medium|high|critical)$")
    finding_ids: Optional[List[uuid.UUID]] = Field(default_factory=list)


class InvestigationUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[str] = Field(None, pattern=r"^(open|active|pending_inspection|closed|dismissed)$")
    severity: Optional[str] = Field(None, pattern=r"^(info|low|medium|high|critical)$")
    assigned_to: Optional[uuid.UUID] = None
    resolution_summary: Optional[str] = None


class InvestigationResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    case_number: str
    title: str
    summary: str
    status: str
    severity: str
    assigned_to: Optional[uuid.UUID] = None
    opened_by: uuid.UUID
    opened_at: datetime
    closed_at: Optional[datetime] = None
    resolution_summary: Optional[str] = None

    model_config = {"from_attributes": True}


class InvestigationActivityCreate(BaseModel):
    activity_type: str = Field(default="note", max_length=50)
    notes: str = Field(..., min_length=2)


class InvestigationActivityResponse(BaseModel):
    id: uuid.UUID
    investigation_id: uuid.UUID
    actor_id: uuid.UUID
    activity_type: str
    notes: str
    created_at: datetime

    model_config = {"from_attributes": True}
