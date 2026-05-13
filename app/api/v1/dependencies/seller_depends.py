# dependencies/auth.py
from fastapi import HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models.seller import Seller
from app.api.v1.dependencies.security import get_token_from_cookie, decode_token
from uuid import UUID

async def get_current_seller(
    request: Request,
    session: AsyncSession = Depends(get_session)
) -> UUID:
    """
    Dependency: получает текущего авторизованного продавца.
    При успехе возвращает его ID.
    """
    access_token = get_token_from_cookie(request)
    if not access_token:
        raise HTTPException(status_code=401, detail="Не авторизованный пользователь")
    
    seller_id = decode_token(access_token, expected_type="access")
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Неверный или просроченный токен")

    seller = await session.get(Seller, seller_id)

    if not seller:
        raise HTTPException(status_code=401, detail="Продавец не найден")

    return seller_id