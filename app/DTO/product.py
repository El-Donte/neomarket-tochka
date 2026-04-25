from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel
from app.DTO.sku import SKURead

class ProductCreate(SQLModel):
    """
    Данные для создания товара.
    
    seller_id НЕ передаётся — берётся из токена авторизации.
    """
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

class ProductUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class ProductDashboardItem(SQLModel):
    id: int
    title: str
    status: str
    sku_count: int = 0
    published_sku_count: int = 0
    created_at: datetime
    updated_at: datetime