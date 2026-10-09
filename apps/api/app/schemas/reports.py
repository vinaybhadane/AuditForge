import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ReportGenerateRequest(BaseModel):
    milestone_id: Optional[uuid.UUID] = None
    reconciliation_run_id: Optional[uuid.UUID] = None
    format: str = Field(default="json", pattern=r"^(json|pdf)$")


class AuditReportResponse(BaseModel):
    project_id: uuid.UUID
    project_name: str
    generated_at: datetime
    milestone_id: Optional[uuid.UUID] = None
    extracted_facts: List[Dict[str, Any]] = Field(default_factory=list)
    deterministic_calculations: List[Dict[str, Any]] = Field(default_factory=list)
    ai_observations: List[Dict[str, Any]] = Field(default_factory=list)
    unresolved_discrepancies: List[Dict[str, Any]] = Field(default_factory=list)
    human_decisions: List[Dict[str, Any]] = Field(default_factory=list)
