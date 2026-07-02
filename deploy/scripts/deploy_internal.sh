#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR=/opt/gift_ai_enterprise
BACKUP_DIR=/opt/gift-ai-backups
ENV_FILE="$APP_DIR/backend/.env"
REF=${1:-codex/project-stability}

if [[ ${EUID} -ne 0 ]]; then
  echo "Run this script as root." >&2
  exit 1
fi

if [[ ! -d "$APP_DIR/.git" ]]; then
  echo "Repository is missing at $APP_DIR." >&2
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Environment file is missing: $ENV_FILE" >&2
  exit 1
fi

if [[ $(stat -c '%a' "$ENV_FILE") != 600 ]]; then
  echo "$ENV_FILE must have mode 600." >&2
  exit 1
fi

if grep -Eiq '^DEBUG=(true|1|yes)$' "$ENV_FILE"; then
  echo "Refusing to deploy with DEBUG enabled." >&2
  exit 1
fi

timestamp=$(date -u +%Y%m%dT%H%M%SZ)
install -d -o giftai -g giftai -m 0750 "$BACKUP_DIR/$timestamp"
for path in backend/gift_ai.db backend/uploads uploads; do
  if [[ -e "$APP_DIR/$path" ]]; then
    tar -C "$APP_DIR" -czf "$BACKUP_DIR/$timestamp/${path//\//_}.tar.gz" "$path"
  fi
done

sudo -u giftai git -C "$APP_DIR" fetch --prune origin
if sudo -u giftai git -C "$APP_DIR" show-ref --verify --quiet "refs/remotes/origin/$REF"; then
  sudo -u giftai git -C "$APP_DIR" checkout -B internal-deploy "origin/$REF"
else
  sudo -u giftai git -C "$APP_DIR" checkout --detach "$REF"
fi

if [[ ! -x "$APP_DIR/.venv/bin/python" ]]; then
  sudo -u giftai python3 -m venv "$APP_DIR/.venv"
fi

sudo -u giftai "$APP_DIR/.venv/bin/python" -m pip install --upgrade pip
sudo -u giftai "$APP_DIR/.venv/bin/python" -m pip install -r "$APP_DIR/requirements.txt"
sudo -u giftai "$APP_DIR/.venv/bin/python" -m pip check
sudo -u giftai "$APP_DIR/.venv/bin/python" -m compileall -q "$APP_DIR/backend/app"
sudo -u giftai bash -c "cd '$APP_DIR/backend' && ../.venv/bin/python init_db.py"
sudo -u giftai bash -c "cd '$APP_DIR/backend' && ../.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v"

install -o root -g root -m 0644 "$APP_DIR/deploy/systemd/gift-ai.service" /etc/systemd/system/gift-ai.service
install -o root -g root -m 0644 "$APP_DIR/deploy/nginx/gift-ai.conf" /etc/nginx/conf.d/gift-ai.conf
systemctl daemon-reload
nginx -t
systemctl enable --now nginx
systemctl enable gift-ai
systemctl restart gift-ai
systemctl reload nginx

for _ in {1..30}; do
  if curl --fail --silent --show-error http://127.0.0.1/health >/dev/null; then
    echo "Deployment healthy at commit $(git -C "$APP_DIR" rev-parse HEAD)."
    exit 0
  fi
  sleep 1
done

echo "Health check failed." >&2
journalctl -u gift-ai --no-pager -n 50 >&2
exit 1
