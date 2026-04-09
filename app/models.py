from typing import Optional
from sqlmodel import Field, SQLModel

class Seller(SQLModel, table=True):
    """Модель продавца"""
    __tablename__ = "sellers"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    legal_name: Optional[str] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None


# Схема для создания
class SellerCreate(SQLModel):
    name: str
    legal_name: Optional[str] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None


# Схема для ответа (с id)
# Если делать регистрацию, то в модели видимо появится хэш пароля, а тут ничего не изменится
class SellerRead(SQLModel):
    id: int
    name: str
    legal_name: Optional[str] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None