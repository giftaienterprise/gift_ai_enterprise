from abc import ABC, abstractmethod


class BaseAIService(ABC):
    """
    AI 基础服务抽象类

    所有第三方 AI 服务都继承它：
    - DeepSeek
    - OpenAI
    - 后续其他模型
    """

    @abstractmethod
    def chat(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        pass