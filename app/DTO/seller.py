from typing import Optional
from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime

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
    email: str
    password: str

class SellerResponse(SQLModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    company_name: str
    phone: Optional[str] = None
    inn: str
    created_at: datetime
    updated_at: datetime

class SellerUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None

class TokenResponse(SQLModel):
    user_id: UUID
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class RefreshRequest(SQLModel):
    refresh_token: str