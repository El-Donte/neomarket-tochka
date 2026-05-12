from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import Optional

from app.models.product import Product
from app.models.sku import SKU, CharacteristicValue
from app.models.invoice import Stock, InvoiceItem


class ProductRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    # ---------- PRODUCT ----------

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_by_id(self, product_id: UUID, seller_id: UUID) -> Optional[Product]:
        result = await self.session.exec(
            select(Product)
            .where(Product.id == product_id)
            .where(Product.seller_id == seller_id)
        )
        return result.first()

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
        await self.session.refresh(product)
        return product

    # ---------- SKU ----------

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

    # ---------- STOCK ----------

    async def get_stock(self, sku_id: UUID) -> Optional[Stock]:
        result = await self.session.exec(
            select(Stock).where(Stock.sku_id == sku_id)
        )
        return result.first()

    async def create_stock(self, stock: Stock) -> None:
        self.session.add(stock)

    async def delete_stock(self, stock: Stock) -> None:
        await self.session.delete(stock)

    # ---------- INVOICE ITEM ----------

    async def get_invoice_item_by_sku(self, sku_id: UUID) -> Optional[InvoiceItem]:
        result = await self.session.exec(
            select(InvoiceItem).where(InvoiceItem.sku_id == sku_id)
        )
        return result.first()

    # ---------- TRANSACTIONS ----------

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def flush(self) -> None:
        await self.session.flush()