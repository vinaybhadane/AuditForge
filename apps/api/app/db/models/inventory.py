import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class InventoryLocation(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "inventory_locations"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location_type: Mapped[str] = mapped_column(String(50), default="main_site_store", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("project_id", "code", name="uq_project_location_code"),
    )


class StockMovement(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "stock_movements"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    material_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    location_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("inventory_locations.id", ondelete="SET NULL"), nullable=True
    )
    movement_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # Types: opening_balance, receipt, issue, return, adjustment, transfer_in, transfer_out, reversal
    quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    source_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source_evidence_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)
    actor_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    reversed_movement_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        Index("ix_stock_proj_mat_date", "project_id", "material_code", "effective_date"),
    )


class PurchaseOrder(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "purchase_orders"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    vendor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("vendors.id", ondelete="SET NULL"), nullable=True
    )
    po_number: Mapped[str] = mapped_column(String(100), nullable=False)
    po_date: Mapped[date] = mapped_column(Date, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="issued", nullable=False)
    source_evidence_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("project_id", "po_number", name="uq_project_po_number"),
    )

    lines = relationship("PurchaseOrderLine", back_populates="purchase_order", cascade="all, delete-orphan")


class PurchaseOrderLine(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "purchase_order_lines"

    purchase_order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    material_code: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    ordered_quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    line_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    purchase_order = relationship("PurchaseOrder", back_populates="lines")


class GoodsReceipt(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "goods_receipts"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    store_location_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("inventory_locations.id", ondelete="SET NULL"), nullable=True
    )
    receipt_number: Mapped[str] = mapped_column(String(100), nullable=False)
    receipt_date: Mapped[date] = mapped_column(Date, nullable=False)
    source_evidence_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)
    received_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="accepted", nullable=False)

    __table_args__ = (
        UniqueConstraint("project_id", "receipt_number", name="uq_project_grn_number"),
    )

    lines = relationship("GoodsReceiptLine", back_populates="goods_receipt", cascade="all, delete-orphan")


class GoodsReceiptLine(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "goods_receipt_lines"

    goods_receipt_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("goods_receipts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    material_code: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    challan_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    condition_notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    goods_receipt = relationship("GoodsReceipt", back_populates="lines")
