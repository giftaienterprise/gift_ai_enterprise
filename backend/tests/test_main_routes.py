import unittest

from fastapi.testclient import TestClient

from app.api import gift as gift_api
from app.main import app
from app.services.crud.gift_service import gift_service


class MainRouteTests(unittest.TestCase):
    def test_original_api_routes_remain_registered(self):
        paths = {route.path for route in app.routes}
        expected = {
            "/api/auth/register",
            "/api/auth/login",
            "/api/auth/me",
            "/api/settings/public",
            "/api/admin/summary",
            "/api/categories/",
            "/api/brands/",
            "/api/gifts/",
            "/api/upload/image",
            "/api/gift-images/{image_id}",
            "/ai/product-description",
            "/agent/run",
        }
        self.assertTrue(expected.issubset(paths), expected - paths)

    def test_gift_routes_use_the_crud_service_singleton(self):
        self.assertIs(gift_api.gift_service, gift_service)

    def test_root_and_health_contracts(self):
        client = TestClient(app)
        root = client.get("/")
        health = client.get("/health")

        self.assertEqual(root.status_code, 200)
        self.assertEqual(root.json()["message"], "Gift AI Enterprise API")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json(), {"status": "healthy"})


if __name__ == "__main__":
    unittest.main()
