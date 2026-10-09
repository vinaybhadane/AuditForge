import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.session import get_db
from app.schemas.reconciliation import (
    ReconciliationDetailResponse,
    ReconciliationLineResponse,
    ReconciliationRunResponse,
    ReconciliationStartRequest,
)
from app.services.reconciliation_service import ReconciliationService

router = APIRouter(tags=["Material Reconciliation"])


@router.post(
    "/projects/{id}/reconciliations",
    response_model=ReconciliationRunResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Start Deterministic Material Reconciliation",
)
async def start_reconciliation(
    id: uuid.UUID,
    data: ReconciliationStartRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReconciliationRunResponse:
    # Requires Auditor, Project Manager, or Org Admin
    await verify_project_access(
        id, user, db, allowed_roles={"project_auditor", "project_manager", "org_admin"}
    )
    run = ReconciliationService.execute_reconciliation(db, id, user.id, data)
    return ReconciliationRunResponse.model_validate(run)


@router.get(
    "/reconciliations/{run_id}",
    response_model=ReconciliationDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Reconciliation Run and Lines",
)
async def get_reconciliation_details(
    run_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReconciliationDetailResponse:
    run = ReconciliationService.get_run(db, run_id)
    await verify_project_access(run.project_id, user, db)
    lines = ReconciliationService.get_run_lines(db, run_id)
    return ReconciliationDetailResponse(
        run=ReconciliationRunResponse.model_validate(run),
        lines=[ReconciliationLineResponse.model_validate(line) for line in lines],
    )

