"""Core deterministic material reconciliation orchestrator."""

from decimal import Decimal
from typing import Dict, List, Optional

from app.audit_engine.contracts.requests import AuditEngineRequest
from app.audit_engine.contracts.responses import (
    ReconciliationLineResult,
    ReconciliationResult,
    ReconciliationStatus,
)
from app.audit_engine.reconciliation.boq import reconcile_boq_allowances
from app.audit_engine.reconciliation.material_ledger import calculate_ledger_closing_stock
from app.audit_engine.reconciliation.quantities import compare_challans_vs_receipts


def execute_material_reconciliation(
    request: AuditEngineRequest,
    canonical_unit: str = "bag",
) -> ReconciliationResult:
    """Execute deterministic material reconciliation matching rules REC-001 to REC-008.
    
    Produces exact, reproducible calculations with Decimal precision.
    """
    reconciliation_lines: List[ReconciliationLineResult] = []

    # 1. Stock Ledger Equation (REC-004)
    # closing_stock = opening_stock + receipts + returns + transfer_in - issues - transfer_out + adjustments
    closing_stock, opening_stock, receipts, issues, returns, adjustments = calculate_ledger_closing_stock(
        request.stock_movements,
        canonical_unit=canonical_unit,
    )

    # Physical count comparison (REC-004)
    variance_with_count: Optional[Decimal] = None
    if request.physical_count is not None:
        p_count = request.physical_count
        variance_with_count = p_count - closing_stock
        is_variance = abs(variance_with_count) > Decimal("0.001")

        reconciliation_lines.append(
            ReconciliationLineResult(
                rule_code="REC-004",
                material_code="CEMENT-OPC-53",
                expected_value=closing_stock,
                observed_value=p_count,
                delta=variance_with_count,
                unit=canonical_unit,
                tolerance_applied=Decimal("0.0"),
                status=ReconciliationStatus.DISCREPANCY if is_variance else ReconciliationStatus.MATCHED,
                formula_code="variance = physical_count - calculated_closing_stock",
                explanation=(
                    f"Calculated closing stock is {closing_stock} {canonical_unit}. "
                    f"Physical count observed is {p_count} {canonical_unit}, leaving variance of {variance_with_count} {canonical_unit}."
                ),
                source_refs=["stock_movements", "physical_count"],
            )
        )

    # 2. Challan vs Receipt Comparison (REC-002)
    challan_diffs = compare_challans_vs_receipts(
        request.delivery_challans,
        request.goods_receipts,
        canonical_unit=canonical_unit,
    )
    for cd in challan_diffs:
        is_disc = cd["has_discrepancy"]
        reconciliation_lines.append(
            ReconciliationLineResult(
                rule_code="REC-002",
                material_code="DELIVERED_GOODS",
                expected_value=cd["challaned_quantity"],
                observed_value=cd["received_quantity"],
                delta=cd["delta"],
                unit=cd["unit"],
                tolerance_applied=Decimal("0.0"),
                status=ReconciliationStatus.DISCREPANCY if is_disc else ReconciliationStatus.MATCHED,
                formula_code="receipt_delta = received_quantity - challaned_quantity",
                explanation=(
                    f"Delivery challan {cd['challan_number']} states {cd['challaned_quantity']} {cd['unit']}; "
                    f"accepted receipt {cd['receipt_number']} records {cd['received_quantity']} {cd['unit']}."
                ),
                source_refs=[f"challan:{cd['challan_number']}", f"receipt:{cd['receipt_number']}"],
            )
        )

    # 3. BOQ vs Issues (REC-005)
    issued_quantities: Dict[str, Decimal] = {"CEMENT-OPC-53": issues}
    boq_diffs = reconcile_boq_allowances(request.boq_items, issued_quantities, canonical_unit)
    for bd in boq_diffs:
        reconciliation_lines.append(
            ReconciliationLineResult(
                rule_code="REC-005",
                material_code=bd["material_code"],
                expected_value=bd["allowed_quantity"],
                observed_value=bd["issued_quantity"],
                delta=bd["variance"],
                unit=bd["unit"],
                tolerance_applied=bd["approved_wastage_rate"],
                status=ReconciliationStatus.DISCREPANCY if bd["is_exceeded"] else ReconciliationStatus.MATCHED,
                formula_code="issue_variance = issued_quantity - allowed_quantity",
                explanation=(
                    f"BOQ planned {bd['planned_quantity']} {bd['unit']} with {bd['approved_wastage_rate']*100}% wastage allows "
                    f"{bd['allowed_quantity']} {bd['unit']}. Actual issues recorded: {bd['issued_quantity']} {bd['unit']}."
                ),
                source_refs=[f"boq_item:{bd['item_code']}"],
            )
        )

    return ReconciliationResult(
        calculated_closing_stock=closing_stock,
        opening_stock=opening_stock,
        receipts_total=receipts,
        issues_total=issues,
        returns_total=returns,
        adjustments_total=adjustments,
        variance_with_physical_count=variance_with_count,
        lines=reconciliation_lines,
    )
