"""Delivery challan extractor."""

import re
from decimal import Decimal
from typing import Any, Dict, List
from uuid import UUID

from app.audit_engine.contracts.responses import ExtractedRecord
from app.audit_engine.extraction.structured_fields import (
    make_field,
    normalize_unit,
    parse_date_safe,
    parse_decimal_safe,
)


def extract_challan_fields(text: str, evidence_id: UUID) -> ExtractedRecord:
    """Extract structured fields and delivered items from delivery challan text."""
    fields = {}
    line_items: List[Dict[str, Any]] = []

    # 1. Challan Number
    ch_num_match = re.search(r"(?:challan\s*(?:no|number|#)?[:\s]*)([A-Za-z0-9\-_/]+)", text, re.IGNORECASE)
    ch_num = ch_num_match.group(1).strip() if ch_num_match else None
    fields["challan_number"] = make_field(
        "challan_number", ch_num, ch_num, confidence=0.95 if ch_num else 0.0, is_uncertain=not bool(ch_num)
    )

    # 2. Vendor Name
    vendor_match = re.search(r"(?:vendor|carrier|supplier|from)[:\s]*([A-Za-z0-9\s.,&]+?)(?:\n|challan|date|vehicle)", text, re.IGNORECASE)
    vendor_name = vendor_match.group(1).strip() if vendor_match else None
    fields["vendor_name"] = make_field("vendor_name", vendor_name, vendor_name, confidence=0.90 if vendor_name else 0.0)

    # 3. Delivery Date
    date_match = re.search(r"(?:date|delivery\s*date)[:\s]*(\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}|\d{1,2}\s+[A-Za-z]+\s+\d{4})", text, re.IGNORECASE)
    raw_date = date_match.group(1).strip() if date_match else None
    norm_date = parse_date_safe(raw_date)
    fields["delivery_date"] = make_field("delivery_date", raw_date, norm_date, confidence=0.92 if norm_date else 0.0)

    # 4. PO Reference
    po_match = re.search(r"(?:po\s*(?:no|number|ref|order)?[:\s]*)([A-Za-z0-9\-_/]+)", text, re.IGNORECASE)
    po_ref = po_match.group(1).strip() if po_match else None
    fields["po_reference"] = make_field("po_reference", po_ref, po_ref, confidence=0.88 if po_ref else 0.0)

    # 5. Delivered Items
    lines = text.split("\n")
    for line in lines:
        item_match = re.search(
            r"([A-Za-z0-9\s\-_]+?)\s+[-:]?\s*(\d+(?:\.\d+)?)\s*(bags?|kgs?|tonnes?|nos?|pcs?|m|cum)\b",
            line,
            re.IGNORECASE,
        )
        if item_match:
            desc = item_match.group(1).strip()
            qty = parse_decimal_safe(item_match.group(2))
            unit = normalize_unit(item_match.group(3))
            if qty and qty > Decimal("0"):
                line_items.append({
                    "description": desc,
                    "delivered_quantity": qty,
                    "unit": unit,
                })

    return ExtractedRecord(
        evidence_id=evidence_id,
        document_type="delivery_challan",
        document_number=ch_num,
        vendor_name=vendor_name,
        document_date=norm_date,
        fields=fields,
        line_items=line_items,
    )
