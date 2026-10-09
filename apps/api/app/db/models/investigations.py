import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Investigation(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "investigations"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    case_number: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="open", nullable=False)  # open, active, pending_inspection, closed, dismissed
    severity: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)  # info, low, medium, high, critical
    assigned_to: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    opened_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("project_id", "case_number", name="uq_project_case_number"),
    )

    findings = relationship("InvestigationFinding", back_populates="investigation", cascade="all, delete-orphan")
    activities = relationship("InvestigationActivity", back_populates="investigation", cascade="all, delete-orphan")


class InvestigationFinding(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "investigation_findings"

    investigation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    finding_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("anomaly_findings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    added_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    rationale: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("investigation_id", "finding_id", name="uq_investigation_finding"),
    )

    investigation = relationship("Investigation", back_populates="findings")


class InvestigationActivity(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "investigation_activities"

    investigation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    actor_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # note, status_change, assignment, inspection_request
    notes: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    investigation = relationship("Investigation", back_populates="activities")
