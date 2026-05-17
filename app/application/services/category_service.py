from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, List, Dict
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

    async def _generate_unique_slug(self, name: str) -> str:
        """Генерирует уникальный slug, проверяя существующие в БД."""

        existing_slugs = await self.repo.get_existing_slugs()
        return Category.generate_slug(name, existing_slugs)
    
    async def _validate_parent(self, parent_id: Optional[UUID], category_id: Optional[UUID] = None) -> Optional[Category]:
        """Проверяет существование родителя и отсутствие цикла."""
        if parent_id is None:
            return None
        parent = await self.repo.get_by_id(parent_id, include_children=True)
        if not parent:
            raise HTTPException(status_code=400, detail="Родительская категория не существует")
        
        if category_id is not None and parent_id == category_id:
            raise HTTPException(status_code=400, detail="Категория не может быть родителем самой себя")
        
        if category_id is not None:
            descendants = await self.repo.get_all_descendants(category_id)
            if parent_id in [d.id for d in descendants]:
                raise HTTPException(status_code=400, detail="Нельзя сделать потомка родителем")
            
        return parent

    async def create_category(self, data: CategoryCreate) -> Category:
        slug = await self._generate_unique_slug(data.name)

        level = 0
        path = ""

        parent = await self._validate_parent(data.parent_id)

        if parent:
            level = parent.level + 1
            path = f"{parent.path}/{parent.id}".strip("/")

        new_category = Category(
            **data.model_dump(),
            slug=slug,
            level=level,
            path=path,
        )
            
        created_category = await self.repo.create(new_category)
        return await self.repo.get_by_id(created_category.id, include_children=True)
    
    async def get_category_with_children(self, category_id: UUID) -> Category:
        category = await self.repo.get_by_id(category_id, include_children=True)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    
    async def update_category(self, category_id: UUID, schema: CategoryUpdate) -> Category:
        category = await self.repo.get_by_id(category_id, include_children=True)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        data = schema.model_dump(exclude_unset=True)
        
        if "name" in data and data["name"] != category.name:
            existing_slugs = await self.repo.get_existing_slugs()
            category.slug = Category.generate_slug(data["name"], existing_slugs)

        if "parent_id" in data and data["parent_id"] != category.parent_id:
            new_parent_id = data["parent_id"]

            if new_parent_id == category.id:
                raise HTTPException(status_code=400, detail="Cannot set category as its own parent")
            
            old_full_path_prefix = f"{category.path}/{category.id}".strip("/")
            old_level = category.level
            
            if new_parent_id:
                parent = await self.repo.get_by_id(new_parent_id, include_children=True)

                if not parent:
                    raise HTTPException(status_code=404, detail="New parent category not found")
                
                if old_full_path_prefix in parent.path:
                    raise HTTPException(status_code=400, detail="Cannot move category into its own descendant")
                
                category.parent_id = new_parent_id
                category.level = parent.level + 1
                category.path = f"{parent.path}/{parent.id}".strip("/")
            else:
                category.parent_id = None
                category.level = 0
                category.path = ""

            new_full_path_prefix = f"{category.path}/{category.id}".strip("/")
            level_delta = category.level - old_level

            await self.repo.update_descendants_path(
                old_full_path=old_full_path_prefix,
                new_full_path=new_full_path_prefix,
                level_delta=level_delta
            )

        for key, value in data.items():
            if key not in ["parent_id"]:
                setattr(category, key, value)
            
        return await self.repo.update(category)

    async def get_category(self, category_id: UUID) -> Category:

        category = await self.repo.get_by_id(category_id, include_children=True)

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Категория не найдена",
            )

        return category

    async def delete_category(self, category_id: UUID):

        category = await self.repo.get_by_id(category_id, include_children=True)

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
        
        if await self.repo.has_products(category_id):
            raise HTTPException(status_code=409, detail="Cannot delete category with products")

        await self.repo.delete(category)

    async def get_breadcrumbs(self, category_id: UUID) -> List[Category]:
        category = await self.repo.get_by_id(category_id, include_children=True)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        if not category.path:
            return [category]

        ids = [UUID(id_str) for id_str in category.path.split("/") if id_str]
        ids.append(category.id)
        
        categories = await self.repo.get_by_ids(ids)

        cat_dict = {cat.id: cat for cat in categories}
        return [cat_dict[id_] for id_ in ids if id_ in cat_dict]

    async def get_tree(self) -> List[Dict]:
        all_cats = await self.repo.get_all_for_tree()

        tree = []
        nodes = {cat.id: {"id": cat.id, "name": cat.name, "children": []} for cat in all_cats}
        
        for cat in all_cats:
            node = nodes[cat.id]
            if cat.parent_id is None:
                tree.append(node)
            else:
                parent_node = nodes.get(cat.parent_id)
                if parent_node:
                    parent_node["children"].append(node)
        
        return tree
    
    async def get_category_list(
    self,
    parent_id: Optional[UUID],
    only_root: bool,
) -> List[Category]:
        return await self.repo.list(parent_id=parent_id, only_root=only_root)