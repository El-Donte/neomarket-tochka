from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from uuid6 import uuid7

if TYPE_CHECKING:
    from app.models.sku import SKU

class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    seller_id: UUID = Field(foreign_key="sellers.id")
    category_id: Optional[int] = None
    title: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    status: str = Field(default="CREATED")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    skus: List["SKU"] = Relationship(back_populates="product")