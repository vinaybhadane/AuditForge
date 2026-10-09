import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import NotFoundException
from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.models.review_and_certificates import ClearanceCertificate
from app.db.session import get_db
from app.schemas.milestones import CertificateResponse

router = APIRouter(tags=["Clearance Certificates"])


@router.get(
    "/certificates/{id}",
    response_model=CertificateResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Certificate Metadata",
)
async def get_certificate(
    id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CertificateResponse:
    cert = db.execute(select(ClearanceCertificate).where(ClearanceCertificate.id == id)).scalar_one_or_none()
    if not cert:
        raise NotFoundException(message="Certificate not found")
    await verify_project_access(cert.project_id, user, db)
    return CertificateResponse.model_validate(cert)


@router.get(
    "/certificates/{id}/download",
    status_code=status.HTTP_200_OK,
    summary="Get Short-lived Certificate Download URL",
)
async def get_certificate_download_url(
    id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    cert = db.execute(select(ClearanceCertificate).where(ClearanceCertificate.id == id)).scalar_one_or_none()
    if not cert:
        raise NotFoundException(message="Certificate not found")
    await verify_project_access(cert.project_id, user, db)

    expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.SIGNED_URL_TTL_SECONDS)
    download_url = f"{settings.SUPABASE_URL}/storage/v1/object/sign/{settings.REPORTS_BUCKET}/{cert.report_object_key}?token=mock-cert-dl-sig"

    return {
        "certificate_id": str(cert.id),
        "certificate_number": cert.certificate_number,
        "download_url": download_url,
        "expires_at": expires_at.isoformat(),
    }
