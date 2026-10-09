"""Client adapter for communicating with Member 3's AI Audit Engine.

Per docs/08_AI_EVIDENCE_PIPELINE.md:
- Does not independently implement OCR or VLM algorithms.
- Validates typed contracts on ingress and egress.
- Bounded retries for transient HTTP errors.
- Clearly flags test/synthetic adapter responses in development mode.
- Quarantines and rejects invalid structured model outputs.
"""

import asyncio
from datetime import datetime, timezone
from typing import Optional

import httpx
from pydantic import ValidationError

from app.core.errors import AuditForgeException, ErrorCode
from app.core.logging import get_logger
from app.integrations.ai_engine_contracts import (
    DocumentExtractionInput,
    DocumentExtractionOutput,
    ExtractedFieldItem,
    ObservationItem,
    ObservationRef,
    VisualAssessmentInput,
    VisualAssessmentOutput,
)

logger = get_logger("ai_engine_client")


class AIEngineClient:
    """Production client and test adapter for Member 3's AI Engine."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout_seconds: int = 30,
        max_retries: int = 2,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout_seconds
        self.max_retries = max_retries

    async def run_visual_assessment(self, payload: VisualAssessmentInput) -> VisualAssessmentOutput:
        """Submit visual assessment task for live site photo."""
        if not self.base_url:
            return self._mock_visual_assessment(payload)

        url = f"{self.base_url.rstrip('/')}/api/v1/ai/visual-assessment"
        attempt = 0
        last_error = None

        while attempt <= self.max_retries:
            attempt += 1
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, json=payload.model_dump(mode="json"))
                    if response.status_code == 200:
                        raw_data = response.json()
                        try:
                            return VisualAssessmentOutput.model_validate(raw_data)
                        except ValidationError as ve:
                            logger.error("AI Engine returned invalid schema: %s", str(ve))
                            raise AuditForgeException(
                                code=ErrorCode.PROCESSING_FAILED,
                                message="AI Engine output failed validation schema",
                                status_code=502,
                            )
                    elif response.status_code >= 500:
                        last_error = f"HTTP {response.status_code}"
                    else:
                        raise AuditForgeException(
                            code=ErrorCode.PROCESSING_FAILED,
                            message=f"AI Engine rejected request: {response.text}",
                            status_code=502,
                        )
            except (httpx.TimeoutException, httpx.NetworkError) as e:
                last_error = str(e)
                logger.warning("Transient error connecting to AI engine (attempt %d): %s", attempt, str(e))

            if attempt <= self.max_retries:
                await asyncio.sleep(0.5 * attempt)

        raise AuditForgeException(
            code=ErrorCode.PROVIDER_UNAVAILABLE,
            message=f"AI Engine unavailable after retries: {last_error}",
            status_code=503,
        )

    async def run_document_extraction(self, payload: DocumentExtractionInput) -> DocumentExtractionOutput:
        """Submit document extraction task for vendor document."""
        if not self.base_url:
            return self._mock_document_extraction(payload)

        url = f"{self.base_url.rstrip('/')}/api/v1/ai/document-extraction"
        attempt = 0
        last_error = None

        while attempt <= self.max_retries:
            attempt += 1
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, json=payload.model_dump(mode="json"))
                    if response.status_code == 200:
                        raw_data = response.json()
                        try:
                            return DocumentExtractionOutput.model_validate(raw_data)
                        except ValidationError as ve:
                            logger.error("AI Engine returned invalid doc schema: %s", str(ve))
                            raise AuditForgeException(
                                code=ErrorCode.PROCESSING_FAILED,
                                message="AI Engine document output failed validation",
                                status_code=502,
                            )
                    elif response.status_code >= 500:
                        last_error = f"HTTP {response.status_code}"
                    else:
                        raise AuditForgeException(
                            code=ErrorCode.PROCESSING_FAILED,
                            message=f"AI Engine rejected doc request: {response.text}",
                            status_code=502,
                        )
            except (httpx.TimeoutException, httpx.NetworkError) as e:
                last_error = str(e)

            if attempt <= self.max_retries:
                await asyncio.sleep(0.5 * attempt)

        raise AuditForgeException(
            code=ErrorCode.PROVIDER_UNAVAILABLE,
            message=f"AI Engine unavailable: {last_error}",
            status_code=503,
        )

    def _mock_visual_assessment(self, payload: VisualAssessmentInput) -> VisualAssessmentOutput:
        """Deterministic test adapter used in development when Member 3 service is external."""
        return VisualAssessmentOutput(
            schema_version="1.0",
            result_type="visual_observation",
            observations=[
                ObservationItem(
                    observation="Concrete column framing visible in submitted live camera capture.",
                    criterion_id=None,
                    evidence_refs=[ObservationRef(evidence_id=payload.evidence_id)],
                    classification="observed",
                    confidence_value=0.88,
                    confidence_semantics="uncalibrated",
                    limitations=[
                        "Single camera angle cannot determine internal rebar quality or total structural capacity."
                    ],
                    requires_human_review=True,
                )
            ],
            provider={"name": "test_adapter", "model": "mock-vlm-v1"},
            prompt_version="visual-audit-v1",
            processed_at=datetime.now(timezone.utc),
        )

    def _mock_document_extraction(self, payload: DocumentExtractionInput) -> DocumentExtractionOutput:
        """Deterministic test adapter used in development when Member 3 service is external."""
        return DocumentExtractionOutput(
            schema_version="1.0",
            document_type=payload.document_type,
            raw_document_number="CH-2026-088",
            normalized_document_number="CH2026088",
            vendor_name="Ultratech Concrete Supplies Ltd",
            document_date=datetime.now(timezone.utc),
            currency="INR",
            total_amount=154200.0,
            fields=[
                ExtractedFieldItem(
                    field_name="document_number",
                    raw_value="CH-2026-088",
                    normalized_value="CH2026088",
                    confidence=0.95,
                    confidence_semantics="uncalibrated",
                    page_number=1,
                ),
                ExtractedFieldItem(
                    field_name="vendor_name",
                    raw_value="Ultratech Concrete Supplies Ltd",
                    normalized_value="Ultratech Concrete Supplies Ltd",
                    confidence=0.92,
                    confidence_semantics="uncalibrated",
                    page_number=1,
                ),
                ExtractedFieldItem(
                    field_name="material_code",
                    raw_value="OPC 53 Cement",
                    normalized_value="CEMENT_OPC_53",
                    confidence=0.89,
                    confidence_semantics="uncalibrated",
                    page_number=1,
                ),
                ExtractedFieldItem(
                    field_name="quantity",
                    raw_value="500 bags",
                    normalized_value="500",
                    confidence=0.94,
                    confidence_semantics="uncalibrated",
                    page_number=1,
                ),
            ],
            provider={"name": "test_adapter", "model": "mock-ocr-doc-v1"},
            processed_at=datetime.now(timezone.utc),
        )


ai_engine_client = AIEngineClient()
