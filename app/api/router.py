from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.api.v1 import products, auth, sku, invoices, upload, categories, seller, public, inventory, moderation

security = HTTPBearer()

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["Products"], dependencies=[Depends(security)])
api_router.include_router(sku.router, prefix="/skus", tags=["SKU"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
api_router.include_router(upload.router, prefix="/images", tags=["Images"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(seller.router, prefix="/seller", tags=["Seller"])
api_router.include_router(public.router, prefix="/public", tags=["Public Catalog"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(moderation.router, prefix="/moderation", tags=["Moderation Events"])