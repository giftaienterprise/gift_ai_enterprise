import json

from app.services.ai.deepseek_ai_service import deepseek_ai_service
from app.services.ai.prompt_manager import prompt_manager
from app.services.ai.vision_ai_service import vision_ai_service
from app.services.ai.context.context_builder import product_context_builder
from app.services.ai.result_merger import result_merger

class GiftAIService:
    """
    Gift AI 能力统一入口
    """

    def test_ai_connection(self) -> str:
        return deepseek_ai_service.chat(
            prompt="请只回复：Gift AI Enterprise DeepSeek API 接入成功。",
            system_prompt="你是 Gift AI Enterprise 的 AI 服务测试助手。",
        )

    def generate_product_description(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        price: float | None = None,
    ) -> dict:
        system_prompt, user_prompt = prompt_manager.build_product_description(
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            price=price,
        )

        content = deepseek_ai_service.chat(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )

        return self._parse_json_response(content)

    def generate_product_tags(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        description: str | None = None,
        price: float | None = None,
    ) -> dict:
        system_prompt, user_prompt = prompt_manager.build_product_tags(
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            description=description,
            price=price,
        )

        content = deepseek_ai_service.chat(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )

        return self._parse_json_response(content)

    def _parse_json_response(self, content: str) -> dict:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "raw": content,
            }

    def recognize_product_image(
        self,
        image_url: str,
    ) -> dict:
        """
        AI 商品图片识别
        """

        system_prompt, user_prompt = prompt_manager.build_image_recognition(
            image_url=image_url,
        )

        return vision_ai_service.recognize_product_image(
            image_url=image_url,
            prompt=user_prompt,
            system_prompt=system_prompt,
        )

    def analyze_product(
            self,
            name: str,
            category_name: str | None = None,
            brand_name: str | None = None,
            description: str | None = None,
            price: float | None = None,
            image_url: str | None = None,
    ) -> dict:
        """
        AI 商品统一分析
        """

        product_description = self.generate_product_description(
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            price=price,
        )

        product_tags = self.generate_product_tags(
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            description=description or product_description.get("description"),
            price=price,
        )

        image_result = None
        if image_url:
            image_result = self.recognize_product_image(
                image_url=image_url,
            )

        return {
            "title": product_description.get("title"),
            "subtitle": product_description.get("subtitle"),
            "description": product_description.get("description"),
            "selling_points": product_description.get("selling_points", []),
            "tags": product_tags.get("tags", []),
            "image": image_result,
        }

    def analyze_product(
            self,
            name: str,
            category_name: str | None = None,
            brand_name: str | None = None,
            description: str | None = None,
            price: float | None = None,
            image_url: str | None = None,
    ) -> dict:
        """
        🚀 单次 AI 商品全量分析（性能优化版）
        """

        system_prompt, user_prompt = prompt_manager.build_product_analysis(
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            description=description,
            price=price,
            image_url=image_url,
        )

        content = deepseek_ai_service.chat(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )

        return self._parse_json_response(content)

    def quick_analyze(self, ctx) -> dict:
        """
        🚀 快速分析：title + tags
        """

        system_prompt = "你是商品命名与标签专家，只输出JSON"

        prompt = f"""
    商品名称：{ctx.name}
    类目：{ctx.category}
    品牌：{ctx.brand}

    请输出 JSON：
    {{
      "title": "",
      "tags": []
    }}
    """

        content = deepseek_ai_service.chat(
            prompt=prompt,
            system_prompt=system_prompt
        )

        return self._parse_json_response(content)

    def generate_description(self, ctx) -> dict:
        """
        🧠 商品描述生成
        """

        system_prompt, user_prompt = prompt_manager.build_product_description(
            name=ctx.name,
            category_name=ctx.category,
            brand_name=ctx.brand,
            price=ctx.price,
        )

        content = deepseek_ai_service.chat(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )

        return self._parse_json_response(content)

    def analyze_image(self, ctx) -> dict:
        """
        🖼 图片识别
        """

        if not ctx.image_url:
            return None

        system_prompt, user_prompt = prompt_manager.build_image_recognition(
            image_url=ctx.image_url
        )

        content = deepseek_ai_service.chat(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )

        return self._parse_json_response(content)

    async def analyze_product_parallel(
            self,
            name: str,
            category_name: str | None = None,
            brand_name: str | None = None,
            description: str | None = None,
            price: float | None = None,
            image_url: str | None = None,
    ) -> dict:
        """
        🚀 并行 AI 商品分析
        """

        import asyncio

        ctx = product_context_builder.build(
            name=name,
            category=category_name,
            brand=brand_name,
            price=price,
            description=description,
            image_url=image_url,
        )

        tasks = [
            asyncio.to_thread(self.quick_analyze, ctx),
            asyncio.to_thread(self.generate_description, ctx),
            asyncio.to_thread(self.analyze_image, ctx),
        ]

        quick, desc, image = await asyncio.gather(*tasks)

        return result_merger.merge(
            quick=quick,
            desc=desc,
            image=image,
        )


gift_ai_service = GiftAIService()