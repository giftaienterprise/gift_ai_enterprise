import asyncio
import json
import unittest
from unittest.mock import AsyncMock, Mock, patch

from app.schemas.ai_facade import AIRequest, AIResponse
from app.services.ai.ai_facade import ai_facade
from app.services.ai.prompts.product_description import (
    build_product_description_prompt,
)
from app.services.ai.provider_router import ai_provider_router
from app.services.ai.providers.base import BaseAIProvider
from app.services.ai.ai_core_service import ai_core_service
from app.services.business.gift_business_service import gift_business_service


class RecordingProvider(BaseAIProvider):
    provider_name = "recording"

    def __init__(self):
        self.request = None

    async def execute(self, request: AIRequest) -> AIResponse:
        self.request = request
        return AIResponse(
            success=True,
            task_type=request.task_type,
            provider=self.provider_name,
            data={"text": "ok"},
        )


class InvalidResponseProvider(BaseAIProvider):
    provider_name = "invalid-response"

    async def execute(self, request: AIRequest) -> AIResponse:
        return object()


class ProductDescriptionPromptTests(unittest.TestCase):
    def test_serializes_product_dictionary(self):
        prompt = build_product_description_prompt(
            name="测试礼物",
            category_name="礼品",
            brand_name="GiftAI",
            price=99,
        )

        payload = json.loads(prompt[prompt.index("{") :])
        self.assertEqual(payload["name"], "测试礼物")
        self.assertEqual(payload["category"], "礼品")
        self.assertEqual(payload["brand"], "GiftAI")
        self.assertEqual(payload["price"], 99)


class AIFacadeTests(unittest.TestCase):
    def setUp(self):
        self.provider = RecordingProvider()
        ai_provider_router.register_provider(self.provider)

    def tearDown(self):
        ai_provider_router.providers.pop(self.provider.provider_name, None)

    def test_builds_string_prompt_and_preserves_system_prompt(self):
        request = AIRequest(
            task_type="product_description",
            provider=self.provider.provider_name,
            context={
                "name": "测试礼物",
                "category_name": "礼品",
                "brand_name": "GiftAI",
                "price": 99,
            },
        )

        response = asyncio.run(ai_facade.execute(request))

        self.assertTrue(response.success)
        self.assertEqual(response.data, {"text": "ok"})
        self.assertIsInstance(self.provider.request.prompt, str)
        self.assertIn("测试礼物", self.provider.request.prompt)
        self.assertIsInstance(
            self.provider.request.context.get("system_prompt"),
            str,
        )

    def test_rejects_invalid_provider_response(self):
        provider = InvalidResponseProvider()
        ai_provider_router.register_provider(provider)
        self.addCleanup(ai_provider_router.providers.pop, provider.provider_name, None)
        request = AIRequest(task_type="generic", provider=provider.provider_name)

        with self.assertRaisesRegex(TypeError, "AIResponse"):
            asyncio.run(ai_facade.execute(request))


class CompatibilityServiceTests(unittest.TestCase):
    def test_gift_business_description_uses_legacy_ai_service(self):
        fake_service = Mock()
        fake_service.generate_product_description.return_value = {"title": "ok"}
        with patch(
            "app.services.business.gift_business_service.gift_ai_service",
            fake_service,
        ):
            result = gift_business_service.generate_ai_description(name="礼物")

        self.assertEqual(result, {"title": "ok"})

    def test_ai_core_delegates_generic_request_to_facade(self):
        expected = AIResponse(
            success=True,
            task_type="generic",
            provider="test",
            data={"text": "ok"},
        )
        with patch(
            "app.services.ai.ai_core_service.ai_facade.execute",
            new=AsyncMock(return_value=expected),
        ) as execute:
            result = asyncio.run(ai_core_service.call_ai(prompt="hello"))

        self.assertIs(result, expected)
        request = execute.await_args.args[0]
        self.assertEqual(request.task_type, "generic")
        self.assertEqual(request.prompt, "hello")


if __name__ == "__main__":
    unittest.main()
