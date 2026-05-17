from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey
from uuid import UUID
from uuid6 import uuid7

if TYPE_CHECKING:
    from app.models.invoice import Stock, InvoiceItem
    from app.models.product import Product
    from app.models.image import Image

class CharacteristicValue(SQLModel, table=True):
    __tablename__ = "sku_characteristics"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    sku_id: UUID = Field(foreign_key="skus.id")
    name: str
    value: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))

    sku: Optional["SKU"] = Relationship(back_populates="characteristics")

class SKU(SQLModel, table=True):
    __tablename__ = "skus"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id")
    name: str
    price: int  # В копейках/центах
    discount: int = Field(default=0)
    cost_price: Optional[int] = Field(default=None)
    article: Optional[str] = Field(default=None)
    old_price: Optional[int] = Field(default=None)
    status: str = Field(default="ACTIVE")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))

    @property
    def stock_quantity(self) -> int:
        return self.stock.stock_quantity if self.stock else 0

    @property
    def active_quantity(self) -> int:
        return self.stock.active_quantity if self.stock else 0

    @property
    def reserved_quantity(self) -> int:
        return self.stock.reserved_quantity if self.stock else 0

    product: "Product" = Relationship(back_populates="skus")
    characteristics: List[CharacteristicValue] = Relationship(back_populates="sku")
    stock: Optional["Stock"] = Relationship(back_populates="sku")
    invoice_items: List["InvoiceItem"] = Relationship(back_populates="sku")
    images: List["Image"] = Relationship(back_populates="sku", sa_relationship_kwargs={"cascade": "all, delete-orphan"})