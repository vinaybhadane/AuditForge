from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser, get_current_user
from app.db.models.auth import Organization, OrganizationMembership, ProjectMembership
from app.db.models.projects import Project
from app.db.session import get_db
from app.schemas.auth import (
    OrgMembershipSummary,
    ProjectMembershipSummary,
    UserContextResponse,
    UserProfileResponse,
)

router = APIRouter(tags=["User Profile & Context"])


@router.get(
    "/me",
    response_model=UserContextResponse,
    status_code=status.HTTP_200_OK,
    summary="User Profile and Context",
    description="Returns verified user profile, active organization memberships, and project assignments.",
)
async def get_my_context(
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserContextResponse:
    # Get organization memberships
    org_stmt = (
        select(OrganizationMembership, Organization.name)
        .join(Organization, OrganizationMembership.organization_id == Organization.id)
        .where(OrganizationMembership.user_id == user.id)
    )
    org_results = db.execute(org_stmt).all()
    org_summaries = [
        OrgMembershipSummary(
            organization_id=m.organization_id,
            organization_name=org_name,
            role=m.role,
            status=m.status,
        )
        for m, org_name in org_results
    ]

    # Get project memberships
    proj_stmt = (
        select(ProjectMembership, Project.name)
        .join(Project, ProjectMembership.project_id == Project.id)
        .where(ProjectMembership.user_id == user.id)
    )
    proj_results = db.execute(proj_stmt).all()
    proj_summaries = [
        ProjectMembershipSummary(
            project_id=m.project_id,
            project_name=proj_name,
            role=m.role,
            status=m.status,
        )
        for m, proj_name in proj_results
    ]

    return UserContextResponse(
        user=UserProfileResponse.model_validate(user.user_profile),
        organizations=org_summaries,
        projects=proj_summaries,
    )
