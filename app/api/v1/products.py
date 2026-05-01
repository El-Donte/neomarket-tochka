from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import datetime, timezone
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import Optional

from app.database import get_session
from app.models.invoice import Stock, InvoiceItem
from app.models.product import Product
from app.models.sku import SKU, CharacteristicValue
from app.DTO.product import ProductCreate, ProductRead, ProductUpdate, ProductDashboardItem
from app.DTO.sku import SKURead, SKUCreate
from app.api.v1.dependencies.seller_depends import get_current_seller

router = APIRouter()

@router.post("/", response_model=ProductRead)
def create_product(
    product_in: ProductCreate, 
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
):
    """
    Создать товар.
    
    seller_id берётся из токена авторизации, не передаётся в теле запроса.
    """
    db_product = Product.model_validate(
        product_in,
        update={"seller_id": seller_id, "status": "CREATED"})
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
    
@router.put("/{id}", response_model=ProductRead)
def update_product(
    id: int,
    product_in: ProductCreate, 
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
):
    """
    Полное обновление товара и отправка на модерацию.
    
    Внимание: этот метод требует передачи всех полей товара.
    Для частичного обновления используйте PATCH.
    """
    statement = (
        select(Product)
        .where(Product.id == id)
        .where(Product.seller_id == seller_id)
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
            response_model=list[ProductRead])
def get_products( 
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)):

    statement = (
        select(Product)
        .where(Product.seller_id == seller_id)
    )
    db_products = session.exec(statement)
    return db_products
    

# === ENDPOINTS FOR DASHBOARD ===

@router.get("/dashboard/", response_model=list[ProductDashboardItem])
def get_products_dashboard(
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller),
    status: Optional[str] = Query(None, description="Фильтр по статусу: MODERATION или PUBLISHED")
):
    """
    ДАШБОРД: Получить список товаров для отображения в дашборде.
    
    Возвращает краткую информацию о каждом товаре:
    - id, title, status — основная информация
    - sku_count — общее количество SKU у товара
    - published_sku_count — количество SKU со статусом PUBLISHED
    
    Параметр status позволяет фильтровать:
    - status=MODERATION — только товары на модерации
    - status=PUBLISHED — только опубликованные товары
    - без параметра — все товары
    """
    statement = select(Product).where(Product.seller_id == seller_id)
    
    if status:
        status_upper = status.upper()
        if status_upper == "MODERATION":
            statement = statement.where(Product.status == "ON_MODERATION")
        elif status_upper == "PUBLISHED":
            statement = statement.where(Product.status == "PUBLISHED")
        else:
            raise HTTPException(status_code=400, detail=f"Неизвестный статус: {status}. Используйте MODERATION или PUBLISHED")
    
    statement = statement.options(selectinload(Product.skus))
    db_products = session.exec(statement).all()
    
    result = []
    for product in db_products:
        sku_count = len(product.skus)
        published_sku_count = sum(1 for sku in product.skus if sku.status == "PUBLISHED")
        
        result.append(ProductDashboardItem(
            id=product.id,
            title=product.title,
            status=product.status,
            sku_count=sku_count,
            published_sku_count=published_sku_count,
            created_at=product.created_at,
            updated_at=product.updated_at
        ))
    
    return result


# === ENDPOINTS FOR PRODUCT EDITOR ===

@router.patch("/{id}", response_model=ProductRead)
def update_product_partial(
    id: int,
    product_in: ProductUpdate,
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
):
    """
    РЕДАКТОР: Частичное обновление товара.
    
    Позволяет редактировать описание, название или категорию товара
    БЕЗ смены статуса (товар остаётся в текущем состоянии).
    
    Используется в форме редактирования, где продавец может
    вносить правки без отправки на повторную модерацию.
    """
    statement = (
        select(Product)
        .where(Product.id == id)
        .where(Product.seller_id == seller_id)
        .options(selectinload(Product.skus))
    )
    db_product = session.exec(statement).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    product_data = product_in.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    
    db_product.updated_at = datetime.now(timezone.utc)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    session.refresh(db_product, ["skus"])
    
    return db_product


