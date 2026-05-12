from fastapi import APIRouter
from app.api.v1 import products, auth, sku, invoices, upload


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(sku.router, prefix="/skus", tags=["SKU"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])