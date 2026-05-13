from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey
from uuid import UUID
from uuid6 import uuid7

from app.models.category import Category

if TYPE_CHECKING:
    from app.models.sku import SKU
    from app.models.seller import Seller
    from app.models.image import Image

class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    seller_id: UUID = Field(foreign_key="sellers.id")
    category_id: Optional[UUID] = Field(default=None, foreign_key="categories.id")
    title: str
    description: Optional[str] = None
    status: str = Field(default="CREATED")
    rating: float = Field(default=0.0)
    orders_count: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
    
    images: List["Image"] = Relationship(back_populates="product", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    seller: "Seller" = Relationship(back_populates="products")
    category: Optional[Category] = Relationship(back_populates="products")
    skus: List["SKU"] = Relationship(back_populates="product")