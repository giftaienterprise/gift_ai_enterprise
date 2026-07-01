import json
from abc import ABC, abstractmethod

from app.core.config import settings
from app.services.ai.deepseek_ai_service import deepseek_ai_service


class BaseVisionAIService(ABC):
    """
    Vision AI 抽象层
    """

    @abstractmethod
    def recognize_product_image(
        self,
        image_url: str,
        system_prompt: str,
        prompt: str,
    ) -> dict:
        pass


class VisionAIService(BaseVisionAIService):
    """
    企业级 Vision AI 服务（支持多模型切换）
    当前默认：DeepSeek（文本模拟识图）
    """

    def recognize_product_image(
        self,
        image_url: str,
        system_prompt: str,
        prompt: str,
    ) -> dict:

        # =========================
        # 当前方案：DeepSeek fallback（文本模拟视觉）
        # =========================

        full_prompt = f"""
你是多模态商品识别AI。

虽然你不能真正看到图片，但请根据图片URL进行合理推断。

图片URL：
{image_url}

任务：
{prompt}

请严格输出 JSON：
"""

        content = deepseek_ai_service.chat(
            prompt=full_prompt,
            system_prompt=system_prompt,
        )

        return self._safe_parse(content, image_url)

    def _safe_parse(self, content: str, image_url: str) -> dict:
        """
        安全 JSON 解析
        """

        try:
            return json.loads(content)
        except Exception:
            return {
                "image_url": image_url,
                "category": "",
                "brand": "",
                "title": "",
                "description": content,
                "tags": [],
                "style": "",
                "message": "JSON解析失败，已返回原始内容",
            }


vision_ai_service = VisionAIService()