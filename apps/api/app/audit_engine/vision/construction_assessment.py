"""Visual inspection evaluation and milestone criteria mapping."""

from typing import List

from app.audit_engine.contracts.evidence import EvidencePayload, EvidenceType
from app.audit_engine.contracts.requests import AcceptanceCriterion
from app.audit_engine.contracts.responses import (
    VisualAssessmentResult,
)
from app.audit_engine.vision.provider import VisualAssessmentProvider


async def assess_site_photographs(
    evidence_items: List[EvidencePayload],
    criteria: List[AcceptanceCriterion],
    provider: VisualAssessmentProvider,
) -> List[VisualAssessmentResult]:
    """Assess all site photo evidence against explicit milestone acceptance criteria.
    
    CRITICAL PRINCIPLE (AGENTS.md & docs/08_AI_EVIDENCE_PIPELINE.md):
    AI observations are review signals and candidate observations;
    AI confidence cannot autonomously approve a milestone or clear a certificate.
    """
    results: List[VisualAssessmentResult] = []

    site_photos = [e for e in evidence_items if e.evidence_type == EvidenceType.SITE_PHOTO]
    for photo in site_photos:
        raw_bytes = photo.content_bytes or b""
        if not raw_bytes and photo.content_base64:
            import base64
            raw_bytes = base64.b64decode(photo.content_base64)

        assessment = await provider.assess_milestone(
            image_bytes=raw_bytes,
            evidence_id=photo.evidence_id,
            criteria=criteria,
            project_context={"source_notes": photo.source_notes},
        )
        results.append(assessment)

    return results
