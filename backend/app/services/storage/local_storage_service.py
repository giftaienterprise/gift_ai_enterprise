import os
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.services.storage.storage_service import StorageService


class LocalStorageService(StorageService):
    """
    本地文件存储服务

    负责：
    - 保存上传文件
    - 删除本地文件
    - 判断文件是否存在
    """

    def save(self, file: UploadFile, folder: str = "temp") -> str:
        ext = os.path.splitext(file.filename or "")[1]
        filename = f"{uuid.uuid4().hex}{ext}"

        save_dir = Path(settings.UPLOAD_DIR) / folder
        save_dir.mkdir(parents=True, exist_ok=True)

        file_path = save_dir / filename

        with open(file_path, "wb") as f:
            f.write(file.file.read())

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