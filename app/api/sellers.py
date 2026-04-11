from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import engine
from app.models import Seller, SellerCreate, SellerRead

router = APIRouter()

@router.post("/", response_model=SellerRead)
def create_seller(seller: SellerCreate, session: Session = Depends(lambda: Session(engine))):
    db_seller = Seller.model_validate(seller)
    session.add(db_seller)
    session.commit()
    session.refresh(db_seller)
    return db_seller