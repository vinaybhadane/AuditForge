import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import NotFoundException
from app.db.models.evidence import (
    AIObservation,
    Document,
    EvidenceAsset,
    EvidenceProcessingJob,
    ExtractedFieldVersion,
)
from app.integrations.ai_engine_client import ai_engine_client
from app.integrations.ai_engine_contracts import DocumentExtractionInput, VisualAssessmentInput


class AuditJobService:
    @staticmethod
    async def create_and_run_job(
        db: Session,
        evidence: EvidenceAsset,
        job_type: str = "visual_assessment",
        idempotency_key: Optional[str] = None,
    ) -> EvidenceProcessingJob:
        # Check idempotency
        if idempotency_key:
            existing = db.execute(
                select(EvidenceProcessingJob).where(
                    and_(
                        EvidenceProcessingJob.project_id == evidence.project_id,
                        EvidenceProcessingJob.idempotency_key == idempotency_key,
                    )
                )
            ).scalar_one_or_none()
            if existing:
                return existing

        job = EvidenceProcessingJob(
            organization_id=evidence.organization_id,
            project_id=evidence.project_id,
            evidence_id=evidence.id,
            job_type=job_type,
            status="running",
            attempt_count=1,
            max_attempts=settings.JOB_MAX_ATTEMPTS,
            idempotency_key=idempotency_key,
            started_at=datetime.now(timezone.utc),
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        try:
            if job_type == "visual_assessment":
                assessment_input = VisualAssessmentInput(
                    job_id=job.id,
                    evidence_id=evidence.id,
                    project_id=evidence.project_id,
                    milestone_id=evidence.milestone_id,
                    media_url=f"storage://{settings.EVIDENCE_BUCKET}/{evidence.object_key}",
                    media_type=evidence.media_type,
                )
                output = await ai_engine_client.run_visual_assessment(assessment_input)

                # Persist immutable AI observations
                for obs in output.observations:
                    ai_obs = AIObservation(
                        evidence_id=evidence.id,
                        project_id=evidence.project_id,
                        milestone_id=evidence.milestone_id,
                        job_id=job.id,
                        observation_type="visual_assessment",
                        observation_text=obs.observation,
                        criterion_id=obs.criterion_id,
                        confidence_value=obs.confidence_value,
                        confidence_semantics=obs.confidence_semantics,
                        limitations=obs.limitations,
                        provider_metadata=output.provider,
                        review_status="unreviewed",
                    )
                    db.add(ai_obs)

                job.status = "succeeded"
                job.provider_name = output.provider.get("name")
                job.model_name = output.provider.get("model")
                job.finished_at = datetime.now(timezone.utc)
                db.commit()

            elif job_type in ["document_extraction", "ocr_scan"]:
                doc_input = DocumentExtractionInput(
                    job_id=job.id,
                    evidence_id=evidence.id,
                    project_id=evidence.project_id,
                    document_type=evidence.evidence_type,
                    document_url=f"storage://{settings.EVIDENCE_BUCKET}/{evidence.object_key}",
                    media_type=evidence.media_type,
                )
                doc_output = await ai_engine_client.run_document_extraction(doc_input)

                # Create document record
                doc = Document(
                    evidence_id=evidence.id,
                    project_id=evidence.project_id,
                    document_type=doc_output.document_type,
                    raw_document_number=doc_output.raw_document_number,
                    normalized_document_number=doc_output.normalized_document_number,
                    vendor_name=doc_output.vendor_name,
                    document_date=doc_output.document_date,
                    currency=doc_output.currency,
                    total_amount=doc_output.total_amount,
                    processing_status="extracted",
                )
                db.add(doc)
                db.flush()

                # Add versioned extracted fields
                for field in doc_output.fields:
                    ext_field = ExtractedFieldVersion(
                        document_id=doc.id,
                        field_name=field.field_name,
                        raw_value=field.raw_value,
                        normalized_value=field.normalized_value,
                        confidence=field.confidence,
                        confidence_semantics=field.confidence_semantics,
                        page_number=field.page_number,
                        version=1,
                        review_status="extracted",
                    )
                    db.add(ext_field)

                job.status = "succeeded"
                job.provider_name = doc_output.provider.get("name")
                job.model_name = doc_output.provider.get("model")
                job.finished_at = datetime.now(timezone.utc)
                db.commit()

        except Exception as e:
            job.status = "failed"
            job.error_details = {"message": str(e), "occurred_at": datetime.now(timezone.utc).isoformat()}
            job.finished_at = datetime.now(timezone.utc)
            db.commit()
            raise

        db.refresh(job)
        return job

    @staticmethod
    def get_job(db: Session, job_id: uuid.UUID) -> EvidenceProcessingJob:
        job = db.execute(select(EvidenceProcessingJob).where(EvidenceProcessingJob.id == job_id)).scalar_one_or_none()
        if not job:
            raise NotFoundException(message="Processing job not found")
        return job
