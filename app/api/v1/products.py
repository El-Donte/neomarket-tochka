from fastapi import APIRouter, Depends, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Union
from uuid import UUID

from app.database import get_session
from app.api.v1.dependencies.seller_depends import get_current_seller
from app.DTO.product import ProductCreate, ProductResponse, ProductUpdate, ProductDashboardItem, ProductPaginatedResponse, ProductPublicResponse
from app.DTO.sku import SKURead, SKUCreate
from app.infrastructure.repositories.product_repository import ProductRepository
from app.application.services.product_service import ProductService
from app.DTO.image import ImageCreate, ImageResponse, ImageUpdate

router = APIRouter()


async def get_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    return ProductService(ProductRepository(session))


@router.post("/", response_model=ProductResponse)
async def create_product(
    product_in: ProductCreate,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.create_product(product_in, seller_id)


@router.get("/", response_model=ProductPaginatedResponse)
async def get_products(
    seller_id: UUID = Depends(get_current_seller),
    limit: int = 20,
    offset: int = 0,
    status: Optional[str] = None,
    include_deleted: bool = False,
    service: ProductService = Depends(get_service),
):
    return await service.list_my_products(seller_id, limit, offset, status, include_deleted)


@router.get("/dashboard/", response_model=list[ProductDashboardItem])
async def get_products_dashboard(
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
    status: Optional[str] = Query(None),
):
    return await service.get_dashboard(seller_id, status)


@router.get("/{product_id}", response_model=Union[ProductResponse, ProductPublicResponse])
async def get_product(
    product_id: UUID,
    x_service_key: Optional[str] = Header(None, alias="X-Service-Key"),
    service: ProductService = Depends(get_service),
):
    product = await service.get_product(product_id)

    if x_service_key:
        return ProductPublicResponse.model_validate(product)
    
    return product

@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    product_in: ProductUpdate,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.update_product(product_id, product_in, seller_id)

@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: UUID,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    await service.delete_product(product_id, seller_id)


@router.post("/{id}/submit", response_model=ProductResponse)
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

@router.post("/{product_id}/images", response_model=ImageResponse, status_code=201)
async def add_product_image(
    product_id: UUID,
    image_in: ImageCreate,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.add_product_image(product_id, image_in, seller_id)

@router.patch("/images/{image_id}", response_model=ImageResponse)
async def update_product_image(
    image_id: UUID,
    image_in: ImageUpdate,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    return await service.update_product_image(image_id, image_in, seller_id)

@router.delete("/images/{image_id}", status_code=204)
async def delete_product_image(
    image_id: UUID,
    seller_id: UUID = Depends(get_current_seller),
    service: ProductService = Depends(get_service),
):
    await service.delete_product_image(image_id, seller_id)