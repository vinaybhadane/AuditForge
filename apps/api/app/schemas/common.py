from typing import List, Optional

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    field: Optional[str] = None
    code: str
    message: Optional[str] = None


class ErrorEnvelopeBody(BaseModel):
    code: str
    message: str
    request_id: str
    details: List[ErrorDetail] = Field(default_factory=list)


class ErrorEnvelope(BaseModel):
    error: ErrorEnvelopeBody


class PaginationParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    cursor: Optional[str] = None
