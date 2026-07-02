from app.schemas.ai_facade import AIRequest, AIResponse
from app.services.ai.ai_facade import ai_facade


class AICoreService:
    """
    AI 核心统一调用层（打断循环）
    """

    async def call_ai(
        self,
        prompt: str,
        image_url: str | None = None,
        use_cache: bool = True,
    ) -> AIResponse:
        return await ai_facade.execute(
            AIRequest(
                task_type="generic",
                prompt=prompt,
                image_url=image_url,
                use_cache=use_cache,
            )
        )


ai_core_service = AICoreService()
