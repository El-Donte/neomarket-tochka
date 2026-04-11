from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

# --- СЕЛЛЕРЫ ---
class Seller(SQLModel, table=True):
    __tablename__ = "sellers"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    legal_name: Optional[str] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None

class SellerCreate(SQLModel):
    name: str
    legal_name: Optional[str] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None

class SellerRead(SQLModel):
    id: int
    name: str
    legal_name: Optional[str] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None

class CharacteristicValue(SQLModel, table=True):
    __tablename__ = "sku_characteristics"
    id: Optional[int] = Field(default=None, primary_key=True)
    sku_id: int = Field(foreign_key="skus.id")
    name: str
    value: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CharacteristicRead(SQLModel):
    id: int
    name: str
    value: str

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

class ProductCreate(SQLModel):
    seller_id: int
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None

class SKU(SQLModel, table=True):
    __tablename__ = "skus"
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    seller_id: int = Field(foreign_key="sellers.id")
    name: str
    price: int 
    status: str = Field(default="ACTIVE")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    product: "Product" = Relationship(back_populates="skus")
    characteristics: List[CharacteristicValue] = Relationship()

class SKUCreate(SQLModel):
    product_id: int
    seller_id: int
    name: str
    price: int

class SKURead(SQLModel):
    id: int
    product_id: int
    seller_id: int
    name: str
    price: int
    status: str
    created_at: datetime
    characteristics: List[CharacteristicRead] = []

class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"
    id: Optional[int] = Field(default=None, primary_key=True)
    seller_id: int = Field(foreign_key="sellers.id")
    number: Optional[str] = None
    status: str = Field(default="CREATED")
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class InvoiceCreate(SQLModel):
    seller_id: int
    number: Optional[str] = None
    comment: Optional[str] = None

class InvoiceRead(SQLModel):
    id: int
    seller_id: int
    number: Optional[str] = None
    status: str
    created_at: datetime

class InvoiceItem(SQLModel, table=True):
    __tablename__ = "invoice_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoices.id")
    sku_id: int = Field(foreign_key="skus.id")
    quantity: int
    purchase_price: Optional[int] = None

class Stock(SQLModel, table=True):
    __tablename__ = "stocks"
    id: Optional[int] = Field(default=None, primary_key=True)
    sku_id: int = Field(foreign_key="skus.id", unique=True)
    quantity: int = Field(default=0)
    updated_at: datetime = Field(default_factory=datetime.utcnow)