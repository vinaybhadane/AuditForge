import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.session import get_db
from app.schemas.evidence import (
    EvidenceCompleteUploadRequest,
    EvidenceListResponse,
    EvidenceResponse,
    EvidenceUploadInitiateRequest,
    EvidenceUploadInitiateResponse,
)
from app.schemas.jobs import EvidenceProcessRequest, JobResponse
from app.services.audit_job_service import AuditJobService
from app.services.evidence_service import EvidenceService

router = APIRouter(tags=["Evidence Ingestion & Management"])


@router.post(
    "/projects/{project_id}/evidence/uploads",
    response_model=EvidenceUploadInitiateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Initiate Evidence Ingestion",
    description="Enforces modality rules: site progress photos strictly require live_capture; vendor documents support file_upload and live_capture.",
)
async def initiate_evidence_upload(
    project_id: uuid.UUID,
    data: EvidenceUploadInitiateRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EvidenceUploadInitiateResponse:
    ctx = await verify_project_access(project_id, user, db, require_write=True)
    return EvidenceService.initiate_upload(
        db=db,
        project_id=project_id,
        organization_id=ctx.project.organization_id,
        uploader_id=user.id,
        data=data,
    )


@router.post(
    "/evidence/{id}/complete-upload",
    response_model=EvidenceResponse,
    status_code=status.HTTP_200_OK,
    summary="Complete and Verify Evidence Upload",
)
async def complete_evidence_upload(
    id: uuid.UUID,
    data: EvidenceCompleteUploadRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EvidenceResponse:
    evidence = EvidenceService.get_evidence(db, id)
    await verify_project_access(evidence.project_id, user, db, require_write=True)
    updated = EvidenceService.complete_upload(db, id, data)
    return EvidenceResponse.model_validate(updated)


@router.get(
    "/projects/{project_id}/evidence",
    response_model=EvidenceListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Evidence Assets",
)
async def list_evidence(
    project_id: uuid.UUID,
    milestone_id: Optional[uuid.UUID] = Query(None),
    evidence_type: Optional[str] = Query(None),
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EvidenceListResponse:
    await verify_project_access(project_id, user, db)
    items = EvidenceService.list_evidence(db, project_id, milestone_id, evidence_type)
    evidence_schemas = [EvidenceResponse.model_validate(e) for e in items]
    return EvidenceListResponse(items=evidence_schemas, total=len(evidence_schemas))


@router.get(
    "/evidence/{id}",
    response_model=EvidenceResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Evidence Asset Details",
)
async def get_evidence(
    id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EvidenceResponse:
    evidence = EvidenceService.get_evidence(db, id)
    await verify_project_access(evidence.project_id, user, db)
    return EvidenceResponse.model_validate(evidence)


@router.post(
    "/evidence/{id}/process",
    response_model=JobResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger Evidence Processing Job",
)
async def process_evidence(
    id: uuid.UUID,
    data: EvidenceProcessRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JobResponse:
    evidence = EvidenceService.get_evidence(db, id)
    await verify_project_access(evidence.project_id, user, db, require_write=True)
    job = await AuditJobService.create_and_run_job(
        db=db,
        evidence=evidence,
        job_type=data.job_type,
        idempotency_key=data.idempotency_key,
    )
    return JobResponse(
        id=job.id,
        project_id=job.project_id,
        evidence_id=job.evidence_id,
        status=job.status,
        job_type=job.job_type,
        attempt_count=job.attempt_count,
        created_at=job.created_at,
        started_at=job.started_at,
        finished_at=job.finished_at,
        error=job.error_details.get("message") if job.error_details else None,
        result_available=(job.status == "succeeded"),
    )
