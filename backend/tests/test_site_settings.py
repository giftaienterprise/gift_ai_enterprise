import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.database.session import Base, SessionLocal, engine
from app.main import app
from app.models.user import User


class SiteSettingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    def _create_user(self, username: str, is_admin: bool = False) -> tuple[User, str]:
        db = SessionLocal()
        try:
            existing = db.query(User).filter(User.username == username).first()
            if existing:
                db.delete(existing)
                db.commit()
            user = User(
                username=username,
                password_hash=hash_password("secret123"),
                is_admin=is_admin,
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            token = create_access_token(str(user.id))
            return user, token
        finally:
            db.close()

    def test_public_settings_hide_internal_fields(self):
        response = self.client.get("/api/settings/public")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.json()["data"]),
            {
                "wechat_id",
                "wechat_qr_url",
                "phone",
                "share_title",
                "share_description",
                "share_image_url",
            },
        )

    def test_regular_user_cannot_update_settings(self):
        _, token = self._create_user("member-settings", is_admin=False)
        response = self.client.put(
            "/api/settings",
            headers={"Authorization": f"Bearer {token}"},
            json={"phone": "10086"},
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_can_update_settings(self):
        _, token = self._create_user("admin-settings", is_admin=True)
        response = self.client.put(
            "/api/settings",
            headers={"Authorization": f"Bearer {token}"},
            json={"phone": "10010", "wechat_id": "gift-ai"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["phone"], "10010")
        self.assertEqual(response.json()["data"]["wechat_id"], "gift-ai")


if __name__ == "__main__":
    unittest.main()
