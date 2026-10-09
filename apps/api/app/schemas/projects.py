import uuid
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    organization_id: uuid.UUID
    name: str = Field(..., min_length=2, max_length=255)
    project_code: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None
    timezone: str = Field(default="UTC", max_length=50)
    currency_code: str = Field(default="INR", max_length=10)
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    timezone: Optional[str] = None
    currency_code: Optional[str] = None
    status: Optional[str] = None
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None


class ProjectResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    name: str
    project_code: str
    description: Optional[str] = None
    timezone: str
    currency_code: str
    status: str
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    current_baseline_version: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    items: List[ProjectResponse]
    total: int
