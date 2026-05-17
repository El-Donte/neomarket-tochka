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
    """
    product_id: UUID
    name: str
    price: int
    discount: int = 0
    cost_price: Optional[int] = None
    article: Optional[str] = None
    images: Optional[list[ImageCreate]] = []
    characteristics: Optional[List[CharacteristicCreate]] = []

class SKUUpdate(SQLModel):
    """Данные для обновления SKU (все поля опциональны)"""
    name: Optional[str] = None
    price: Optional[int] = None
    discount: Optional[int] = None
    cost_price: Optional[int] = None
    article: Optional[str] = None
    characteristics: Optional[List[CharacteristicCreate]] = None

class SKURead(SQLModel):
    id: UUID
    product_id: UUID
    name: str
    price: int
    discount: int = 0
    cost_price: Optional[int] = None
    stock_quantity: int = 0
    active_quantity: int = 0
    reserved_quantity: int = 0
    article: Optional[str] = None
    images: Optional[list[ImageResponse]] = []
    characteristics: List[CharacteristicRead] = []
    created_at: datetime
    updated_at: datetime

class SKUPublicResponse(SQLModel):
    id: UUID
    product_id: UUID
    name: str
    price: int
    discount: int = 0
    stock_quantity: int = 0
    active_quantity: int = 0
    article: Optional[str] = None
    images: Optional[list[ImageResponse]] = []
    characteristics: List[CharacteristicRead] = []

class InventoryItem(SQLModel):
    sku_id: UUID
    quantity: int

class ReserveRequest(SQLModel):
    idempotency_key: UUID
    order_id: UUID
    items: List[InventoryItem]

class ReserveResponse(SQLModel):
    order_id: UUID
    status: str
    reserved_at: datetime

class InventoryOrderRequest(SQLModel):
    order_id: UUID
    items: List[InventoryItem]

class InventoryOrderResponse(SQLModel):
    order_id: UUID
    status: str
    processed_at: datetime