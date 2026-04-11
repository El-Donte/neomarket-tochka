from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel
from app.DTO.sku import SKURead

class ProductCreate(SQLModel):
    seller_id: int
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None

class ProductRead(SQLModel):
    id: int
    seller_id: int
    category_id: Optional[int]
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    skus: List[SKURead] = []