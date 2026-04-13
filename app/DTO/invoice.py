from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel

class InvoiceItemCreate(SQLModel):
    sku_id: int
    quantity: int
    purchase_price: Optional[int] = None

class InvoiceItemRead(SQLModel):
    id: int
    sku_id: int
    quantity: int
    purchase_price: Optional[int] = None

class InvoiceCreate(SQLModel):
    seller_id: int
    number: Optional[str] = None
    comment: Optional[str] = None
    items: List[InvoiceItemCreate]

class InvoiceRead(SQLModel):
    id: int
    seller_id: int
    number: Optional[str] = None
    status: str
    created_at: datetime
    items: List[InvoiceItemRead] = []
