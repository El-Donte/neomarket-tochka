from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from sqlmodel import Session
from app.database import engine
from app.models import SKU, SKUCreate, SKURead

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", response_model=SKURead)
def create_sku(sku_in: SKUCreate, session: Session = Depends(get_session)):
    """Создать SKU"""
    db_sku = SKU.model_validate(sku_in)
    session.add(db_sku)
    session.commit()
    session.refresh(db_sku)
    return db_sku

@router.put("/", response_model=SKURead)
def update_sku(sku_id: int, sku_in: SKUCreate, session: Session = Depends(get_session)):
    """Изменить SKU"""
    db_sku = session.get(SKU, sku_id)
    if not db_sku:
        raise HTTPException(status_code=404, detail="SKU не найден")
    
    sku_data = sku_in.model_dump(exclude_unset=True)
    for key, value in sku_data.items():
        setattr(db_sku, key, value)
    
    db_sku.updated_at = datetime.utcnow()
    session.add(db_sku)
    session.commit()
    session.refresh(db_sku)
    return db_sku