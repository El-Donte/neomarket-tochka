from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status

from app.models.product import Product, ProductStatus
from app.models.sku import SKU, CharacteristicValue
from app.models.invoice import Stock
from app.DTO.product import ProductCreate, ProductUpdate, ProductDashboardItem
from app.DTO.sku import SKUCreate
from app.infrastructure.repositories.product_repository import ProductRepository
from app.models.image import Image
from app.DTO.image import ImageCreate, ImageResponse, ImageUpdate


class ProductService:

    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def create_product(self, product_in: ProductCreate, seller_id: UUID) -> Product:
        new_product = Product(
            **product_in.model_dump(),
            seller_id=seller_id,
            status=ProductStatus.CREATED,
            is_deleted=False,
        )
        return await self.repo.create(new_product)

    async def get_product(self, product_id: UUID) -> Product:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден")
        return product

    async def update_product(
        self,
        product_id: UUID,
        product_in: ProductUpdate,
        seller_id: UUID,
    ) -> Product:
        product = await self.get_product(product_id)

        if product.seller_id != seller_id:
            raise HTTPException(status_code=403)

        if product.status == ProductStatus.HARD_BLOCKED:
            raise HTTPException(status_code=403, detail="Product is hard blocked and cannot be edited")
        
        data = product_in.model_dump(exclude_unset=True)

        if product.status in [ProductStatus.MODERATED, ProductStatus.BLOCKED]:
            product.status = ProductStatus.ON_MODERATION

        for key, value in data.items():
            setattr(product, key, value)

        return await self.repo.update(product)
    
    async def delete_product(self, product_id: UUID, seller_id: UUID) -> None:
        product = await self.get_product(product_id)
        if product.seller_id != seller_id:
            raise HTTPException(status_code=403)
        
        product.is_deleted = True
        await self.repo.update(product)

    async def list_my_products(
        self,
        seller_id: UUID,
        limit: int,
        offset: int,
        status_filter: Optional[str],
        include_deleted: bool,
    ):
        items, total = await self.repo.get_paginated(seller_id, limit, offset, status_filter, include_deleted)
        return {"items": items, "total_count": total, "limit": limit, "offset": offset}

    async def get_dashboard(
        self,
        seller_id: UUID,
        status: Optional[str],
    ) -> list[ProductDashboardItem]:

        status_map = {
            "MODERATION": "ON_MODERATION",
            "PUBLISHED": "PUBLISHED",
        }

        db_status = None
        if status:
            status_upper = status.upper()
            if status_upper not in status_map:
                raise HTTPException(
                    status_code=400,
                    detail=f"Неизвестный статус: {status}. Используйте MODERATION или PUBLISHED",
                )
            db_status = status_map[status_upper]

        products = await self.repo.list_by_seller_with_skus(seller_id, db_status)

        return [
            ProductDashboardItem(
                id=p.id,
                title=p.title,
                image_url=p.image_url,
                status=p.status,
                sku_count=len(p.skus),
                published_sku_count=sum(1 for sku in p.skus if sku.status == "PUBLISHED"),
                created_at=p.created_at,
                updated_at=p.updated_at,
            )
            for p in products
        ]

    async def submit_for_moderation(self, product_id: UUID, seller_id: UUID) -> Product:
        db_product = await self.repo.get_by_id_with_skus(product_id, seller_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Товар не найден")

        if not db_product.skus:
            raise HTTPException(
                status_code=400,
                detail="Нельзя отправить товар на модерацию без SKU",
            )
        if db_product.status == "ON_MODERATION":
            raise HTTPException(status_code=400, detail="Товар уже на модерации")

        if db_product.status == "PUBLISHED":
            raise HTTPException(
                status_code=400,
                detail="Товар уже опубликован. Для изменений используйте редактирование.",
            )

        db_product.status = "ON_MODERATION"
        db_product.updated_at = datetime.now(timezone.utc)

        return await self.repo.save(db_product)

    async def add_sku(self, product_id: UUID, sku_in: SKUCreate, seller_id: UUID) -> SKU:
        db_product = await self.repo.get_by_id(product_id, seller_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Товар не найден")

        db_sku = SKU(
            product_id=product_id,
            seller_id=seller_id,
            name=sku_in.name,
            price=sku_in.price,
            image_url=sku_in.image_url,
        )

        if hasattr(sku_in, "characteristics") and sku_in.characteristics:
            db_sku.characteristics = [
                CharacteristicValue(name=char.name, value=char.value)
                for char in sku_in.characteristics
            ]

        try:
            await self.repo.create_sku(db_sku)
            await self.repo.create_stock(Stock(sku_id=db_sku.id, quantity=0))
            await self.repo.commit()
        except Exception:
            await self.repo.rollback()
            raise

        await self.repo.session.refresh(db_sku)
        return db_sku

    async def remove_sku(self, product_id: UUID, sku_id: UUID, seller_id: UUID) -> dict:
        db_product = await self.repo.get_by_id(product_id, seller_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Товар не найден")

        db_sku = await self.repo.get_sku(sku_id)
        if not db_sku:
            raise HTTPException(status_code=404, detail="SKU не найден")

        if db_sku.product_id != product_id:
            raise HTTPException(status_code=400, detail="SKU не принадлежит этому товару")

        stock = await self.repo.get_stock(sku_id)
        if stock:
            if stock.quantity > 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Нельзя удалить SKU с остатками ({stock.quantity} шт)",
                )
            await self.repo.delete_stock(stock)

        invoice_item = await self.repo.get_invoice_item_by_sku(sku_id)
        if invoice_item:
            raise HTTPException(
                status_code=400,
                detail="Нельзя удалить SKU — он используется в накладных",
            )

        try:
            await self.repo.delete_sku(db_sku)
            await self.repo.commit()
        except Exception:
            await self.repo.rollback()
            raise

        return {"message": "SKU успешно удалён", "sku_id": sku_id}

    async def update_sku(self, sku_id: UUID, sku_in: SKUCreate, seller_id: UUID) -> SKU:
        db_product = await self.repo.get_by_id(sku_in.product_id, seller_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Товар не найден")

        db_sku = await self.repo.get_sku(sku_id)
        if not db_sku:
            raise HTTPException(status_code=404, detail="SKU не найден")

        if db_sku.product_id != sku_in.product_id:
            raise HTTPException(status_code=400, detail="SKU не принадлежит этому товару")

        sku_data = sku_in.model_dump(exclude_unset=True, exclude={"characteristics"})
        for key, value in sku_data.items():
            setattr(db_sku, key, value)

        db_sku.updated_at = datetime.now(timezone.utc)

        return await self.repo.save_sku(db_sku)
    
    async def add_product_image(
        self,
        product_id: UUID,
        image_in: ImageCreate,
        seller_id: UUID,
    ) -> Image:
        product = await self.get_product(product_id)
        if product.seller_id != seller_id:
            raise HTTPException(status_code=403)

        new_image = Image(
            product_id=product_id,
            **image_in.model_dump()
        )

        return await self.repo.save_product_image(new_image)
    
    async def update_product_image(
        self,
        image_id: UUID,
        image_in: ImageUpdate,
        seller_id: UUID,
    ) -> Image:

        image = await self.repo.get_product_image(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Изображение не найдено")

        product = await self.get_product(image.product_id)
        if product.seller_id != seller_id:
            raise HTTPException(status_code=403)

        for key, value in image_in.model_dump(exclude_unset=True).items():
            setattr(image, key, value)

        return await self.repo.update(image)
    
    async def delete_product_image(
        self,
        image_id: UUID,
        seller_id: UUID,
    ) -> None:

        image = await self.repo.get_product_image(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Изображение не найдено")

        product = await self.get_product(image.product_id)
        if product.seller_id != seller_id:
            raise HTTPException(status_code=403)

        await self.repo.delete_product_image(image)