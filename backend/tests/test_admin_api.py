import unittest

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.database.session import Base, SessionLocal, engine
from app.main import app
from app.models.user import User


class AdminAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    def _headers(self, username: str, is_admin: bool) -> dict[str, str]:
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
            return {"Authorization": f"Bearer {token}"}
        finally:
            db.close()

    def test_auth_me_returns_current_user(self):
        headers = self._headers("member", is_admin=False)
        response = self.client.get("/api/auth/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "member")

    def test_admin_summary_requires_admin(self):
        headers = self._headers("member-summary", is_admin=False)
        self.assertEqual(
            self.client.get("/api/admin/summary", headers=headers).status_code,
            403,
        )

    def test_admin_summary_returns_counts(self):
        headers = self._headers("admin-summary", is_admin=True)
        response = self.client.get("/api/admin/summary", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertIn("gift_count", data)
        self.assertIn("active_gift_count", data)
        self.assertIn("category_count", data)
        self.assertIn("brand_count", data)
        self.assertIn("recent_gifts", data)


if __name__ == "__main__":
    unittest.main()
