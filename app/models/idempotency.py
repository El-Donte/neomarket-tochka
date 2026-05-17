from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime
from uuid import UUID

class IdempotencyKey(SQLModel, table=True):
    __tablename__ = "idempotency_keys"
    
    key: str = Field(primary_key=True)
    response_body: Optional[str] = None
    response_status_code: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
