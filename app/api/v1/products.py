from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import datetime, timezone
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.models.product import Product
from app.DTO.product import ProductCreate, ProductRead
from app.api.v1.seller_depends import get_current_seller

router = APIRouter()

@router.post("/", response_model=Product)
def create_product(
    product_in: ProductCreate, 
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
):
    """Создать товар"""
    db_product = Product.model_validate(product_in)
    db_product.seller_id = seller_id #Принудительно присваиеваем ID текущего seller
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.get("/{id}", response_model=ProductRead)
def get_product(
    id: int, 
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
):
    """Получить товар"""
    statement = (
        select(Product)
        .where(Product.id == id)
        .where(Product.seller_id == seller_id) # Проверка, что товар принадлежит текущему продавцу
        .options(selectinload(Product.skus))
    )
    product = session.exec(statement).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@router.put("/{id}", response_model=Product)
def update_product(
    id: int, 
    product_in: ProductCreate, 
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
):
    """Изменить товар и отправить на модерацию"""
    statement = (
        select(Product)
        .where(Product.id == id)
        .where(Product.seller_id == seller_id) # Проверяем, что товар есть и принадлежит текущему продавцу
    )
    db_product = session.exec(statement).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    product_data = product_in.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    
    db_product.status = "ON_MODERATION" 
    db_product.updated_at = datetime.now(timezone.utc)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.get("/", 
            response_model=list[ProductRead],
            response_model_include={"id", "title", "status", "created_at", "updated_at"})
def get_products( 
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)):

    statement = (
        select(Product)
        .where(Product.seller_id == seller_id)
    )
    db_products = session.exec(statement)
    return db_products