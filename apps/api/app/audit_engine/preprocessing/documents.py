"""Document structural preprocessing and page budget enforcement."""

import re
from typing import Tuple

from app.audit_engine.config import engine_config
from app.audit_engine.exceptions import EngineValidationError


def estimate_pdf_pages(content: bytes) -> int:
    """Estimate or count pages in a PDF document from /Type /Page objects."""
    matches = re.findall(rb"/Type\s*/Page\b", content)
    # /Type /Pages is parent node; matches will count individual /Page
    page_count = len(matches)
    return max(1, page_count) if page_count > 0 else 1


def validate_document_page_budget(content: bytes) -> int:
    """Ensure PDF does not exceed allowed page budget (100 pages)."""
    pages = estimate_pdf_pages(content)
    if pages > engine_config.MAX_PDF_PAGES:
        raise EngineValidationError(
            f"MAX_PDF_PAGES exceeded: Document contains ~{pages} pages, exceeding maximum limit "
            f"of {engine_config.MAX_PDF_PAGES}."
        )
    return pages


def check_pdf_text_density(content: bytes) -> Tuple[bool, int]:
    """Check if PDF contains extractable native text streams or is a scanned image.
    
    Returns:
        (has_extractable_text, estimated_character_count)
    """
    # Look for text-showing operators in PDF content streams: Tj, TJ, ', "
    text_matches = re.findall(rb"\((.*?)\)\s*Tj", content)
    array_matches = re.findall(rb"\[(.*?)\]\s*TJ", content)

    char_count = sum(len(m) for m in text_matches) + sum(len(m) for m in array_matches)
    has_text = char_count > 50  # More than 50 characters of text stream
    return has_text, char_count
