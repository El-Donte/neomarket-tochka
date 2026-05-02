from typing import Optional
from sqlmodel import Field, SQLModel

class Seller(SQLModel, table=True):
    __tablename__ = "sellers"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    legal_name: Optional[str] = None
    inn: str
    kpp: Optional[str] = None
    password_hash: str