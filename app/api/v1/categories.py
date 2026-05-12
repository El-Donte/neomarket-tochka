from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from uuid import UUID

from app.database import get_session
from app.DTO.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryWithChildrenResponse,
)
from app.application.services.category_service import CategoryService
from app.infrastructure.repositories.category_repository import CategoryRepository
from app.api.v1.dependencies.seller_depends import get_current_seller


router = APIRouter()


def get_service(
    session: AsyncSession = Depends(get_session),
) -> CategoryService:
    return CategoryService(CategoryRepository(session))

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    parent_id: Optional[UUID] = Query(default=None),
    only_root: bool = Query(default=False),
    service: CategoryService = Depends(get_service),
):
    return await service.get_category_list(parent_id, only_root)

@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_service),
    seller_id: UUID = Depends(get_current_seller)
):
    return await service.create_category(data)

@router.get(
    "/{category_id}",
    response_model=CategoryWithChildrenResponse,
)
async def get_category(
    category_id: UUID,
    service: CategoryService = Depends(get_service),
):
    return await service.get_category(category_id)

@router.patch(
    "/{category_id}",
    response_model=CategoryWithChildrenResponse,
)
async def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_service),
    seller_id: UUID = Depends(get_current_seller)
):
    return await service.update_category(category_id, data)

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    category_id: UUID,
    service: CategoryService = Depends(get_service),
    seller_id: UUID = Depends(get_current_seller)
):
    await service.delete_category(category_id)