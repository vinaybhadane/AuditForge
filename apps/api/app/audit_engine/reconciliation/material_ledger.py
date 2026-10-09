"""Material stock ledger calculations and transaction balance."""

from decimal import Decimal
from typing import List, Tuple

from app.audit_engine.contracts.requests import StockMovementPayload
from app.audit_engine.reconciliation.units import convert_quantity


def calculate_ledger_closing_stock(
    movements: List[StockMovementPayload],
    canonical_unit: str,
    opening_stock_default: Decimal = Decimal("0"),
) -> Tuple[Decimal, Decimal, Decimal, Decimal, Decimal, Decimal]:
    """Calculate material ledger closing stock using strict signed transaction algebra.
    
    Formula (docs/09_MATERIAL_RECONCILIATION.md):
    closing_stock = opening_stock + receipts + returns + transfer_in - issues - transfer_out + adjustments
    
    Returns:
        (closing_stock, opening_stock, receipts, issues, returns, adjustments)
    """
    opening_stock = opening_stock_default
    receipts = Decimal("0")
    issues = Decimal("0")
    returns = Decimal("0")
    transfer_in = Decimal("0")
    transfer_out = Decimal("0")
    adjustments = Decimal("0")

    for m in movements:
        norm_qty = convert_quantity(m.quantity, m.unit, canonical_unit)
        m_type = m.movement_type.lower()

        if m_type == "opening_balance":
            opening_stock = norm_qty
        elif m_type == "receipt":
            receipts += norm_qty
        elif m_type in ("issue", "consumption"):
            issues += norm_qty
        elif m_type in ("return", "return_from_site"):
            returns += norm_qty
        elif m_type == "return_to_supplier":
            # Direct return of received goods to vendor reduces stock
            receipts -= norm_qty
        elif m_type == "transfer_in":
            transfer_in += norm_qty
        elif m_type == "transfer_out":
            transfer_out += norm_qty
        elif m_type == "adjustment":
            # Signed adjustment
            adjustments += norm_qty

    closing_stock = (
        opening_stock
        + receipts
        + transfer_in
        + returns
        - issues
        - transfer_out
        + adjustments
    )

    return closing_stock, opening_stock, receipts, issues, returns, adjustments
