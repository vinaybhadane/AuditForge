"""Unit tests for deterministic material reconciliation calculations."""

from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest

from app.audit_engine.contracts.requests import BOQItemPayload, StockMovementPayload
from app.audit_engine.exceptions import UnitConversionError
from app.audit_engine.reconciliation.boq import reconcile_boq_allowances
from app.audit_engine.reconciliation.material_ledger import calculate_ledger_closing_stock
from app.audit_engine.reconciliation.units import convert_quantity


def test_unit_conversion_math():
    # 2.5 tonnes = 2500 kg
    assert convert_quantity(Decimal("2.5"), "tonne", "kg") == Decimal("2500.0")
    # 5000 mm = 5 m
    assert convert_quantity(Decimal("5000"), "mm", "m") == Decimal("5.0")


def test_incompatible_unit_conversion_blocked():
    """Verify docs/09_MATERIAL_RECONCILIATION.md:
    Cross-dimension conversion without verified density must raise UnitConversionError.
    """
    with pytest.raises(UnitConversionError):
        convert_quantity(Decimal("100"), "kg", "ltr")


def test_stock_ledger_worked_example():
    """Verify worked calculation from docs/09_MATERIAL_RECONCILIATION.md:
    Opening: 100, Receipts: 80, Issues: 120, Returns: 5, Adjustment: +2
    Expected closing stock = 100 + 80 - 120 + 5 + 2 = 67 bags
    """
    now = datetime.now(timezone.utc)
    movements = [
        StockMovementPayload(movement_id=uuid4(), material_code="CEMENT", movement_type="opening_balance", quantity=Decimal("100"), unit="bag", effective_date=now),
        StockMovementPayload(movement_id=uuid4(), material_code="CEMENT", movement_type="receipt", quantity=Decimal("80"), unit="bag", effective_date=now),
        StockMovementPayload(movement_id=uuid4(), material_code="CEMENT", movement_type="issue", quantity=Decimal("120"), unit="bag", effective_date=now),
        StockMovementPayload(movement_id=uuid4(), material_code="CEMENT", movement_type="return", quantity=Decimal("5"), unit="bag", effective_date=now),
        StockMovementPayload(movement_id=uuid4(), material_code="CEMENT", movement_type="adjustment", quantity=Decimal("2"), unit="bag", effective_date=now),
    ]

    closing, opening, receipts, issues, returns, adjustments = calculate_ledger_closing_stock(movements, "bag")
    assert closing == Decimal("67")
    assert opening == Decimal("100")
    assert receipts == Decimal("80")
    assert issues == Decimal("120")
    assert returns == Decimal("5")
    assert adjustments == Decimal("2")


def test_boq_wastage_allowance():
    """Planned 100 bags, approved wastage 5% -> allowed 105 bags.
    Actual issue 120 bags -> variance +15 bags (exceeded).
    """
    boq = [
        BOQItemPayload(
            item_code="COL-01",
            description="Columns",
            material_code="CEMENT",
            planned_quantity=Decimal("100"),
            unit="bag",
            approved_wastage_rate=Decimal("0.05"),
        )
    ]
    issues = {"CEMENT": Decimal("120")}
    res = reconcile_boq_allowances(boq, issues, "bag")
    assert len(res) == 1
    assert res[0]["allowed_quantity"] == Decimal("105.00")
    assert res[0]["variance"] == Decimal("15.00")
    assert res[0]["is_exceeded"] is True
