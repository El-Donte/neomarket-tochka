from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from uuid6 import uuid7
from app.models.product import Product

class Seller(SQLModel, table=True):
    __tablename__ = "sellers"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str
    legal_name: Optional[str] = None
    inn: str
    kpp: Optional[str] = None
    password_hash: str
    
    products: List["Product"] = Relationship(back_populates="seller")