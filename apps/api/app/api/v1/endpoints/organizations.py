import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.errors import NotFoundException
from app.core.security import AuthenticatedUser, RequireOrgRole, get_current_user
from app.db.models.auth import (
    MembershipStatus,
    Organization,
    OrganizationMembership,
    OrgRole,
    UserProfile,
)
from app.db.session import get_db
from app.schemas.organizations import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
    OrgMemberInvite,
    OrgMemberResponse,
)
from app.services.project_service import ProjectService

router = APIRouter(tags=["Organizations"])


@router.get(
    "/organizations",
    response_model=List[OrganizationResponse],
    status_code=status.HTTP_200_OK,
    summary="List Organizations",
)
async def list_organizations(
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[OrganizationResponse]:
    orgs = ProjectService.get_user_organizations(db, user.id)
    return [OrganizationResponse.model_validate(o) for o in orgs]


@router.post(
    "/organizations",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Organization",
)
async def create_organization(
    data: OrganizationCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> OrganizationResponse:
    org = ProjectService.create_organization(db, data, user.id)
    return OrganizationResponse.model_validate(org)


@router.get(
    "/organizations/{id}",
    response_model=OrganizationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Organization Details",
)
async def get_organization(
    id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> OrganizationResponse:
    # Check membership
    membership = db.execute(
        select(OrganizationMembership).where(
            and_(
                OrganizationMembership.organization_id == id,
                OrganizationMembership.user_id == user.id,
                OrganizationMembership.status == MembershipStatus.ACTIVE.value,
            )
        )
    ).scalar_one_or_none()
    if not membership:
        raise NotFoundException(message="Organization not found")

    org = db.execute(select(Organization).where(Organization.id == id)).scalar_one_or_none()
    if not org:
        raise NotFoundException(message="Organization not found")
    return OrganizationResponse.model_validate(org)


@router.patch(
    "/organizations/{id}",
    response_model=OrganizationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Organization",
)
async def update_organization(
    id: uuid.UUID,
    data: OrganizationUpdate,
    membership: OrganizationMembership = Depends(RequireOrgRole(allowed_roles=[OrgRole.ORG_ADMIN.value])),
    db: Session = Depends(get_db),
) -> OrganizationResponse:
    org = db.execute(select(Organization).where(Organization.id == id)).scalar_one_or_none()
    if not org:
        raise NotFoundException(message="Organization not found")
    if data.name:
        org.name = data.name
    if data.status:
        org.status = data.status
    db.commit()
    db.refresh(org)
    return OrganizationResponse.model_validate(org)


@router.get(
    "/organizations/{id}/members",
    response_model=List[OrgMemberResponse],
    status_code=status.HTTP_200_OK,
    summary="List Organization Members",
)
async def list_members(
    id: uuid.UUID,
    membership: OrganizationMembership = Depends(RequireOrgRole()),
    db: Session = Depends(get_db),
) -> List[OrgMemberResponse]:
    stmt = (
        select(OrganizationMembership, UserProfile.display_name, UserProfile.email)
        .join(UserProfile, OrganizationMembership.user_id == UserProfile.id)
        .where(OrganizationMembership.organization_id == id)
    )
    results = db.execute(stmt).all()
    members = []
    for m, name, email in results:
        res = OrgMemberResponse.model_validate(m)
        res.display_name = name
        res.email = email
        members.append(res)
    return members


@router.post(
    "/organizations/{id}/members",
    response_model=OrgMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Invite/Add Organization Member",
)
async def invite_member(
    id: uuid.UUID,
    data: OrgMemberInvite,
    membership: OrganizationMembership = Depends(RequireOrgRole(allowed_roles=[OrgRole.ORG_ADMIN.value])),
    db: Session = Depends(get_db),
) -> OrgMemberResponse:
    target_user = db.execute(select(UserProfile).where(UserProfile.id == data.user_id)).scalar_one_or_none()
    if not target_user:
        raise NotFoundException(message="User profile not found")

    new_member = OrganizationMembership(
        organization_id=id,
        user_id=data.user_id,
        role=data.role,
        status=MembershipStatus.ACTIVE.value,
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    res = OrgMemberResponse.model_validate(new_member)
    res.display_name = target_user.display_name
    res.email = target_user.email
    return res
