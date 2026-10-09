"""Unit tests for document extraction and line arithmetic."""

from decimal import Decimal
from uuid import uuid4

from app.audit_engine.extraction.delivery_challans import extract_challan_fields
from app.audit_engine.extraction.invoices import extract_invoice_fields
from app.audit_engine.extraction.structured_fields import (
    normalize_unit,
    parse_date_safe,
    parse_decimal_safe,
)


def test_unit_normalization():
    assert normalize_unit("kgs") == "kg"
    assert normalize_unit("tonnes") == "tonne"
    assert normalize_unit("bags") == "bag"
    assert normalize_unit("MTR") == "m"
    assert normalize_unit("sq.m") == "sq_m"


def test_safe_parsing_helpers():
    assert parse_decimal_safe("1,250.50") == Decimal("1250.50")
    assert parse_decimal_safe("₹ 380.00") == Decimal("380.00")
    assert parse_date_safe("02-10-2026") == "2026-10-02"
    assert parse_date_safe("2026-10-02") == "2026-10-02"


def test_invoice_field_and_arithmetic_extraction():
    text = (
        "Invoice No: INV-9901\n"
        "Vendor: Ambuja Cements\n"
        "Date: 2026-10-01\n"
        "PO Ref: PO-800\n"
        "OPC 53 Cement - 50 bags @ 400 = 20000\n"
        "Total Amount: 20000\n"
    )
    rec = extract_invoice_fields(text, uuid4())
    assert rec.document_number == "INV-9901"
    assert rec.vendor_name == "Ambuja Cements"
    assert rec.fields["total_amount"].normalized_value == Decimal("20000")
    assert len(rec.line_items) == 1
    assert rec.line_items[0]["quantity"] == Decimal("50")
    assert rec.line_items[0]["unit_price"] == Decimal("400")
    assert rec.line_items[0]["arithmetic_mismatch"] is False


def test_invoice_line_arithmetic_mismatch_detected():
    # 10 bags @ 500 = 5000, but stated total says 5500
    text = (
        "Invoice No: INV-DISC\n"
        "Date: 2026-10-01\n"
        "Cement - 10 bags @ 500 = 5500\n"
        "Total Amount: 5500\n"
    )
    rec = extract_invoice_fields(text, uuid4())
    assert len(rec.line_items) == 1
    assert rec.line_items[0]["arithmetic_mismatch"] is True


def test_challan_field_extraction():
    text = (
        "Challan No: DC-551\n"
        "Vendor: Tata Steel Ltd\n"
        "Date: 2026-10-04\n"
        "TMT Rebar 12mm - 5 tonnes\n"
    )
    rec = extract_challan_fields(text, uuid4())
    assert rec.document_number == "DC-551"
    assert len(rec.line_items) == 1
    assert rec.line_items[0]["delivered_quantity"] == Decimal("5")
    assert rec.line_items[0]["unit"] == "tonne"
