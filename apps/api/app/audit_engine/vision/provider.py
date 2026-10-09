"""Abstract provider interface for visual construction assessment."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID

from app.audit_engine.contracts.requests import AcceptanceCriterion
from app.audit_engine.contracts.responses import VisualAssessmentResult


class VisualAssessmentProvider(ABC):
    """Abstract interface for VLM visual inspection providers."""

    @abstractmethod
    async def assess_milestone(
        self,
        image_bytes: bytes,
        evidence_id: UUID,
        criteria: List[AcceptanceCriterion],
        project_context: Dict[str, Any],
    ) -> VisualAssessmentResult:
        """Assess an on-site photograph against explicit milestone acceptance criteria."""
        pass
