"""Evidence models and ingestion modality contracts."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator


class EvidenceType(str, Enum):
    SITE_PHOTO = "site_photo"
    INVOICE = "invoice"
    DELIVERY_CHALLAN = "delivery_challan"
    PURCHASE_ORDER = "purchase_order"
    GOODS_RECEIPT = "goods_receipt"
    OTHER = "other"


class IngestionSource(str, Enum):
    LIVE_CAPTURE = "live_capture"
    FILE_UPLOAD = "file_upload"


class CaptureTelemetry(BaseModel):
    """Telemetry captured from device sensor/camera during in-app live capture."""
    captured_at: datetime = Field(..., description="Client device timestamp at capture moment")
    device_client: str = Field(default="AuditForge Camera Stream v1", description="Client user-agent or identifier")
    camera_facing: Optional[str] = Field(default="environment", description="'environment' or 'user'")
    latitude: Optional[float] = Field(default=None, description="GPS latitude coordinates")
    longitude: Optional[float] = Field(default=None, description="GPS longitude coordinates")
    accuracy_meters: Optional[float] = Field(default=None, description="GPS accuracy radius in meters")


class EvidenceRef(BaseModel):
    """Reference to an existing verified evidence asset in storage."""
    evidence_id: UUID = Field(default_factory=uuid4)
    evidence_type: EvidenceType
    ingestion_source: IngestionSource
    sha256_hash: Optional[str] = None
    original_filename: Optional[str] = None
    media_type: str = "application/octet-stream"
    size_bytes: int = 0
    capture_telemetry: Optional[CaptureTelemetry] = None
    source_notes: Optional[str] = None


class EvidencePayload(BaseModel):
    """Evidence file content passed to the engine for ingestion and extraction."""
    evidence_id: UUID = Field(default_factory=uuid4)
    evidence_type: EvidenceType
    ingestion_source: IngestionSource
    filename: str
    declared_content_type: str
    content_bytes: Optional[bytes] = Field(default=None, repr=False)
    content_base64: Optional[str] = Field(default=None, repr=False)
    size_bytes: int = 0
    sha256_hash: Optional[str] = None
    capture_telemetry: Optional[CaptureTelemetry] = None
    source_notes: Optional[str] = None

    @model_validator(mode="after")
    def validate_modality_policy(self) -> "EvidencePayload":
        """Strict policy from AGENTS.md & docs/07_SECURITY_AND_ACCESS_CONTROL.md:
        Construction site progress photos strictly require live camera capture.
        Pre-existing image file upload is disallowed for site photos.
        Vendor documents (invoices, challans, etc.) permit both live scan and file upload.
        """
        if self.evidence_type == EvidenceType.SITE_PHOTO and self.ingestion_source != IngestionSource.LIVE_CAPTURE:
            raise ValueError(
                "INVALID_INGESTION_SOURCE: Construction site progress photos strictly require live camera capture. "
                "Local file upload is rejected to enforce fresh provenance and physical presence."
            )
        return self
