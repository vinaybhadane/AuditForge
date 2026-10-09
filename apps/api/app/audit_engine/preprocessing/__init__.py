"""Preprocessing utilities for evidence validation and inspection."""

from app.audit_engine.preprocessing.documents import (
    check_pdf_text_density,
    estimate_pdf_pages,
    validate_document_page_budget,
)
from app.audit_engine.preprocessing.images import (
    compute_perceptual_hash,
    get_image_dimensions,
    hamming_distance,
    validate_image_pixel_budget,
)
from app.audit_engine.preprocessing.validation import (
    calculate_sha256,
    detect_file_format,
    validate_evidence_payload,
)

__all__ = [
    "detect_file_format",
    "calculate_sha256",
    "validate_evidence_payload",
    "get_image_dimensions",
    "validate_image_pixel_budget",
    "compute_perceptual_hash",
    "hamming_distance",
    "estimate_pdf_pages",
    "validate_document_page_budget",
    "check_pdf_text_density",
]
