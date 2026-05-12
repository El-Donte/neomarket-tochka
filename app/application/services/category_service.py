from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import HTTPException, status

from app.models.category import Category
from app.DTO.category import (
    CategoryCreate,
    CategoryUpdate,
)
from app.infrastructure.repositories.category_repository import CategoryRepository


class CategoryService:

    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def create_category(self, data: CategoryCreate) -> Category:

        category = Category(
            name = data.name
        )

        if data.parent_id:
            parent = await self.repo.get_by_id(data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=400,
                    detail="Родительская категория не существует",
                )
            
            category.parent_id = data.parent_id
            
        return await self.repo.create(category)

    async def get_category(self, category_id: UUID) -> Category:

        category = await self.repo.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Категория не найдена",
            )

        return category

    async def update_category(
        self,
        category_id: UUID,
        data: CategoryUpdate,
    ) -> Category:

        category = await self.repo.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Категория не найдена",
            )

        if data.parent_id:
            if data.parent_id == category_id:
                raise HTTPException(
                    status_code=400,
                    detail="Категория не может быть родителем самой себя",
                )

            parent = await self.repo.get_by_id(data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=400,
                    detail="Родительская категория не существует",
                )

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(category, key, value)

        return await self.repo.save(category)

    async def delete_category(self, category_id: UUID):

        category = await self.repo.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Категория не найдена",
            )

        if category.children:
            raise HTTPException(
                status_code=400,
                detail="Нельзя удалить категорию с подкатегориями",
            )

        await self.repo.delete(category)

    async def get_category_tree(self, category_id: UUID, only_root: bool):

        categories = await self.repo.get_all()

        if only_root:
            return [c for c in categories if c.parent_id is None]

        category_map = {c.id: c for c in categories}

        for c in categories:
            c.children = []

        root = category_map.get(category_id)

        if not root:
            raise HTTPException(status_code=404, detail="Категория не найдена")

        for c in categories:
            if c.parent_id and c.parent_id in category_map:
                parent = category_map[c.parent_id]
                parent.children.append(c)

        return root
    
    async def get_category_list(
    self,
    parent_id: Optional[UUID],
    only_root: bool,
) -> List[Category]:

        categories = await self.repo.get_all()

        if only_root:
            return [c for c in categories if c.parent_id is None]

        if parent_id is None:
            return categories

        category_map = {c.id: c for c in categories}

        for c in categories:
            c.children = []

        for c in categories:
            if c.parent_id and c.parent_id in category_map:
                category_map[c.parent_id].children.append(c)

        root = category_map.get(parent_id)

        if not root:
            raise HTTPException(status_code=404, detail="Категория не найдена")

        return [root]