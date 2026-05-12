from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.database import get_session
from app.api.v1.dependencies.seller_depends import get_current_seller
from app.DTO.product import ProductCreate, ProductRead, ProductUpdate, ProductDashboardItem
from app.DTO.sku import SKURead, SKUCreate
from app.infrastructure.repositories.product_repository import ProductRepository
from app.application.services.product_service import ProductService

router = APIRouter()


async def get_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    return ProductService(ProductRepository(session))


@router.post("/", response_model=ProductRead)
async def create_product(
    product_in: ProductCreate,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.create_product(product_in, seller_id)


@router.get("/", response_model=list[ProductRead])
async def get_products(
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.list_products(seller_id)


@router.get("/dashboard/", response_model=list[ProductDashboardItem])
async def get_products_dashboard(
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
    status: Optional[str] = Query(None),
):
    return await service.get_dashboard(seller_id, status)


@router.get("/{id}", response_model=ProductRead)
async def get_product(
    id: UUID,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.get_product(id, seller_id)


@router.put("/{id}", response_model=ProductRead)
async def update_product(
    id: UUID,
    product_in: ProductCreate,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.update_product(id, product_in, seller_id)


@router.patch("/{id}", response_model=ProductRead)
async def update_product_partial(
    id: UUID,
    product_in: ProductUpdate,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.update_product_partial(id, product_in, seller_id)


@router.post("/{id}/submit", response_model=ProductRead)
async def submit_product_for_moderation(
    id: UUID,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.submit_for_moderation(id, seller_id)


@router.post("/{id}/skus", response_model=SKURead)
async def add_sku_to_product(
    id: UUID,
    sku_in: SKUCreate,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.add_sku(id, sku_in, seller_id)


@router.delete("/{id}/skus/{sku_id}", response_model=dict)
async def remove_sku_from_product(
    id: UUID,
    sku_id: UUID,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.remove_sku(id, sku_id, seller_id)


@router.put("/{id}/skus/{sku_id}", response_model=SKURead)
async def update_product_sku(
    id: UUID,
    sku_id: UUID,
    sku_in: SKUCreate,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.update_sku(sku_id, sku_in, seller_id)