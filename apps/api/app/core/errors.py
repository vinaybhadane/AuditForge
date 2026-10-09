from enum import Enum
from typing import Any, Dict, List, Optional

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import request_id_ctx


class ErrorCode(str, Enum):
    AUTH_REQUIRED = "AUTH_REQUIRED"
    FORBIDDEN = "FORBIDDEN"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_INGESTION_SOURCE = "INVALID_INGESTION_SOURCE"
    STATE_CONFLICT = "STATE_CONFLICT"
    IDEMPOTENCY_CONFLICT = "IDEMPOTENCY_CONFLICT"
    UNSUPPORTED_MEDIA_TYPE = "UNSUPPORTED_MEDIA_TYPE"
    PAYLOAD_TOO_LARGE = "PAYLOAD_TOO_LARGE"
    RATE_LIMITED = "RATE_LIMITED"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    PROCESSING_FAILED = "PROCESSING_FAILED"
    CLEARANCE_BLOCKED = "CLEARANCE_BLOCKED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class AuditForgeException(Exception):
    """Base exception for AuditForge domain and API errors."""

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []


class NotFoundException(AuditForgeException):
    def __init__(self, message: str = "Resource not found", details: Optional[List[Dict[str, Any]]] = None) -> None:
        super().__init__(
            code=ErrorCode.RESOURCE_NOT_FOUND,
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class ForbiddenException(AuditForgeException):
    def __init__(self, message: str = "Access forbidden", details: Optional[List[Dict[str, Any]]] = None) -> None:
        super().__init__(
            code=ErrorCode.FORBIDDEN,
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details,
        )


class UnauthorizedException(AuditForgeException):
    def __init__(self, message: str = "Authentication required", details: Optional[List[Dict[str, Any]]] = None) -> None:
        super().__init__(
            code=ErrorCode.AUTH_REQUIRED,
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
        )


def build_error_response(
    code: str,
    message: str,
    status_code: int,
    request_id: Optional[str] = None,
    details: Optional[List[Dict[str, Any]]] = None,
) -> JSONResponse:
    req_id = request_id or request_id_ctx.get() or "unknown-request-id"
    payload = {
        "error": {
            "code": code,
            "message": message,
            "request_id": req_id,
            "details": details or [],
        }
    }
    return JSONResponse(status_code=status_code, content=payload)


async def auditforge_exception_handler(request: Request, exc: AuditForgeException) -> JSONResponse:
    return build_error_response(
        code=exc.code.value if isinstance(exc.code, ErrorCode) else str(exc.code),
        message=exc.message,
        status_code=exc.status_code,
        request_id=request_id_ctx.get(),
        details=exc.details,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    details: List[Dict[str, Any]] = []
    for err in exc.errors():
        field_path = ".".join(str(loc) for loc in err.get("loc", []) if loc != "body")
        details.append({
            "field": field_path or "root",
            "code": err.get("type", "VALIDATION_ERROR").upper(),
            "message": err.get("msg", "Invalid value"),
        })

    return build_error_response(
        code=ErrorCode.VALIDATION_ERROR.value,
        message="The request could not be processed.",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        request_id=request_id_ctx.get(),
        details=details,
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    code_map = {
        401: ErrorCode.AUTH_REQUIRED.value,
        403: ErrorCode.FORBIDDEN.value,
        404: ErrorCode.RESOURCE_NOT_FOUND.value,
        405: "METHOD_NOT_ALLOWED",
        429: ErrorCode.RATE_LIMITED.value,
    }
    code = code_map.get(exc.status_code, f"HTTP_{exc.status_code}")
    return build_error_response(
        code=code,
        message=str(exc.detail) if exc.detail else "An HTTP error occurred.",
        status_code=exc.status_code,
        request_id=request_id_ctx.get(),
        details=[],
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return build_error_response(
        code=ErrorCode.INTERNAL_ERROR.value,
        message="An unexpected server error occurred.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        request_id=request_id_ctx.get(),
        details=[],
    )
