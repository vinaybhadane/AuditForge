"""Security dependencies, JWT extraction, and centralized role-based authorization.

Per docs/07_SECURITY_AND_ACCESS_CONTROL.md:
- Extracts bearer token and validates cryptographic signature, expiry, and claims.
- Never trusts client-supplied roles or organization/project IDs.
- Enforces tenant and project isolation on every protected endpoint.
- Uses consistent 403 Forbidden vs 404 Not Found to prevent leaking resource existence.
"""

import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

from fastapi import Depends, Header
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.errors import ForbiddenException, NotFoundException, UnauthorizedException
from app.db.models.auth import (
    MembershipStatus,
    OrganizationMembership,
    OrgRole,
    ProjectMembership,
    UserProfile,
)
from app.db.models.projects import Project
from app.db.session import get_db
from app.integrations.supabase_auth import supabase_verifier


@dataclass
class AuthenticatedUser:
    """Authenticated user context derived from verified JWT."""
    id: uuid.UUID
    email: Optional[str]
    claims: Dict[str, Any]
    user_profile: Optional[UserProfile] = None


@dataclass
class ProjectContext:
    """Authorized project execution context."""
    project: Project
    user: AuthenticatedUser
    role: str  # User's effective role on the project or organization
    is_admin: bool


def extract_bearer_token(authorization: Optional[str] = Header(None, alias="Authorization")) -> str:
    """Extract bearer token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException(
            message="Missing or malformed Authorization header",
            details=[{"field": "Authorization", "code": "BEARER_REQUIRED"}],
        )
    token = authorization[7:].strip()
    if not token:
        raise UnauthorizedException(message="Empty bearer token provided")
    return token


async def get_current_user(
    token: str = Depends(extract_bearer_token),
    db: Session = Depends(get_db),
) -> AuthenticatedUser:
    """Validate JWT signature and claims, then resolve user profile from database."""
    payload = supabase_verifier.verify_token(token)
    user_id = uuid.UUID(payload["sub"])
    email = payload.get("email")

    # Fetch or auto-create UserProfile record for authenticated Supabase user
    user = db.execute(select(UserProfile).where(UserProfile.id == user_id)).scalar_one_or_none()
    if not user:
        display_name = (
            payload.get("user_metadata", {}).get("full_name")
            or payload.get("user_metadata", {}).get("name")
            or (email.split("@")[0] if email else "User")
        )
        user = UserProfile(
            id=user_id,
            display_name=display_name,
            email=email,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    if user.disabled_at is not None:
        raise UnauthorizedException(message="User account has been disabled")

    return AuthenticatedUser(
        id=user_id,
        email=email,
        claims=payload,
        user_profile=user,
    )


class RequireOrgRole:
    """Dependency verifying that user belongs to organization with required roles."""

    def __init__(self, allowed_roles: Optional[List[str]] = None) -> None:
        self.allowed_roles = set(allowed_roles) if allowed_roles else None

    async def __call__(
        self,
        organization_id: uuid.UUID,
        user: AuthenticatedUser = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> OrganizationMembership:
        membership = db.execute(
            select(OrganizationMembership).where(
                and_(
                    OrganizationMembership.organization_id == organization_id,
                    OrganizationMembership.user_id == user.id,
                    OrganizationMembership.status == MembershipStatus.ACTIVE.value,
                )
            )
        ).scalar_one_or_none()

        if not membership:
            # 404 to avoid leaking existence of an organization the user does not belong to
            raise NotFoundException(message="Organization not found")

        if self.allowed_roles and membership.role not in self.allowed_roles:
            raise ForbiddenException(
                message=f"Action requires one of roles: {', '.join(sorted(self.allowed_roles))}"
            )

        return membership


async def verify_project_access(
    project_id: uuid.UUID,
    user: AuthenticatedUser,
    db: Session,
    allowed_roles: Optional[Set[str]] = None,
    require_write: bool = False,
) -> ProjectContext:
    """Verifies that the user has authorized access to the project within their organization."""
    project = db.execute(select(Project).where(Project.id == project_id)).scalar_one_or_none()
    if not project:
        raise NotFoundException(message="Project not found")

    # Check user's organization membership
    org_membership = db.execute(
        select(OrganizationMembership).where(
            and_(
                OrganizationMembership.organization_id == project.organization_id,
                OrganizationMembership.user_id == user.id,
                OrganizationMembership.status == MembershipStatus.ACTIVE.value,
            )
        )
    ).scalar_one_or_none()

    if not org_membership:
        # Cross-organization attempt: return 404 so existence is concealed
        raise NotFoundException(message="Project not found")

    is_admin = org_membership.role == OrgRole.ORG_ADMIN.value
    effective_role = org_membership.role

    # Check project-specific assignment if available
    project_membership = db.execute(
        select(ProjectMembership).where(
            and_(
                ProjectMembership.project_id == project_id,
                ProjectMembership.user_id == user.id,
                ProjectMembership.status == MembershipStatus.ACTIVE.value,
            )
        )
    ).scalar_one_or_none()

    if project_membership:
        effective_role = project_membership.role

    # If viewer attempting write operation
    if require_write and effective_role == OrgRole.VIEWER.value and not is_admin:
        raise ForbiddenException(message="Write access forbidden for viewer role")

    # If specific roles are required
    if allowed_roles and effective_role not in allowed_roles and not is_admin:
        raise ForbiddenException(
            message=f"Action requires one of roles: {', '.join(sorted(allowed_roles))}"
        )

    return ProjectContext(
        project=project,
        user=user,
        role=effective_role,
        is_admin=is_admin,
    )
