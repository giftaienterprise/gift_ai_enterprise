import unittest
from unittest.mock import Mock

from fastapi import HTTPException

from app.core.dependencies import require_admin


class AdminSecurityTests(unittest.TestCase):
    def test_require_admin_returns_admin(self):
        admin = Mock(is_admin=True, is_active=True)
        self.assertIs(require_admin(admin), admin)

    def test_require_admin_rejects_regular_user(self):
        try:
            require_admin(Mock(is_admin=False, is_active=True))
        except HTTPException as exc:
            self.assertEqual(exc.status_code, 403)
            self.assertEqual(exc.detail, "ADMIN_REQUIRED")
        else:
            raise AssertionError("regular user was accepted")


if __name__ == "__main__":
    unittest.main()
