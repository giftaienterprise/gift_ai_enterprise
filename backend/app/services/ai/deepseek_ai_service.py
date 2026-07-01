from openai import OpenAI

from app.core.config import settings
from app.services.ai.base_ai_service import BaseAIService


class DeepSeekAIService(BaseAIService):
    """
    DeepSeek AI 服务封装
    """

    def __init__(self):
        self.client = None

    def _get_client(self) -> OpenAI:
        if not settings.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY 未配置，请检查 backend/.env 文件")

        if self.client is None:
            self.client = OpenAI(
                api_key=settings.DEEPSEEK_API_KEY,
                base_url=settings.DEEPSEEK_BASE_URL,
                timeout=30,
                max_retries=1,
            )

        return self.client

    def chat(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        if system_prompt is None:
            system_prompt = "你是 Gift AI Enterprise 的企业级 AI 助手。"

        client = self._get_client()

        try:
            response = client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            return response.choices[0].message.content or ""

        except Exception as e:
            return (
                "{"
                f'"error": "AI_SERVICE_ERROR", '
                f'"message": "{str(e)}"'
                "}"
            )


deepseek_ai_service = DeepSeekAIService()