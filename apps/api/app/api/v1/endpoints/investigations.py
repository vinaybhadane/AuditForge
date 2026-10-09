import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.session import get_db
from app.schemas.investigations import (
    InvestigationActivityCreate,
    InvestigationActivityResponse,
    InvestigationCreate,
    InvestigationResponse,
    InvestigationUpdate,
)
from app.services.investigation_service import InvestigationService

router = APIRouter(tags=["Investigations & Case Management"])


@router.post(
    "/projects/{id}/investigations",
    response_model=InvestigationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Open Investigation Case",
)
async def open_investigation(
    id: uuid.UUID,
    data: InvestigationCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> InvestigationResponse:
    await verify_project_access(
        id, user, db, allowed_roles={"project_auditor", "project_manager", "org_admin"}
    )
    inv = InvestigationService.create_investigation(db, id, user.id, data)
    return InvestigationResponse.model_validate(inv)


@router.get(
    "/investigations/{id}",
    response_model=InvestigationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Investigation Case",
)
async def get_investigation(
    id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> InvestigationResponse:
    inv = InvestigationService.get_investigation(db, id)
    await verify_project_access(inv.project_id, user, db)
    return InvestigationResponse.model_validate(inv)


@router.patch(
    "/investigations/{id}",
    response_model=InvestigationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Investigation Case",
)
async def update_investigation(
    id: uuid.UUID,
    data: InvestigationUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> InvestigationResponse:
    inv = InvestigationService.get_investigation(db, id)
    await verify_project_access(
        inv.project_id, user, db, allowed_roles={"project_auditor", "project_manager", "org_admin"}
    )
    updated = InvestigationService.update_investigation(db, id, user.id, data)
    return InvestigationResponse.model_validate(updated)


@router.post(
    "/investigations/{id}/activities",
    response_model=InvestigationActivityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Investigation Case Activity",
)
async def add_investigation_activity(
    id: uuid.UUID,
    data: InvestigationActivityCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> InvestigationActivityResponse:
    inv = InvestigationService.get_investigation(db, id)
    await verify_project_access(inv.project_id, user, db, require_write=True)
    activity = InvestigationService.add_activity(db, id, user.id, data)
    return InvestigationActivityResponse.model_validate(activity)
