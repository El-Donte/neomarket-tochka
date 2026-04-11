from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class CharacteristicValue(SQLModel, table=True):
    __tablename__ = "sku_characteristics"
    id: Optional[int] = Field(default=None, primary_key=True)
    sku_id: int = Field(foreign_key="skus.id")
    name: str
    value: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SKU(SQLModel, table=True):
    __tablename__ = "skus"
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    seller_id: int = Field(foreign_key="sellers.id")
    name: str
    price: int
    status: str = Field(default="ACTIVE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    product: "Product" = Relationship(back_populates="skus")
    characteristics: List[CharacteristicValue] = Relationship()