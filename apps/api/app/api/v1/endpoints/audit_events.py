import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.models.review_and_certificates import AuditEvent
from app.db.session import get_db

router = APIRouter(tags=["Audit Events"])


class AuditEventResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    project_id: uuid.UUID
    actor_id: uuid.UUID
    action: str
    target_type: str
    target_id: str
    request_id: str
    outcome: str
    metadata_payload: Any = None
    created_at: Any

    model_config = {"from_attributes": True}


@router.get(
    "/projects/{id}/audit-events",
    response_model=List[AuditEventResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Project Audit Trail",
)
async def list_audit_events(
    id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[AuditEventResponse]:
    await verify_project_access(id, user, db, allowed_roles={"project_auditor", "project_manager", "org_admin"})
    events = list(
        db.execute(select(AuditEvent).where(AuditEvent.project_id == id).order_by(AuditEvent.created_at.desc())).scalars().all()
    )
    return [AuditEventResponse.model_validate(e) for e in events]
