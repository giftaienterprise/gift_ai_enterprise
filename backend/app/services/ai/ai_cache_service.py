import hashlib
import json
from typing import Optional


class AICacheService:
    """
    企业级 AI 缓存服务
    """

    def __init__(self):
        # 临时内存缓存（后面可升级 Redis）
        self.cache: dict[str, str] = {}

    # =========================
    # 生成缓存Key
    # =========================
    def _make_key(
        self,
        task_type: str,
        prompt: str,
        model: str = "default",
    ) -> str:
        raw = f"{task_type}:{prompt}:{model}"
        return hashlib.md5(raw.encode("utf-8")).hexdigest()

    # =========================
    # 获取缓存
    # =========================
    def get(
        self,
        task_type: str,
        prompt: str,
        model: str = "default",
    ) -> Optional[str]:
        key = self._make_key(task_type, prompt, model)
        return self.cache.get(key)

    # =========================
    # 写入缓存
    # =========================
    def set(
        self,
        task_type: str,
        prompt: str,
        value: str,
        model: str = "default",
    ):
        key = self._make_key(task_type, prompt, model)
        self.cache[key] = value


ai_cache_service = AICacheService()