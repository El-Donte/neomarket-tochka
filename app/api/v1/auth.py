from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from anyio.to_thread import run_sync
from app.models.seller import Seller
from app.DTO.seller import SellerCreate, SellerLogin, SellerRead
from app.api.v1.dependencies.security import hash_password, set_auth_cookies, verify_password, decode_token

router = APIRouter()

@router.post("/register", response_model=SellerRead, status_code=201)    
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
        first_name=seller.first_name,
        password_hash=hash_password(seller.password),
        last_name=seller.last_name,
        inn=seller.inn,
        middle_name=seller.middle_name,
        company_name=seller.company_name,
        phone=seller.phone,
        email=seller.email
    )

    session.add(db_seller)

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    await session.refresh(db_seller)

    set_auth_cookies(response, seller_id=db_seller.id)
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
    
    set_auth_cookies(response, seller_id=existing_seller.id)
    return existing_seller

@router.post("/logout", status_code=204)
async def logout_seller(response: Response):
    """
    Выход из аккаунта продавца.
    Удаляет куку с JWT токеном.
    """

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

@router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    seller_id = decode_token(refresh_token, expected_type="refresh")
    if seller_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    set_auth_cookies(response, seller_id)