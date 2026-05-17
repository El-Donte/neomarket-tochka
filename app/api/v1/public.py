from fastapi import APIRouter, Depends, Query, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any
from uuid import UUID

from app.database import get_session
from app.DTO.product import (
    ProductPublicResponse, 
    ProductPublicShortResponse, 
    ProductPublicPaginatedResponse
)
from app.DTO.sku import SKUPublicResponse
from app.infrastructure.repositories.product_repository import ProductRepository
from app.infrastructure.repositories.category_repository import CategoryRepository
from app.application.services.product_service import ProductService

router = APIRouter()


def get_service(session: AsyncSession = Depends(get_session)):
    repo = ProductRepository(session)
    cat_repo = CategoryRepository(session)
    return ProductService(repo, cat_repo)


@router.get("/products", response_model=ProductPublicPaginatedResponse)
async def list_public_products(
    x_service_key: str = Header(..., alias="X-Service-Key"),
    category_id: Optional[UUID] = Query(None),
    search: Optional[str] = Query(None, min_length=3),
    min_price: Optional[int] = Query(None, ge=0),
    max_price: Optional[int] = Query(None, ge=0),
    seller_id: Optional[UUID] = Query(None),
    sort: str = Query("created_desc"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ProductService = Depends(get_service),
):
    return await service.get_public_products(
        category_id=category_id,
        search=search,
        min_price=min_price,
        max_price=max_price,
        seller_id=seller_id,
        sort=sort,
        limit=limit,
        offset=offset
    )


@router.post("/products/batch", response_model=List[ProductPublicResponse])
async def batch_public_products(
    body: Dict[str, List[UUID]],
    x_service_key: str = Header(..., alias="X-Service-Key"),
    service: ProductService = Depends(get_service),
):
    product_ids = body.get("product_ids", [])
    if len(product_ids) > 100:
        raise HTTPException(status_code=400, detail="Too many product IDs")
    
    return await service.get_public_batch(product_ids)


@router.get("/products/{product_id}", response_model=ProductPublicResponse)
async def get_public_product(
    product_id: UUID,
    x_service_key: str = Header(..., alias="X-Service-Key"),
    service: ProductService = Depends(get_service),
):
    return await service.get_public_product(product_id)


@router.get("/products/{product_id}/similar", response_model=List[ProductPublicShortResponse])
async def get_public_similar_products(
    product_id: UUID,
    x_service_key: str = Header(..., alias="X-Service-Key"),
    limit: int = Query(10, ge=1, le=50),
    service: ProductService = Depends(get_service),
):
    return await service.get_similar_products(product_id, limit)


@router.get("/skus/{sku_id}", response_model=SKUPublicResponse)
async def get_public_sku(
    sku_id: UUID,
    x_service_key: str = Header(..., alias="X-Service-Key"),
    service: ProductService = Depends(get_service),
):
    return await service.get_public_sku(sku_id)
