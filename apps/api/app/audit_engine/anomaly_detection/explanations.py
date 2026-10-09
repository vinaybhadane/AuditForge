"""Objective explanation helpers and audit finding rationale."""

from app.audit_engine.contracts.findings import AnomalyFinding


def format_finding_audit_summary(finding: AnomalyFinding) -> str:
    """Format an objective, audit-grade explanation of a finding without accusatory language."""
    summary_parts = [
        f"[{finding.rule_id} - {finding.severity.value.upper()}] {finding.title}:",
        finding.explanation,
    ]
    if finding.calculation_formula:
        summary_parts.append(f"Formula: {finding.calculation_formula}")
    if finding.uncertainty_notes:
        summary_parts.append(f"Caveats & Limitations: {finding.uncertainty_notes}")
    summary_parts.append(f"Recommended Action: {finding.recommended_action}")
    return "\n".join(summary_parts)
