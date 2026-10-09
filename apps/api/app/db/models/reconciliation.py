import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    JSON,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ReconciliationRun(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "reconciliation_runs"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    baseline_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("project_baseline_versions.id"), nullable=True
    )
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    input_snapshot_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    algorithm_version: Mapped[str] = mapped_column(String(50), default="1.0", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="queued", nullable=False)  # queued, running, completed, failed
    created_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    summary_metrics: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    error_details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("project_id", "idempotency_key", name="uq_project_reconciliation_idempotency"),
    )

    lines = relationship("ReconciliationLine", back_populates="run", cascade="all, delete-orphan")


class ReconciliationLine(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "reconciliation_lines"

    run_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("reconciliation_runs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    rule_code: Mapped[str] = mapped_column(String(50), nullable=False)  # REC-001 through REC-008
    line_type: Mapped[str] = mapped_column(String(50), nullable=False)
    material_code: Mapped[str] = mapped_column(String(100), nullable=False)
    source_references: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    raw_expected_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 6), nullable=True)
    raw_observed_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 6), nullable=True)
    normalized_expected_quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    normalized_observed_quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    delta_quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    tolerance: Mapped[Decimal] = mapped_column(Numeric(20, 6), default=Decimal("0.0"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # matched, within_tolerance, discrepancy, inconclusive, not_applicable
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    run = relationship("ReconciliationRun", back_populates="lines")


class AnomalyFinding(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "anomaly_findings"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    finding_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)  # info, low, medium, high, critical
    status: Mapped[str] = mapped_column(String(50), default="open", nullable=False)  # open, under_review, resolved, dismissed, false_positive
    rule_code: Mapped[str] = mapped_column(String(50), nullable=False)
    rule_version: Mapped[str] = mapped_column(String(50), default="1.0", nullable=False)
    subject_references: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    calculation_details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    limitations: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    recommended_action: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_finding_proj_severity_status", "project_id", "severity", "status"),
    )

    evidence_links = relationship("FindingEvidenceLink", back_populates="finding", cascade="all, delete-orphan")


class FindingEvidenceLink(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "finding_evidence_links"

    finding_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("anomaly_findings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    evidence_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("evidence_assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    relation_type: Mapped[str] = mapped_column(String(50), default="supports", nullable=False)  # supports, contradicts, context
    rationale: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("finding_id", "evidence_id", name="uq_finding_evidence_link"),
    )

    finding = relationship("AnomalyFinding", back_populates="evidence_links")
