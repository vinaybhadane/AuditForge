import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import AuditForgeException, ErrorCode, NotFoundException
from app.db.models.evidence import EvidenceAsset
from app.schemas.evidence import (
    EvidenceCompleteUploadRequest,
    EvidenceUploadInitiateRequest,
    EvidenceUploadInitiateResponse,
    UploadInstructions,
)


class EvidenceService:
    @staticmethod
    def initiate_upload(
        db: Session,
        project_id: uuid.UUID,
        organization_id: uuid.UUID,
        uploader_id: uuid.UUID,
        data: EvidenceUploadInitiateRequest,
    ) -> EvidenceUploadInitiateResponse:
        # Crucial Modality Policy Check (Defense-in-depth on service boundary)
        if data.evidence_type == "site_photo" and data.ingestion_source != "live_capture":
            raise AuditForgeException(
                code=ErrorCode.INVALID_INGESTION_SOURCE,
                message="Construction site photos must originate exclusively from verified live camera capture.",
                status_code=422,
                details=[{
                    "field": "ingestion_source",
                    "code": "INVALID_INGESTION_SOURCE",
                    "message": "Physical presence rule: file upload is disabled for site progress photos."
                }]
            )

        # Sanitize filename
        safe_filename = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", data.filename)
        object_key = f"projects/{project_id}/evidence/{uuid.uuid4().hex}_{safe_filename}"

        evidence = EvidenceAsset(
            organization_id=organization_id,
            project_id=project_id,
            milestone_id=data.milestone_id,
            uploader_id=uploader_id,
            evidence_type=data.evidence_type,
            ingestion_source=data.ingestion_source,
            original_filename=data.filename,
            object_key=object_key,
            media_type=data.declared_content_type,
            size_bytes=data.size_bytes,
            upload_status="initiated",
            claimed_captured_at=data.capture_metadata.captured_at if data.capture_metadata else None,
            capture_metadata=data.capture_metadata.model_dump(mode="json") if data.capture_metadata else None,
            source_notes=data.source_notes,
        )
        db.add(evidence)
        db.commit()
        db.refresh(evidence)

        # Upload instructions with signed URL (simulated / storage compatible)
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.SIGNED_URL_TTL_SECONDS)
        upload_url = f"{settings.SUPABASE_URL}/storage/v1/object/upload/sign/{settings.EVIDENCE_BUCKET}/{object_key}?token=mock-upload-sig"

        return EvidenceUploadInitiateResponse(
            id=evidence.id,
            project_id=evidence.project_id,
            milestone_id=evidence.milestone_id,
            evidence_type=evidence.evidence_type,
            ingestion_source=evidence.ingestion_source,
            original_filename=evidence.original_filename,
            object_key=evidence.object_key,
            upload_status=evidence.upload_status,
            upload_instructions=UploadInstructions(
                upload_url=upload_url,
                method="PUT",
                required_headers={"Content-Type": data.declared_content_type},
                expires_at=expires_at,
            ),
        )

    @staticmethod
    def complete_upload(
        db: Session,
        evidence_id: uuid.UUID,
        data: EvidenceCompleteUploadRequest,
    ) -> EvidenceAsset:
        evidence = db.execute(select(EvidenceAsset).where(EvidenceAsset.id == evidence_id)).scalar_one_or_none()
        if not evidence:
            raise NotFoundException(message="Evidence record not found")

        evidence.sha256_hash = data.sha256_hash.lower()
        evidence.size_bytes = data.size_bytes
        evidence.upload_status = "verified"
        evidence.verified_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(evidence)
        return evidence

    @staticmethod
    def list_evidence(
        db: Session,
        project_id: uuid.UUID,
        milestone_id: Optional[uuid.UUID] = None,
        evidence_type: Optional[str] = None,
    ) -> List[EvidenceAsset]:
        stmt = select(EvidenceAsset).where(EvidenceAsset.project_id == project_id)
        if milestone_id:
            stmt = stmt.where(EvidenceAsset.milestone_id == milestone_id)
        if evidence_type:
            stmt = stmt.where(EvidenceAsset.evidence_type == evidence_type)
        stmt = stmt.order_by(EvidenceAsset.created_at.desc())
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def get_evidence(db: Session, evidence_id: uuid.UUID) -> EvidenceAsset:
        evidence = db.execute(select(EvidenceAsset).where(EvidenceAsset.id == evidence_id)).scalar_one_or_none()
        if not evidence:
            raise NotFoundException(message="Evidence not found")
        return evidence
