"""Base provider definitions and error handling."""

from typing import Optional

from pydantic import BaseModel


class ProviderInfo(BaseModel):
    name: str
    model_id: str
    is_available: bool = False
    endpoint_url: Optional[str] = None
