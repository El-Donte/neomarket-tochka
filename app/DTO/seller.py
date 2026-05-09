from typing import Optional
from sqlmodel import SQLModel
from uuid import UUID

class SellerCreate(SQLModel):
    name: str
    password: str
    legal_name: Optional[str] = None
    inn: str
    kpp: Optional[str] = None

class SellerRead(SQLModel):
    id: UUID
    name: str
    legal_name: Optional[str] = None
    inn: str
    kpp: Optional[str] = None

class SellerLogin(SQLModel):
    inn: str
    password: str