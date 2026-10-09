import hashlib
import uuid
from decimal import Decimal
from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.errors import NotFoundException
from app.db.models.inventory import StockMovement
from app.db.models.projects import BOQItem
from app.db.models.reconciliation import AnomalyFinding, ReconciliationLine, ReconciliationRun
from app.schemas.reconciliation import ReconciliationStartRequest


class ReconciliationService:
    @staticmethod
    def execute_reconciliation(
        db: Session,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        data: ReconciliationStartRequest,
    ) -> ReconciliationRun:
        # Check idempotency
        if data.idempotency_key:
            existing = db.execute(
                select(ReconciliationRun).where(
                    and_(
                        ReconciliationRun.project_id == project_id,
                        ReconciliationRun.idempotency_key == data.idempotency_key,
                    )
                )
            ).scalar_one_or_none()
            if existing:
                return existing

        # Compute deterministic snapshot hash of inputs
        snapshot_content = f"{project_id}:{data.period_start.isoformat()}:{data.period_end.isoformat()}"
        snapshot_hash = hashlib.sha256(snapshot_content.encode("utf-8")).hexdigest()

        run = ReconciliationRun(
            project_id=project_id,
            baseline_version_id=data.baseline_version_id,
            period_start=data.period_start,
            period_end=data.period_end,
            input_snapshot_hash=snapshot_hash,
            algorithm_version="1.0",
            status="running",
            created_by=user_id,
            idempotency_key=data.idempotency_key,
        )
        db.add(run)
        db.flush()

        lines: List[ReconciliationLine] = []

        # 1. Fetch BOQ Items for planned quantities
        boq_items = list(db.execute(select(BOQItem).where(BOQItem.project_id == project_id)).scalars().all())

        # 2. Fetch Stock Movements in period
        movements = list(
            db.execute(
                select(StockMovement).where(
                    and_(
                        StockMovement.project_id == project_id,
                        StockMovement.effective_date >= data.period_start.date(),
                        StockMovement.effective_date <= data.period_end.date(),
                    )
                )
            ).scalars().all()
        )


        # Group movements by material
        mat_movements = {}
        for m in movements:
            mat_movements.setdefault(m.material_code, []).append(m)

        # Calculate REC-005: Issue vs BOQ allowance
        for boq in boq_items:
            mat_code = boq.material_code or boq.item_code
            moves = mat_movements.get(mat_code, [])
            total_issued = sum(m.quantity for m in moves if m.movement_type == "issue")
            allowed = boq.planned_quantity * (Decimal("1.0") + boq.approved_wastage_rate)
            delta = total_issued - allowed

            status = "matched"
            if delta > Decimal("0.0"):
                status = "discrepancy"
                # Flag candidate anomaly
                finding = AnomalyFinding(
                    project_id=project_id,
                    finding_type="excess_issue",
                    severity="high" if delta > allowed * Decimal("0.1") else "medium",
                    status="open",
                    rule_code="AN-006",
                    explanation=f"Issued quantity ({total_issued} {boq.unit}) exceeds planned BOQ allowance ({allowed:.2f} {boq.unit}) for {mat_code}.",
                    calculation_details={
                        "planned": float(boq.planned_quantity),
                        "allowed": float(allowed),
                        "issued": float(total_issued),
                        "delta": float(delta),
                    },
                    limitations=["Issue is not conclusive proof of physical consumption or diversion."],
                    recommended_action="Inspect site supervisor issue slips and unconsumed floor stock.",
                )
                db.add(finding)

            line = ReconciliationLine(
                run_id=run.id,
                rule_code="REC-005",
                line_type="issue_vs_boq_allowance",
                material_code=mat_code,
                raw_expected_quantity=boq.planned_quantity,
                raw_observed_quantity=total_issued,
                normalized_expected_quantity=allowed,
                normalized_observed_quantity=total_issued,
                unit=boq.unit,
                delta_quantity=delta,
                tolerance=Decimal("0.0"),
                status=status,
                explanation=f"BOQ allowance: {allowed:.2f} {boq.unit}, Actual issues: {total_issued:.2f} {boq.unit}",
            )
            lines.append(line)
            db.add(line)

        # Calculate REC-004: Stock ledger balance calculation
        for mat_code, moves in mat_movements.items():
            receipts = sum(m.quantity for m in moves if m.movement_type == "receipt")
            issues = sum(m.quantity for m in moves if m.movement_type == "issue")
            returns = sum(m.quantity for m in moves if m.movement_type == "return")
            adj = sum(m.quantity for m in moves if m.movement_type == "adjustment")
            closing = receipts + returns + adj - issues

            if closing < Decimal("0.0"):
                # AN-005 Negative stock finding
                finding = AnomalyFinding(
                    project_id=project_id,
                    finding_type="negative_stock",
                    severity="critical",
                    status="open",
                    rule_code="AN-005",
                    explanation=f"Calculated closing stock is negative ({closing} units) for material {mat_code}.",
                    calculation_details={"closing_stock": float(closing)},
                    limitations=["Could indicate delayed receipt posting or ledger entry timing skew."],
                    recommended_action="Verify pending Goods Receipt Notes with Store In-Charge.",
                )
                db.add(finding)

            line = ReconciliationLine(
                run_id=run.id,
                rule_code="REC-004",
                line_type="stock_ledger_closing",
                material_code=mat_code,
                normalized_expected_quantity=closing,
                normalized_observed_quantity=closing,
                unit=moves[0].unit if moves else "unit",
                delta_quantity=Decimal("0.0"),
                tolerance=Decimal("0.0"),
                status="matched" if closing >= Decimal("0.0") else "discrepancy",
                explanation=f"Calculated closing stock: {closing:.2f}",
            )
            lines.append(line)
            db.add(line)

        run.status = "completed"
        run.summary_metrics = {
            "total_lines": len(lines),
            "discrepancies_count": sum(1 for line in lines if line.status == "discrepancy"),
        }

        db.commit()
        db.refresh(run)
        return run

    @staticmethod
    def get_run(db: Session, run_id: uuid.UUID) -> ReconciliationRun:
        run = db.execute(select(ReconciliationRun).where(ReconciliationRun.id == run_id)).scalar_one_or_none()
        if not run:
            raise NotFoundException(message="Reconciliation run not found")
        return run

    @staticmethod
    def get_run_lines(db: Session, run_id: uuid.UUID) -> List[ReconciliationLine]:
        stmt = select(ReconciliationLine).where(ReconciliationLine.run_id == run_id)
        return list(db.execute(stmt).scalars().all())
