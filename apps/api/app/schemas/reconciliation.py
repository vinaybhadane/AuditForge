import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ReconciliationScope(BaseModel):
    material_codes: Optional[List[str]] = Field(default_factory=list)
    location_ids: Optional[List[uuid.UUID]] = Field(default_factory=list)


class ReconciliationStartRequest(BaseModel):
    period_start: datetime
    period_end: datetime
    baseline_version_id: Optional[uuid.UUID] = None
    scope: Optional[ReconciliationScope] = None
    idempotency_key: Optional[str] = Field(None, max_length=128)


class ReconciliationLineResponse(BaseModel):
    id: uuid.UUID
    rule_code: str
    line_type: str
    material_code: str
    raw_expected_quantity: Optional[Decimal] = None
    raw_observed_quantity: Optional[Decimal] = None
    normalized_expected_quantity: Decimal
    normalized_observed_quantity: Decimal
    unit: str
    delta_quantity: Decimal
    tolerance: Decimal
    status: str
    explanation: str

    model_config = {"from_attributes": True}


class ReconciliationRunResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    baseline_version_id: Optional[uuid.UUID] = None
    period_start: datetime
    period_end: datetime
    input_snapshot_hash: str
    algorithm_version: str
    status: str
    created_at: datetime
    summary_metrics: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}


class ReconciliationDetailResponse(BaseModel):
    run: ReconciliationRunResponse
    lines: List[ReconciliationLineResponse]
