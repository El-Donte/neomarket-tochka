from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., title="Name")
    parent_id: Optional[UUID] = Field(
        default=None,
        title="Parent Id",
    )

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        title="Name",
    )
    parent_id: Optional[UUID] = Field(
        default=None,
        title="Parent Id",
    )

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    parent_id: Optional[UUID]
    created_at: datetime

    model_config = {
        "from_attributes": True  # важно для SQLModel
    }

class CategoryWithChildrenResponse(BaseModel):
    id: UUID
    name: str
    parent_id: Optional[UUID]
    created_at: datetime
    children: List[CategoryResponse] = []

    model_config = {
        "from_attributes": True
    }