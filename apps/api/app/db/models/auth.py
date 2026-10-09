import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class OrgRole(str, Enum):
    ORG_ADMIN = "org_admin"
    PROJECT_MANAGER = "project_manager"
    PROJECT_AUDITOR = "project_auditor"
    SITE_SUPERVISOR = "site_supervisor"
    STORE_IN_CHARGE = "store_in_charge"
    VIEWER = "viewer"


class MembershipStatus(str, Enum):
    ACTIVE = "active"
    INVITED = "invited"
    SUSPENDED = "suspended"


class UserProfile(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "user_profiles"

    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    disabled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    org_memberships = relationship("OrganizationMembership", back_populates="user", cascade="all, delete-orphan")
    project_memberships = relationship("ProjectMembership", back_populates="user", cascade="all, delete-orphan")


class Organization(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)

    # Relationships
    memberships = relationship("OrganizationMembership", back_populates="organization", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="organization", cascade="all, delete-orphan")


class OrganizationMembership(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "organization_memberships"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False, default=OrgRole.VIEWER.value)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default=MembershipStatus.ACTIVE.value)

    __table_args__ = (
        UniqueConstraint("organization_id", "user_id", name="uq_org_user_membership"),
        Index("ix_org_user_status", "organization_id", "user_id", "status"),
    )

    organization = relationship("Organization", back_populates="memberships")
    user = relationship("UserProfile", back_populates="org_memberships")


class ProjectMembership(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "project_memberships"

    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="viewer")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default=MembershipStatus.ACTIVE.value)

    __table_args__ = (
        UniqueConstraint("project_id", "user_id", name="uq_project_user_membership"),
    )

    project = relationship("Project", back_populates="memberships")
    user = relationship("UserProfile", back_populates="project_memberships")
