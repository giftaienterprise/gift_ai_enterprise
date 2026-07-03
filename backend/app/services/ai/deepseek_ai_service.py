import logging

from openai import OpenAI

from app.core.config import settings


logger = logging.getLogger(__name__)


class DeepSeekAIService:
    def __init__(self):
        self.client = None

    def _get_client(self) -> OpenAI:
        if not settings.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY is not configured")

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
            system_prompt = "You are the Gift AI Enterprise assistant."

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
        except Exception as exc:
            logger.exception("DeepSeek request failed")
            raise RuntimeError("DeepSeek request failed") from exc


deepseek_ai_service = DeepSeekAIService()
