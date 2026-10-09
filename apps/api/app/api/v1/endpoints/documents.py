import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.errors import NotFoundException
from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.models.evidence import Document, ExtractedFieldVersion
from app.db.session import get_db
from app.schemas.documents import (
    DocumentResponse,
    ExtractedFieldCorrectionRequest,
    ExtractedFieldResponse,
)

router = APIRouter(tags=["Documents & Field Corrections"])


@router.get(
    "/projects/{project_id}/documents",
    response_model=List[DocumentResponse],
    status_code=status.HTTP_200_OK,
    summary="List Extracted Documents",
)
async def list_documents(
    project_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[DocumentResponse]:
    await verify_project_access(project_id, user, db)
    docs = list(db.execute(select(Document).where(Document.project_id == project_id)).scalars().all())
    return [DocumentResponse.model_validate(d) for d in docs]


@router.get(
    "/documents/{id}",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Document and Fields",
)
async def get_document(
    id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DocumentResponse:
    doc = db.execute(select(Document).where(Document.id == id)).scalar_one_or_none()
    if not doc:
        raise NotFoundException(message="Document not found")
    await verify_project_access(doc.project_id, user, db)
    return DocumentResponse.model_validate(doc)


@router.post(
    "/documents/{id}/fields/{field_name}/corrections",
    response_model=ExtractedFieldResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record Versioned Field Correction",
    description="Appends a new field version with reviewer provenance while preserving the original extraction.",
)
async def record_field_correction(
    id: uuid.UUID,
    field_name: str,
    data: ExtractedFieldCorrectionRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExtractedFieldResponse:
    doc = db.execute(select(Document).where(Document.id == id)).scalar_one_or_none()
    if not doc:
        raise NotFoundException(message="Document not found")
    await verify_project_access(doc.project_id, user, db, require_write=True)

    # Find highest existing version of the field
    latest_field = db.execute(
        select(ExtractedFieldVersion)
        .where(
            and_(
                ExtractedFieldVersion.document_id == id,
                ExtractedFieldVersion.field_name == field_name,
            )
        )
        .order_by(ExtractedFieldVersion.version.desc())
    ).scalars().first()

    current_version = latest_field.version if latest_field else 0
    raw_val = latest_field.raw_value if latest_field else data.normalized_value

    new_field = ExtractedFieldVersion(
        document_id=id,
        field_name=field_name,
        raw_value=raw_val,
        normalized_value=data.normalized_value,
        version=current_version + 1,
        review_status="corrected",
        corrected_by=user.id,
        correction_reason=data.correction_reason,
    )
    db.add(new_field)
    db.commit()
    db.refresh(new_field)
    return ExtractedFieldResponse.model_validate(new_field)
