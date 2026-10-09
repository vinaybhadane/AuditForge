import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.session import get_db
from app.schemas.jobs import JobResponse
from app.services.audit_job_service import AuditJobService

router = APIRouter(tags=["Audit Jobs"])


@router.get(
    "/jobs/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Job Status and Metadata",
)
async def get_job_status(
    job_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JobResponse:
    job = AuditJobService.get_job(db, job_id)
    await verify_project_access(job.project_id, user, db)
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
