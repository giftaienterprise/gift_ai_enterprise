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
  sudo -u giftai python3.11 -m venv "$APP_DIR/.venv"
fi

sudo -u giftai "$APP_DIR/.venv/bin/python" -m pip install --upgrade pip
sudo -u giftai "$APP_DIR/.venv/bin/python" -m pip install -r "$APP_DIR/requirements.txt"
sudo -u giftai "$APP_DIR/.venv/bin/python" -m pip check
sudo -u giftai "$APP_DIR/.venv/bin/python" -m compileall -q "$APP_DIR/backend/app"
sudo -u giftai bash -c "cd '$APP_DIR/backend' && ../.venv/bin/python init_db.py"
sudo -u giftai bash -c "cd '$APP_DIR/backend' && ../.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v"

# shellcheck source=lib/sync_static.sh
source "$APP_DIR/deploy/scripts/lib/sync_static.sh"

if command -v npm >/dev/null 2>&1; then
  release_id=$(date -u +%Y%m%dT%H%M%SZ)
  storefront_release="$APP_DIR/releases/storefront/$release_id"
  admin_release="$APP_DIR/releases/admin/$release_id"
  install -d -o giftai -g giftai -m 0755 "$APP_DIR/releases/storefront" "$APP_DIR/releases/admin"
  install -d -o giftai -g giftai -m 0755 "$storefront_release" "$admin_release"

  sudo -u giftai bash -c "cd '$APP_DIR/frontend' && npm ci && npm run build"
  sudo -u giftai bash -c "cd '$APP_DIR/admin' && npm ci && npm run build"

  sync_release_dir "$APP_DIR/frontend/dist" "$storefront_release"
  sync_release_dir "$APP_DIR/admin/dist" "$admin_release"
  chown -R giftai:giftai "$APP_DIR/releases"

  ln -sfn "$storefront_release" "$APP_DIR/releases/storefront/current"
  ln -sfn "$admin_release" "$APP_DIR/releases/admin/current"

  chmod o+x "$APP_DIR"
  chmod o+x "$APP_DIR/releases"
  chmod o+x "$APP_DIR/releases/storefront"
  chmod o+x "$APP_DIR/releases/admin"
  find "$APP_DIR/releases/storefront" -type d -exec chmod o+rx {} \;
  find "$APP_DIR/releases/storefront" -type f -exec chmod o+r {} \;
  find "$APP_DIR/releases/admin" -type d -exec chmod o+rx {} \;
  find "$APP_DIR/releases/admin" -type f -exec chmod o+r {} \;

  if [[ ! -f "$APP_DIR/releases/storefront/current/index.html" ]]; then
    echo "Storefront build is missing index.html." >&2
    exit 1
  fi
  if [[ ! -f "$APP_DIR/releases/admin/current/index.html" ]]; then
    echo "Admin build is missing index.html." >&2
    exit 1
  fi
  if ! sudo -u nginx test -r "$APP_DIR/releases/storefront/current/index.html"; then
    echo "nginx cannot read storefront static files." >&2
    exit 1
  fi
else
  echo "npm is not installed; frontend and admin cannot be deployed." >&2
  exit 1
fi

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
    deployed_commit=$(sudo -u giftai git -C "$APP_DIR" rev-parse HEAD)
    echo "Deployment healthy at commit $deployed_commit."
    exit 0
  fi
  sleep 1
done

echo "Health check failed." >&2
journalctl -u gift-ai --no-pager -n 50 >&2
exit 1
