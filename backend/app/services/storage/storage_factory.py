from app.core.config import settings
from app.services.storage.local_storage_service import (
    local_storage_service,
)
from app.services.storage.storage_service import StorageService


class StorageFactory:
    """
    存储服务工厂
    """

    def get_storage(self) -> StorageService:
        driver = settings.STORAGE_DRIVER.lower()

        if driver == "local":
            return local_storage_service

        raise ValueError(
            f"Unsupported storage driver: {driver}"
        )


storage_factory = StorageFactory()