import unittest
from unittest.mock import Mock

from fastapi import HTTPException

from app.core.dependencies import enforce_ai_rate_limit
from app.core.rate_limit import SlidingWindowRateLimiter


class SlidingWindowRateLimiterTests(unittest.TestCase):
    def test_limits_each_user_and_expires_old_requests(self):
        clock = Mock(return_value=100.0)
        limiter = SlidingWindowRateLimiter(
            limit=10,
            window_seconds=60,
            clock=clock,
        )

        for _ in range(10):
            self.assertTrue(limiter.allow("7"))
        self.assertFalse(limiter.allow("7"))
        self.assertTrue(limiter.allow("8"))

        clock.return_value = 161.0
        self.assertTrue(limiter.allow("7"))

    def test_rejects_invalid_configuration(self):
        with self.assertRaises(ValueError):
            SlidingWindowRateLimiter(limit=0, window_seconds=60)
        with self.assertRaises(ValueError):
            SlidingWindowRateLimiter(limit=10, window_seconds=0)

    def test_dependency_returns_429_on_eleventh_request(self):
        limiter = SlidingWindowRateLimiter(limit=10, window_seconds=60)
        user = Mock(id=7)
        with unittest.mock.patch(
            "app.core.dependencies.ai_rate_limiter",
            limiter,
        ):
            for _ in range(10):
                self.assertIs(enforce_ai_rate_limit(user), user)
            with self.assertRaises(HTTPException) as raised:
                enforce_ai_rate_limit(user)
        self.assertEqual(raised.exception.status_code, 429)
        self.assertEqual(raised.exception.detail, "AI_RATE_LIMIT_EXCEEDED")


if __name__ == "__main__":
    unittest.main()
