"""AuditEngine configuration and operational defaults."""

from decimal import Decimal
from typing import Dict

from pydantic import BaseModel, Field


class EngineConfig(BaseModel):
    """Configuration settings for the AuditForge AI Audit Engine."""

    # Schema & Pipeline Versioning
    SCHEMA_VERSION: str = "1.0"
    PIPELINE_VERSION: str = "audit-pipeline-v1"
    VLM_PROMPT_VERSION: str = "visual-audit-v1"
    EXTRACTION_PIPELINE_VERSION: str = "doc-extract-v1"

    # Ingestion Limits
    MAX_FILE_BYTES: int = 20_971_520  # 20 MB
    MAX_PDF_PAGES: int = 100
    MAX_IMAGE_PIXELS: int = 40_000_000

    # Reconciliation Defaults
    DEFAULT_QUANTITY_TOLERANCE_PERCENT: Decimal = Decimal("0.01")  # 1% allowable tolerance
    DEFAULT_FINANCIAL_TOLERANCE_ABSOLUTE: Decimal = Decimal("1.00")  # Currency unit tolerance
    DEFAULT_WASTAGE_PERCENT: Decimal = Decimal("0.05")  # 5% standard wastage allowance

    # Rule Severity Weights (for composite review priority, not fraud probability)
    SEVERITY_WEIGHTS: Dict[str, int] = Field(
        default_factory=lambda: {
            "info": 1,
            "low": 2,
            "medium": 4,
            "high": 8,
            "critical": 16,
        }
    )

    # Provider Timeouts and Backoff
    PROVIDER_TIMEOUT_SECONDS: float = 60.0
    PROVIDER_MAX_RETRIES: int = 3
    RETRY_BACKOFF_BASE_SECONDS: float = 1.5


engine_config = EngineConfig()
