import asyncio

from app.services.ai.gift_ai_service import gift_ai_service
from app.services.business.base import BaseBusinessService
from app.services.cache.ai_cache_decorator import ai_cache


class AIBusinessService(BaseBusinessService):
    """
    AI 企业业务层
    """

    def test_connection(self) -> str:
        return gift_ai_service.test_ai_connection()

    @ai_cache(task_type="product_description")
    async def generate_product_description(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        price: float | None = None,
    ):
        return await asyncio.to_thread(
            gift_ai_service.generate_product_description,
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            price=price,
        )

    @ai_cache(task_type="product_tags")
    async def generate_product_tags(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        description: str | None = None,
        price: float | None = None,
    ):
        return await asyncio.to_thread(
            gift_ai_service.generate_product_tags,
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            description=description,
            price=price,
        )

    @ai_cache(task_type="image_recognition")
    async def recognize_product_image(
        self,
        image_url: str,
    ):
        return await asyncio.to_thread(
            gift_ai_service.recognize_product_image,
            image_url=image_url,
        )


ai_business_service = AIBusinessService()