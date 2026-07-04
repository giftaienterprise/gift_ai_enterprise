import json
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class AdvisorRecommendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_recommend_returns_gifts_with_purchase_urls(self):
        mock_payload = {
            "combo_title": "测试方案",
            "gifts": [
                {
                    "name": "蓝牙音箱",
                    "price_yuan": 399,
                    "emoji": "🎵",
                    "reason": "适合音乐爱好者",
                    "match": "92%",
                    "meaning": "陪伴日常",
                    "tip": "支持蓝牙5.0",
                    "tags": ["音乐"],
                }
            ],
        }
        with patch(
            "app.services.ai.gift_recommendation_service.deepseek_ai_service.chat",
            return_value=json.dumps(mock_payload),
        ):
            with patch(
                "app.services.ai.gift_recommendation_service.settings.DEEPSEEK_API_KEY",
                "test-key",
            ):
                response = self.client.post(
                    "/api/advisor/recommend",
                    json={
                        "relation": "恋人",
                        "scene": "纪念日",
                        "budget": "200-500",
                        "note": "喜欢音乐",
                        "platform": "taobao",
                    },
                )

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertTrue(data["success"])
        self.assertEqual(len(data["gifts"]), 1)
        self.assertIn("purchase_url", data["gifts"][0])
        self.assertIn("taobao.com", data["gifts"][0]["purchase_url"])


if __name__ == "__main__":
    unittest.main()
