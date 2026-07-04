from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.dependencies import require_admin
from app.core.response import success
from app.services.storage.storage_factory import storage_factory
from app.services.storage.local_storage_service import (
    UnsupportedImageError,
    UploadTooLargeError,
)


router = APIRouter(
    prefix="/upload",
    tags=["upload"],
)


@router.post("/image", dependencies=[Depends(require_admin)])
def upload_image(
    file: UploadFile = File(...),
):
    storage = storage_factory.get_storage()

    try:
        image_url = storage.save(
            file=file,
            folder="temp",
        )
    except UploadTooLargeError as exc:
        raise HTTPException(status_code=413, detail="IMAGE_TOO_LARGE") from exc
    except UnsupportedImageError as exc:
        raise HTTPException(
            status_code=415,
            detail="UNSUPPORTED_IMAGE_TYPE",
        ) from exc

    return success(
        {
            "image_url": image_url,
        }
    )
