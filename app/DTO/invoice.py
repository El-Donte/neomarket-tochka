from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel
from app.DTO.sku import SKURead

class InvoiceItemCreate(SQLModel):
    sku_id: int
    quantity: int
    purchase_price: Optional[int] = None

class InvoiceItemRead(SQLModel):
    id: int
    sku_id: int
    quantity: int
    purchase_price: Optional[int] = None

class InvoiceItemDetailRead(SQLModel):
    id: int
    sku_id: int
    quantity: int
    purchase_price: Optional[int] = None
    sku_name: Optional[str] = None
    sku_price: Optional[int] = None

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

class InvoiceDetailRead(SQLModel):
    """
    Детальная информация о накладной для страницы склада.
    Включает полную информацию о позициях с данными SKU.
    """
    id: int
    seller_id: int
    number: Optional[str] = None
    status: str
    comment: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[InvoiceItemDetailRead] = []
