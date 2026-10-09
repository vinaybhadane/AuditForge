"""AuditEngine custom exception hierarchy."""

from typing import Any, Dict, List, Optional


class AuditEngineError(Exception):
    """Base exception for all AuditEngine errors."""

    def __init__(self, message: str, details: Optional[List[Dict[str, Any]]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or []


class EngineValidationError(AuditEngineError):
    """Raised when request payload or evidence violates schema constraints."""
    pass


class IngestionModalityViolationError(AuditEngineError):
    """Raised when an evidence asset violates ingestion modality policy (e.g. file upload for site photo)."""
    pass


class UnsupportedFileFormatError(AuditEngineError):
    """Raised when input file MIME or magic bytes are unsupported or corrupted."""
    pass


class DocumentExtractionError(AuditEngineError):
    """Raised when text/field extraction fails critically."""
    pass


class UnitConversionError(AuditEngineError):
    """Raised when incompatible or unmapped units of measure are encountered."""
    pass


class ProviderUnavailableError(AuditEngineError):
    """Raised when external AI provider is unconfigured, unreachable, or timed out."""
    pass


class ProviderResponseValidationError(AuditEngineError):
    """Raised when AI provider returns malformed or non-schema-compliant output."""
    pass
