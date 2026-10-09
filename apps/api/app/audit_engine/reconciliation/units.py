"""Deterministic unit conversion and dimension compatibility checks."""

from decimal import Decimal
from typing import Dict, Optional

from app.audit_engine.exceptions import UnitConversionError
from app.audit_engine.extraction.structured_fields import normalize_unit

# Dimension classifications
UNIT_DIMENSIONS: Dict[str, str] = {
    "kg": "mass",
    "tonne": "mass",
    "quintal": "mass",
    "g": "mass",
    "m": "length",
    "mm": "length",
    "cm": "length",
    "km": "length",
    "sq_m": "area",
    "sq_ft": "area",
    "cu_m": "volume",
    "ltr": "volume",
    "bag": "count_bag",
    "pcs": "count",
    "box": "count_box",
}

# Base conversion factors to canonical unit of each dimension
# mass -> kg, length -> m, area -> sq_m, volume -> cu_m
BASE_FACTORS: Dict[str, Decimal] = {
    # Mass (base: kg)
    "kg": Decimal("1.0"),
    "tonne": Decimal("1000.0"),
    "quintal": Decimal("100.0"),
    "g": Decimal("0.001"),
    # Length (base: m)
    "m": Decimal("1.0"),
    "mm": Decimal("0.001"),
    "cm": Decimal("0.01"),
    "km": Decimal("1000.0"),
    # Area (base: sq_m)
    "sq_m": Decimal("1.0"),
    "sq_ft": Decimal("0.092903"),
    # Volume (base: cu_m)
    "cu_m": Decimal("1.0"),
    "ltr": Decimal("0.001"),
    # Count (base: pcs)
    "pcs": Decimal("1.0"),
    "bag": Decimal("1.0"),  # bags preserved in bag dimension
}


def get_dimension(unit: str) -> str:
    norm = normalize_unit(unit)
    return UNIT_DIMENSIONS.get(norm, "unknown")


def convert_quantity(
    quantity: Decimal,
    from_unit: str,
    to_unit: str,
    density_kg_per_cum: Optional[Decimal] = None,
) -> Decimal:
    """Deterministically convert a quantity between compatible units.
    
    Raises UnitConversionError if dimensions are incompatible.
    """
    u_from = normalize_unit(from_unit)
    u_to = normalize_unit(to_unit)

    if u_from == u_to:
        return quantity

    dim_from = get_dimension(u_from)
    dim_to = get_dimension(u_to)

    # Cross-dimension conversion: mass <-> volume requires explicit verified density
    if dim_from == "mass" and dim_to == "volume":
        if not density_kg_per_cum:
            raise UnitConversionError(
                f"INCOMPATIBLE_UNITS: Cannot convert mass '{u_from}' to volume '{u_to}' without verified material density."
            )
        # 1. Convert to kg
        qty_kg = quantity * BASE_FACTORS[u_from]
        # 2. Convert kg to cu_m using density (cu_m = kg / density)
        qty_cum = qty_kg / density_kg_per_cum
        # 3. Convert cu_m to target volume unit
        return qty_cum / BASE_FACTORS[u_to]

    if dim_from != dim_to or dim_from == "unknown":
        raise UnitConversionError(
            f"INCOMPATIBLE_UNITS: Incompatible dimensions for '{u_from}' ({dim_from}) and '{u_to}' ({dim_to})."
        )

    # Standard intra-dimension conversion
    factor_from = BASE_FACTORS.get(u_from)
    factor_to = BASE_FACTORS.get(u_to)

    if not factor_from or not factor_to:
        raise UnitConversionError(
            f"UNKNOWN_CONVERSION: Conversion factors for '{u_from}' or '{u_to}' are undefined."
        )

    # Convert to base, then to target
    base_qty = quantity * factor_from
    return base_qty / factor_to
