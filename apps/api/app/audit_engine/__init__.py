"""AuditForge AI Audit Engine.

Evidence-first AI construction auditing engine:
- Document & OCR extraction
- Construction photo visual assessment
- Deterministic material reconciliation
- Explainable anomaly detection
- Traceable evidence correlation
"""

from app.audit_engine.config import engine_config
from app.audit_engine.contracts import (
    AnomalyFinding,
    AuditEngineRequest,
    AuditEngineResponse,
    EngineStatus,
    EvidencePayload,
    EvidenceType,
    FindingCategory,
    FindingSeverity,
    IngestionSource,
    ReconciliationResult,
)
from app.audit_engine.exceptions import (
    AuditEngineError,
    EngineValidationError,
    IngestionModalityViolationError,
    UnitConversionError,
)
from app.audit_engine.pipeline import AuditEnginePipeline

__all__ = [
    "AuditEnginePipeline",
    "AuditEngineRequest",
    "AuditEngineResponse",
    "AnomalyFinding",
    "EvidencePayload",
    "EvidenceType",
    "IngestionSource",
    "FindingCategory",
    "FindingSeverity",
    "EngineStatus",
    "ReconciliationResult",
    "engine_config",
    "AuditEngineError",
    "EngineValidationError",
    "IngestionModalityViolationError",
    "UnitConversionError",
]
