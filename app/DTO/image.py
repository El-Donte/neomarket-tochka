from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl


class ImageCreate(BaseModel):
    url: HttpUrl
    ordering: int = Field(default=0, ge=0)

class ImageResponse(BaseModel):
    id: UUID
    url: HttpUrl
    ordering: int

class ImageUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    ordering: Optional[int] = Field(default=0, ge=0)