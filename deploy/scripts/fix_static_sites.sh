#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR=/opt/gift_ai_enterprise
STOREFRONT_CURRENT="$APP_DIR/releases/storefront/current"
ADMIN_CURRENT="$APP_DIR/releases/admin/current"

if [[ ${EUID} -ne 0 ]]; then
  echo "Run this script as root." >&2
  exit 1
fi

# shellcheck source=lib/sync_static.sh
source "$APP_DIR/deploy/scripts/lib/sync_static.sh"

ensure_static_release() {
  local name=$1
  local source_dir=$2
  local target_root=$3
  local current_link="$target_root/current"

  if [[ ! -f "$source_dir/index.html" ]]; then
    echo "Missing build output: $source_dir/index.html" >&2
    return 1
  fi

  if [[ ! -f "$current_link/index.html" ]]; then
    release_id=$(date -u +%Y%m%dT%H%M%SZ)
    release_dir="$target_root/$release_id"
    install -d -o giftai -g giftai -m 0755 "$release_dir"
    sync_release_dir "$source_dir" "$release_dir"
    ln -sfn "$release_dir" "$current_link"
    echo "Published $name release: $release_dir"
  fi
}

make_static_readable() {
  chmod o+x "$APP_DIR"
  chmod o+x "$APP_DIR/releases"
  chmod o+x "$APP_DIR/releases/storefront"
  chmod o+x "$APP_DIR/releases/admin"
  find "$APP_DIR/releases/storefront" -type d -exec chmod o+rx {} \;
  find "$APP_DIR/releases/storefront" -type f -exec chmod o+r {} \;
  find "$APP_DIR/releases/admin" -type d -exec chmod o+rx {} \;
  find "$APP_DIR/releases/admin" -type f -exec chmod o+r {} \;
}

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is not installed. Run bootstrap_alinux3.sh first." >&2
  exit 1
fi

if [[ ! -f "$STOREFRONT_CURRENT/index.html" || ! -f "$ADMIN_CURRENT/index.html" ]]; then
  echo "Static releases missing; building frontend and admin..."
  install -d -o giftai -g giftai -m 0755 "$APP_DIR/releases/storefront" "$APP_DIR/releases/admin"
  sudo -u giftai bash -c "cd '$APP_DIR/frontend' && npm ci && npm run build"
  sudo -u giftai bash -c "cd '$APP_DIR/admin' && npm ci && npm run build"
  ensure_static_release "storefront" "$APP_DIR/frontend/dist" "$APP_DIR/releases/storefront"
  ensure_static_release "admin" "$APP_DIR/admin/dist" "$APP_DIR/releases/admin"
fi

if [[ ! -f "$STOREFRONT_CURRENT/index.html" || ! -f "$ADMIN_CURRENT/index.html" ]]; then
  echo "Static site files are still missing after build." >&2
  exit 1
fi

make_static_readable

if ! sudo -u nginx test -r "$STOREFRONT_CURRENT/index.html"; then
  echo "nginx user still cannot read storefront index.html" >&2
  ls -la "$STOREFRONT_CURRENT/index.html" >&2
  exit 1
fi

if ! sudo -u nginx test -r "$ADMIN_CURRENT/index.html"; then
  echo "nginx user still cannot read admin index.html" >&2
  ls -la "$ADMIN_CURRENT/index.html" >&2
  exit 1
fi

install -o root -g root -m 0644 "$APP_DIR/deploy/nginx/gift-ai.conf" /etc/nginx/conf.d/gift-ai.conf
nginx -t
systemctl reload nginx

echo "Storefront: $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1/)"
echo "Admin: $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1/admin/)"
echo "Static sites repaired."
