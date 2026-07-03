import unittest
from unittest.mock import Mock, patch

from fastapi import HTTPException
from jose import JWTError

from app.core.dependencies import get_current_user


class AuthenticationDependencyTests(unittest.TestCase):
    def test_returns_active_user(self):
        user = Mock(id=7, is_active=True)
        db = Mock()
        db.get.return_value = user

        with patch("app.core.security.jwt.decode", return_value={"sub": "7"}):
            self.assertIs(get_current_user("token", db), user)

        db.get.assert_called_once()

    def assert_rejected(self, token_payload=None, decode_error=None, user=None):
        db = Mock()
        db.get.return_value = user
        decode = patch("app.core.security.jwt.decode")
        with decode as mocked_decode:
            if decode_error:
                mocked_decode.side_effect = decode_error
            else:
                mocked_decode.return_value = token_payload
            with self.assertRaises(HTTPException) as raised:
                get_current_user("token", db)

        self.assertEqual(raised.exception.status_code, 401)
        self.assertEqual(raised.exception.detail, "INVALID_AUTHENTICATION")
        self.assertEqual(raised.exception.headers["WWW-Authenticate"], "Bearer")

    def test_rejects_missing_user(self):
        self.assert_rejected(token_payload={"sub": "7"})

    def test_rejects_inactive_user(self):
        self.assert_rejected(
            token_payload={"sub": "7"},
            user=Mock(id=7, is_active=False),
        )

    def test_rejects_non_numeric_subject(self):
        self.assert_rejected(token_payload={"sub": "not-a-number"})

    def test_rejects_invalid_or_expired_token(self):
        self.assert_rejected(decode_error=JWTError("expired or invalid"))


if __name__ == "__main__":
    unittest.main()
