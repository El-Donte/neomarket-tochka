from uuid import UUID
from uuid6 import uuid7
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID as PSU_UUID

if TYPE_CHECKING:
    from app.models.product import Product

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str
    slug: str = Field(unique=True, index=True)
    description: Optional[str] = None
    parent_id: Optional[UUID] = Field(default=None, foreign_key="categories.id")
    image_url: Optional[str] = None
    is_active: bool = Field(default=True)
    
    # SEO поля
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    meta_tags: Optional[dict] = Field(default_factory=dict, sa_column=Column(JSONB))
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    parent: Optional["Category"] = Relationship(
        sa_relationship_kwargs={"remote_side": "Category.id"},
        back_populates="children"
    )
    children: List["Category"] = Relationship(back_populates="parent")
    products: List["Product"] = Relationship(back_populates="category")