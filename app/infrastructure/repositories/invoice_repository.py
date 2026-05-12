from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
from datetime import datetime, timezone

from app.models.invoice import Invoice, InvoiceItem, Stock
from app.models.sku import SKU


class InvoiceRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    # ---------- CREATE ----------

    async def create_invoice(self, invoice: Invoice):
        self.session.add(invoice)
        await self.session.flush()
        return invoice

    async def add_items(self, items: list[InvoiceItem]):
        for item in items:
            self.session.add(item)

    # ---------- GET ----------

    async def get_by_id(self, invoice_id: UUID):
        statement = (
            select(Invoice)
            .where(Invoice.id == invoice_id)
            .options(selectinload(Invoice.items))
        )
        result = await self.session.exec(statement)
        return result.first()

    async def list_by_seller(self, seller_id: UUID):
        statement = select(Invoice).where(Invoice.seller_id == seller_id)
        result = await self.session.exec(statement)
        return result.all()

    async def get_items(self, invoice_id: UUID):
        result = await self.session.exec(
            select(InvoiceItem).where(InvoiceItem.invoice_id == invoice_id)
        )
        return result.all()

    async def get_sku(self, sku_id: UUID):
        return await self.session.get(SKU, sku_id)

    async def get_stock(self, sku_id: UUID):
        result = await self.session.exec(
            select(Stock).where(Stock.sku_id == sku_id)
        )
        return result.first()

    async def save(self, obj):
        self.session.add(obj)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()