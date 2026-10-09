"""Full-scale AuditEngine pipeline orchestrator."""

import time
from datetime import datetime, timezone
from typing import List, Optional

from app.audit_engine.anomaly_detection.rules import (
    check_boq_allowance_exceeded,
    check_delivery_receipt_variance,
    check_duplicate_document_numbers,
    check_exact_duplicate_hash,
    check_line_arithmetic_mismatches,
    check_missing_milestone_evidence,
    check_stock_ledger_variance,
)
from app.audit_engine.contracts.evidence import EvidenceType
from app.audit_engine.contracts.findings import AnomalyFinding
from app.audit_engine.contracts.requests import AuditEngineRequest
from app.audit_engine.contracts.responses import (
    AuditEngineResponse,
    EngineStatus,
    EvidenceCorrelationLink,
    ExtractedRecord,
    ProcessingMetadata,
    ReconciliationResult,
    VisualAssessmentResult,
)
from app.audit_engine.correlation.evidence_graph import build_evidence_correlation_links
from app.audit_engine.extraction.delivery_challans import extract_challan_fields
from app.audit_engine.extraction.invoices import extract_invoice_fields
from app.audit_engine.extraction.pdf_text import extract_native_pdf_text
from app.audit_engine.pipeline.stages import PipelineStage
from app.audit_engine.preprocessing.validation import validate_evidence_payload
from app.audit_engine.providers.gemini_provider import GeminiVlmProvider
from app.audit_engine.reconciliation.reconciliation import execute_material_reconciliation
from app.audit_engine.vision.construction_assessment import assess_site_photographs
from app.audit_engine.vision.provider import VisualAssessmentProvider


class AuditEnginePipeline:
    """Core AuditEngine orchestrator.
    
    Can be imported and invoked programmatically by Member 2 without
    starting a web server or external worker daemon.
    """

    def __init__(self, vlm_provider: Optional[VisualAssessmentProvider] = None):
        self.vlm_provider = vlm_provider or GeminiVlmProvider()

    async def execute(self, request: AuditEngineRequest) -> AuditEngineResponse:
        """Execute full evidence auditing pipeline."""
        start_ts = datetime.now(timezone.utc)
        start_mono = time.monotonic()
        stages_run: List[str] = []
        warnings: List[str] = []
        errors: List[str] = []
        findings: List[AnomalyFinding] = []
        extracted_records: List[ExtractedRecord] = []
        reconciliation_res: Optional[ReconciliationResult] = None
        visual_assessments: List[VisualAssessmentResult] = []
        correlation_links: List[EvidenceCorrelationLink] = []

        try:
            # Stage 1: Input Validation & Preprocessing
            stages_run.append(PipelineStage.EVIDENCE_PREPROCESSING.value)
            for item in request.evidence_items:
                try:
                    mime, sha, size = validate_evidence_payload(item)
                    item.sha256_hash = sha
                    item.size_bytes = size
                except Exception as ex:
                    warnings.append(f"Preprocess error for {item.filename}: {str(ex)}")

            # Stage 2: Document Extraction
            if request.options.run_ocr_extraction:
                stages_run.append(PipelineStage.DOCUMENT_EXTRACTION.value)
                for item in request.evidence_items:
                    raw_bytes = item.content_bytes or b""
                    if not raw_bytes and item.content_base64:
                        import base64
                        raw_bytes = base64.b64decode(item.content_base64)

                    if item.evidence_type in (EvidenceType.INVOICE, EvidenceType.DELIVERY_CHALLAN, EvidenceType.OTHER):
                        text, _ = extract_native_pdf_text(raw_bytes)
                        if item.evidence_type == EvidenceType.INVOICE:
                            rec = extract_invoice_fields(text, item.evidence_id)
                            extracted_records.append(rec)
                        elif item.evidence_type == EvidenceType.DELIVERY_CHALLAN:
                            rec = extract_challan_fields(text, item.evidence_id)
                            extracted_records.append(rec)

            # Stage 3: Material Reconciliation (REC-001 - REC-008)
            if request.options.run_reconciliation:
                stages_run.append(PipelineStage.MATERIAL_RECONCILIATION.value)
                try:
                    reconciliation_res = execute_material_reconciliation(request)
                except Exception as ex:
                    warnings.append(f"Reconciliation error: {str(ex)}")

            # Stage 4: Visual Assessment
            if request.options.run_visual_assessment:
                stages_run.append(PipelineStage.VISUAL_ASSESSMENT.value)
                try:
                    visual_assessments = await assess_site_photographs(
                        request.evidence_items,
                        request.acceptance_criteria,
                        self.vlm_provider,
                    )
                except Exception as ex:
                    warnings.append(f"Visual assessment error: {str(ex)}")

            # Stage 5: Anomaly Detection (AN-001 - AN-011)
            if request.options.run_anomaly_detection:
                stages_run.append(PipelineStage.ANOMALY_DETECTION.value)
                findings.extend(check_exact_duplicate_hash(request.evidence_items))
                findings.extend(check_duplicate_document_numbers(extracted_records))
                findings.extend(check_delivery_receipt_variance(reconciliation_res))
                findings.extend(check_stock_ledger_variance(reconciliation_res))
                findings.extend(check_boq_allowance_exceeded(reconciliation_res))
                findings.extend(check_missing_milestone_evidence(request))
                findings.extend(check_line_arithmetic_mismatches(extracted_records))

            # Stage 6: Evidence Correlation Graph
            stages_run.append(PipelineStage.EVIDENCE_CORRELATION.value)
            correlation_links = build_evidence_correlation_links(
                request,
                extracted_records,
                reconciliation_res or execute_material_reconciliation(request),
                findings,
            )

        except Exception as ex:
            errors.append(f"Fatal pipeline error: {str(ex)}")

        finish_ts = datetime.now(timezone.utc)
        duration_ms = int((time.monotonic() - start_mono) * 1000)

        status = EngineStatus.COMPLETED
        if errors:
            status = EngineStatus.FAILED
        elif warnings:
            status = EngineStatus.COMPLETED_WITH_WARNINGS

        metadata = ProcessingMetadata(
            pipeline_version="audit-pipeline-v1",
            start_time=start_ts,
            finish_time=finish_ts,
            duration_ms=duration_ms,
            stages_executed=stages_run,
        )

        return AuditEngineResponse(
            schema_version="1.0",
            job_id=request.job_id,
            status=status,
            findings=findings,
            extracted_records=extracted_records,
            reconciliation_result=reconciliation_res,
            visual_assessments=visual_assessments,
            correlation_links=correlation_links,
            warnings=warnings,
            errors=errors,
            metadata=metadata,
        )
