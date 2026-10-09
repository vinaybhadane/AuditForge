"""Unit tests for AuditEngine contracts and ingestion modality rules."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.audit_engine.contracts.evidence import (
    EvidencePayload,
    EvidenceType,
    IngestionSource,
)


def test_site_photo_rejects_file_upload_modality():
    """Verify FR-006 & docs/07_SECURITY_AND_ACCESS_CONTROL.md:
    Site progress photos strictly require live camera capture.
    Attempting file_upload for site_photo must raise validation error.
    """
    with pytest.raises(ValidationError) as exc:
        EvidencePayload(
            evidence_id=uuid4(),
            evidence_type=EvidenceType.SITE_PHOTO,
            ingestion_source=IngestionSource.FILE_UPLOAD,  # DISALLOWED
            filename="gallery_photo.jpg",
            declared_content_type="image/jpeg",
            content_bytes=b"\xff\xd8\xff\xe0test",
        )
    assert "INVALID_INGESTION_SOURCE" in str(exc.value)


def test_site_photo_accepts_live_capture_modality():
    """Verify site progress photo accepts live_capture."""
    payload = EvidencePayload(
        evidence_id=uuid4(),
        evidence_type=EvidenceType.SITE_PHOTO,
        ingestion_source=IngestionSource.LIVE_CAPTURE,  # ALLOWED
        filename="live_capture.jpg",
        declared_content_type="image/jpeg",
        content_bytes=b"\xff\xd8\xff\xe0test",
    )
    assert payload.ingestion_source == IngestionSource.LIVE_CAPTURE


def test_vendor_document_accepts_both_modalities():
    """Verify vendor documents (invoices, challans) support both file upload and live camera scanning."""
    inv_upload = EvidencePayload(
        evidence_id=uuid4(),
        evidence_type=EvidenceType.INVOICE,
        ingestion_source=IngestionSource.FILE_UPLOAD,
        filename="invoice.pdf",
        declared_content_type="application/pdf",
        content_bytes=b"%PDF-1.4",
    )
    assert inv_upload.ingestion_source == IngestionSource.FILE_UPLOAD

    challan_scan = EvidencePayload(
        evidence_id=uuid4(),
        evidence_type=EvidenceType.DELIVERY_CHALLAN,
        ingestion_source=IngestionSource.LIVE_CAPTURE,
        filename="scan.jpg",
        declared_content_type="image/jpeg",
        content_bytes=b"\xff\xd8\xff\xe0test",
    )
    assert challan_scan.ingestion_source == IngestionSource.LIVE_CAPTURE
