import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    id: uuid.UUID
    display_name: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class OrgMembershipSummary(BaseModel):
    organization_id: uuid.UUID
    organization_name: str
    role: str
    status: str


class ProjectMembershipSummary(BaseModel):
    project_id: uuid.UUID
    project_name: str
    role: str
    status: str


class UserContextResponse(BaseModel):
    user: UserProfileResponse
    organizations: List[OrgMembershipSummary]
    projects: List[ProjectMembershipSummary]
