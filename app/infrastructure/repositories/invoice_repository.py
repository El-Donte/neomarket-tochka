from sqlmodel import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional

from app.models.invoice import Invoice, InvoiceItem, Stock
from app.models.sku import SKU


class InvoiceRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_invoice(self, invoice: Invoice):
        self.session.add(invoice)
        await self.session.flush()
        return invoice

    async def add_items(self, items: list[InvoiceItem]):
        for item in items:
            self.session.add(item)

    async def get_by_id(self, invoice_id: UUID) -> Optional[Invoice]:
        statement = (
            select(Invoice)
            .where(Invoice.id == invoice_id)
            .options(selectinload(Invoice.items))
        )
        result = await self.session.exec(statement)
        return result.first()

    async def list_invoices(self, seller_id: UUID, limit: int, offset: int, status: Optional[str] = None):
        statement = select(Invoice).where(Invoice.seller_id == seller_id)
        if status:
            statement = statement.where(Invoice.status == status)
        
        # Add total count
        count_statement = select(func.count()).select_from(statement.subquery())
        total_count = await self.session.scalar(count_statement)
        
        statement = statement.limit(limit).offset(offset).options(selectinload(Invoice.items))
        result = await self.session.exec(statement)
        
        return result.all(), total_count

    async def get_items(self, invoice_id: UUID):
        result = await self.session.exec(
            select(InvoiceItem).where(InvoiceItem.invoice_id == invoice_id)
        )
        return result.all()

    async def update_stock(self, sku_id: UUID, quantity_to_add: int):
        statement = select(Stock).where(Stock.sku_id == sku_id).with_for_update()
        result = await self.session.exec(statement)
        stock = result.first()
        
        now = datetime.now(timezone.utc)
        if stock:
            stock.stock_quantity += quantity_to_add
            stock.active_quantity += quantity_to_add
            stock.updated_at = now
            self.session.add(stock)
        else:
            new_stock = Stock(
                sku_id=sku_id,
                stock_quantity=quantity_to_add,
                active_quantity=quantity_to_add,
                reserved_quantity=0,
                updated_at=now
            )
            self.session.add(new_stock)

    async def save(self, obj):
        self.session.add(obj)

    async def delete(self, obj):
        await self.session.delete(obj)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def refresh(self, obj):
        await self.session.refresh(obj)