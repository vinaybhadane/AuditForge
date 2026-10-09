"""Pipeline stage enumerations."""

from enum import Enum


class PipelineStage(str, Enum):
    INPUT_VALIDATION = "input_validation"
    EVIDENCE_PREPROCESSING = "evidence_preprocessing"
    DOCUMENT_EXTRACTION = "document_extraction"
    MATERIAL_RECONCILIATION = "material_reconciliation"
    VISUAL_ASSESSMENT = "visual_assessment"
    ANOMALY_DETECTION = "anomaly_detection"
    EVIDENCE_CORRELATION = "evidence_correlation"
    RESPONSE_ASSEMBLY = "response_assembly"
