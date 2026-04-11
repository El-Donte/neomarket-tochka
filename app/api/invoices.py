from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.database import engine
from app.models import Invoice, InvoiceCreate, InvoiceRead

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", response_model=InvoiceRead)
def create_invoice(invoice_in: InvoiceCreate, session: Session = Depends(get_session)):
    """Создать накладную"""
    db_invoice = Invoice.model_validate(invoice_in)
    session.add(db_invoice)
    session.commit()
    session.refresh(db_invoice)
    return db_invoice

@router.post("/accept")
def accept_invoice(invoice_id: int, session: Session = Depends(get_session)):
    """Принять накладную (склад)"""
    db_invoice = session.get(Invoice, invoice_id)
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Накладная не найдена")
    
    db_invoice.status = "ACCEPTED"
    session.add(db_invoice)
    session.commit()
    return {"status": "accepted", "invoice_id": invoice_id}