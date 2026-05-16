from uuid import UUID
from uuid6 import uuid7
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID as PSU_UUID
from slugify import slugify

if TYPE_CHECKING:
    from app.models.product import Product

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str
    description: Optional[str] = None
    parent_id: Optional[UUID] = Field(default=None, foreign_key="categories.id")
    image_url: Optional[str] = None
    is_active: bool = Field(default=True)
    level: int = Field(default=0)
    path: str = Field(default="")
    slug: str
    
    # SEO поля
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    meta_tags: Optional[dict] = Field(default_factory=dict, sa_column=Column(JSONB))
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))

    parent: Optional["Category"] = Relationship(
        sa_relationship_kwargs={"remote_side": "Category.id"},
        back_populates="children"
    )
    children: List["Category"] = Relationship(back_populates="parent")
    products: List["Product"] = Relationship(back_populates="category")

    @staticmethod
    def generate_slug(name: str, existing_slugs: Optional[set]) -> str:
        base = slugify(name, max_length=100)
        if not base:
            base = "category"
        slug = base
        counter = 1
        while existing_slugs and slug in existing_slugs:
            slug = f"{base}-{counter}"
            counter += 1
            
        return slug