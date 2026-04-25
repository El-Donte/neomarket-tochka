from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.models.invoice import Invoice, InvoiceItem, Stock
from app.models.sku import SKU
from app.DTO.invoice import InvoiceCreate, InvoiceRead, InvoiceDetailRead, InvoiceItemDetailRead
from app.database import get_session
from app.api.v1.seller_depends import get_current_seller

router = APIRouter()

@router.post("/", response_model=InvoiceRead)
def create_invoice(
    invoice_in: InvoiceCreate, 
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
    ):
    """Создать черновик накладной"""

    invoice = Invoice(
        seller_id=seller_id,
        number=invoice_in.number,
        comment=invoice_in.comment
    )
    session.add(invoice)
    session.flush()

    for item_data in invoice_in.items:
        item = InvoiceItem(
            invoice_id=invoice.id,
            sku_id=item_data.sku_id,
            quantity=item_data.quantity,
            purchase_price=item_data.purchase_price
        )
        session.add(item)
    
    session.commit()
    session.refresh(invoice)

    session.refresh(invoice, ["items"])
    
    return invoice

@router.post("/accept", response_model=InvoiceRead)
def accept_invoice(
    invoice_id: int, 
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)):
    """
    ПРИЁМКА НАКЛАДНОЙ: Принять накладную и обновить остатки на складе.
    
    Логика:
    1. Проверяет, что накладная существует и принадлежит продавцу
    2. Проверяет, что накладная в статусе CREATED (ещё не принята)
    3. Проходит по всем позициям накладной
    4. Для каждого SKU:
       - Проверяет, что SKU существует и принадлежит этому продавцу
       - Суммирует количество (если один SKU встречается несколько раз)
    5. Обновляет остатки в таблице Stock:
       - Если запись есть — увеличивает quantity
       - Если записи нет — создаёт новую
    6. Меняет статус накладной на ACCEPTED
    """

    statement = select(Invoice).where(Invoice.id == invoice_id).options(selectinload(Invoice.items))
    invoice = session.exec(statement).first()
    
    if not invoice or invoice.seller_id != seller_id:
        raise HTTPException(status_code=404, detail="Накладная не найдена")
    
    if invoice.status != "CREATED":
        raise HTTPException(status_code=400, detail=f"Накладная уже {invoice.status}, нельзя принять")

    items_statement = select(InvoiceItem).where(InvoiceItem.invoice_id == invoice_id)
    items = session.exec(items_statement).all()
    
    if not items:
        raise HTTPException(status_code=400, detail="Накладная пуста")

    sku_quantities = {}
    for item in items:
        if item.sku_id in sku_quantities:
            sku_quantities[item.sku_id] += item.quantity
        else:
            sku_quantities[item.sku_id] = item.quantity

    for sku_id, quantity in sku_quantities.items():
        sku = session.get(SKU, sku_id)
        if not sku:
            raise HTTPException(
                status_code=404, 
                detail=f"SKU {sku_id} не найден. Операция откатывается."
            )

        if sku.seller_id != seller_id:
            raise HTTPException(
                status_code=400, 
                detail=f"SKU {sku_id} не принадлежит этому продавцу. Операция откатывается."
            )

        stock = session.exec(
            select(Stock).where(Stock.sku_id == sku_id)
        ).first()
            
        if stock:
            stock.quantity += quantity
            stock.updated_at = datetime.now(timezone.utc)
            session.add(stock)
        else:
            new_stock = Stock(
                sku_id=sku_id,
                quantity=quantity
            )
            session.add(new_stock)

    invoice.status = "ACCEPTED"
    invoice.updated_at = datetime.now(timezone.utc)
    session.add(invoice)
        
    session.commit()
    
    return invoice

@router.get("/", 
            response_model=list[InvoiceRead])
def get_invoices( 
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)):
    """
    СКЛАД: Получить список всех накладных продавца.

    Возвращает краткий список накладных с основными полями:
    - id, number — идентификатор и номер накладной
    - status — статус (CREATED, ACCEPTED)
    - comment — комментарий
    - created_at — дата создания
    """

    statement = (
        select(Invoice)
        .where(Invoice.seller_id == seller_id)
    )
    db_invoices= session.exec(statement)
    return db_invoices


@router.get("/{id}", response_model=InvoiceDetailRead)
def get_invoice(
    id: int,
    session: Session = Depends(get_session),
    seller_id: int = Depends(get_current_seller)
):
    """
    СКЛАД: Получить детальную информацию о накладной.
    
    Возвращает полную информацию о накладной, включая:
    - Основные данные (номер, статус, комментарий)
    - Все позиции (items) с информацией о SKU и количестве
    - Позволяет перед приёмкой проверить, какие именно товары
      и в каком количестве ожидаются на склад.
    """
    statement = (
        select(Invoice)
        .where(Invoice.id == id)
        .where(Invoice.seller_id == seller_id)
    )
    invoice = session.exec(statement).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Накладная не найдена")

    statement_items = select(InvoiceItem).where(InvoiceItem.invoice_id == id)
    items = session.exec(statement_items).all()
    
    detail_items = []
    for item in items:
        sku = session.get(SKU, item.sku_id)
        detail_items.append(InvoiceItemDetailRead(
            id=item.id,
            sku_id=item.sku_id,
            quantity=item.quantity,
            purchase_price=item.purchase_price,
            sku_name=sku.name if sku else None,
            sku_price=sku.price if sku else None
        ))
    
    return InvoiceDetailRead(
        id=invoice.id,
        seller_id=invoice.seller_id,
        number=invoice.number,
        status=invoice.status,
        comment=invoice.comment,
        created_at=invoice.created_at,
        updated_at=invoice.updated_at,
        items=detail_items
    )