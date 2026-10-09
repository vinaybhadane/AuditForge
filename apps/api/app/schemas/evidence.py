import uuid
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, model_validator

from app.core.errors import AuditForgeException, ErrorCode


class GeoLocation(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    accuracy_meters: Optional[float] = None


class CaptureMetadata(BaseModel):
    captured_at: Optional[datetime] = None
    device_client: Optional[str] = None
    camera_facing: Optional[str] = None  # environment, user
    geo_location: Optional[GeoLocation] = None


class EvidenceUploadInitiateRequest(BaseModel):
    evidence_type: str = Field(
        ...,
        pattern=r"^(site_photo|invoice|delivery_challan|goods_receipt|purchase_order|other)$",
        description="Type of evidence"
    )
    ingestion_source: str = Field(
        ...,
        pattern=r"^(live_capture|file_upload)$",
        description="Must be live_capture for site_photo"
    )
    filename: str = Field(..., min_length=1, max_length=255)
    declared_content_type: str = Field(..., min_length=3, max_length=100)
    size_bytes: int = Field(..., gt=0, le=20971520)  # max 20 MB
    milestone_id: Optional[uuid.UUID] = None
    capture_metadata: Optional[CaptureMetadata] = None
    source_notes: Optional[str] = None

    @model_validator(mode="after")
    def validate_modality_policy(self) -> "EvidenceUploadInitiateRequest":
        # Crucial domain rule: Construction site progress evidence strictly requires live camera capture.
        # Uploading pre-existing disk/gallery image files is forbidden.
        if self.evidence_type == "site_photo" and self.ingestion_source != "live_capture":
            raise AuditForgeException(
                code=ErrorCode.INVALID_INGESTION_SOURCE,
                message="Construction site photos must originate exclusively from verified live camera capture.",
                status_code=422,
                details=[{
                    "field": "ingestion_source",
                    "code": "INVALID_INGESTION_SOURCE",
                    "message": "Site progress photos require live_capture; pre-existing file_upload is disabled to enforce presence and freshness."
                }]
            )
        return self


class UploadInstructions(BaseModel):
    upload_url: str
    method: str = "PUT"
    required_headers: Dict[str, str] = Field(default_factory=dict)
    expires_at: datetime


class EvidenceUploadInitiateResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    milestone_id: Optional[uuid.UUID] = None
    evidence_type: str
    ingestion_source: str
    original_filename: str
    object_key: str
    upload_status: str
    upload_instructions: UploadInstructions


class EvidenceCompleteUploadRequest(BaseModel):
    sha256_hash: str = Field(..., min_length=64, max_length=64, pattern=r"^[a-fA-F0-9]{64}$")
    size_bytes: int = Field(..., gt=0)


class EvidenceResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    project_id: uuid.UUID
    milestone_id: Optional[uuid.UUID] = None
    uploader_id: uuid.UUID
    evidence_type: str
    ingestion_source: str
    original_filename: str
    media_type: str
    size_bytes: int
    sha256_hash: Optional[str] = None
    upload_status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class EvidenceListResponse(BaseModel):
    items: List[EvidenceResponse]
    total: int
