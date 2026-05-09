from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from sqlmodel import Session, select
from app.database import get_session
from app.models.sku import SKU, CharacteristicValue
from app.models.invoice import Stock, InvoiceItem
from app.models.product import Product
from app.DTO.sku import SKUCreate, SKUUpdate, SKURead
from app.api.v1.dependencies.seller_depends import get_current_seller
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=SKURead)
def create_sku(
    sku_in: SKUCreate, 
    session: Session = Depends(get_session),
    seller_id: UUID = Depends(get_current_seller)
):
    """
    Создать SKU.
    
    product_id передаётся явно — проверяется, что товар существует
    и принадлежит текущему продавцу.
    seller_id берётся из токена авторизации.
    """
    
    statement = select(Product).where(
        Product.id == sku_in.product_id
    ).where(Product.seller_id == seller_id)
    product = session.exec(statement).first()
    
    if not product:
        raise HTTPException(
            status_code=404, 
            detail="Товар не найден или не принадлежит вам"
        )
    
    db_sku = SKU(
        product_id=sku_in.product_id,
        seller_id=seller_id,
        name=sku_in.name,
        price=sku_in.price,
        image_url=sku_in.image_url
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
    

@router.put("/{sku_id}", response_model=SKURead)
def update_sku(
    sku_id: UUID, 
    sku_in: SKUUpdate,
    session: Session = Depends(get_session),
    seller_id: UUID = Depends(get_current_seller)
):
    """
    Обновить SKU.
    
    Проверяет, что SKU принадлежит текущему продавцу.
    """
    statement = select(SKU).where(SKU.id == sku_id).where(SKU.seller_id == seller_id)
    db_sku = session.exec(statement).first()
    
    if not db_sku:
        raise HTTPException(status_code=404, detail="SKU не найден")
    
    sku_data = sku_in.model_dump(exclude_unset=True)
    for key, value in sku_data.items():
        setattr(db_sku, key, value)
    
    db_sku.updated_at = datetime.now(timezone.utc)
    session.add(db_sku)
    session.commit()
    session.refresh(db_sku)
    return db_sku


@router.get("/{sku_id}", response_model=SKURead)
def get_sku(
    sku_id: UUID,
    session: Session = Depends(get_session),
    seller_id: UUID = Depends(get_current_seller)
):
    """
    Получить информацию о SKU.
    
    Проверяет, что SKU принадлежит текущему продавцу.
    """
    statement = select(SKU).where(SKU.id == sku_id).where(SKU.seller_id == seller_id)
    db_sku = session.exec(statement).first()
    
    if not db_sku:
        raise HTTPException(status_code=404, detail="SKU не найден")
    
    return db_sku


@router.delete("/{sku_id}", response_model=dict)
def delete_sku(
    sku_id: UUID,
    session: Session = Depends(get_session),
    seller_id: UUID = Depends(get_current_seller)
):
    """
    Удалить SKU.
    
    Проверяет, что SKU принадлежит текущему продавцу.
    Нельзя удалить SKU, если у него есть остатки на складе.
    """
    statement = select(SKU).where(SKU.id == sku_id).where(SKU.seller_id == seller_id)
    db_sku = session.exec(statement).first()
    
    if not db_sku:
        raise HTTPException(status_code=404, detail="SKU не найден")
    
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
    

@router.get("/inventory/all", response_model=list[dict])
def get_inventory(
    session: Session = Depends(get_session),
    seller_id: UUID = Depends(get_current_seller)
):
    """
    ИНВЕНТАРЬ: Получить список всех SKU продавца с текущими остатками.
    """
    statement = (
        select(SKU, Stock, Product.title)
        .join(Stock, SKU.id == Stock.sku_id)
        .join(Product, SKU.product_id == Product.id)
        .where(SKU.seller_id == seller_id)
    )
    results = session.exec(statement).all()
    
    inventory = []
    for sku, stock, product_title in results:
        inventory.append({
            "sku_id": sku.id,
            "sku_name": sku.name,
            "product_title": product_title,
            "price": sku.price,
            "quantity": stock.quantity,
            "updated_at": stock.updated_at
        })
    
    return inventory