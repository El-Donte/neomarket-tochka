from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum

class ImageEntityType(str, Enum):
    PRODUCT = "PRODUCT"
    SKU = "SKU"

class ImageCreate(BaseModel):
    url: HttpUrl
    ordering: int = Field(default=0, ge=0)

class ImageAttachRequest(BaseModel):
    image_id: Optional[UUID] = None
    url: HttpUrl
    ordering: int = Field(default=0, ge=0)

class ImageUploadResponse(BaseModel):
    id: UUID
    url: HttpUrl
    ordering: int
    entity_type: ImageEntityType
    entity_id: Optional[UUID] = None

class ImageResponse(BaseModel):
    id: UUID
    url: HttpUrl
    ordering: int

class ImageUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    ordering: Optional[int] = Field(default=0, ge=0)