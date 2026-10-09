import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import NotFoundException
from app.db.models.reconciliation import AnomalyFinding
from app.schemas.findings import FindingDispositionRequest


class AnomalyService:
    @staticmethod
    def list_findings(
        db: Session,
        project_id: uuid.UUID,
        severity: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[AnomalyFinding]:
        stmt = select(AnomalyFinding).where(AnomalyFinding.project_id == project_id)
        if severity:
            stmt = stmt.where(AnomalyFinding.severity == severity)
        if status:
            stmt = stmt.where(AnomalyFinding.status == status)
        stmt = stmt.order_by(AnomalyFinding.detected_at.desc())
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def get_finding(db: Session, finding_id: uuid.UUID) -> AnomalyFinding:
        finding = db.execute(select(AnomalyFinding).where(AnomalyFinding.id == finding_id)).scalar_one_or_none()
        if not finding:
            raise NotFoundException(message="Anomaly finding not found")
        return finding

    @staticmethod
    def record_disposition(
        db: Session,
        finding_id: uuid.UUID,
        reviewer_id: uuid.UUID,
        data: FindingDispositionRequest,
    ) -> AnomalyFinding:
        finding = AnomalyService.get_finding(db, finding_id)
        finding.status = data.status
        finding.resolved_at = datetime.now(timezone.utc)
        finding.resolved_by = reviewer_id
        finding.resolution_notes = data.resolution_notes
        db.commit()
        db.refresh(finding)
        return finding
