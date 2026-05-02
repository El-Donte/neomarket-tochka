import jwt
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, TypedDict
from fastapi import Response, Request
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_DAYS"))
JWT_SECURE = os.getenv("JWT_SECURE").lower() == "true"

class TokenPayload(TypedDict):
    seller_id: int
    exp: int

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(seller_id:int) -> str:
    expire = int((datetime.now() + timedelta(days=JWT_ACCESS_TOKEN_EXPIRE_DAYS)).timestamp())
    to_encode=TokenPayload(seller_id=seller_id, exp=expire)
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def get_token_from_cookie(request: Request) -> Optional[str]:
    """
    Достает JWT токен из cookie.
    """
    token = request.cookies.get("access_token")
    if not token:
        return None
    return token

def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        seller_id = payload.get("seller_id")
        exp = payload.get("exp")
        
        if seller_id is None or not isinstance(seller_id, int):
            return None
        if exp is None or not isinstance(exp, int):
            return None
        
        return seller_id
        
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def set_auth_cookie(response: Response, seller_id: int):
    """
    Создаёт токен и устанавливает его в HttpOnly куку.
    """
    token = create_access_token(seller_id=seller_id)
    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,    # True => передача только по HTTPS
        samesite="lax",  # кука не подставляется при отправке запроса с чужого сайта
        max_age=JWT_ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

def delete_auth_cookie(response: Response) -> None:
    """Удаляет куку с токеном"""
    response.delete_cookie("access_token")