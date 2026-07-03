from app.schemas.ai_facade import AIRequest, AIResponse
from app.services.ai.providers.base import BaseAIProvider
from app.services.ai.deepseek_ai_service import deepseek_ai_service
from app.services.ai.ai_redis_cache import ai_redis_cache
from app.services.ai.model_router import ai_model_router
from app.services.ai.cost_controller import ai_cost_controller


class DeepSeekProvider(BaseAIProvider):
    provider_name = "deepseek"

    async def execute(self, request: AIRequest) -> AIResponse:
        try:
            # =========================
            # 1. 成本控制
            # =========================
            if not ai_cost_controller.check_limit(
                request.prompt or "",
                2000,
            ):
                return AIResponse(
                    success=False,
                    task_type=request.task_type,
                    provider=self.provider_name,
                    data=None,
                    error="TOKEN_LIMIT_EXCEEDED",
                    cache_hit=False,
                    meta={"provider": self.provider_name},
                )

            # =========================
            # 2. 模型选择
            # =========================
            model = ai_model_router.select_model(request)

            # =========================
            # 3. Redis缓存
            # =========================
            cached = ai_redis_cache.get(
                task_type=request.task_type,
                prompt=request.prompt or "",
                model=model,
            )

            if cached:
                return AIResponse(
                    success=True,
                    task_type=request.task_type,
                    provider=self.provider_name,
                    data=cached,
                    cache_hit=True,
                    meta={"model": model},
                )

            # =========================
            # 4. 调用 AI
            # =========================
            result = deepseek_ai_service.chat(
                prompt=request.prompt or "",
                system_prompt=request.context.get("system_prompt"),
            )

            # =========================
            # 5. 写缓存
            # =========================
            ai_redis_cache.set(
                task_type=request.task_type,
                prompt=request.prompt or "",
                value=result,
                model=model,
            )

            return AIResponse(
                success=True,
                task_type=request.task_type,
                provider=self.provider_name,
                data=result,
                cache_hit=False,
                meta={"model": model},
            )

        except Exception as e:
            return AIResponse(
                success=False,
                task_type=request.task_type,
                provider=self.provider_name,
                data=None,
                error=str(e),
                cache_hit=False,
                meta={"provider": self.provider_name},
            )