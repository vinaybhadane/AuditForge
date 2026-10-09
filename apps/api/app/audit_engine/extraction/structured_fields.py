"""Field normalization and typed extraction helpers."""

import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Optional

from app.audit_engine.contracts.responses import ExtractedField

# Canonical unit mapping dictionary
UNIT_SYNONYMS = {
    "kg": "kg",
    "kgs": "kg",
    "kilogram": "kg",
    "kilograms": "kg",
    "tonne": "tonne",
    "tonnes": "tonne",
    "ton": "tonne",
    "tons": "tonne",
    "mt": "tonne",
    "bag": "bag",
    "bags": "bag",
    "mtr": "m",
    "meter": "m",
    "meters": "m",
    "m": "m",
    "mm": "mm",
    "millimeter": "mm",
    "sqm": "sq_m",
    "sq_m": "sq_m",
    "sq.m": "sq_m",
    "cum": "cu_m",
    "cu_m": "cu_m",
    "cu.m": "cu_m",
    "ltr": "ltr",
    "litre": "ltr",
    "litres": "ltr",
    "l": "ltr",
    "pcs": "pcs",
    "pieces": "pcs",
    "nos": "pcs",
    "box": "box",
    "boxes": "box",
}


def normalize_unit(raw_unit: Optional[str]) -> str:
    """Normalize raw unit strings to canonical unit codes."""
    if not raw_unit:
        return "unknown"
    cleaned = raw_unit.strip().lower().replace(".", "")
    return UNIT_SYNONYMS.get(cleaned, cleaned)


def parse_decimal_safe(raw_value: Optional[str]) -> Optional[Decimal]:
    """Parse string numbers with commas and currency symbols into Decimal."""
    if not raw_value:
        return None
    cleaned = re.sub(r"[^\d.-]", "", raw_value.strip())
    try:
        return Decimal(cleaned)
    except (InvalidOperation, ValueError):
        return None


def parse_date_safe(raw_date: Optional[str]) -> Optional[str]:
    """Parse common document date formats into ISO-8601 (YYYY-MM-DD)."""
    if not raw_date:
        return None
    cleaned = raw_date.strip()
    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d %b %Y",
        "%d %B %Y",
        "%Y/%m/%d",
    ]
    for fmt in formats:
        try:
            parsed = datetime.strptime(cleaned, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return cleaned  # Return raw cleaned if unrecognized format


def make_field(
    name: str,
    raw_val: Optional[str],
    normalized_val: Optional[Any] = None,
    confidence: float = 1.0,
    method: str = "native_pdf",
    is_uncertain: bool = False,
    notes: Optional[str] = None,
) -> ExtractedField:
    """Factory for standard ExtractedField models."""
    return ExtractedField(
        field_name=name,
        raw_value=raw_val,
        normalized_value=normalized_val if normalized_val is not None else raw_val,
        confidence=confidence,
        extraction_method=method,
        is_uncertain=is_uncertain,
        notes=notes,
    )
