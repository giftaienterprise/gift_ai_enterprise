import json
from typing import Any

from app.core.config import settings
from app.services.cache.redis_client import redis_client
from app.services.cache.cache_key_builder import cache_key_builder


class AICacheService:
    """
    企业级 AI 缓存服务
    """

    def build_cache_key(
        self,
        task_type: str,
        prompt_data: dict[str, Any],
    ) -> str:
        return cache_key_builder.build(
            namespace="ai_cache",
            task_type=task_type,
            prompt_version=settings.AI_CACHE_PROMPT_VERSION,
            model_version=settings.AI_CACHE_MODEL_VERSION,
            payload=prompt_data,
        )

    def get(
        self,
        task_type: str,
        prompt_data: dict[str, Any],
    ) -> Any | None:
        key = self.build_cache_key(task_type, prompt_data)
        value = redis_client.get(key)

        if not value:
            return None

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            redis_client.delete(key)
            return None

    def set(
        self,
        task_type: str,
        prompt_data: dict[str, Any],
        result: Any,
        ttl: int | None = None,
    ) -> bool:
        key = self.build_cache_key(task_type, prompt_data)

        value = json.dumps(
            result,
            ensure_ascii=False,
        )

        return redis_client.set(
            key=key,
            value=value,
            ttl=ttl or settings.AI_CACHE_TTL_SECONDS,
        )

    def delete(
        self,
        task_type: str,
        prompt_data: dict[str, Any],
    ) -> bool:
        key = self.build_cache_key(task_type, prompt_data)
        return redis_client.delete(key)


ai_cache_service = AICacheService()