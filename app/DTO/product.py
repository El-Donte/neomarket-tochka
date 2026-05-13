from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel
from app.DTO.sku import SKURead
from uuid import UUID

from app.DTO.image import ImageCreate, ImageResponse

class ProductCreate(SQLModel):
    """
    Данные для создания товара.
    
    seller_id НЕ передаётся — берётся из токена авторизации.
    """
    title: str
    images: Optional[list[ImageCreate]] = []
    description: Optional[str] = None
    category_id: Optional[UUID] = None

class ProductRead(SQLModel):
    id: UUID
    seller_id: UUID
    category_id: Optional[UUID]
    title: str
    images: Optional[list[ImageResponse]] = []
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    skus: List[SKURead] = []

class ProductUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None

class ProductDashboardItem(SQLModel):
    id: UUID
    title: str
    images: Optional[list[ImageResponse]] = []
    status: str
    sku_count: int = 0
    published_sku_count: int = 0
    created_at: datetime
    updated_at: datetime