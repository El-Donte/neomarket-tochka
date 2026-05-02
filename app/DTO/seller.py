from typing import Optional
from sqlmodel import SQLModel

class SellerCreate(SQLModel):
    name: str
    password: str
    legal_name: Optional[str] = None
    inn: str
    kpp: Optional[str] = None

class SellerRead(SQLModel):
    id: int
    name: str
    legal_name: Optional[str] = None
    inn: str
    kpp: Optional[str] = None

class SellerLogin(SQLModel):
    inn: str
    password: str