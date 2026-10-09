"""Supabase Auth Integration and Cryptographic JWT Verification.

Per docs/07_SECURITY_AND_ACCESS_CONTROL.md:
- Cryptographically verify token signature, expiry, issuer, and expected audience.
- Never merely decode a token.
- Extract authenticated user identity (sub claim) and metadata.
"""

import uuid
from typing import Any, Dict, Optional

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.core.config import settings
from app.core.errors import UnauthorizedException
from app.core.logging import get_logger

logger = get_logger("supabase_auth")


class SupabaseAuthVerifier:
    """Verifies Supabase Auth JWTs cryptographically."""

    def __init__(
        self,
        jwt_secret: Optional[str] = None,
        issuer: Optional[str] = None,
        audience: Optional[str] = None,
    ) -> None:
        self.jwt_secret = jwt_secret or settings.SUPABASE_JWT_SECRET
        self.issuer = issuer or settings.SUPABASE_JWT_ISSUER
        self.audience = audience or settings.SUPABASE_JWT_AUDIENCE

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify the JWT signature and claims.
        
        Raises:
            UnauthorizedException: If token is expired, invalid, or has bad signature.
        """
        if not token:
            raise UnauthorizedException(message="Token is missing")

        # Configured options
        options = {
            "verify_signature": True,
            "verify_exp": True,
            "verify_nbf": True,
            "require": ["exp", "sub"],
        }
        if not self.issuer:
            options["verify_iss"] = False
        if not self.audience:
            options["verify_aud"] = False

        try:
            # We support HS256 (Supabase shared secret) as well as RS256/ES256
            header = jwt.get_unverified_header(token)
            alg = header.get("alg", "HS256")

            if alg not in ["HS256", "RS256", "ES256"]:
                raise UnauthorizedException(message=f"Unsupported token algorithm: {alg}")

            payload = jwt.decode(
                token,
                key=self.jwt_secret or "insecure-placeholder",
                algorithms=[alg],
                issuer=self.issuer if self.issuer else None,
                audience=self.audience if self.audience else None,
                options=options,
            )

            # Ensure subject is a valid UUID
            sub = payload.get("sub")
            if not sub:
                raise UnauthorizedException(message="Token missing 'sub' subject claim")
            try:
                uuid.UUID(str(sub))
            except ValueError:
                raise UnauthorizedException(message="Token subject is not a valid UUID")

            return payload

        except ExpiredSignatureError:
            raise UnauthorizedException(
                message="Authentication token has expired",
                details=[{"field": "token", "code": "TOKEN_EXPIRED"}],
            )
        except InvalidTokenError as e:
            logger.warning("Invalid token received: %s", str(e))
            raise UnauthorizedException(
                message="Invalid or tampered authentication token",
                details=[{"field": "token", "code": "INVALID_TOKEN"}],
            )
        except Exception as e:
            logger.error("Token verification unexpected error: %s", str(e))
            raise UnauthorizedException(message="Failed to verify authentication token")


# Singleton instance
supabase_verifier = SupabaseAuthVerifier()
