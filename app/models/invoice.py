from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.sku import SKU

class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"
    id: Optional[int] = Field(default=None, primary_key=True)
    seller_id: int = Field(foreign_key="sellers.id")
    number: Optional[str] = None
    status: str = Field(default="CREATED")
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    items: List["InvoiceItem"] = Relationship(back_populates="invoice")


class InvoiceItem(SQLModel, table=True):
    __tablename__ = "invoice_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoices.id")
    sku_id: int = Field(foreign_key="skus.id")
    quantity: int
    purchase_price: Optional[int] = None

    invoice: "Invoice" = Relationship(back_populates="items")
    sku: "SKU" = Relationship(back_populates="invoice_items")


class Stock(SQLModel, table=True):
    __tablename__ = "stocks"
    id: Optional[int] = Field(default=None, primary_key=True)
    sku_id: int = Field(foreign_key="skus.id", unique=True)
    quantity: int = Field(default=0)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    sku: Optional["SKU"] = Relationship(back_populates="stock")