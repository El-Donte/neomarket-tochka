from fastapi import HTTPException, status

from app.infrastructure.repositories.seller_repository import SellerRepository
from app.DTO.seller import SellerUpdate
from app.models.seller import Seller


class SellerService:
    def __init__(self, repo: SellerRepository):
        self.repository = repo

    async def get_my_profile(self, seller_id: int) -> Seller:
        seller = await self.repository.get_by_seller_id(seller_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found",
            )
        return seller

    async def update_profile(self, seller_id: int, data: SellerUpdate) -> Seller:
        seller = await self.repository.get_by_seller_id(seller_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found",
            )

        updated_seller = await self.repository.update(seller, data)
        return updated_seller

    async def delete_profile(self, seller_id: int) -> None:
        seller = await self.repository.get_by_seller_id(seller_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found",
            )

        await self.repository.delete(seller)