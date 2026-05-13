from typing import Optional
from sqlmodel import SQLModel
from uuid import UUID

class SellerCreate(SQLModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    password: str
    email: str
    company_name: str
    phone: Optional[str] = None
    inn: str
    
class SellerLogin(SQLModel):
    inn: str
    password: str