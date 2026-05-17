from sqlalchemy.ext.asyncio import AsyncSession
from app.models.image import Image
from uuid import UUID
from typing import Optional

class ImageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, image: Image) -> Image:
        self.session.add(image)
        await self.session.commit()
        await self.session.refresh(image)
        return image

    async def get_by_id(self, image_id: UUID) -> Optional[Image]:
        return await self.session.get(Image, image_id)
