# Internal Test Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy Gift AI Enterprise to Alibaba Cloud Linux 3 as an IP-restricted internal test service behind Nginx.

**Architecture:** Nginx listens on port 80 and proxies to one Uvicorn worker on `127.0.0.1:8000`. systemd runs the application as a dedicated `giftai` user from `/opt/gift_ai_enterprise/backend`; SQLite and uploads remain local and are backed up before updates.

**Tech Stack:** Alibaba Cloud Linux 3, Python 3, FastAPI/Uvicorn, systemd, Nginx, Git, SQLite.

---

### Task 1: Add deployment configuration tests

**Files:**
- Modify: `backend/tests/test_project_hygiene.py`
- Create later: `deploy/systemd/gift-ai.service`
- Create later: `deploy/nginx/gift-ai.conf`

- [ ] **Step 1: Write failing tests for service isolation and proxy boundaries**

Add tests that read both deployment templates and assert:

```python
def test_systemd_service_runs_unprivileged_on_loopback(self):
    service = (ROOT / "deploy/systemd/gift-ai.service").read_text()
    self.assertIn("User=giftai", service)
    self.assertIn("WorkingDirectory=/opt/gift_ai_enterprise/backend", service)
    self.assertIn("--host 127.0.0.1", service)
    self.assertIn("--workers 1", service)
    self.assertIn("EnvironmentFile=/opt/gift_ai_enterprise/backend/.env", service)

def test_nginx_only_proxies_to_loopback(self):
    nginx = (ROOT / "deploy/nginx/gift-ai.conf").read_text()
    self.assertIn("listen 80", nginx)
    self.assertIn("proxy_pass http://127.0.0.1:8000", nginx)
    self.assertIn("client_max_body_size 10m", nginx)
```

- [ ] **Step 2: Run tests and verify they fail because templates do not exist**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest tests.test_project_hygiene.ProjectHygieneTests -v`

Expected: ERROR with `FileNotFoundError` for deployment templates.

### Task 2: Create systemd and Nginx templates

**Files:**
- Create: `deploy/systemd/gift-ai.service`
- Create: `deploy/nginx/gift-ai.conf`

- [ ] **Step 1: Create the systemd unit**

```ini
[Unit]
Description=Gift AI Enterprise internal test API
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=giftai
Group=giftai
WorkingDirectory=/opt/gift_ai_enterprise/backend
EnvironmentFile=/opt/gift_ai_enterprise/backend/.env
ExecStart=/opt/gift_ai_enterprise/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1 --proxy-headers
Restart=on-failure
RestartSec=5
TimeoutStopSec=30
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ReadWritePaths=/opt/gift_ai_enterprise/backend /opt/gift_ai_enterprise/uploads

[Install]
WantedBy=multi-user.target
```

- [ ] **Step 2: Create the Nginx site configuration**

```nginx
server {
    listen 80 default_server;
    server_name _;
    client_max_body_size 10m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 5s;
        proxy_read_timeout 120s;
    }
}
```

- [ ] **Step 3: Re-run deployment configuration tests**

Expected: both new tests PASS.

### Task 3: Create a safe server bootstrap script

**Files:**
- Create: `deploy/scripts/bootstrap_alinux3.sh`

- [ ] **Step 1: Implement idempotent package, user, directory, and Swap setup**

The script must:

- require root;
- install `git`, `python3`, `python3-pip`, `python3-devel`, `gcc`, and `nginx` with `dnf`;
- create the system user `giftai` only if absent;
- create `/opt/gift_ai_enterprise` owned by `giftai`;
- create `/swapfile` at 2 GiB only when no Swap exists;
- add `/swapfile none swap sw 0 0` to `/etc/fstab` only once;
- enable Nginx but not expose Uvicorn.

- [ ] **Step 2: Validate shell syntax locally**

Run under Git Bash or WSL: `bash -n deploy/scripts/bootstrap_alinux3.sh`

Expected: exit code 0.

### Task 4: Create deployment and rollback scripts

**Files:**
- Create: `deploy/scripts/deploy_internal.sh`
- Create: `deploy/scripts/rollback_internal.sh`

- [ ] **Step 1: Implement deployment preconditions**

`deploy_internal.sh` must require root, require `/opt/gift_ai_enterprise/backend/.env`, verify `.env` mode is `600`, and refuse to continue if `DEBUG=true`.

- [ ] **Step 2: Implement backup and update**

Before updating, create a timestamped backup under `/opt/gift-ai-backups/` containing existing `backend/gift_ai.db` and `uploads/`. Fetch the requested Git ref, create or reuse `.venv`, install `requirements.txt`, run `pip check`, compile the app, initialize missing tables, and run all tests.

- [ ] **Step 3: Install and validate services**

Copy the systemd unit and Nginx config, run `systemctl daemon-reload`, `nginx -t`, enable/restart both services, then poll `http://127.0.0.1/health` until it returns success.

