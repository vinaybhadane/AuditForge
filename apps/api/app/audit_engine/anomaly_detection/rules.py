"""Deterministic anomaly detection rules (AN-001 through AN-011)."""

from decimal import Decimal
from typing import Dict, List, Optional, Tuple

from app.audit_engine.contracts.evidence import EvidencePayload, EvidenceType
from app.audit_engine.contracts.findings import (
    AnomalyFinding,
    FindingCategory,
    FindingProvenance,
    FindingSeverity,
)
from app.audit_engine.contracts.requests import AuditEngineRequest
from app.audit_engine.contracts.responses import ExtractedRecord, ReconciliationResult


def check_exact_duplicate_hash(evidence_items: List[EvidencePayload]) -> List[AnomalyFinding]:
    """AN-001: Exact duplicate SHA-256 hash detection."""
    findings = []
    seen_hashes: Dict[str, List[EvidencePayload]] = {}

    for e in evidence_items:
        h = e.sha256_hash or ""
        if h:
            seen_hashes.setdefault(h, []).append(e)

    for h, items in seen_hashes.items():
        if len(items) > 1:
            findings.append(
                AnomalyFinding(
                    rule_id="AN-001",
                    category=FindingCategory.EXACT_DUPLICATE,
                    severity=FindingSeverity.HIGH,
                    title="Exact Duplicate Evidence File Detected",
                    explanation=(
                        f"SHA-256 hash {h[:16]}... appears in {len(items)} submitted evidence items "
                        f"({', '.join(i.filename for i in items)}). Identical byte payload suggests potential file reuse."
                    ),
                    evidence_refs=[i.evidence_id for i in items],
                    observed_value=f"{len(items)} occurrences of hash {h[:12]}",
                    expected_value="Unique asset per submission",
                    uncertainty_notes=(
                        "Legitimate file reuse is possible (e.g. multi-page master document attached to several records). "
                        "Inspect submission context before concluding redundant submission."
                    ),
                    recommended_action="Verify whether this asset was intentionally attached to multiple distinct milestones or records.",
                    provenance=FindingProvenance(rule_version="v1"),
                )
            )

    return findings


def check_duplicate_document_numbers(extracted_records: List[ExtractedRecord]) -> List[AnomalyFinding]:
    """AN-002: Duplicate vendor document number detection."""
    findings = []
    seen_docs: Dict[Tuple[str, str], List[ExtractedRecord]] = {}

    for r in extracted_records:
        if r.document_number and r.vendor_name:
            key = (r.vendor_name.strip().lower(), r.document_number.strip().lower())
            seen_docs.setdefault(key, []).append(r)

    for (vendor, doc_num), records in seen_docs.items():
        if len(records) > 1:
            findings.append(
                AnomalyFinding(
                    rule_id="AN-002",
                    category=FindingCategory.DOCUMENT_DUPLICATE,
                    severity=FindingSeverity.HIGH,
                    title="Duplicate Vendor Document Number",
                    explanation=(
                        f"Document number '{doc_num.upper()}' from vendor '{vendor.title()}' "
                        f"appears {len(records)} times across submitted records."
                    ),
                    evidence_refs=[rec.evidence_id for rec in records],
                    subject_ids=[doc_num],
                    observed_value=f"{len(records)} documents with number {doc_num}",
                    expected_value="1 document per vendor invoice/challan number",
                    uncertainty_notes="Vendor numbering may occasionally restart across fiscal years or branches.",
                    recommended_action="Cross-reference billing periods and purchase orders to confirm whether this is a duplicated claim.",
                    provenance=FindingProvenance(rule_version="v1"),
                )
            )

    return findings


def check_delivery_receipt_variance(reconciliation: Optional[ReconciliationResult]) -> List[AnomalyFinding]:
    """AN-004: Delivery challan vs physically accepted goods receipt mismatch."""
    findings = []
    if not reconciliation:
        return findings

    for line in reconciliation.lines:
        if line.rule_code == "REC-002" and line.status == "discrepancy":
            findings.append(
                AnomalyFinding(
                    rule_id="AN-004",
                    category=FindingCategory.DELIVERY_MISMATCH,
                    severity=FindingSeverity.HIGH,
                    title="Challan Delivery vs Goods Receipt Variance",
                    explanation=(
                        f"Delivery challan recorded {line.expected_value} {line.unit}, but accepted goods receipt "
                        f"recorded {line.observed_value} {line.unit}, leaving a delta of {line.delta} {line.unit}."
                    ),
                    calculation_formula=line.formula_code,
                    expected_value=f"{line.expected_value} {line.unit}",
                    observed_value=f"{line.observed_value} {line.unit}",
                    uncertainty_notes="Partial delivery, transport damage, or delayed secondary delivery may explain quantity variance.",
                    recommended_action="Inspect delivery transit notes and verify whether partial receipt was acknowledged by store in-charge.",
                    provenance=FindingProvenance(rule_version="v1"),
                )
            )

    return findings


