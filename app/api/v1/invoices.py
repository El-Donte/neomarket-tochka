from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_session
from app.api.v1.dependencies.seller_depends import get_current_seller
from app.DTO.invoice import InvoiceCreate, InvoiceRead
from app.infrastructure.repositories.invoice_repository import InvoiceRepository
from app.application.services.invoice_service import InvoiceService

router = APIRouter()

async def get_invoice_service(db: AsyncSession = Depends(get_session)):
    repository = InvoiceRepository(db)
    return InvoiceService(repository) 

@router.post("/", response_model=InvoiceRead)
async def create_invoice(
    invoice_in: InvoiceCreate,
    service: InvoiceService = Depends(get_invoice_service),
    seller_id: UUID = Depends(get_current_seller),
):

    return await service.create_invoice(invoice_in, seller_id)


@router.post("/accept", response_model=InvoiceRead)
async def accept_invoice(
    invoice_id: UUID,
    service: InvoiceService = Depends(get_session),
    seller_id: UUID = Depends(get_current_seller),
):

    return await service.accept_invoice(invoice_id, seller_id)