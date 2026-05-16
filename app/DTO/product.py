from datetime import datetime
from typing import Optional, List
from app.DTO.sku import SKURead
from pydantic import BaseModel, Field
from uuid import UUID

from app.DTO.image import ImageCreate, ImageResponse
from app.models.product import ProductStatus

class ProductCreate(BaseModel):
    """
    Данные для создания товара.
    
    seller_id НЕ передаётся — берётся из токена авторизации.
    """
    title: str
    images: list[ImageCreate] = Field(default_factory=list)
    description: str
    category_id: UUID
    slug: Optional[str] = None

    model_config = {"from_attributes": True}

class ProductResponse(BaseModel):
    id: UUID
    seller_id: UUID
    category_id: Optional[UUID] = None
    title: str
    slug: str
    images: list[ImageResponse]
    description: str
    status: ProductStatus
    is_deleted: bool
    blocking_reason_id: Optional[UUID] = None
    moderator_comment: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    skus: List[SKURead]

    model_config = {"from_attributes": True}

class ProductPublicResponse(BaseModel):
    id: UUID
    seller_id: UUID
    category_id: Optional[UUID] = None
    title: str
    slug: str
    images: list[ImageResponse]
    description: str
    status: ProductStatus
    created_at: datetime
    updated_at: datetime
    skus: List[SKURead] = []

    model_config = {"from_attributes": True}

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None

    model_config = {"from_attributes": True}

class ProductDashboardItem(BaseModel):
    id: UUID
    title: str
    images: list[ImageResponse] = Field(default_factory=list)
    status: ProductStatus
    sku_count: int = 0
    published_sku_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ProductShortResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    status: ProductStatus
    category_id: UUID
    is_deleted: bool
    created_at: datetime
    min_price: Optional[int] = None
    cover_image: Optional[str] = None

    model_config = {"from_attributes": True}

class ProductPaginatedResponse(BaseModel):
    items: List[ProductShortResponse] = []
    total_count: int
    limit: int
    offset: int

    model_config = {"from_attributes": True}