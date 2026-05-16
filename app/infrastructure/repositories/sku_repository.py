from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional, List

from app.models.sku import SKU, CharacteristicValue
from app.models.invoice import Stock, InvoiceItem
from app.models.product import Product
from app.models.image import Image


class SKURepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    # ---------- PRODUCT CHECK ----------

    async def get_product_for_seller(
        self, product_id: UUID, seller_id: UUID
    ) -> Optional[Product]:
        result = await self.session.exec(
            select(Product)
            .where(Product.id == product_id)
            .where(Product.seller_id == seller_id)
        )
        return result.first()
    
    async def get_skus_by_product(
        self, product_id: UUID
    ) -> List[SKU]:
        result = await self.session.exec(
            select(SKU)
            .where(SKU.product_id == product_id)
        )

        return list(result.all())

    # ---------- SKU ----------

    async def get_sku_for_seller(
        self, sku_id: UUID, seller_id: UUID
    ) -> Optional[SKU]:
        result = await self.session.exec(
            select(SKU)
            .join(Product, SKU.product_id == Product.id)
            .where(SKU.id == sku_id)
            .where(Product.seller_id == seller_id)
        )
        return result.unique().first()
    
    async def create_sku(self, sku: SKU) -> SKU:
        self.session.add(sku)
        await self.session.flush()
        return sku

    async def save_sku(self, sku: SKU) -> SKU:
        self.session.add(sku)
        await self.session.commit()
        await self.session.refresh(sku)
        return sku

    async def delete_sku(self, sku: SKU):
        await self.session.delete(sku)
    # ---------- STOCK ----------

    async def get_stock(self, sku_id: UUID) -> Optional[Stock]:
        result = await self.session.exec(
            select(Stock).where(Stock.sku_id == sku_id)
        )
        return result.first()

    async def create_stock(self, stock: Stock):
        self.session.add(stock)

    async def delete_stock(self, stock: Stock):
        await self.session.delete(stock)

    # ---------- INVOICE CHECK ----------

    async def sku_used_in_invoice(self, sku_id: UUID) -> bool:
        result = await self.session.exec(
            select(InvoiceItem).where(InvoiceItem.sku_id == sku_id)
        )
        return result.first() is not None

    # ---------- INVENTORY ----------

    async def get_inventory(self, seller_id: UUID):
        statement = (
            select(SKU, Stock, Product.title)
            .join(Stock, SKU.id == Stock.sku_id)
            .join(Product, SKU.product_id == Product.id)
            .where(SKU.seller_id == seller_id)
        )
        result = await self.session.exec(statement)
        return result.all()

    # ---------- TRANSACTIONS ----------

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    # ----------  Images -------------

    async def get_image_for_seller(
        self, image_id: UUID, seller_id: UUID
    ) -> Optional[Image]:
        """Получить изображение, только если его SKU → Product принадлежит продавцу"""
        result = await self.session.exec(
            select(Image)
            .join(SKU, Image.sku_id == SKU.id)
            .join(Product, SKU.product_id == Product.id)
            .where(Image.id == image_id)
            .where(Product.seller_id == seller_id)
        )
        return result.first()

    async def add_image(self, image: Image) -> Image:
        self.session.add(image)
        await self.session.flush()
        return image

    async def update_image(self, image: Image) -> Image:
        self.session.add(image)
        await self.session.flush()
        return image

    async def delete_image(self, image: Image):
        await self.session.delete(image)