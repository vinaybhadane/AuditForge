import uuid
from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.errors import AuditForgeException, ErrorCode, NotFoundException
from app.db.models.projects import AcceptanceCriterion, Milestone
from app.schemas.milestones import AcceptanceCriterionCreate, MilestoneCreate


class MilestoneService:
    @staticmethod
    def create_milestone(db: Session, project_id: uuid.UUID, data: MilestoneCreate) -> Milestone:
        existing = db.execute(
            select(Milestone).where(
                and_(
                    Milestone.project_id == project_id,
                    Milestone.code == data.code,
                )
            )
        ).scalar_one_or_none()
        if existing:
            raise AuditForgeException(
                code=ErrorCode.STATE_CONFLICT,
                message=f"Milestone code '{data.code}' already exists in this project",
                status_code=409,
            )

        milestone = Milestone(
            project_id=project_id,
            code=data.code,
            name=data.name,
            description=data.description,
            planned_start_date=data.planned_start_date,
            planned_end_date=data.planned_end_date,
            status="planned",
        )
        db.add(milestone)
        db.commit()
        db.refresh(milestone)
        return milestone

    @staticmethod
    def list_milestones(db: Session, project_id: uuid.UUID) -> List[Milestone]:
        stmt = select(Milestone).where(Milestone.project_id == project_id).order_by(Milestone.created_at.asc())
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def get_milestone(db: Session, milestone_id: uuid.UUID) -> Milestone:
        milestone = db.execute(select(Milestone).where(Milestone.id == milestone_id)).scalar_one_or_none()
        if not milestone:
            raise NotFoundException(message="Milestone not found")
        return milestone

    @staticmethod
    def add_criterion(db: Session, milestone_id: uuid.UUID, data: AcceptanceCriterionCreate, creator_id: uuid.UUID) -> AcceptanceCriterion:
        milestone = MilestoneService.get_milestone(db, milestone_id)
        
        criterion = AcceptanceCriterion(
            milestone_id=milestone_id,
            project_id=milestone.project_id,
            version=milestone.criteria_version,
            criterion_code=data.criterion_code,
            description=data.description,
            required_evidence_types=data.required_evidence_types,
            verification_method=data.verification_method,
            is_required=data.is_required,
            created_by=creator_id,
        )
        db.add(criterion)
        db.commit()
        db.refresh(criterion)
        return criterion
