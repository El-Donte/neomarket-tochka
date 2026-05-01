# dependencies/auth.py
from fastapi import Header, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import Optional
from app.database import get_session
from app.models.seller import Seller


def get_current_seller(
    seller_id: Optional[int] = Header(None, alias="Seller-Id"),
    session: Session = Depends(get_session)
) -> int:
    """
    Эмуляция:
    Проверяет, что seller_id существует в БД.
    Смотрит наличие заголовка Seller-Id, который хранит seller_id пользователя. (Пока без jwt-токена)
    !!! При отстутствии заголовка берётся seller с id = 1 (Чисто для тестов)
    Если seller с указанным id не найден, возвращает ошибку
    """

    if seller_id is None:
        statement = select(Seller).limit(1)
        seller = session.exec(statement).first()
        if seller:
            return seller.id
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="В системе нет продавцов. Сначала создайте продавца."
            )
    
    seller = session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продавец с ID {seller_id} не найден"
        )
    
    return seller_id