import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.services.storage.storage_service import StorageService


MAX_IMAGE_BYTES = 5 * 1024 * 1024


class UnsupportedImageError(ValueError):
    pass


class UploadTooLargeError(ValueError):
    pass


def detect_image_type(data: bytes) -> tuple[str, str] | None:
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg", ".jpg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png", ".png"
    if len(data) >= 12 and data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "image/webp", ".webp"
    return None


class LocalStorageService(StorageService):
    """
    本地文件存储服务

    负责：
    - 保存上传文件
    - 删除本地文件
    - 判断文件是否存在
    """

    def save(self, file: UploadFile, folder: str = "temp") -> str:
        data = file.file.read(MAX_IMAGE_BYTES + 1)
        if len(data) > MAX_IMAGE_BYTES:
            raise UploadTooLargeError("Image exceeds 5 MiB")

        detected = detect_image_type(data)
        content_type = (file.content_type or "").lower()
        if detected is None or detected[0] != content_type:
            raise UnsupportedImageError("Unsupported or mismatched image type")

        filename = f"{uuid.uuid4().hex}{detected[1]}"

        save_dir = Path(settings.UPLOAD_DIR) / folder
        save_dir.mkdir(parents=True, exist_ok=True)

        file_path = save_dir / filename

        with open(file_path, "wb") as f:
            f.write(data)

        return f"{settings.UPLOAD_URL_PREFIX}/{folder}/{filename}"

    def delete(self, file_url: str) -> bool:
        if not file_url:
            return False

        relative_path = file_url.replace(
            settings.UPLOAD_URL_PREFIX,
            "",
            1,
        ).lstrip("/")

        file_path = Path(settings.UPLOAD_DIR) / relative_path

        if file_path.exists():
            file_path.unlink()
            return True

        return False

    def exists(self, file_url: str) -> bool:
        if not file_url:
            return False

        relative_path = file_url.replace(
            settings.UPLOAD_URL_PREFIX,
            "",
            1,
        ).lstrip("/")

        file_path = Path(settings.UPLOAD_DIR) / relative_path

        return file_path.exists()


local_storage_service = LocalStorageService()
