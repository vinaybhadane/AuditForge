"""Integration test for the full AuditEngine pipeline using the synthetic demo dataset."""

from decimal import Decimal

import pytest

from app.audit_engine.contracts.responses import EngineStatus
from app.audit_engine.pipeline.orchestrator import AuditEnginePipeline
from tests.audit_engine.fixtures.demo_dataset import build_synthetic_demo_request


@pytest.mark.asyncio
async def test_full_pipeline_execution():
    pipeline = AuditEnginePipeline()
    request = build_synthetic_demo_request()

    response = await pipeline.execute(request)

    # 1. Pipeline Status
    assert response.status in (EngineStatus.COMPLETED, EngineStatus.COMPLETED_WITH_WARNINGS)
    assert response.schema_version == "1.0"
    assert response.job_id == request.job_id

    # 2. Extracted Records (Invoice and Challan)
    assert len(response.extracted_records) >= 2
    doc_types = {r.document_type for r in response.extracted_records}
    assert "invoice" in doc_types
    assert "delivery_challan" in doc_types

    # 3. Deterministic Material Reconciliation (Worked Example)
    # Expected closing: 67 bags, Observed physical: 60 bags, Variance: -7 bags
    assert response.reconciliation_result is not None
    recon = response.reconciliation_result
    assert recon.calculated_closing_stock == Decimal("67")
    assert recon.opening_stock == Decimal("100")
    assert recon.receipts_total == Decimal("80")
    assert recon.issues_total == Decimal("120")
    assert recon.returns_total == Decimal("5")
    assert recon.adjustments_total == Decimal("2")
    assert recon.variance_with_physical_count == Decimal("-7")

    # 4. Explainable Anomaly Findings
    rule_ids = {f.rule_id for f in response.findings}
    # Delivery vs Receipt discrepancy (80 vs 75 bags)
    assert "AN-004" in rule_ids
    # Physical count discrepancy (-7 bags)
    assert "REC-004" in rule_ids

    # Check finding language does not accuse fraud
    for finding in response.findings:
        assert "fraud" not in finding.explanation.lower()
        assert finding.recommended_action is not None

    # 5. Visual Assessment (Criteria-linked with honest limitations)
    assert len(response.visual_assessments) >= 1
    assessment = response.visual_assessments[0]
    for obs in assessment.observations:
        assert obs.requires_human_review is True
        assert len(obs.limitations) > 0

    # 6. Traceability Correlation Links
    assert len(response.correlation_links) >= 1
    relationships = {link.relationship for link in response.correlation_links}
    assert "references_purchase_order" in relationships or "fulfills_order" in relationships

    # 7. Metadata
    assert response.metadata.duration_ms >= 0
    assert len(response.metadata.stages_executed) >= 5
