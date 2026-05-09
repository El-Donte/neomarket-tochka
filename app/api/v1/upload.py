from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
import uuid
import shutil
from app.api.v1.dependencies.seller_depends import get_current_seller
from uuid import UUID

router = APIRouter()

UPLOAD_DIR = "app/static/uploads"

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    seller_id: UUID = Depends(get_current_seller)
):
    """
    Загрузка изображения на сервер.
    Возвращает URL загруженного файла.
    """
    # Проверка типа файла
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Разрешены только изображения")

    # Генерация уникального имени файла
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Сохранение файла
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении файла: {str(e)}")

    # Возвращаем URL (для локальной разработки это /static/uploads/...)
    # В реальности здесь может быть URL CDN
    return {"url": f"/static/uploads/{unique_filename}"}
