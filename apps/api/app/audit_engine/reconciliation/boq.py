"""BOQ planned allowances and wastage reconciliation."""

from decimal import Decimal
from typing import Dict, List

from app.audit_engine.contracts.requests import BOQItemPayload
from app.audit_engine.reconciliation.units import convert_quantity


def reconcile_boq_allowances(
    boq_items: List[BOQItemPayload],
    issued_quantities_by_material: Dict[str, Decimal],
    canonical_unit: str,
) -> List[Dict]:
    """Reconcile cumulative material issues against supported BOQ allowances.
    
    Formula:
    allowed_quantity = planned_quantity * (1 + approved_wastage_rate)
    issue_variance = issued_quantity - allowed_quantity
    """
    results = []

    for boq in boq_items:
        mat = boq.material_code
        norm_planned = convert_quantity(boq.planned_quantity, boq.unit, canonical_unit)
        allowed_qty = norm_planned * (Decimal("1.0") + boq.approved_wastage_rate)
        issued_qty = issued_quantities_by_material.get(mat, Decimal("0"))

        variance = issued_qty - allowed_qty
        is_exceeded = variance > Decimal("0")

        results.append({
            "item_code": boq.item_code,
            "material_code": mat,
            "planned_quantity": norm_planned,
            "approved_wastage_rate": boq.approved_wastage_rate,
            "allowed_quantity": allowed_qty,
            "issued_quantity": issued_qty,
            "variance": variance,
            "is_exceeded": is_exceeded,
            "unit": canonical_unit,
        })

    return results
