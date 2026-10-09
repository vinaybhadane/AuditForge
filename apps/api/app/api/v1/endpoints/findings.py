import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.session import get_db
from app.schemas.findings import (
    AnomalyFindingResponse,
    FindingDispositionRequest,
    FindingListResponse,
)
from app.services.anomaly_service import AnomalyService

router = APIRouter(tags=["Anomaly Findings & Dispositions"])


@router.get(
    "/projects/{id}/findings",
    response_model=FindingListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Anomaly Findings",
)
async def list_findings(
    id: uuid.UUID,
    severity: Optional[str] = Query(None),
    finding_status: Optional[str] = Query(None, alias="status"),
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FindingListResponse:
    await verify_project_access(id, user, db)
    findings = AnomalyService.list_findings(db, id, severity, finding_status)
    items = [AnomalyFindingResponse.model_validate(f) for f in findings]
    return FindingListResponse(items=items, total=len(items))


@router.get(
    "/findings/{id}",
    response_model=AnomalyFindingResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Anomaly Finding Details",
)
async def get_finding(
    id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AnomalyFindingResponse:
    finding = AnomalyService.get_finding(db, id)
    await verify_project_access(finding.project_id, user, db)
    return AnomalyFindingResponse.model_validate(finding)


@router.patch(
    "/findings/{id}/disposition",
    response_model=AnomalyFindingResponse,
    status_code=status.HTTP_200_OK,
    summary="Record Reviewer Disposition on Finding",
)
async def record_disposition(
    id: uuid.UUID,
    data: FindingDispositionRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AnomalyFindingResponse:
    finding = AnomalyService.get_finding(db, id)
    # Requires Auditor, Project Manager, or Org Admin
    await verify_project_access(
        finding.project_id, user, db, allowed_roles={"project_auditor", "project_manager", "org_admin"}
    )
    updated = AnomalyService.record_disposition(db, id, user.id, data)
    return AnomalyFindingResponse.model_validate(updated)
