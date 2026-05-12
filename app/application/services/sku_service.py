from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException, status

from app.models.sku import SKU, CharacteristicValue
from app.models.invoice import Stock
from app.DTO.sku import SKUCreate, SKUUpdate
from app.infrastructure.repositories.sku_repository import SKURepository


class SKUService:

    def __init__(self, repo: SKURepository):
        self.repo = repo

    async def create_sku(self, sku_in: SKUCreate, seller_id: UUID) -> SKU:

        product = await self.repo.get_product_for_seller(
            sku_in.product_id, seller_id
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Товар не найден или не принадлежит вам",
            )

        db_sku = SKU(
            product_id=sku_in.product_id,
            seller_id=seller_id,
            name=sku_in.name,
            price=sku_in.price,
            image_url=sku_in.image_url,
        )

        if sku_in.characteristics:
            db_sku.characteristics = [
                CharacteristicValue(name=c.name, value=c.value)
                for c in sku_in.characteristics
            ]

        try:
            await self.repo.create_sku(db_sku)
            await self.repo.create_stock(
                Stock(sku_id=db_sku.id, quantity=0)
            )
            await self.repo.commit()
        except Exception:
            await self.repo.rollback()
            raise

        return db_sku

    async def update_sku(
        self, sku_id: UUID, sku_in: SKUUpdate, seller_id: UUID
    ) -> SKU:

        db_sku = await self.repo.get_sku_for_seller(sku_id, seller_id)

        if not db_sku:
            raise HTTPException(status_code=404, detail="SKU не найден")

        sku_data = sku_in.model_dump(exclude_unset=True)

        for key, value in sku_data.items():
            setattr(db_sku, key, value)

        db_sku.updated_at = datetime.now(timezone.utc)

        return await self.repo.save_sku(db_sku)

    async def get_sku(self, sku_id: UUID, seller_id: UUID) -> SKU:

        db_sku = await self.repo.get_sku_for_seller(sku_id, seller_id)

        if not db_sku:
            raise HTTPException(status_code=404, detail="SKU не найден")

        return db_sku

    async def delete_sku(self, sku_id: UUID, seller_id: UUID):

        db_sku = await self.repo.get_sku_for_seller(sku_id, seller_id)

        if not db_sku:
            raise HTTPException(status_code=404, detail="SKU не найден")

        stock = await self.repo.get_stock(sku_id)

        if stock and stock.quantity > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Нельзя удалить SKU с остатками ({stock.quantity} шт)",
            )

        if await self.repo.sku_used_in_invoice(sku_id):
            raise HTTPException(
                status_code=400,
                detail="Нельзя удалить SKU — используется в накладных",
            )

        try:
            if stock:
                await self.repo.delete_stock(stock)

            await self.repo.delete_sku(db_sku)
            await self.repo.commit()
        except Exception:
            await self.repo.rollback()
            raise

        return {"message": "SKU успешно удалён", "sku_id": sku_id}

    async def get_inventory(self, seller_id: UUID):

        results = await self.repo.get_inventory(seller_id)

        return [
            {
                "sku_id": sku.id,
                "sku_name": sku.name,
                "product_title": product_title,
                "price": sku.price,
                "quantity": stock.quantity,
                "updated_at": stock.updated_at,
            }
            for sku, stock, product_title in results
        ]