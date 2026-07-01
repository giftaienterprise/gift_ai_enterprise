from app.services.storage.storage_factory import storage_factory


class BaseBusinessService:
    """
    企业级 Business 基类

    统一封装 Business 层通用能力：
    - 获取 Storage
    - 后续扩展事务
    - 后续扩展日志
    - 后续扩展权限
    """

    def get_storage(self):
        return storage_factory.get_storage()