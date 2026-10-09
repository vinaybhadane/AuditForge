import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    slug: str = Field(..., min_length=2, max_length=100, pattern=r"^[a-z0-9\-]+$")


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    status: Optional[str] = Field(None, max_length=50)


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class OrgMemberInvite(BaseModel):
    user_id: uuid.UUID
    role: str = Field(default="viewer", pattern=r"^(org_admin|project_manager|project_auditor|site_supervisor|store_in_charge|viewer)$")


class OrgMemberUpdate(BaseModel):
    role: Optional[str] = Field(None, pattern=r"^(org_admin|project_manager|project_auditor|site_supervisor|store_in_charge|viewer)$")
    status: Optional[str] = Field(None, pattern=r"^(active|suspended|invited)$")


class OrgMemberResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    user_id: uuid.UUID
    role: str
    status: str
    created_at: datetime
    display_name: Optional[str] = None
    email: Optional[str] = None

    model_config = {"from_attributes": True}
