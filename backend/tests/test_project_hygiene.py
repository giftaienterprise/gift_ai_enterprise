import os
import subprocess
import sys
import tempfile
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

    def test_app_creates_missing_upload_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env = os.environ.copy()
            env.update(
                DATABASE_URL="sqlite:///./test.db",
                SECRET_KEY="test-secret",
                PYTHONPATH=str(ROOT / "backend"),
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    (
                        "from pathlib import Path; "
                        "import app.main; "
                        "assert Path('uploads').is_dir()"
                    ),
                ],
                cwd=temp_dir,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)

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
        read_write_paths = next(
            line for line in service.splitlines()
            if line.startswith("ReadWritePaths=")
        )
        self.assertEqual(
            read_write_paths,
            "ReadWritePaths=/opt/gift_ai_enterprise/backend",
        )

    def test_nginx_serves_frontends_and_proxies_api(self):
        nginx = (ROOT / "deploy/nginx/gift-ai.conf").read_text()
        self.assertIn("listen 80", nginx)
        self.assertIn("server_name 112.125.89.10", nginx)
        self.assertIn("releases/storefront/current", nginx)
        self.assertIn("location ^~ /admin/", nginx)
        self.assertIn("releases/admin/current", nginx)
        self.assertIn("location /api/", nginx)
        self.assertIn("proxy_pass http://127.0.0.1:8000/api/", nginx)
        self.assertIn("location /uploads/", nginx)
        self.assertIn("try_files $uri $uri/ /index.html", nginx)
        self.assertIn("return 301 /admin/", nginx)
        self.assertNotIn(":8000;", nginx)

    def test_deploy_script_publishes_readable_static_files(self):
        deploy = (ROOT / "deploy/scripts/deploy_internal.sh").read_text()
        fix = (ROOT / "deploy/scripts/fix_static_sites.sh").read_text()
        self.assertIn("chmod o+x", deploy)
        self.assertIn("nginx cannot read storefront static files", deploy)
        self.assertIn("make_static_readable", fix)

    def test_deploy_script_builds_frontends_when_npm_available(self):
        deploy = (ROOT / "deploy/scripts/deploy_internal.sh").read_text()
        self.assertIn("npm ci", deploy)
        self.assertIn("sync_release_dir", deploy)
        self.assertIn("frontend/dist", deploy)
        self.assertIn("admin/dist", deploy)

    def test_alinux_deployment_uses_python311_without_replacing_system_python(self):
        bootstrap = (ROOT / "deploy/scripts/bootstrap_alinux3.sh").read_text()
        deploy = (ROOT / "deploy/scripts/deploy_internal.sh").read_text()
        self.assertIn("python3.11", bootstrap)
        self.assertIn("rsync", bootstrap)
        self.assertIn("python3.11 -m venv", deploy)
        self.assertIn(
            'sudo -u giftai git -C "$APP_DIR" rev-parse HEAD',
            deploy,
        )
        self.assertNotIn("alternatives", bootstrap)
        self.assertNotIn("/usr/local/bin/python3", bootstrap)

    def test_create_admin_script_exists(self):
        script = ROOT / "backend/scripts/create_admin.py"
        wrapper = ROOT / "deploy/scripts/create_admin.sh"
        self.assertTrue(script.is_file())
        self.assertTrue(wrapper.is_file())
        self.assertIn("create_admin.py", wrapper.read_text())

    def test_backend_ci_matches_deployment_checks(self):
        workflow = (ROOT / ".github/workflows/backend-tests.yml").read_text()
        self.assertIn("pull_request:", workflow)
        self.assertIn("master", workflow)
        self.assertIn("codex/**", workflow)
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("uses: actions/checkout@v6", workflow)
        self.assertIn("uses: actions/setup-python@v6", workflow)
        self.assertIn("python-version: '3.11'", workflow)
        self.assertIn("cache: pip", workflow)
        self.assertIn("python -m pip check", workflow)
        self.assertIn("python -m compileall -q app", workflow)
        self.assertIn(
            "python -m unittest discover -s tests -p 'test_*.py' -v",
            workflow,
        )
        self.assertIn("DATABASE_URL: sqlite:///./ci.db", workflow)
        self.assertIn("SECRET_KEY: ci-only-secret", workflow)


if __name__ == "__main__":
    unittest.main()
