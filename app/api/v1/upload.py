from fastapi import APIRouter, UploadFile, File, Depends
from uuid import UUID

from app.api.v1.dependencies.seller_depends import get_current_seller
from app.application.services.upload_service import UploadService

UPLOAD_DIR = "app/static/uploads"

router = APIRouter()


def get_service() -> UploadService:
    return UploadService(upload_dir=UPLOAD_DIR)


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    seller_id: UUID = Depends(get_current_seller),
    service: UploadService = Depends(get_service),
):
    return await service.save_image(file, seller_id)