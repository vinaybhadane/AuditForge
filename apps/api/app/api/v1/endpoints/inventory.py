import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.models.inventory import GoodsReceipt, GoodsReceiptLine, StockMovement
from app.db.session import get_db
from app.schemas.inventory import (
    GoodsReceiptCreate,
    GoodsReceiptResponse,
    StockMovementCreate,
    StockMovementResponse,
)

router = APIRouter(tags=["Inventory & Stock Movements"])


@router.get(
    "/projects/{id}/inventory/receipts",
    response_model=List[GoodsReceiptResponse],
    status_code=status.HTTP_200_OK,
    summary="List Goods Receipts",
)
async def list_receipts(
    id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[GoodsReceiptResponse]:
    await verify_project_access(id, user, db)
    receipts = list(db.execute(select(GoodsReceipt).where(GoodsReceipt.project_id == id)).scalars().all())
    return [GoodsReceiptResponse.model_validate(r) for r in receipts]


@router.post(
    "/projects/{id}/inventory/receipts",
    response_model=GoodsReceiptResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Goods Receipt",
)
async def create_receipt(
    id: uuid.UUID,
    data: GoodsReceiptCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GoodsReceiptResponse:
    # Requires Store in-charge, project manager, or admin
    await verify_project_access(
        id, user, db, allowed_roles={"store_in_charge", "project_manager", "org_admin"}
    )

    grn = GoodsReceipt(
        project_id=id,
        store_location_id=data.store_location_id,
        receipt_number=data.receipt_number,
        receipt_date=data.receipt_date,
        source_evidence_id=data.source_evidence_id,
        received_by=user.id,
        status="accepted",
    )
    db.add(grn)
    db.flush()

    for line in data.lines:
        grn_line = GoodsReceiptLine(
            goods_receipt_id=grn.id,
            material_code=line.material_code,
            quantity=line.quantity,
            unit=line.unit,
            challan_reference=line.challan_reference,
            condition_notes=line.condition_notes,
        )
        db.add(grn_line)

        # Automatically post positive stock receipt movement
        movement = StockMovement(
            project_id=id,
            material_code=line.material_code,
            location_id=data.store_location_id,
            movement_type="receipt",
            quantity=line.quantity,
            unit=line.unit,
            effective_date=data.receipt_date,
            source_reference=data.receipt_number,
            actor_id=user.id,
        )
        db.add(movement)

    db.commit()
    db.refresh(grn)
    return GoodsReceiptResponse.model_validate(grn)


@router.get(
    "/projects/{id}/inventory/movements",
    response_model=List[StockMovementResponse],
    status_code=status.HTTP_200_OK,
    summary="List Stock Movements",
)
async def list_movements(
    id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[StockMovementResponse]:
    await verify_project_access(id, user, db)
    movements = list(
        db.execute(select(StockMovement).where(StockMovement.project_id == id).order_by(StockMovement.created_at.desc())).scalars().all()
    )
    return [StockMovementResponse.model_validate(m) for m in movements]


@router.post(
    "/projects/{id}/inventory/movements",
    response_model=StockMovementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record Stock Movement",
)
async def record_movement(
    id: uuid.UUID,
    data: StockMovementCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StockMovementResponse:
    await verify_project_access(id, user, db, require_write=True)
    m = StockMovement(
        project_id=id,
        material_code=data.material_code,
        location_id=data.location_id,
        movement_type=data.movement_type,
        quantity=data.quantity,
        unit=data.unit,
        effective_date=data.effective_date,
        source_reference=data.source_reference,
        source_evidence_id=data.source_evidence_id,
        actor_id=user.id,
        notes=data.notes,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return StockMovementResponse.model_validate(m)
