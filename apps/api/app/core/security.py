"""Security utilities and authentication scaffolding.

Actual cryptographic JWT verification, Supabase integration, and project-level
membership authorization are implemented in Phase 02 per docs/07_SECURITY_AND_ACCESS_CONTROL.md.
"""

from typing import Optional

from fastapi import Header

from app.core.errors import UnauthorizedException


async def get_current_user_token(
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> str:
    """Extract bearer token from authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException(message="Missing or malformed Authorization header")
    return authorization.replace("Bearer ", "").strip()
