import unittest

from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

from app.core.dependencies import get_current_user
from app.main import app


PROTECTED = {
    ("POST", "/api/brands/"),
    ("PUT", "/api/brands/{brand_id}"),
    ("DELETE", "/api/brands/{brand_id}"),
    ("POST", "/api/categories/"),
    ("PUT", "/api/categories/{category_id}"),
    ("DELETE", "/api/categories/{category_id}"),
    ("POST", "/api/gifts/"),
    ("PUT", "/api/gifts/{gift_id}"),
    ("DELETE", "/api/gifts/{gift_id}"),
    ("POST", "/api/gifts/{gift_id}/images"),
    ("DELETE", "/api/gift-images/{image_id}"),
    ("POST", "/api/upload/image"),
}


def route_for(method: str, path: str) -> APIRoute:
    return next(
        route
        for route in app.routes
        if isinstance(route, APIRoute)
        and route.path == path
        and method in route.methods
    )


class RouteSecurityTests(unittest.TestCase):
    def test_mutations_declare_active_user_dependency(self):
        for method, path in PROTECTED:
            with self.subTest(method=method, path=path):
                calls = {
                    dependency.call
                    for dependency in route_for(method, path).dependant.dependencies
                }
                self.assertIn(get_current_user, calls)

    def test_ai_and_agent_reject_missing_token(self):
        client = TestClient(app)
        self.assertEqual(client.get("/ai/test").status_code, 401)
        self.assertEqual(
            client.post("/agent/run", json={"goal": "test"}).status_code,
            401,
        )

    def test_public_routes_do_not_require_active_user(self):
        public = {
            ("GET", "/"),
            ("GET", "/health"),
            ("POST", "/api/auth/register"),
            ("POST", "/api/auth/login"),
            ("GET", "/api/brands/"),
            ("GET", "/api/categories/"),
            ("GET", "/api/gifts/"),
            ("GET", "/api/gifts/{gift_id}"),
        }
        for method, path in public:
            with self.subTest(method=method, path=path):
                calls = {
                    dependency.call
                    for dependency in route_for(method, path).dependant.dependencies
                }
                self.assertNotIn(get_current_user, calls)


if __name__ == "__main__":
    unittest.main()
