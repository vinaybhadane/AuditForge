import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import NotFoundException
from app.db.models.investigations import Investigation, InvestigationActivity, InvestigationFinding
from app.schemas.investigations import (
    InvestigationActivityCreate,
    InvestigationCreate,
    InvestigationUpdate,
)


class InvestigationService:
    @staticmethod
    def create_investigation(
        db: Session,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        data: InvestigationCreate,
    ) -> Investigation:
        inv = Investigation(
            project_id=project_id,
            case_number=data.case_number,
            title=data.title,
            summary=data.summary,
            severity=data.severity,
            status="open",
            opened_by=user_id,
            opened_at=datetime.now(timezone.utc),
        )
        db.add(inv)
        db.flush()

        if data.finding_ids:
            for fid in data.finding_ids:
                link = InvestigationFinding(
                    investigation_id=inv.id,
                    finding_id=fid,
                    added_by=user_id,
                )
                db.add(link)

        # Record opening activity
        activity = InvestigationActivity(
            investigation_id=inv.id,
            actor_id=user_id,
            activity_type="case_opened",
            notes=f"Investigation case {data.case_number} opened: {data.title}",
        )
        db.add(activity)

        db.commit()
        db.refresh(inv)
        return inv

    @staticmethod
    def get_investigation(db: Session, investigation_id: uuid.UUID) -> Investigation:
        inv = db.execute(select(Investigation).where(Investigation.id == investigation_id)).scalar_one_or_none()
        if not inv:
            raise NotFoundException(message="Investigation case not found")
        return inv

    @staticmethod
    def update_investigation(
        db: Session,
        investigation_id: uuid.UUID,
        user_id: uuid.UUID,
        data: InvestigationUpdate,
    ) -> Investigation:
        inv = InvestigationService.get_investigation(db, investigation_id)
        if data.title:
            inv.title = data.title
        if data.summary:
            inv.summary = data.summary
        if data.severity:
            inv.severity = data.severity
        if data.assigned_to:
            inv.assigned_to = data.assigned_to
        if data.status:
            inv.status = data.status
            if data.status in ["closed", "dismissed"]:
                inv.closed_at = datetime.now(timezone.utc)
                inv.resolution_summary = data.resolution_summary

        act = InvestigationActivity(
            investigation_id=inv.id,
            actor_id=user_id,
            activity_type="case_updated",
            notes="Case details updated.",
        )
        db.add(act)

        db.commit()
        db.refresh(inv)
        return inv

    @staticmethod
    def add_activity(
        db: Session,
        investigation_id: uuid.UUID,
        user_id: uuid.UUID,
        data: InvestigationActivityCreate,
    ) -> InvestigationActivity:
        InvestigationService.get_investigation(db, investigation_id)
        act = InvestigationActivity(
            investigation_id=investigation_id,
            actor_id=user_id,
            activity_type=data.activity_type,
            notes=data.notes,
        )
        db.add(act)
        db.commit()
        db.refresh(act)
        return act
