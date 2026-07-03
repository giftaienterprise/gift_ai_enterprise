import subprocess
import sys
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
                sys.executable,
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

    def test_systemd_service_runs_unprivileged_on_loopback(self):
        service = (ROOT / "deploy/systemd/gift-ai.service").read_text()
        self.assertIn("User=giftai", service)
        self.assertIn(
            "WorkingDirectory=/opt/gift_ai_enterprise/backend",
            service,
        )
        self.assertIn("--host 127.0.0.1", service)
        self.assertIn("--workers 1", service)
        self.assertIn(
            "EnvironmentFile=/opt/gift_ai_enterprise/backend/.env",
            service,
        )

    def test_nginx_only_proxies_to_loopback(self):
        nginx = (ROOT / "deploy/nginx/gift-ai.conf").read_text()
        self.assertIn("listen 80", nginx)
        self.assertIn("proxy_pass http://127.0.0.1:8000", nginx)
        self.assertIn("client_max_body_size 10m", nginx)

    def test_alinux_deployment_uses_python311_without_replacing_system_python(self):
        bootstrap = (ROOT / "deploy/scripts/bootstrap_alinux3.sh").read_text()
        deploy = (ROOT / "deploy/scripts/deploy_internal.sh").read_text()
        self.assertIn("python3.11", bootstrap)
        self.assertIn("python3.11 -m venv", deploy)
        self.assertNotIn("alternatives", bootstrap)
        self.assertNotIn("/usr/local/bin/python3", bootstrap)


if __name__ == "__main__":
    unittest.main()
