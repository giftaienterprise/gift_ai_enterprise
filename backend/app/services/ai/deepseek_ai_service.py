from openai import OpenAI

from app.core.config import settings


class DeepSeekAIService:
    """
    DeepSeek AI 服务封装（企业级稳定版）
    """

    def __init__(self):
        self.client = None

    # =========================
    # 初始化 Client
    # =========================
    def _get_client(self) -> OpenAI:
        if not settings.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY 未配置")

        if self.client is None:
            self.client = OpenAI(
                api_key=settings.DEEPSEEK_API_KEY,
                base_url=settings.DEEPSEEK_BASE_URL,
                timeout=30,
                max_retries=1,
            )

        return self.client

    # =========================
    # Chat 核心方法
    # =========================
    def chat(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        """
        调用 DeepSeek Chat
        """

        if system_prompt is None:
            system_prompt = "你是 Gift AI Enterprise 企业级AI助手。"

        client = self._get_client()

        try:
            response = client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.7,
            )

            content = response.choices[0].message.content

            return content or ""

        except Exception as e:
            # =========================
            # 企业级降级返回
            # =========================
            return (
                "{"
                f'"error": "DEEPSEEK_ERROR", '
                f'"message": "{str(e)}"'
                "}"
            )


# =========================
# 单例模式
# =========================
deepseek_ai_service = DeepSeekAIService()