from datetime import datetime
from typing import List
from sqlmodel import SQLModel

class CharacteristicRead(SQLModel):
    id: int
    name: str
    value: str

class SKUCreate(SQLModel):
    product_id: int
    seller_id: int
    name: str
    price: int

class SKURead(SQLModel):
    id: int
    product_id: int
    seller_id: int
    name: str
    price: int
    status: str
    active_quantity: int
    created_at: datetime
    characteristics: List[CharacteristicRead] = []