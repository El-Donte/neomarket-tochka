from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from sqlmodel import Session, select
from app.models.invoice import Invoice
from app.DTO.invoice import InvoiceItem
from app.DTO.invoice import InvoiceCreate, InvoiceRead
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=InvoiceRead)
def create_invoice(invoice_in: InvoiceCreate, session: Session = Depends(get_session)):
    """Создать черновик накладной"""
    from app.models.seller import Seller

    seller = session.get(Seller, invoice_in.seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller не найден")

    invoice = Invoice.model_validate(invoice_in)
    session.add(invoice)
    session.flush()

    for item_data in invoice_in.items:
        item = InvoiceItem(
            invoice_id=invoice.id,
            sku_id=item_data["sku_id"],
            quantity=item_data["quantity"],
            purchase_price=item_data.get("purchase_price")
        )
        session.add(item)
    
    session.commit()
    session.refresh(invoice)

    session.refresh(invoice)
    return invoice

@router.post("/accept", response_model=InvoiceRead)
def accept_invoice(invoice_id: int, session: Session = Depends(get_session)):
    """Принять накладную и обновить остатки"""
    from app.models.sku import SKU
    from app.models.invoice import Stock

    statement = select(Invoice).where(Invoice.id == invoice_id)
    invoice = session.exec(statement).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Накладная не найдена")

    if invoice.status != "CREATED":
        raise HTTPException(status_code=400, detail=f"Накладная уже {invoice.status}, нельзя принять")

    items_statement = select(InvoiceItem).where(InvoiceItem.invoice_id == invoice_id)
    items = session.exec(items_statement).all()
    
    if not items:
        raise HTTPException(status_code=400, detail="Накладная пуста")

    with session.begin():
        sku_quantities = {}
        for item in items:
            sku = session.get(SKU, item.sku_id)
            if not sku:
                raise HTTPException(
                    status_code=404, 
                    detail=f"SKU {item.sku_id} не найден. Операция откатывается."
                )

            if item.sku_id in sku_quantities:
                sku_quantities[item.sku_id] += item.quantity
            else:
                sku_quantities[item.sku_id] = item.quantity

        for sku_id, quantity in sku_quantities.items():
            sku = session.get(SKU, sku_id)
            sku.active_quantity += quantity
            sku.updated_at = datetime.now(timezone.utc)
            session.add(sku)

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
        invoice.updated_at =datetime.now(timezone.utc)
        session.add(invoice)
        
        session.commit()

    session.refresh(invoice)
    return invoice
