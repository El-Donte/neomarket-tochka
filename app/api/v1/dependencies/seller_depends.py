# dependencies/auth.py
from fastapi import HTTPException, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models.seller import Seller
from app.api.v1.dependencies.security import decode_token
from uuid import UUID

async def get_current_seller(
    authorization: str = Header(..., alias="Authorization"),
    session: AsyncSession = Depends(get_session)
) -> UUID:
    """
    Dependency: получает текущего авторизованного продавца.
    При успехе возвращает его ID.
    """
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = parts[1]

    seller_id = decode_token(token, expected_type="access")
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    
    seller = await session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=401, detail="Seller not found")
    
    return seller_id