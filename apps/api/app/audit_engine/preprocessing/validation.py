"""File signature sniffing, size limits, and ingestion modality enforcement."""

import hashlib
from typing import Tuple

from app.audit_engine.config import engine_config
from app.audit_engine.contracts.evidence import EvidencePayload, EvidenceType, IngestionSource
from app.audit_engine.exceptions import (
    EngineValidationError,
    IngestionModalityViolationError,
    UnsupportedFileFormatError,
)

# Magic bytes definitions
FILE_SIGNATURES = {
    "pdf": b"%PDF-",
    "jpeg": b"\xff\xd8\xff",
    "png": b"\x89PNG\r\n\x1a\n",
    "tiff_le": b"II*\x00",
    "tiff_be": b"MM\x00*",
}


def detect_file_format(content: bytes) -> str:
    """Detect format from byte magic numbers, ignoring client-declared extensions."""
    if content.startswith(FILE_SIGNATURES["pdf"]):
        return "application/pdf"
    if content.startswith(FILE_SIGNATURES["jpeg"]):
        return "image/jpeg"
    if content.startswith(FILE_SIGNATURES["png"]):
        return "image/png"
    if content.startswith(FILE_SIGNATURES["tiff_le"]) or content.startswith(FILE_SIGNATURES["tiff_be"]):
        return "image/tiff"
    return "application/octet-stream"


def calculate_sha256(content: bytes) -> str:
    """Deterministic SHA-256 hash calculation."""
    return hashlib.sha256(content).hexdigest()


def validate_evidence_payload(payload: EvidencePayload) -> Tuple[str, str, int]:
    """Validate evidence payload for integrity, size limits, and ingestion modality policy.
    
    Returns:
        Tuple of (detected_mime_type, sha256_hash, byte_size)
    """
    content = payload.content_bytes
    if not content:
        if payload.content_base64:
            import base64
            content = base64.b64decode(payload.content_base64)
        else:
            raise EngineValidationError("Evidence payload contains no content bytes or base64 data.")

    byte_size = len(content)
    if byte_size > engine_config.MAX_FILE_BYTES:
        raise EngineValidationError(
            f"PAYLOAD_TOO_LARGE: Evidence size {byte_size} bytes exceeds maximum limit "
            f"of {engine_config.MAX_FILE_BYTES} bytes."
        )

    # Ingestion Modality Policy Enforcement
    # AGENTS.md & docs/07_SECURITY_AND_ACCESS_CONTROL.md
    if payload.evidence_type == EvidenceType.SITE_PHOTO and payload.ingestion_source != IngestionSource.LIVE_CAPTURE:
        raise IngestionModalityViolationError(
            "INVALID_INGESTION_SOURCE: Construction site progress photos strictly require live camera capture. "
            "Uploading pre-existing gallery/disk image files is disabled to enforce physical presence and freshness."
        )

    detected_mime = detect_file_format(content)
    if detected_mime == "application/octet-stream":
        raise UnsupportedFileFormatError(
            "UNSUPPORTED_MEDIA_TYPE: File does not match supported PDF, JPEG, PNG, or TIFF binary signatures."
        )

    # For site photos, verify it's an image
    if payload.evidence_type == EvidenceType.SITE_PHOTO and not detected_mime.startswith("image/"):
        raise EngineValidationError(
            f"INVALID_MEDIA_TYPE: Site progress photo must be an image, received {detected_mime}."
        )

    sha256 = calculate_sha256(content)
    return detected_mime, sha256, byte_size
