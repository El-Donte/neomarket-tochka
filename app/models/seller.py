from typing import Optional
from sqlmodel import Field, SQLModel
from uuid import UUID
from uuid6 import uuid7

class Seller(SQLModel, table=True):
    __tablename__ = "sellers"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str
    legal_name: Optional[str] = None
    inn: str
    kpp: Optional[str] = None
    password_hash: str