def check_stock_ledger_variance(reconciliation: Optional[ReconciliationResult]) -> List[AnomalyFinding]:
    """AN-005 & REC-004: Stock ledger variance with physical count or negative stock."""
    findings = []
    if not reconciliation:
        return findings

    # 1. Negative calculated stock
    if reconciliation.calculated_closing_stock < Decimal("0"):
        findings.append(
            AnomalyFinding(
                rule_id="AN-005",
                category=FindingCategory.NEGATIVE_STOCK,
                severity=FindingSeverity.CRITICAL,
                title="Negative Calculated Stock Balance",
                explanation=(
                    f"Calculated closing stock balance is negative ({reconciliation.calculated_closing_stock}). "
                    f"Recorded issues exceed available opening stock plus recorded receipts."
                ),
                calculation_formula="closing_stock = opening_stock + receipts - issues + adjustments",
                observed_value=str(reconciliation.calculated_closing_stock),
                expected_value=">= 0",
                uncertainty_notes="Delayed posting of receipts or unrecorded inbound transfers may cause temporary negative ledger balance.",
                recommended_action="Review ledger cutoff dates and confirm whether pending delivery receipts have not yet been posted.",
                provenance=FindingProvenance(rule_version="v1"),
            )
        )

    # 2. Physical count discrepancy (REC-004)
    if reconciliation.variance_with_physical_count is not None and abs(reconciliation.variance_with_physical_count) > Decimal("0.001"):
        findings.append(
            AnomalyFinding(
                rule_id="REC-004",
                category=FindingCategory.RECONCILIATION_VARIANCE,
                severity=FindingSeverity.MEDIUM,
                title="Physical Inventory Count Variance",
                explanation=(
                    f"Physical count differs from calculated ledger balance by {reconciliation.variance_with_physical_count} units. "
                    f"Expected closing balance: {reconciliation.calculated_closing_stock}."
                ),
                calculation_formula="variance = physical_count - calculated_closing_stock",
                expected_value=str(reconciliation.calculated_closing_stock),
                observed_value=str(reconciliation.calculated_closing_stock + reconciliation.variance_with_physical_count),
                uncertainty_notes=(
                    "Discrepancy reflects input records and physical audit timing cutoff; "
                    "does not prove theft or unapproved diversion."
                ),
                recommended_action="Conduct recount and audit stock movements posted since last physical verification.",
                provenance=FindingProvenance(rule_version="v1"),
            )
        )

    return findings


def check_boq_allowance_exceeded(reconciliation: Optional[ReconciliationResult]) -> List[AnomalyFinding]:
    """AN-006: Material issue exceeds supported BOQ allowance."""
    findings = []
    if not reconciliation:
        return findings

    for line in reconciliation.lines:
        if line.rule_code == "REC-005" and line.status == "discrepancy":
            findings.append(
                AnomalyFinding(
                    rule_id="AN-006",
                    category=FindingCategory.EXCESS_ISSUE,
                    severity=FindingSeverity.HIGH,
                    title="Material Issues Exceed Supported BOQ Allowance",
                    explanation=line.explanation,
                    calculation_formula=line.formula_code,
                    expected_value=f"{line.expected_value} {line.unit}",
                    observed_value=f"{line.observed_value} {line.unit}",
                    uncertainty_notes="Excess issue does not necessarily equal physical consumption; check unconsumed stock at site.",
                    recommended_action="Verify whether unused material remains on site or if an authorized BOQ scope variation was approved.",
                    provenance=FindingProvenance(rule_version="v1"),
                )
            )

    return findings


def check_missing_milestone_evidence(request: AuditEngineRequest) -> List[AnomalyFinding]:
    """AN-010: Required milestone acceptance criteria lack corresponding evidence."""
    findings = []
    if not request.acceptance_criteria:
        return findings

    site_photos = [e for e in request.evidence_items if e.evidence_type == EvidenceType.SITE_PHOTO]
    if not site_photos:
        findings.append(
            AnomalyFinding(
                rule_id="AN-010",
                category=FindingCategory.MISSING_EVIDENCE,
                severity=FindingSeverity.MEDIUM,
                title="Missing Required Photographic Evidence",
                explanation=(
                    f"Milestone defines {len(request.acceptance_criteria)} mandatory criteria, "
                    f"but no live camera progress photographs were supplied."
                ),
                expected_value=f"At least 1 live capture photo for milestone {request.milestone_id or ''}",
                observed_value="0 site progress photos",
                uncertainty_notes="Missing photo is not proof of fabricated work; inspection may be pending.",
                recommended_action="Request on-site supervisor capture live inspection photographs via mobile device viewfinder.",
                provenance=FindingProvenance(rule_version="v1"),
            )
        )

    return findings


def check_line_arithmetic_mismatches(extracted_records: List[ExtractedRecord]) -> List[AnomalyFinding]:
    """REC-008: Invoice line item arithmetic discrepancy."""
    findings = []
    for rec in extracted_records:
        for item in rec.line_items:
            if item.get("arithmetic_mismatch"):
                qty = item.get("quantity")
                price = item.get("unit_price")
                computed = item.get("computed_total")
                stated = item.get("stated_total")
                findings.append(
                    AnomalyFinding(
                        rule_id="REC-008",
                        category=FindingCategory.ARITHMETIC_MISMATCH,
                        severity=FindingSeverity.MEDIUM,
                        title="Document Line Arithmetic Mismatch",
                        explanation=(
                            f"In invoice {rec.document_number or ''}: {item.get('description')} line states total of {stated}, "
                            f"but quantity ({qty}) × unit price ({price}) calculates to {computed}."
                        ),
                        evidence_refs=[rec.evidence_id],
                        calculation_formula="computed_total = quantity * unit_price",
                        expected_value=str(computed),
                        observed_value=str(stated),
                        uncertainty_notes="Unstated discounts, volume rebates, or tax calculations may explain difference.",
                        recommended_action="Examine invoice header for line discounts or freight fees before accepting authoritative ledger entry.",
                        provenance=FindingProvenance(rule_version="v1"),
                    )
                )

    return findings
