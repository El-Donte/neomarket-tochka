from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import Optional, List

from app.models.category import Category


class CategoryRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        result = await self.session.exec(
            select(Category)
            .where(Category.id == category_id)
            .options(selectinload(Category.children))
        )
        return result.first()

    async def list(
        self,
        parent_id: Optional[UUID] = None,
        only_root: bool = False,
    ) -> List[Category]:

        statement = select(Category)

        if only_root:
            statement = statement.where(Category.parent_id.is_(None))
        elif parent_id is not None:
            statement = statement.where(Category.parent_id == parent_id)

        result = await self.session.exec(statement)
        return result.all()
    
    async def save(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete(self, category: Category):
        await self.session.delete(category)
        await self.session.commit()

    async def get_all(self) -> List[Category]:
        result = await self.session.exec(
            select(Category))
        return result.all()