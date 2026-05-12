from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from uuid6 import uuid7

from app.models.category import Category
from app.models.seller import Seller

if TYPE_CHECKING:
    from app.models.sku import SKU

class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    seller_id: UUID = Field(foreign_key="sellers.id")
    category_id: Optional[UUID] = Field(default=None, foreign_key="categories.id")
    title: str
    slug: str = Field(unique=True, index=True)
    image_url: Optional[str] = None
    description: Optional[str] = None
    status: str = Field(default="CREATED")
    rating: float = Field(default=0.0)
    orders_count: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    seller: Seller = Relationship(back_populates="products")
    category: Optional[Category] = Relationship(back_populates="products")
    skus: List["SKU"] = Relationship(back_populates="product")