"""Transparent review priority scoring and rule weighting."""

from typing import Dict, List

from app.audit_engine.config import engine_config
from app.audit_engine.contracts.findings import AnomalyFinding


def calculate_review_priority_score(findings: List[AnomalyFinding]) -> Dict:
    """Calculate transparent composite review priority score.
    
    CRITICAL PRINCIPLE (docs/10_ANOMALY_DETECTION.md):
    Composite priority score is an operational triage metric for human reviewers,
    NEVER a calibrated probability of fraud or illegality.
    """
    total_score = 0
    severity_counts = {"info": 0, "low": 0, "medium": 0, "high": 0, "critical": 0}

    for f in findings:
        sev_key = f.severity.value
        severity_counts[sev_key] = severity_counts.get(sev_key, 0) + 1
        weight = engine_config.SEVERITY_WEIGHTS.get(sev_key, 1)
        total_score += weight

    return {
        "composite_priority_score": total_score,
        "finding_count": len(findings),
        "severity_breakdown": severity_counts,
        "semantics": "Operational triage priority for human auditor investigation queue",
        "is_calibrated_probability": False,
    }
