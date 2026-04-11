from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
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