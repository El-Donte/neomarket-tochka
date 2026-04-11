from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class InvoiceCreate(SQLModel):
    seller_id: int
    number: Optional[str] = None
    comment: Optional[str] = None

class InvoiceRead(SQLModel):
    id: int
    seller_id: int
    number: Optional[str] = None
    status: str
    created_at: datetime

class InvoiceItem(SQLModel, table=True):
    __tablename__ = "invoice_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoices.id")
    sku_id: int = Field(foreign_key="skus.id")
    quantity: int
    purchase_price: Optional[int] = None