import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.session import get_db
from app.schemas.reports import AuditReportResponse, ReportGenerateRequest
from app.services.report_service import ReportService

router = APIRouter(tags=["Audit Reports"])


@router.post(
    "/projects/{id}/reports",
    response_model=AuditReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate / Retrieve Evidence-Linked Audit Report",
)
async def generate_report(
    id: uuid.UUID,
    data: ReportGenerateRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AuditReportResponse:
    await verify_project_access(id, user, db)
    return ReportService.generate_audit_report(
        db=db,
        project_id=id,
        milestone_id=data.milestone_id,
        reconciliation_run_id=data.reconciliation_run_id,
    )
