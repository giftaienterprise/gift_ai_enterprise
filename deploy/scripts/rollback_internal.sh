#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR=/opt/gift_ai_enterprise
BACKUP_DIR=/opt/gift-ai-backups
COMMIT=${1:-}

if [[ ${EUID} -ne 0 ]]; then
  echo "Run this script as root." >&2
  exit 1
fi

if [[ -z "$COMMIT" ]]; then
  echo "Usage: $0 <verified-git-commit>" >&2
  exit 1
fi

sudo -u giftai git -C "$APP_DIR" cat-file -e "$COMMIT^{commit}"
timestamp=$(date -u +%Y%m%dT%H%M%SZ)-rollback
install -d -o giftai -g giftai -m 0750 "$BACKUP_DIR/$timestamp"
for path in backend/gift_ai.db backend/uploads uploads; do
  if [[ -e "$APP_DIR/$path" ]]; then
    tar -C "$APP_DIR" -czf "$BACKUP_DIR/$timestamp/${path//\//_}.tar.gz" "$path"
  fi
done

sudo -u giftai git -C "$APP_DIR" checkout --detach "$COMMIT"
sudo -u giftai "$APP_DIR/.venv/bin/python" -m pip install -r "$APP_DIR/requirements.txt"
sudo -u giftai "$APP_DIR/.venv/bin/python" -m pip check
sudo -u giftai bash -c "cd '$APP_DIR/backend' && ../.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v"
systemctl restart gift-ai
curl --fail --silent --show-error http://127.0.0.1/health >/dev/null
echo "Rollback complete at commit $(git -C "$APP_DIR" rev-parse HEAD). Data was not restored or deleted."
