import uuid
from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.errors import AuditForgeException, ErrorCode
from app.db.models.auth import (
    MembershipStatus,
    Organization,
    OrganizationMembership,
    OrgRole,
    ProjectMembership,
)
from app.db.models.projects import Project
from app.schemas.organizations import OrganizationCreate
from app.schemas.projects import ProjectCreate


class ProjectService:
    @staticmethod
    def create_organization(db: Session, data: OrganizationCreate, creator_id: uuid.UUID) -> Organization:
        existing = db.execute(select(Organization).where(Organization.slug == data.slug)).scalar_one_or_none()
        if existing:
            raise AuditForgeException(
                code=ErrorCode.STATE_CONFLICT,
                message=f"Organization slug '{data.slug}' already exists",
                status_code=409,
            )

        org = Organization(
            name=data.name,
            slug=data.slug,
            created_by=creator_id,
        )
        db.add(org)
        db.flush()

        # Creator automatically becomes Org Admin
        membership = OrganizationMembership(
            organization_id=org.id,
            user_id=creator_id,
            role=OrgRole.ORG_ADMIN.value,
            status=MembershipStatus.ACTIVE.value,
        )
        db.add(membership)
        db.commit()
        db.refresh(org)
        return org

    @staticmethod
    def get_user_organizations(db: Session, user_id: uuid.UUID) -> List[Organization]:
        stmt = (
            select(Organization)
            .join(OrganizationMembership, Organization.id == OrganizationMembership.organization_id)
            .where(
                and_(
                    OrganizationMembership.user_id == user_id,
                    OrganizationMembership.status == MembershipStatus.ACTIVE.value,
                )
            )
        )
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def create_project(db: Session, data: ProjectCreate, creator_id: uuid.UUID) -> Project:
        existing = db.execute(
            select(Project).where(
                and_(
                    Project.organization_id == data.organization_id,
                    Project.project_code == data.project_code,
                )
            )
        ).scalar_one_or_none()
        if existing:
            raise AuditForgeException(
                code=ErrorCode.STATE_CONFLICT,
                message=f"Project with code '{data.project_code}' already exists in this organization",
                status_code=409,
            )

        project = Project(
            organization_id=data.organization_id,
            name=data.name,
            project_code=data.project_code,
            description=data.description,
            timezone=data.timezone,
            currency_code=data.currency_code,
            planned_start_date=data.planned_start_date,
            planned_end_date=data.planned_end_date,
            created_by=creator_id,
        )
        db.add(project)
        db.flush()

        # Add creator as project manager
        pm_membership = ProjectMembership(
            organization_id=data.organization_id,
            project_id=project.id,
            user_id=creator_id,
            role="project_manager",
            status=MembershipStatus.ACTIVE.value,
        )
        db.add(pm_membership)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def list_user_projects(db: Session, user_id: uuid.UUID) -> List[Project]:
        # User can view projects in organizations where they are org_admin, OR projects where assigned
        stmt = (
            select(Project)
            .join(OrganizationMembership, Project.organization_id == OrganizationMembership.organization_id)
            .where(
                and_(
                    OrganizationMembership.user_id == user_id,
                    OrganizationMembership.status == MembershipStatus.ACTIVE.value,
                )
            )
        )
        return list(db.execute(stmt).scalars().all())
