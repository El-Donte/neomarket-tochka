from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel

class CharacteristicCreate(SQLModel):
    """Данные для создания характеристики SKU"""
    name: str
    value: str

class CharacteristicRead(SQLModel):
    id: int
    name: str
    value: str

class SKUCreate(SQLModel):
    """
    Данные для создания SKU.
    
    product_id передаётся явно — проверяется, что товар существует
    и принадлежит текущему продавцу.
    seller_id НЕ передаётся — берётся из токена авторизации.
    """
    product_id: int
    name: str
    price: int
    characteristics: Optional[List[CharacteristicCreate]] = None

class SKUUpdate(SQLModel):
    """Данные для обновления SKU (все поля опциональны)"""
    name: Optional[str] = None
    price: Optional[int] = None

class SKURead(SQLModel):
    id: int
    product_id: int
    seller_id: int
    name: str
    price: int
    status: str
    created_at: datetime
    updated_at: datetime
    characteristics: List[CharacteristicRead] = []