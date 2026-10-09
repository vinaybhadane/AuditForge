import hashlib
import uuid
from datetime import datetime, timezone
from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.errors import AuditForgeException, ErrorCode, NotFoundException
from app.db.models.evidence import EvidenceAsset
from app.db.models.projects import AcceptanceCriterion, Milestone
from app.db.models.reconciliation import AnomalyFinding
from app.db.models.review_and_certificates import ClearanceCertificate, ReviewDecision
from app.schemas.milestones import (
    CertificateIssueRequest,
    ClearanceEligibilityResponse,
    ReviewDecisionCreate,
)


class ReviewService:
    @staticmethod
    def record_decision(
        db: Session,
        milestone_id: uuid.UUID,
        reviewer_id: uuid.UUID,
        data: ReviewDecisionCreate,
    ) -> ReviewDecision:
        milestone = db.execute(select(Milestone).where(Milestone.id == milestone_id)).scalar_one_or_none()
        if not milestone:
            raise NotFoundException(message="Milestone not found")

        decision = ReviewDecision(
            project_id=milestone.project_id,
            milestone_id=milestone_id,
            decision_type=data.decision_type,
            reason=data.reason,
            reviewer_id=reviewer_id,
            criteria_version=data.criteria_version,
            referenced_finding_ids=data.referenced_finding_ids,
        )
        db.add(decision)

        # Update milestone status based on decision
        if data.decision_type == "approve":
            milestone.status = "under_audit"
        elif data.decision_type in ["hold", "reject", "request_evidence", "request_inspection"]:
            milestone.status = "blocked"

        db.commit()
        db.refresh(decision)
        return decision

    @staticmethod
    def check_eligibility(db: Session, milestone_id: uuid.UUID) -> ClearanceEligibilityResponse:
        milestone = db.execute(select(Milestone).where(Milestone.id == milestone_id)).scalar_one_or_none()
        if not milestone:
            raise NotFoundException(message="Milestone not found")

        blockers: List[str] = []

        # 1. Check open critical or high findings
        open_findings = list(
            db.execute(
                select(AnomalyFinding).where(
                    and_(
                        AnomalyFinding.project_id == milestone.project_id,
                        AnomalyFinding.status.in_(["open", "under_review"]),
                        AnomalyFinding.severity.in_(["high", "critical"]),
                    )
                )
            ).scalars().all()
        )
        if open_findings:
            blockers.append(f"There are {len(open_findings)} unresolved high/critical anomaly findings.")

        # 2. Check for required criteria
        criteria = list(
            db.execute(
                select(AcceptanceCriterion).where(
                    and_(
                        AcceptanceCriterion.milestone_id == milestone_id,
                        AcceptanceCriterion.is_required,
                        AcceptanceCriterion.is_active,
                    )
                )

            ).scalars().all()
        )

        # 3. Check verified evidence count
        verified_evidence = list(
            db.execute(
                select(EvidenceAsset).where(
                    and_(
                        EvidenceAsset.milestone_id == milestone_id,
                        EvidenceAsset.upload_status == "verified",
                    )
                )
            ).scalars().all()
        )

        if not verified_evidence and criteria:
            blockers.append("No verified evidence uploaded for required milestone criteria.")

        # 4. Check latest review decision
        latest_decision = db.execute(
            select(ReviewDecision)
            .where(ReviewDecision.milestone_id == milestone_id)
            .order_by(ReviewDecision.created_at.desc())
        ).scalars().first()

        if not latest_decision:
            blockers.append("No human review decision has been recorded.")
        elif latest_decision.decision_type != "approve":
            blockers.append(f"Latest review decision is '{latest_decision.decision_type}'; must be 'approve'.")

        is_eligible = len(blockers) == 0

        return ClearanceEligibilityResponse(
            milestone_id=milestone_id,
            is_eligible=is_eligible,
            status=milestone.status,
            blockers=blockers,
            unresolved_discrepancies=len(open_findings),
            open_critical_findings=sum(1 for f in open_findings if f.severity == "critical"),
            verified_evidence_count=len(verified_evidence),
            latest_decision=latest_decision.decision_type if latest_decision else None,
        )

    @staticmethod
    def issue_certificate(
        db: Session,
        milestone_id: uuid.UUID,
        issuer_id: uuid.UUID,
        data: CertificateIssueRequest,
    ) -> ClearanceCertificate:
        milestone = db.execute(select(Milestone).where(Milestone.id == milestone_id)).scalar_one_or_none()
        if not milestone:
            raise NotFoundException(message="Milestone not found")

        # Strict eligibility check: Cannot issue if blockers exist!
        eligibility = ReviewService.check_eligibility(db, milestone_id)
        if not eligibility.is_eligible:
            raise AuditForgeException(
                code=ErrorCode.CLEARANCE_BLOCKED,
                message="Milestone is not eligible for clearance certificate issuance.",
                status_code=422,
                details=[{"field": "eligibility", "code": "CLEARANCE_BLOCKED", "message": b} for b in eligibility.blockers],
            )

        # Verify review decision
        decision = db.execute(
            select(ReviewDecision).where(ReviewDecision.id == data.review_decision_id)
        ).scalar_one_or_none()
        if not decision or decision.decision_type != "approve":
            raise AuditForgeException(
                code=ErrorCode.CLEARANCE_BLOCKED,
                message="Referenced review decision is not an approved clearance.",
                status_code=422,
            )

        cert_number = f"CERT-{milestone.code}-{uuid.uuid4().hex[:8].upper()}"
        snapshot_hash = hashlib.sha256(f"{cert_number}:{milestone_id}".encode("utf-8")).hexdigest()
        report_object_key = f"projects/{milestone.project_id}/certificates/{cert_number}.pdf"

        cert = ClearanceCertificate(
            project_id=milestone.project_id,
            milestone_id=milestone_id,
            certificate_number=cert_number,
            decision_id=decision.id,
            report_object_key=report_object_key,
            snapshot_hash=snapshot_hash,
            version=1,
            status="issued",
            issued_by=issuer_id,
            issued_at=datetime.now(timezone.utc),
        )
        milestone.status = "cleared"

        db.add(cert)
        db.commit()
        db.refresh(cert)
        return cert
