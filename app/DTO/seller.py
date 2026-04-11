from typing import Optional
from sqlmodel import SQLModel

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