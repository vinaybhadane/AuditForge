import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EvidenceProcessRequest(BaseModel):
    job_type: str = Field(
        default="visual_assessment",
        pattern=r"^(visual_assessment|document_extraction|ocr_scan)$",
    )
    idempotency_key: Optional[str] = Field(None, max_length=128)


class JobResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    evidence_id: uuid.UUID
    status: str  # queued, running, succeeded, failed, cancelled
    job_type: str
    attempt_count: int
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    error: Optional[str] = None
    result_available: bool = False

    model_config = {"from_attributes": True}
