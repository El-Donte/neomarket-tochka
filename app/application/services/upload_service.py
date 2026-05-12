import os
import uuid
import aiofiles
from fastapi import HTTPException, UploadFile
from uuid import UUID


class UploadService:

    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir

    async def save_image(self, file: UploadFile, seller_id: UUID) -> dict:

        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Разрешены только изображения",
            )

        os.makedirs(self.upload_dir, exist_ok=True)

        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)

        try:
            async with aiofiles.open(file_path, "wb") as out_file:
                content = await file.read()
                await out_file.write(content)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при сохранении файла: {str(e)}",
            )

        return {
            "url": f"/static/uploads/{unique_filename}"
        }