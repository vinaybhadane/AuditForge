import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class EvidenceAsset(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "evidence_assets"

    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    milestone_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("milestones.id", ondelete="SET NULL"), nullable=True, index=True
    )
    uploader_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)  # site_photo, invoice, delivery_challan, goods_receipt, other
    ingestion_source: Mapped[str] = mapped_column(String(50), nullable=False)  # live_capture, file_upload
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    object_key: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    media_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    sha256_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    upload_status: Mapped[str] = mapped_column(String(50), default="initiated", nullable=False)  # initiated, verified, failed
    claimed_captured_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    capture_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    source_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_evidence_proj_type", "project_id", "evidence_type"),
    )

    # Relationships
    jobs = relationship("EvidenceProcessingJob", back_populates="evidence", cascade="all, delete-orphan")
    observations = relationship("AIObservation", back_populates="evidence", cascade="all, delete-orphan")
    document = relationship("Document", back_populates="evidence", uselist=False, cascade="all, delete-orphan")


class EvidenceProcessingJob(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "evidence_processing_jobs"

    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    evidence_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("evidence_assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_type: Mapped[str] = mapped_column(String(50), nullable=False)  # visual_assessment, document_extraction, ocr_scan
    status: Mapped[str] = mapped_column(String(50), default="queued", nullable=False)  # queued, running, succeeded, failed, cancelled
    attempt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    pipeline_version: Mapped[str] = mapped_column(String(50), default="1.0", nullable=False)
    provider_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    model_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    output_reference: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    __table_args__ = (
        Index("ix_job_status_attempts", "status", "attempt_count"),
        UniqueConstraint("project_id", "idempotency_key", name="uq_project_job_idempotency"),
    )

    evidence = relationship("EvidenceAsset", back_populates="jobs")


class AIObservation(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "ai_observations"

    evidence_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("evidence_assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    milestone_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("evidence_processing_jobs.id", ondelete="SET NULL"), nullable=True
    )
    observation_type: Mapped[str] = mapped_column(String(50), nullable=False)
    observation_text: Mapped[str] = mapped_column(Text, nullable=False)
    criterion_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)
    region: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    confidence_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    confidence_semantics: Mapped[str] = mapped_column(String(50), default="not_provided", nullable=False)
    limitations: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    provider_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    review_status: Mapped[str] = mapped_column(String(50), default="unreviewed", nullable=False)  # unreviewed, accepted, rejected, corrected
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    evidence = relationship("EvidenceAsset", back_populates="observations")


class Document(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "documents"

    evidence_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("evidence_assets.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    project_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)  # invoice, delivery_challan, purchase_order, goods_receipt, other
    raw_document_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    normalized_document_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    vendor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    document_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    total_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    processing_status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)  # pending, extracted, verified, error

    evidence = relationship("EvidenceAsset", back_populates="document")
    extracted_fields = relationship("ExtractedFieldVersion", back_populates="document", cascade="all, delete-orphan")


class ExtractedFieldVersion(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "extracted_field_versions"

    document_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    raw_value: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    confidence_semantics: Mapped[str] = mapped_column(String(50), default="not_provided", nullable=False)
    page_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bounding_box: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    review_status: Mapped[str] = mapped_column(String(50), default="extracted", nullable=False)  # extracted, confirmed, corrected
    corrected_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)
    correction_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("document_id", "field_name", "version", name="uq_doc_field_version"),
    )

    document = relationship("Document", back_populates="extracted_fields")
