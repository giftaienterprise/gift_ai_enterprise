from redis import Redis
from redis.exceptions import RedisError

from app.core.config import settings


class RedisClient:
    """
    企业级 Redis Client

    Redis 不可用时：
    - 不影响主业务
    - get 返回 None
    - set/delete/expire 静默跳过
    - ping 返回 False
    """

    def __init__(self):
        self._client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD or None,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
        )

    @property
    def client(self) -> Redis:
        return self._client

    def ping(self) -> bool:
        try:
            return bool(self._client.ping())
        except RedisError:
            return False

    def get(self, key: str):
        try:
            return self._client.get(key)
        except RedisError:
            return None

    def set(
        self,
        key: str,
        value: str,
        ttl: int | None = None,
    ) -> bool:
        try:
            if ttl is None:
                ttl = settings.AI_CACHE_TTL_SECONDS

            return bool(
                self._client.set(
                    name=key,
                    value=value,
                    ex=ttl,
                )
            )
        except RedisError:
            return False

    def delete(self, key: str) -> bool:
        try:
            return bool(self._client.delete(key))
        except RedisError:
            return False

    def exists(self, key: str) -> bool:
        try:
            return bool(self._client.exists(key))
        except RedisError:
            return False

    def expire(
        self,
        key: str,
        ttl: int,
    ) -> bool:
        try:
            return bool(self._client.expire(key, ttl))
        except RedisError:
            return False


redis_client = RedisClient()