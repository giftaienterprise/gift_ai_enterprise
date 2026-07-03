import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.ai_facade import AIResponse
from app.services.business.ai_business_service import ai_business_service


def successful_response(task_type: str, data: dict) -> AIResponse:
    return AIResponse(
        success=True,
        task_type=task_type,
        provider="test",
        data=data,
    )


class AIAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_product_description_route(self):
        response_value = successful_response(
            "product_description",
            {"description": "适合送礼"},
        )
        with patch.object(
            ai_business_service,
            "generate_product_description",
            new=AsyncMock(return_value=response_value),
        ):
            response = self.client.post(
                "/ai/product-description",
                json={"name": "测试礼物", "price": 99},
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.json()["data"]["description"], "适合送礼")

    def test_product_tags_route(self):
        response_value = successful_response("product_tags", {"tags": ["礼品"]})
        with patch.object(
            ai_business_service,
            "generate_product_tags",
            new=AsyncMock(return_value=response_value),
        ):
            response = self.client.post(
                "/ai/product-tags",
                json={"name": "测试礼物"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["tags"], ["礼品"])

    def test_image_recognition_route(self):
        response_value = successful_response(
            "image_recognition",
            {"category": "礼品"},
        )
        with patch.object(
            ai_business_service,
            "recognize_image",
            new=AsyncMock(return_value=response_value),
        ):
            response = self.client.post(
                "/ai/image-recognition",
                json={"image_url": "https://example.com/gift.jpg"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["category"], "礼品")

    def test_analyze_product_route(self):
        response_value = successful_response(
            "analyze_product",
            {"title": "测试礼物", "tags": ["礼品"]},
        )
        with patch.object(
            ai_business_service,
            "analyze_product",
            new=AsyncMock(return_value=response_value),
        ):
            response = self.client.post(
                "/ai/analyze-product",
                json={"name": "测试礼物"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["title"], "测试礼物")

    def test_connection_route(self):
        response_value = successful_response("connection_test", {"text": "ok"})
        with patch.object(
            ai_business_service,
            "test_connection",
            new=AsyncMock(return_value=response_value),
            create=True,
        ):
            response = self.client.get("/ai/test")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["text"], "ok")

    def test_product_description_requires_name(self):
        response = self.client.post("/ai/product-description", json={})
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
