from abc import ABC, abstractmethod


class StorageService(ABC):
    """
    存储服务抽象基类
    """

    @abstractmethod
    def save(self, file, folder: str = "temp") -> str:
        pass

    @abstractmethod
    def delete(self, file_url: str) -> bool:
        pass

    @abstractmethod
    def exists(self, file_url: str) -> bool:
        pass