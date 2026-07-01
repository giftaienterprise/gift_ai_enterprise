from fastapi import APIRouter, UploadFile, File

from app.core.response import success
from app.services.storage.storage_factory import storage_factory


router = APIRouter(
    prefix="/upload",
    tags=["upload"],
)


@router.post("/image")
def upload_image(
    file: UploadFile = File(...),
):
    storage = storage_factory.get_storage()

    image_url = storage.save(
        file=file,
        folder="temp",
    )

    return success(
        {
            "image_url": image_url,
        }
    )