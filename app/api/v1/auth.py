from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from anyio.to_thread import run_sync
from app.models.seller import Seller
from app.DTO.seller import SellerCreate, SellerRead, SellerLogin
from app.api.v1.dependencies.security import hash_password, set_auth_cookie, verify_password, delete_auth_cookie

router = APIRouter()

@router.post("/register", response_model=SellerRead)
async def register_seller(
    seller: SellerCreate,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    statement = select(Seller).where(Seller.inn == seller.inn)

    result = await session.exec(statement)
    existing_seller = result.first()

    if existing_seller:
        raise HTTPException(status_code=409, detail="Пользователь с таким ИНН уже существует")

    db_seller = Seller(
        name=seller.name,
        password_hash=hash_password(seller.password),
        legal_name=seller.legal_name,
        inn=seller.inn,
        kpp=seller.kpp
    )

    session.add(db_seller)

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    await session.refresh(db_seller)

    set_auth_cookie(response, seller_id=db_seller.id)
    return db_seller

@router.post("/login", response_model=SellerRead)
async def login_seller(
    seller: SellerLogin,
    response: Response,
    session: AsyncSession = Depends(get_session)):
    """
    Авторизация продавца.
    На вход получает ИНН и пароль. 
    При успехе возвращает данные продавца и устанавливает JWT токен в cookie.
    """
    statement = (select(Seller).where((Seller.inn == seller.inn)))
    result = await session.exec(statement)
    existing_seller = result.first()

    if not existing_seller:
        raise HTTPException(status_code=401, detail="Неверный ИНН или пароль")
    
    is_valid = await run_sync(
        verify_password,
        seller.password,
        existing_seller.password_hash,
    )
    if not is_valid:
        raise HTTPException(status_code=401, detail="Неверный ИНН или пароль")
    
    set_auth_cookie(response, seller_id=existing_seller.id)
    return existing_seller

@router.post("/logout", status_code=204)
async def logout_seller(response: Response):
    """
    Выход из аккаунта продавца.
    Удаляет куку с JWT токеном.
    """
    delete_auth_cookie(response)