import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Project(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "projects"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    project_code: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    currency_code: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    planned_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    planned_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    current_baseline_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("organization_id", "project_code", name="uq_org_project_code"),
    )

    organization = relationship("Organization", back_populates="projects")
    memberships = relationship("ProjectMembership", back_populates="project", cascade="all, delete-orphan")
    milestones = relationship("Milestone", back_populates="project", cascade="all, delete-orphan")
    baseline_versions = relationship("ProjectBaselineVersion", back_populates="project", cascade="all, delete-orphan")
    boq_items = relationship("BOQItem", back_populates="project", cascade="all, delete-orphan")


class ProjectBaselineVersion(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "project_baseline_versions"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    effective_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    change_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    snapshot_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("project_id", "version_number", name="uq_project_baseline_version"),
    )

    project = relationship("Project", back_populates="baseline_versions")


class Milestone(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "milestones"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    planned_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    planned_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="planned", nullable=False)  # planned, in_progress, under_audit, cleared, blocked
    criteria_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    __table_args__ = (
        UniqueConstraint("project_id", "code", name="uq_project_milestone_code"),
    )

    project = relationship("Project", back_populates="milestones")
    criteria = relationship("AcceptanceCriterion", back_populates="milestone", cascade="all, delete-orphan")


class AcceptanceCriterion(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "acceptance_criteria"

    milestone_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("milestones.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    criterion_code: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    required_evidence_types: Mapped[str] = mapped_column(String(255), nullable=False)  # comma-separated e.g. "site_photo,delivery_challan"
    verification_method: Mapped[str] = mapped_column(String(100), default="visual_assessment", nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("milestone_id", "version", "criterion_code", name="uq_milestone_version_criterion"),
    )

    milestone = relationship("Milestone", back_populates="criteria")


class UnitOfMeasure(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "units_of_measure"

    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    dimension: Mapped[str] = mapped_column(String(50), nullable=False)  # mass, volume, length, area, count, time, other
    canonical_factor: Mapped[Decimal] = mapped_column(Numeric(20, 6), default=Decimal("1.0"), nullable=False)
    is_canonical: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Material(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "materials"

    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    canonical_code: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # cement, steel, aggregate, brick, etc.
    canonical_unit: Mapped[str] = mapped_column(String(20), nullable=False)
    density_kg_per_m3: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 4), nullable=True)

    __table_args__ = (
        UniqueConstraint("organization_id", "canonical_code", name="uq_org_material_code"),
    )


class BOQItem(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "boq_items"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    baseline_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("project_baseline_versions.id"), nullable=True
    )
    item_code: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    material_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    planned_quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    unit_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    approved_wastage_rate: Mapped[Decimal] = mapped_column(Numeric(5, 4), default=Decimal("0.05"), nullable=False)
    milestone_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("milestones.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("project_id", "item_code", name="uq_project_boq_item_code"),
    )

    project = relationship("Project", back_populates="boq_items")


class Vendor(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "vendors"

    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tax_identifier: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_org_vendor_code"),
    )
