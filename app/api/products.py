from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from app.database import engine
from app.models import Product, ProductCreate

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", response_model=Product)
def create_product(product_in: ProductCreate, session: Session = Depends(get_session)):
    """Создать товар"""
    db_product = Product.model_validate(product_in)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.get("/{id}", response_model=Product)
def get_product(id: int, session: Session = Depends(get_session)):
    """Получить товар со всеми его SKU"""
    statement = select(Product).where(Product.id == id).options(joinedload(Product.skus))
    product = session.exec(statement).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@router.put("/{id}", response_model=Product)
def update_product(id: int, product_in: ProductCreate, session: Session = Depends(get_session)):
    """Изменить товар и отправить на модерацию"""
    db_product = session.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    product_data = product_in.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    
    db_product.status = "ON_MODERATION" 
    db_product.updated_at = datetime.utcnow()
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product