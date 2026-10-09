import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import NotFoundException
from app.db.models.evidence import AIObservation, Document
from app.db.models.projects import Project
from app.db.models.reconciliation import AnomalyFinding, ReconciliationRun
from app.db.models.review_and_certificates import ReviewDecision
from app.schemas.reports import AuditReportResponse


class ReportService:
    @staticmethod
    def generate_audit_report(
        db: Session,
        project_id: uuid.UUID,
        milestone_id: Optional[uuid.UUID] = None,
        reconciliation_run_id: Optional[uuid.UUID] = None,
    ) -> AuditReportResponse:
        project = db.execute(select(Project).where(Project.id == project_id)).scalar_one_or_none()
        if not project:
            raise NotFoundException(message="Project not found")

        # 1. Extracted Facts
        docs = list(db.execute(select(Document).where(Document.project_id == project_id)).scalars().all())
        extracted_facts = [
            {
                "document_id": str(d.id),
                "document_type": d.document_type,
                "document_number": d.normalized_document_number or d.raw_document_number,
                "vendor_name": d.vendor_name,
                "amount": float(d.total_amount) if d.total_amount is not None else None,
            }
            for d in docs
        ]

        # 2. Deterministic Calculations
        runs = list(db.execute(select(ReconciliationRun).where(ReconciliationRun.project_id == project_id)).scalars().all())
        deterministic_calculations = [
            {
                "run_id": str(r.id),
                "algorithm_version": r.algorithm_version,
                "period": f"{r.period_start.isoformat()} to {r.period_end.isoformat()}",
                "status": r.status,
                "summary": r.summary_metrics,
            }
            for r in runs
        ]

        # 3. AI Observations
        ai_obs = list(db.execute(select(AIObservation).where(AIObservation.project_id == project_id)).scalars().all())
        ai_observations = [
            {
                "id": str(o.id),
                "observation_text": o.observation_text,
                "confidence": o.confidence_value,
                "confidence_semantics": o.confidence_semantics,
                "limitations": o.limitations,
                "review_status": o.review_status,
            }
            for o in ai_obs
        ]

        # 4. Unresolved Discrepancies
        findings = list(
            db.execute(
                select(AnomalyFinding).where(
                    AnomalyFinding.project_id == project_id,
                    AnomalyFinding.status.in_(["open", "under_review"]),
                )
            ).scalars().all()
        )
        unresolved_discrepancies = [
            {
                "id": str(f.id),
                "finding_type": f.finding_type,
                "severity": f.severity,
                "explanation": f.explanation,
                "rule_code": f.rule_code,
            }
            for f in findings
        ]

        # 5. Human Decisions
        decisions = list(db.execute(select(ReviewDecision).where(ReviewDecision.project_id == project_id)).scalars().all())
        human_decisions = [
            {
                "id": str(dec.id),
                "decision_type": dec.decision_type,
                "reason": dec.reason,
                "reviewer_id": str(dec.reviewer_id),
                "created_at": dec.created_at.isoformat(),
            }
            for dec in decisions
        ]

        return AuditReportResponse(
            project_id=project_id,
            project_name=project.name,
            generated_at=datetime.now(timezone.utc),
            milestone_id=milestone_id,
            extracted_facts=extracted_facts,
            deterministic_calculations=deterministic_calculations,
            ai_observations=ai_observations,
            unresolved_discrepancies=unresolved_discrepancies,
            human_decisions=human_decisions,
        )
