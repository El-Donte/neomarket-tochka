from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel
from uuid import UUID

from app.DTO.image import ImageResponse, ImageCreate

class CharacteristicCreate(SQLModel):
    """Данные для создания характеристики SKU"""
    name: str
    value: str

class CharacteristicRead(SQLModel):
    id: UUID
    name: str
    value: str

class SKUCreate(SQLModel):
    """
    Данные для создания SKU.
    
    product_id передаётся явно — проверяется, что товар существует
    и принадлежит текущему продавцу.
    seller_id НЕ передаётся — берётся из токена авторизации.
    """
    product_id: UUID
    name: str
    price: int
    images: Optional[list[ImageCreate]] = []
    characteristics: Optional[List[CharacteristicCreate]] = None

class SKUUpdate(SQLModel):
    """Данные для обновления SKU (все поля опциональны)"""
    name: Optional[str] = None
    price: Optional[int] = None

class SKURead(SQLModel):
    id: UUID
    product_id: UUID
    seller_id: UUID
    name: str
    price: int
    images: Optional[list[ImageResponse]] = []
    status: str
    created_at: datetime
    updated_at: datetime
    characteristics: List[CharacteristicRead] = []