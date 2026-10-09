from datetime import datetime, timezone

from fastapi import APIRouter, status

from app import __version__
from app.core.config import settings
from app.schemas.health import HealthCheckItem, HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/live",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Process Liveness",
    description="Returns HTTP 200 if the FastAPI application process is alive and receiving traffic.",
)
async def check_liveness() -> HealthResponse:
    return HealthResponse(
        status="pass",
        version=__version__,
        timestamp=datetime.now(timezone.utc),
        environment=settings.APP_ENV,
        checks={"process": HealthCheckItem(status="pass", message="API process active")},
    )


@router.get(
    "/ready",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Dependency Readiness",
    description="Returns HTTP 200 if the service dependencies are configured and ready. Does not expose credentials.",
)
async def check_readiness() -> HealthResponse:
    # Readiness checks: verify basic configuration presence without leaking secrets
    checks = {
        "configuration": HealthCheckItem(status="pass", message="Settings validated"),
        "database_scaffolding": HealthCheckItem(
            status="pass" if settings.DATABASE_URL else "warn",
            message="Database URL configured" if settings.DATABASE_URL else "Database URL not configured",
        ),
        "storage_scaffolding": HealthCheckItem(
            status="pass" if settings.EVIDENCE_BUCKET else "warn",
            message="Evidence bucket defined",
        ),
    }

    overall_status = "pass"
    for check in checks.values():
        if check.status == "fail":
            overall_status = "fail"
            break
        elif check.status == "warn" and overall_status != "fail":
            overall_status = "warn"

    return HealthResponse(
        status=overall_status,
        version=__version__,
        timestamp=datetime.now(timezone.utc),
        environment=settings.APP_ENV,
        checks=checks,
    )
