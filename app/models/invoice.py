from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey
from uuid import UUID
from uuid6 import uuid7

if TYPE_CHECKING:
    from app.models.sku import SKU

class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    seller_id: UUID = Field(foreign_key="sellers.id")
    number: Optional[str] = None
    status: str = Field(default="CREATED")
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
    accepted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    accepted_by: Optional[UUID] = None

    items: List["InvoiceItem"] = Relationship(back_populates="invoice")


class InvoiceItem(SQLModel, table=True):
    __tablename__ = "invoice_items"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    invoice_id: UUID = Field(foreign_key="invoices.id")
    sku_id: UUID = Field(foreign_key="skus.id")
    quantity: int
    purchase_price: Optional[int] = None
    accepted_quantity: int = Field(default=0)

    invoice: "Invoice" = Relationship(back_populates="items")
    sku: "SKU" = Relationship(back_populates="invoice_items")


class Stock(SQLModel, table=True):
    __tablename__ = "stocks"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    sku_id: UUID = Field(foreign_key="skus.id", unique=True)
    stock_quantity: int = Field(default=0)
    active_quantity: int = Field(default=0)
    reserved_quantity: int = Field(default=0)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))

    sku: Optional["SKU"] = Relationship(back_populates="stock")