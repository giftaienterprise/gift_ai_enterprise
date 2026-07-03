import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import UploadFile
from starlette.datastructures import Headers

from app.services.storage.local_storage_service import (
    MAX_IMAGE_BYTES,
    UnsupportedImageError,
    UploadTooLargeError,
    local_storage_service,
)
from app.services.storage.storage_factory import storage_factory


JPEG = b"\xff\xd8\xff" + b"safe"
PNG = b"\x89PNG\r\n\x1a\n" + b"safe"
WEBP = b"RIFF\x04\x00\x00\x00WEBP" + b"safe"


def upload(filename: str, content_type: str, data: bytes) -> UploadFile:
    return UploadFile(
        filename=filename,
        file=io.BytesIO(data),
        headers=Headers({"content-type": content_type}),
    )


class UploadSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.settings_patch = patch(
            "app.services.storage.local_storage_service.settings.UPLOAD_DIR",
            self.temp_dir.name,
        )
        self.settings_patch.start()
        self.addCleanup(self.settings_patch.stop)

    def saved_files(self):
        return [path for path in Path(self.temp_dir.name).rglob("*") if path.is_file()]

    def test_accepts_supported_signatures_with_server_extensions(self):
        cases = [
            ("image/jpeg", JPEG, ".jpg"),
            ("image/png", PNG, ".png"),
            ("image/webp", WEBP, ".webp"),
        ]
        for content_type, data, extension in cases:
            with self.subTest(content_type=content_type):
                url = local_storage_service.save(
                    upload("untrusted.exe", content_type, data),
                    folder="safe",
                )
                self.assertTrue(url.endswith(extension))

    def test_rejects_spoofed_and_disallowed_content_without_writing(self):
        cases = [
            ("image/jpeg", PNG),
            ("image/gif", b"GIF89a"),
            ("image/svg+xml", b"<svg></svg>"),
            ("image/png", b"MZ executable"),
        ]
        for content_type, data in cases:
            with self.subTest(content_type=content_type):
                with self.assertRaises(UnsupportedImageError):
                    local_storage_service.save(upload("x", content_type, data))
        self.assertEqual(self.saved_files(), [])

    def test_rejects_oversized_image_without_writing(self):
        data = b"\xff\xd8\xff" + b"x" * (MAX_IMAGE_BYTES - 2)
        with self.assertRaises(UploadTooLargeError):
            local_storage_service.save(upload("large.jpg", "image/jpeg", data))
        self.assertEqual(self.saved_files(), [])

    def test_storage_factory_defaults_to_local(self):
        self.assertIs(storage_factory.get_storage(), local_storage_service)


if __name__ == "__main__":
    unittest.main()
