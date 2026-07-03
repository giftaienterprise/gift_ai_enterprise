from typing import Dict

from app.services.ai.providers.deepseek_provider import DeepSeekProvider
from app.services.ai.providers.base import BaseAIProvider
from app.schemas.ai_facade import AIRequest


class AIProviderRouter:
    """
    企业级 Provider 路由器（带兜底）
    """

    def __init__(self):
        self.providers: Dict[str, object] = {
            "deepseek": DeepSeekProvider(),
        }

        self.default_provider_name = "deepseek"

    # =========================
    # 关键修复：安全获取 provider
    # =========================
    def get_provider(self, request: AIRequest):

        # =========================
        # 1. 安全读取 provider（兜底核心）
        # =========================
        provider_name = getattr(request, "provider", None)

        if not provider_name:
            provider_name = self.default_provider_name

        # =========================
        # 2. 防止非法值
        # =========================
        if provider_name not in self.providers:
            provider_name = self.default_provider_name

        return self.providers[provider_name]

    def register_provider(self, provider: BaseAIProvider) -> None:
        if not provider.provider_name:
            raise ValueError("provider_name must not be empty")

        self.providers[provider.provider_name] = provider


# 单例
ai_provider_router = AIProviderRouter()
