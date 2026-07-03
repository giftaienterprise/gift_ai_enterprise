from abc import ABC, abstractmethod

from app.schemas.ai_facade import AIRequest, AIResponse


class BaseAIProvider(ABC):
    """
    企业级 AI Provider 抽象基类
    """

    provider_name: str

    @abstractmethod
    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        执行 AI 请求
        """
        pass

    def get_provider_name(self) -> str:
        """
        获取 Provider 名称
        """
        return self.provider_name