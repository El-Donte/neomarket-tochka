from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import Optional, Sequence

from app.models.product import Product
from app.models.sku import SKU, CharacteristicValue
from app.models.invoice import Stock, InvoiceItem
from app.models.image import Image


class ProductRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_paginated(
        self, 
        seller_id: UUID, 
        limit: int, 
        offset: int, 
        status: Optional[str] = None, 
        include_deleted: bool = False
    ) -> (Sequence[Product], int):
        query = select(Product).where(Product.seller_id == seller_id)
        
        if not include_deleted:
            query = query.where(Product.is_deleted == False)
        if status:
            query = query.where(Product.status == status)

        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.exec(count_query)

        query = query.limit(limit).offset(offset).options(selectinload(Product.images))
        result = await self.session.exec(query)
        return result.all(), total.one()

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()

        return await self.get_by_id(product.id)

    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        result = await self.session.exec(
            select(Product)
            .where(Product.id == product_id)
            .options(selectinload(Product.images), selectinload(Product.skus))
        )
        return result.first()
    
    async def update(self, product: Product) -> Product:
        await self.session.commit()
        
        return await self.get_by_id(product.id)

    async def get_by_id_with_skus(self, product_id: UUID, seller_id: UUID) -> Optional[Product]:
        result = await self.session.exec(
            select(Product)
            .where(Product.id == product_id)
            .where(Product.seller_id == seller_id)
            .options(selectinload(Product.skus))
        )
        return result.first()

    async def list_by_seller(self, seller_id: UUID) -> list[Product]:
        result = await self.session.exec(
            select(Product).where(Product.seller_id == seller_id)
        )
        return result.all()

    async def list_by_seller_with_skus(
        self,
        seller_id: UUID,
        status: Optional[str] = None,
    ) -> list[Product]:
        statement = (
            select(Product)
            .where(Product.seller_id == seller_id)
            .options(selectinload(Product.skus))
        )
        if status:
            statement = statement.where(Product.status == status)

        result = await self.session.exec(statement)
        return result.all()

    async def save(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()

        return await self.get_by_id(product.id)

    async def get_sku(self, sku_id: UUID) -> Optional[SKU]:
        return await self.session.get(SKU, sku_id)

    async def create_sku(self, sku: SKU) -> SKU:
        self.session.add(sku)
        await self.session.flush()
        return sku

    async def save_sku(self, sku: SKU) -> SKU:
        self.session.add(sku)
        await self.session.commit()
        await self.session.refresh(sku)
        return sku

    async def delete_sku(self, sku: SKU) -> None:
        await self.session.delete(sku)

    async def get_stock(self, sku_id: UUID) -> Optional[Stock]:
        result = await self.session.exec(
            select(Stock).where(Stock.sku_id == sku_id)
        )
        return result.first()

    async def create_stock(self, stock: Stock) -> None:
        self.session.add(stock)

    async def delete_stock(self, stock: Stock) -> None:
        await self.session.delete(stock)

    async def get_invoice_item_by_sku(self, sku_id: UUID) -> Optional[InvoiceItem]:
        result = await self.session.exec(
            select(InvoiceItem).where(InvoiceItem.sku_id == sku_id)
        )
        return result.first()

    async def get_product_image(self, image_id: UUID) -> Optional[Image]:
        result = await self.session.exec(select(Image).where(Image.id == image_id))
        return result.first()


    async def save_product_image(self, image: Image) -> Image:
        self.session.add(image)
        await self.session.commit()
        await self.session.refresh(image)
        return image


    async def delete_product_image(self, image: Image) -> None:
        await self.session.delete(image)
        await self.session.commit()