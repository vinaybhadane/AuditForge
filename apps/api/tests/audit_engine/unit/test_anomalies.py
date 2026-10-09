"""Unit tests for anomaly detection rules and priority scoring."""

from decimal import Decimal
from uuid import uuid4

from app.audit_engine.anomaly_detection.rules import (
    check_duplicate_document_numbers,
    check_exact_duplicate_hash,
    check_stock_ledger_variance,
)
from app.audit_engine.anomaly_detection.scoring import calculate_review_priority_score
from app.audit_engine.contracts.evidence import EvidencePayload, EvidenceType, IngestionSource
from app.audit_engine.contracts.responses import ExtractedRecord, ReconciliationResult


def test_exact_duplicate_hash_detector():
    e1 = EvidencePayload(
        evidence_id=uuid4(),
        evidence_type=EvidenceType.INVOICE,
        ingestion_source=IngestionSource.FILE_UPLOAD,
        filename="inv1.pdf",
        declared_content_type="application/pdf",
        sha256_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        content_bytes=b"%PDF-1.4",
    )
    e2 = EvidencePayload(
        evidence_id=uuid4(),
        evidence_type=EvidenceType.INVOICE,
        ingestion_source=IngestionSource.FILE_UPLOAD,
        filename="inv2_copy.pdf",
        declared_content_type="application/pdf",
        sha256_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        content_bytes=b"%PDF-1.4",
    )
    findings = check_exact_duplicate_hash([e1, e2])
    assert len(findings) == 1
    assert findings[0].rule_id == "AN-001"
    assert findings[0].severity.value == "high"


def test_duplicate_document_number_detector():
    r1 = ExtractedRecord(
        evidence_id=uuid4(),
        document_type="invoice",
        document_number="INV-88",
        vendor_name="Ultratech",
    )
    r2 = ExtractedRecord(
        evidence_id=uuid4(),
        document_type="invoice",
        document_number="INV-88",
        vendor_name="Ultratech",
    )
    findings = check_duplicate_document_numbers([r1, r2])
    assert len(findings) == 1
    assert findings[0].rule_id == "AN-002"


def test_negative_stock_anomaly():
    recon = ReconciliationResult(
        calculated_closing_stock=Decimal("-15"),
        opening_stock=Decimal("10"),
        receipts_total=Decimal("0"),
        issues_total=Decimal("25"),
        returns_total=Decimal("0"),
        adjustments_total=Decimal("0"),
    )
    findings = check_stock_ledger_variance(recon)
    assert any(f.rule_id == "AN-005" for f in findings)


def test_review_priority_scoring():
    e1 = EvidencePayload(
        evidence_id=uuid4(),
        evidence_type=EvidenceType.INVOICE,
        ingestion_source=IngestionSource.FILE_UPLOAD,
        filename="inv1.pdf",
        declared_content_type="application/pdf",
        sha256_hash="samehash",
        content_bytes=b"%PDF-1.4",
    )
    e2 = EvidencePayload(
        evidence_id=uuid4(),
        evidence_type=EvidenceType.INVOICE,
        ingestion_source=IngestionSource.FILE_UPLOAD,
        filename="inv2.pdf",
        declared_content_type="application/pdf",
        sha256_hash="samehash",
        content_bytes=b"%PDF-1.4",
    )
    findings = check_exact_duplicate_hash([e1, e2])
    score_report = calculate_review_priority_score(findings)
    assert score_report["composite_priority_score"] > 0
    assert score_report["is_calibrated_probability"] is False
