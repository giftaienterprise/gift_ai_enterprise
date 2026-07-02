import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ProjectHygieneTests(unittest.TestCase):
    def test_local_artifacts_are_ignored(self):
        candidates = [
            ".venv/Scripts/python.exe",
            "backend/app/__pycache__/main.pyc",
            "backend/gift_ai.db",
            "backend/.env",
            "uploads/example.png",
            ".pytest_cache/state",
            ".ruff_cache/state",
        ]
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "-z", "--stdin"],
            cwd=ROOT,
            input=("\0".join(candidates) + "\0").encode(),
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        ignored = {item.decode() for item in result.stdout.split(b"\0") if item}
        self.assertEqual(ignored, set(candidates))

    def test_tool_package_import_is_silent(self):
        result = subprocess.run(
            [
                str(ROOT / ".venv" / "Scripts" / "python.exe"),
                "-c",
                "import app.services.ai.tools.init",
            ],
            cwd=ROOT / "backend",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
