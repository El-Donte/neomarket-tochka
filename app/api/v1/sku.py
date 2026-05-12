from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_session
from app.api.v1.dependencies.seller_depends import get_current_seller
from app.DTO.sku import SKUCreate, SKUUpdate, SKURead
from app.infrastructure.repositories.sku_repository import SKURepository
from app.application.services.sku_service import SKUService


router = APIRouter()


async def get_service(
    session: AsyncSession = Depends(get_session),
) -> SKUService:
    return SKUService(SKURepository(session))


@router.post("/", response_model=SKURead)
async def create_sku(
    sku_in: SKUCreate,
    seller_id: UUID = Depends(get_current_seller),
    service: SKUService = Depends(get_service),
):
    return await service.create_sku(sku_in, seller_id)


@router.put("/{sku_id}", response_model=SKURead)
async def update_sku(
    sku_id: UUID,
    sku_in: SKUUpdate,
    seller_id: UUID = Depends(get_current_seller),
    service: SKUService = Depends(get_service),
):
    return await service.update_sku(sku_id, sku_in, seller_id)


@router.get("/{sku_id}", response_model=SKURead)
async def get_sku(
    sku_id: UUID,
    seller_id: UUID = Depends(get_current_seller),
    service: SKUService = Depends(get_service),
):
    return await service.get_sku(sku_id, seller_id)


@router.delete("/{sku_id}", response_model=dict)
async def delete_sku(
    sku_id: UUID,
    seller_id: UUID = Depends(get_current_seller),
    service: SKUService = Depends(get_service),
):
    return await service.delete_sku(sku_id, seller_id)


@router.get("/inventory/all", response_model=list[dict])
async def get_inventory(
    seller_id: UUID = Depends(get_current_seller),
    service: SKUService = Depends(get_service),
):
    return await service.get_inventory(seller_id)