from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime, timezone
from typing import List

from app.database import get_session
from app.DTO.product import ModerationEventRequest, ProductStatus
from app.infrastructure.repositories.product_repository import ProductRepository

from app.models.idempotency import IdempotencyKey

router = APIRouter()


@router.post("/events", status_code=204)
async def receive_moderation_event(
    request: ModerationEventRequest,
    x_service_key: str = Header(..., alias="X-Service-Key"),
    session: AsyncSession = Depends(get_session),
):
    key = f"{x_service_key}_{request.idempotency_key}"
    idemp = await session.get(IdempotencyKey, key)
    if idemp:
        return

    repo = ProductRepository(session)
    product = await repo.get_by_id(request.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if request.event_type == "MODERATED":
        product.status = ProductStatus.MODERATED
    elif request.event_type == "BLOCKED":
        if request.hard_block:
            product.status = ProductStatus.HARD_BLOCKED
        else:
            product.status = ProductStatus.BLOCKED
        
        product.blocking_reason_id = request.blocking_reason_id
        product.moderator_comment = request.moderator_comment

    product.updated_at = datetime.now(timezone.utc)
    
    await repo.save(product)
    
    session.add(IdempotencyKey(
        key=key,
        response_status_code=204
    ))
    await session.commit()
    return
