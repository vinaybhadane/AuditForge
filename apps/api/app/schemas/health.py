from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


class HealthCheckItem(BaseModel):
    status: str
    message: Optional[str] = None


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall health status: pass, warn, or fail")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(..., description="UTC ISO-8601 timestamp")
    environment: str = Field(..., description="Execution environment")
    checks: Dict[str, HealthCheckItem] = Field(default_factory=dict, description="Component readiness checks")