@router.post("/{id}/submit", response_model=ProductRead)
def submit_product_for_moderation(
    id: int,
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
):
    """
    РЕДАКТОР: Отправить товар на модерацию.
    
    Меняет статус товара на ON_MODERATION.
    Вызывается после того, как продавец закончил редактирование
    и готов отправить товар на проверку.
    
    Проверяет, что у товара есть хотя бы один SKU.
    """
    statement = (
        select(Product)
        .where(Product.id == id)
        .where(Product.seller_id == seller_id)
        .options(selectinload(Product.skus))
    )
    db_product = session.exec(statement).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    if not db_product.skus or len(db_product.skus) == 0:
        raise HTTPException(
            status_code=400,
            detail="Нельзя отправить товар на модерацию без SKU. Добавьте хотя бы одну вариацию товара."
        )
    
    if db_product.status == "ON_MODERATION":
        raise HTTPException(status_code=400, detail="Товар уже находится на модерации")
    
    if db_product.status == "PUBLISHED":
        raise HTTPException(status_code=400, detail="Товар уже опубликован. Для изменений используйте редактирование.")
    
    db_product.status = "ON_MODERATION"
    db_product.updated_at = datetime.now(timezone.utc)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    session.refresh(db_product, ["skus"])
    
    return db_product


@router.post("/{id}/skus", response_model=SKURead)
def add_sku_to_product(
    id: int,
    sku_in: SKUCreate,
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
):
    """
    РЕДАКТОР: Добавить новый SKU к товару.
    
    Создаёт новую вариацию товара (SKU) в рамках существующего продукта.
    SKU привязывается к товару по product_id.
    
    Используется в редакторе для добавления новых вариантов (размер, цвет и т.д.).
    """

    statement = select(Product).where(Product.id == id).where(Product.seller_id == seller_id)
    db_product = session.exec(statement).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    db_sku = SKU(
        product_id=id,
        seller_id=seller_id,
        name=sku_in.name,
        price=sku_in.price,
    )

    if hasattr(sku_in, 'characteristics') and sku_in.characteristics:
        for char in sku_in.characteristics:
            db_sku.characteristics.append(
                CharacteristicValue(name=char.name, value=char.value)
            )
    
    session.add(db_sku)
    session.flush()
    session.add(Stock(sku_id=db_sku.id, quantity=0))
    session.commit()
    session.refresh(db_sku)
    
    return db_sku


@router.delete("/{id}/skus/{sku_id}", response_model=dict)
def remove_sku_from_product(
    id: int,
    sku_id: int,
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
):
    """
    РЕДАКТОР: Удалить SKU из товара.
    
    Удаляет вариацию товара. Нельзя удалить SKU, если у него есть остатки на складе
    или он участвует в активных заказах.
    """

    statement = select(Product).where(Product.id == id).where(Product.seller_id == seller_id)
    db_product = session.exec(statement).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    # Проверяем SKU
    db_sku = session.get(SKU, sku_id)
    
    if not db_sku:
        raise HTTPException(status_code=404, detail="SKU не найден")
    
    if db_sku.product_id != id:
        raise HTTPException(status_code=400, detail="SKU не принадлежит этому товару")

    stock = session.exec(select(Stock).where(Stock.sku_id == sku_id)).first()
    
    if stock:
        if stock.quantity > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Нельзя удалить SKU с остатками на складе ({stock.quantity} шт)."
            )
        else:
            session.delete(stock)

    invoice_item = session.exec(select(InvoiceItem).where(InvoiceItem.sku_id == sku_id)).first()
    if invoice_item:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить SKU, так как он используется в накладных (история операций)"
        )

    session.delete(db_sku)
    session.commit()
    
    return {"message": "SKU успешно удалён", "sku_id": sku_id}


@router.put("/{id}/skus/{sku_id}", response_model=SKURead)
def update_product_sku(
    sku_id: int,
    sku_in: SKUCreate,
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
):
    """
    РЕДАКТОР: Обновить SKU товара.
    
    Позволяет изменить название или цену SKU в рамках редактора товара.
    """

    statement = select(Product).where(Product.id == sku_in.product_id).where(Product.seller_id == seller_id)
    db_product = session.exec(statement).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    db_sku = session.get(SKU, sku_id)
    
    if not db_sku:
        raise HTTPException(status_code=404, detail="SKU не найден")
    
    if db_sku.product_id != sku_in.product_id:
        raise HTTPException(status_code=400, detail="SKU не принадлежит этому товару")

    sku_data = sku_in.model_dump(exclude_unset=True, exclude={"characteristics"})
    for key, value in sku_data.items():
        setattr(db_sku, key, value)
    
    db_sku.updated_at = datetime.now(timezone.utc)
    
    session.add(db_sku)
    session.commit()
    session.refresh(db_sku)
    
    return db_sku
