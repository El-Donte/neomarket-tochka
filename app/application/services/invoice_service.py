from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException, status

from app.models.invoice import Invoice, InvoiceItem, Stock
from app.DTO.invoice import InvoiceCreate
from app.infrastructure.repositories.invoice_repository import InvoiceRepository


class InvoiceService:

    def __init__(self, repo: InvoiceRepository):
        self.repo = repo

    async def create_invoice(self, invoice_in: InvoiceCreate, seller_id: UUID):

        invoice = Invoice(
            seller_id=seller_id,
            number=invoice_in.number,
            comment=invoice_in.comment,
        )

        await self.repo.create_invoice(invoice)

        items = [
            InvoiceItem(
                invoice_id=invoice.id,
                sku_id=item.sku_id,
                quantity=item.quantity,
                purchase_price=item.purchase_price,
            )
            for item in invoice_in.items
        ]

        await self.repo.add_items(items)
        await self.repo.commit()

        return invoice

    async def accept_invoice(self, invoice_id: UUID, seller_id: UUID):
        invoice = await self.repo.get_by_id(invoice_id)

        if not invoice or invoice.seller_id != seller_id:
            raise HTTPException(status_code=404, detail="Накладная не найдена")

        if invoice.status != "CREATED":
            raise HTTPException(
                status_code=400,
                detail=f"Накладная уже {invoice.status}",
            )

        items = await self.repo.get_items(invoice_id)

        if not items:
            raise HTTPException(status_code=400, detail="Накладная пуста")

        sku_quantities = {}
        for item in items:
            sku_quantities[item.sku_id] = (
                sku_quantities.get(item.sku_id, 0) + item.quantity
            )

        try:
            for sku_id, quantity in sku_quantities.items():

                sku = await self.repo.get_sku(sku_id)

                if not sku or sku.seller_id != seller_id:
                    raise HTTPException(
                        status_code=400,
                        detail=f"SKU {sku_id} недоступен",
                    )

                stock = await self.repo.get_stock(sku_id)

                if stock:
                    stock.quantity += quantity
                    stock.updated_at = datetime.now(timezone.utc)
                    await self.repo.save(stock)
                else:
                    new_stock = Stock(
                        sku_id=sku_id,
                        quantity=quantity,
                    )
                    await self.repo.save(new_stock)

            invoice.status = "ACCEPTED"
            invoice.updated_at = datetime.now(timezone.utc)
            await self.repo.save(invoice)

            await self.repo.commit()

        except Exception:
            await self.repo.rollback()
            raise

        return invoice