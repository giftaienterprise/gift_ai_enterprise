import unittest
from unittest.mock import AsyncMock, Mock, patch

from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.dependencies import enforce_ai_rate_limit
from app.main import app
from app.schemas.ai_facade import AIRequest
from app.services.ai.agent_brain import agent_brain
from app.services.ai.deepseek_ai_service import deepseek_ai_service
from app.services.ai.providers.deepseek_provider import DeepSeekProvider


SECRET_ERROR = "secret path /opt/private and key sk-sensitive"


class ErrorRedactionTests(unittest.IsolatedAsyncioTestCase):
    async def test_provider_returns_stable_error(self):
        provider = DeepSeekProvider()
        request = AIRequest(task_type="generic", prompt="hello")
        with (
            patch.object(settings, "AI_CACHE_ENABLED", False),
            patch.object(
                deepseek_ai_service,
                "chat",
                side_effect=RuntimeError(SECRET_ERROR),
            ),
        ):
            result = await provider.execute(request)

        self.assertFalse(result.success)
        self.assertEqual(result.error, "AI_PROVIDER_ERROR")
        self.assertNotIn("secret", result.error)
        self.assertNotIn("/opt/private", result.error)

    def test_deepseek_service_raises_generic_error(self):
        old_client = deepseek_ai_service.client
        self.addCleanup(setattr, deepseek_ai_service, "client", old_client)
        deepseek_ai_service.client = Mock()
        deepseek_ai_service.client.chat.completions.create.side_effect = RuntimeError(
            SECRET_ERROR
        )

        with (
            patch.object(settings, "DEEPSEEK_API_KEY", "test-only"),
            self.assertRaisesRegex(RuntimeError, "DeepSeek request failed") as raised,
        ):
            deepseek_ai_service.chat("hello")
        self.assertNotIn("secret", str(raised.exception))

    async def test_agent_api_returns_stable_error(self):
        app.dependency_overrides[enforce_ai_rate_limit] = lambda: object()
        self.addCleanup(app.dependency_overrides.pop, enforce_ai_rate_limit, None)
        with patch.object(
            agent_brain,
            "run",
            new=AsyncMock(side_effect=RuntimeError(SECRET_ERROR)),
        ):
            response = TestClient(app).post(
                "/agent/run",
                json={"goal": "test"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["error"], "AGENT_EXECUTION_FAILED")
        self.assertNotIn("secret", response.text)
        self.assertNotIn("/opt/private", response.text)


if __name__ == "__main__":
    unittest.main()
