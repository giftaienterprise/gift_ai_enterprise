import hashlib
import json
import redis

from app.core.config import settings


class AIRedisCache:
    """
    企业级 AI Redis 缓存
    """

    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )

        self.ttl = settings.AI_CACHE_TTL_SECONDS

    # =========================
    # 生成缓存Key
    # =========================
    def _make_key(self, task_type: str, prompt: str, model: str) -> str:
        raw = f"{task_type}:{prompt}:{model}"
        return "ai_cache:" + hashlib.md5(raw.encode("utf-8")).hexdigest()

    # =========================
    # 获取缓存
    # =========================
    def get(self, task_type: str, prompt: str, model: str) -> str | None:
        key = self._make_key(task_type, prompt, model)
        return self.client.get(key)

    # =========================
    # 写入缓存
    # =========================
    def set(self, task_type: str, prompt: str, value: str, model: str):
        key = self._make_key(task_type, prompt, model)
        self.client.setex(key, self.ttl, value)


ai_redis_cache = AIRedisCache()