- [ ] **Step 4: Implement rollback**

`rollback_internal.sh` must require an explicit Git commit argument, back up current data, check out that commit, reinstall locked requirements, run tests, and restart the service. It must not restore or delete database files automatically.

- [ ] **Step 5: Validate script syntax**

Run: `bash -n deploy/scripts/deploy_internal.sh deploy/scripts/rollback_internal.sh`

Expected: exit code 0.

### Task 5: Add environment and operator documentation

**Files:**
- Create: `deploy/internal.env.example`
- Create: `deploy/README.md`

- [ ] **Step 1: Add a production-safe environment template**

Include variable names and safe placeholders only:

```dotenv
APP_NAME=Gift AI Enterprise Internal Test
APP_VERSION=2.0.0
DEBUG=false
DATABASE_URL=sqlite:///./gift_ai.db
SECRET_KEY=replace-on-server
UPLOAD_DIR=uploads
UPLOAD_URL_PREFIX=/uploads
DEEPSEEK_API_KEY=
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
AI_CACHE_ENABLED=false
```

- [ ] **Step 2: Document the exact operator flow**

Document SSH connection, security-group prerequisites, bootstrap, repository checkout, server-side `.env` creation, deploy, health verification, logs, backup location, rollback, and reboot verification. Never include a real IP, secret, password, or private-key path.

### Task 6: Run local verification and publish deployment files

**Files:**
- Review all deployment and test files.

- [ ] **Step 1: Run complete local checks**

Run:

```powershell
.\.venv\Scripts\python.exe -m compileall -q backend\app
Push-Location backend
..\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_*.py' -v
Pop-Location
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

Expected: compile succeeds, all tests PASS, dependencies are consistent, and diff check is clean.

- [ ] **Step 2: Commit and push deployment configuration**

Commit the deployment files and tests to `codex/project-stability`, then push so PR #1 includes the internal-test deployment artifacts.

### Task 7: Establish SSH trust and inspect the server

**Files:**
- No repository changes.

- [ ] **Step 1: Obtain non-secret connection facts from the user**

Required: public IP, SSH username, and whether login uses a bound SSH key or password. Never request the private key contents or password.

- [ ] **Step 2: Connect interactively and verify the host key fingerprint**

Run: `ssh root@SERVER_IP` or the confirmed username. The user must compare the first-connection fingerprint with the ECS console before accepting it.

- [ ] **Step 3: Inspect resources**

Run:

```bash
cat /etc/os-release
uname -m
nproc
free -h
df -h /
ss -lntup
```

Expected: Alibaba Cloud Linux 3, x86_64, 2 CPUs, about 2 GiB RAM, and no unexpected public listeners.

### Task 8: Bootstrap and deploy internal testing

**Files:**
- Remote server state under `/opt`, `/etc/systemd/system`, and `/etc/nginx`.

- [ ] **Step 1: Transfer or fetch the reviewed deployment scripts**

Use the GitHub branch after Task 6 is pushed. Do not copy local `.env`, SQLite data, uploads, or private keys.

- [ ] **Step 2: Run bootstrap as root**

Expected: packages installed, `giftai` user created, 2 GiB Swap active, Nginx enabled.

- [ ] **Step 3: Create server `.env` interactively**

Generate `SECRET_KEY` on the server, set `DEBUG=false`, set mode `600`, and assign ownership to `giftai:giftai`. Do not print the secret back into chat.

- [ ] **Step 4: Run deployment for `codex/project-stability`**

Expected: tests pass, missing tables initialize, systemd and Nginx become active, and local health returns HTTP 200.

- [ ] **Step 5: Verify from the authorized client IP**

Check `/health`, `/openapi.json`, `/api/gifts/`, `/api/categories/`, and `/api/brands/`. Verify direct access to port 8000 fails.

- [ ] **Step 6: Reboot verification**

Reboot once, reconnect, and require Nginx and `gift-ai` to return active with health HTTP 200 before declaring the internal environment ready.
