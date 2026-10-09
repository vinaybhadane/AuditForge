import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class FindingDispositionRequest(BaseModel):
    status: str = Field(
        ...,
        pattern=r"^(under_review|resolved|dismissed|false_positive)$",
        description="Updated finding review status"
    )
    resolution_notes: str = Field(..., min_length=5, max_length=1000)


class AnomalyFindingResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    finding_type: str
    severity: str
    status: str
    rule_code: str
    rule_version: str
    explanation: str
    calculation_details: Optional[Dict[str, Any]] = None
    limitations: Optional[List[str]] = None
    recommended_action: Optional[str] = None
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None

    model_config = {"from_attributes": True}


class FindingListResponse(BaseModel):
    items: List[AnomalyFindingResponse]
    total: int
