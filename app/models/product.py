from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sku import SKU

class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: Optional[int] = Field(default=None, primary_key=True)
    seller_id: int = Field(foreign_key="sellers.id")
    category_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: str = Field(default="DRAFT")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    skus: List["SKU"] = Relationship(back_populates="product")