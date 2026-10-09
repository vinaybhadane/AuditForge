"""Purchase order line and delivery receipt quantity comparisons."""

from decimal import Decimal
from typing import Dict, List

from app.audit_engine.contracts.requests import (
    DeliveryChallanPayload,
    GoodsReceiptPayload,
    PurchaseOrderPayload,
)
from app.audit_engine.reconciliation.units import convert_quantity


def compare_po_vs_receipts(
    pos: List[PurchaseOrderPayload],
    receipts: List[GoodsReceiptPayload],
    canonical_unit: str,
) -> List[Dict]:
    """Compare ordered PO line quantities with accepted received quantities."""
    # Sum receipts by material
    received_by_mat: Dict[str, Decimal] = {}
    for r in receipts:
        for line in r.lines:
            mat = line.material_code
            qty = convert_quantity(line.received_quantity, line.unit, canonical_unit)
            received_by_mat[mat] = received_by_mat.get(mat, Decimal("0")) + qty

    results = []
    for po in pos:
        for po_line in po.lines:
            mat = po_line.material_code
            ordered = convert_quantity(po_line.ordered_quantity, po_line.unit, canonical_unit)
            received = received_by_mat.get(mat, Decimal("0"))
            remaining = ordered - received

            results.append({
                "po_number": po.po_number,
                "material_code": mat,
                "ordered_quantity": ordered,
                "received_quantity": received,
                "remaining_quantity": remaining,
                "unit": canonical_unit,
                "is_over_received": remaining < Decimal("0"),
            })

    return results


def compare_challans_vs_receipts(
    challans: List[DeliveryChallanPayload],
    receipts: List[GoodsReceiptPayload],
    canonical_unit: str,
) -> List[Dict]:
    """Compare delivered challan quantities against physically accepted receipt quantities.
    
    receipt_delta = received_quantity - challaned_quantity
    """
    challan_by_num: Dict[str, Decimal] = {}
    for c in challans:
        c_qty = sum(
            (convert_quantity(line.challaned_quantity, line.unit, canonical_unit) for line in c.lines),
            Decimal("0"),
        )
        challan_by_num[c.challan_number] = c_qty

    results = []
    for r in receipts:
        ref_ch = r.challan_number
        if ref_ch and ref_ch in challan_by_num:
            challaned_qty = challan_by_num[ref_ch]
            received_qty = sum(
                (convert_quantity(line.received_quantity, line.unit, canonical_unit) for line in r.lines),
                Decimal("0"),
            )
            delta = received_qty - challaned_qty

            results.append({
                "challan_number": ref_ch,
                "receipt_number": r.receipt_number,
                "challaned_quantity": challaned_qty,
                "received_quantity": received_qty,
                "delta": delta,
                "has_discrepancy": abs(delta) > Decimal("0.001"),
                "unit": canonical_unit,
            })

    return results
