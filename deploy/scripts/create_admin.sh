#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR=/opt/gift_ai_enterprise
BACKEND_DIR="$APP_DIR/backend"
PYTHON="$APP_DIR/.venv/bin/python"

if [[ ${EUID} -ne 0 ]]; then
  echo "Run this script as root." >&2
  exit 1
fi

if [[ ! -x "$PYTHON" ]]; then
  echo "Virtual environment is missing at $APP_DIR/.venv." >&2
  exit 1
fi

if [[ ! -f "$BACKEND_DIR/.env" ]]; then
  echo "Environment file is missing: $BACKEND_DIR/.env" >&2
  exit 1
fi

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 USERNAME [--promote-only] [--password PASSWORD]" >&2
  exit 1
fi

sudo -u giftai bash -c "cd '$BACKEND_DIR' && '$PYTHON' scripts/create_admin.py $*"
