from typing import Optional
from sqlmodel import Field, SQLModel

class Seller(SQLModel, table=True):
    __tablename__ = "sellers"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    legal_name: Optional[str] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None