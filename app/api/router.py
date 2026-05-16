from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.api.v1 import products, auth, sku, invoices, upload, categories, seller

security = HTTPBearer()

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(sku.router, prefix="/skus", tags=["SKU"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"], dependencies=[Depends(security)])
api_router.include_router(seller.router, prefix="/seller", tags=["Seller"])