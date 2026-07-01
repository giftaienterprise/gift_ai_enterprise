from functools import wraps
from typing import Any, Callable

from app.core.config import settings
from app.services.cache.ai_cache_service import ai_cache_service


def ai_cache(
    task_type: str,
):
    """
    AI 缓存装饰器
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not settings.AI_CACHE_ENABLED:
                result = await func(*args, **kwargs)

                if isinstance(result, dict):
                    result["cache_enabled"] = False
                    result["cache_hit"] = False
                    result["cache_task_type"] = task_type

                return result

            prompt_data: dict[str, Any] = {
                "args": args[1:] if len(args) > 1 else [],
                "kwargs": kwargs,
            }

            cached_result = ai_cache_service.get(
                task_type=task_type,
                prompt_data=prompt_data,
            )

            if cached_result is not None:
                if isinstance(cached_result, dict):
                    cached_result["cache_enabled"] = True
                    cached_result["cache_hit"] = True
                    cached_result["cache_task_type"] = task_type

                return cached_result

            result = await func(*args, **kwargs)

            ai_cache_service.set(
                task_type=task_type,
                prompt_data=prompt_data,
                result=result,
            )

            if isinstance(result, dict):
                result["cache_enabled"] = True
                result["cache_hit"] = False
                result["cache_task_type"] = task_type

            return result

        return wrapper

    return decorator