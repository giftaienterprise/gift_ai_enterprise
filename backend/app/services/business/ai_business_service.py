from app.schemas.ai_facade import AIRequest
from app.services.ai.ai_facade import ai_facade
from app.services.ai.context.product_context import ProductContext


class AIBusinessService:
    """
    AI 企业级业务服务层（统一入口）
    """

    async def generate_product_description(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        price: float | None = None,
    ):
        request = AIRequest(
            task_type="product_description",
            context={
                "name": name,
                "category_name": category_name,
                "brand_name": brand_name,
                "price": price,
            },
            use_cache=True,
        )

        return await ai_facade.execute(request)

    async def generate_product_tags(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        description: str | None = None,
        price: float | None = None,
    ):
        request = AIRequest(
            task_type="product_tags",
            context={
                "name": name,
                "category_name": category_name,
                "brand_name": brand_name,
                "description": description,
                "price": price,
            },
            use_cache=True,
        )

        return await ai_facade.execute(request)

    async def recognize_image(self, image_url: str):
        request = AIRequest(
            task_type="image_recognition",
            context={
                "image_url": image_url,
            },
            image_url=image_url,
            use_cache=True,
        )

        return await ai_facade.execute(request)

    async def analyze_product(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        description: str | None = None,
        price: float | None = None,
        image_url: str | None = None,
    ):
        requests = [
            await self.generate_product_description(
                name=name,
                category_name=category_name,
                brand_name=brand_name,
                price=price,
            ),
            await self.generate_product_tags(
                name=name,
                category_name=category_name,
                brand_name=brand_name,
                description=description,
                price=price,
            ),
        ]

        image_result = None
        if image_url:
            image_result = await self.recognize_image(image_url)

        return {
            "description": requests[0].data,
            "tags": requests[1].data,
            "image": image_result.data if image_result else None,
        }

    async def test_connection(self):
        request = AIRequest(
            task_type="product_description",
            context={
                "name": "test",
                "category_name": "test",
                "brand_name": "test",
                "price": 1,
            },
            use_cache=False,
        )

        return await ai_facade.execute(request)


ai_business_service = AIBusinessService()