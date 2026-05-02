# dependencies/auth.py
from fastapi import HTTPException, Depends, Request
from sqlmodel import Session, select
from app.database import get_session
from app.models.seller import Seller
from app.api.v1.dependencies.security import get_token_from_cookie, decode_token

def get_current_seller(
    request: Request,
    session: Session = Depends(get_session)
) -> int:
    """
    Dependency: получает текущего авторизованного продавца.
    При успехе возвращает его ID.
    """
    token = get_token_from_cookie(request)
    if not token:
        raise HTTPException(status_code=401, detail="Продавец не найден")
    
    seller_id = decode_token(token)
    if not seller_id:
        raise HTTPException(status_code=401, detail="Неверный или просроченный токен")

    statement = (select(Seller).where((Seller.id == seller_id)))
    seller = session.exec(statement).first()

    if not seller:
        raise HTTPException(status_code=401, detail="Продавец не найден")

    return seller_id