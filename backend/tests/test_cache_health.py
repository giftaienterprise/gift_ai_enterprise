from app.services.cache.redis_client import redis_client
from app.services.cache.ai_cache_service import ai_cache_service


def main():
    print("Redis Ping:", redis_client.ping())

    cache_key = ai_cache_service.build_cache_key(
        task_type="health_check",
        prompt_data={
            "name": "Gift AI Enterprise",
            "version": "Sprint 9.5",
        },
    )

    print("Cache Key:", cache_key)


if __name__ == "__main__":
    main()