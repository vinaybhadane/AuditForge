"""Unit tests for preprocessing, file signatures, and limits."""

from app.audit_engine.preprocessing.documents import (
    check_pdf_text_density,
    estimate_pdf_pages,
)
from app.audit_engine.preprocessing.images import (
    compute_perceptual_hash,
    hamming_distance,
)
from app.audit_engine.preprocessing.validation import (
    calculate_sha256,
    detect_file_format,
)


def test_detect_file_format_signatures():
    assert detect_file_format(b"%PDF-1.4...") == "application/pdf"
    assert detect_file_format(b"\xff\xd8\xff\xe0...") == "image/jpeg"
    assert detect_file_format(b"\x89PNG\r\n\x1a\n...") == "image/png"
    assert detect_file_format(b"random-bytes") == "application/octet-stream"


def test_calculate_sha256_deterministic():
    data = b"auditforge-immutable-evidence"
    h1 = calculate_sha256(data)
    h2 = calculate_sha256(data)
    assert h1 == h2
    assert len(h1) == 64


def test_perceptual_hashing_and_distance():
    img1 = b"A" * 1000
    img2 = b"A" * 999 + b"B"
    img3 = b"Z" * 1000

    hash1 = compute_perceptual_hash(img1)
    hash2 = compute_perceptual_hash(img2)
    hash3 = compute_perceptual_hash(img3)

    assert len(hash1) == 16
    assert hamming_distance(hash1, hash2) <= 2
    assert hamming_distance(hash1, hash3) >= 0


def test_pdf_page_and_density_checks():
    pdf_content = b"%PDF-1.4\n/Type /Page\n(Invoice Total: 500) Tj\n/Type /Page\n"
    pages = estimate_pdf_pages(pdf_content)
    assert pages == 2

    has_text, char_count = check_pdf_text_density(pdf_content)
    assert char_count > 0
