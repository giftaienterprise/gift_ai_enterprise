#!/usr/bin/env bash
# Publish already-built frontend/admin dist/ into nginx releases/.
set -Eeuo pipefail

APP_DIR=/opt/gift_ai_enterprise
RELEASE_ID=$(date -u +%Y%m%dT%H%M%SZ)

if [[ ! -f "$APP_DIR/frontend/dist/index.html" || ! -f "$APP_DIR/admin/dist/index.html" ]]; then
  echo "Build output missing. Run frontend/admin npm run build first." >&2
  exit 1
fi

mkdir -p "$APP_DIR/releases/storefront/$RELEASE_ID"
mkdir -p "$APP_DIR/releases/admin/$RELEASE_ID"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$APP_DIR/frontend/dist/" "$APP_DIR/releases/storefront/$RELEASE_ID/"
  rsync -a --delete "$APP_DIR/admin/dist/" "$APP_DIR/releases/admin/$RELEASE_ID/"
else
  cp -a "$APP_DIR/frontend/dist/." "$APP_DIR/releases/storefront/$RELEASE_ID/"
  cp -a "$APP_DIR/admin/dist/." "$APP_DIR/releases/admin/$RELEASE_ID/"
fi

ln -sfn "$APP_DIR/releases/storefront/$RELEASE_ID" "$APP_DIR/releases/storefront/current"
ln -sfn "$APP_DIR/releases/admin/$RELEASE_ID" "$APP_DIR/releases/admin/current"
chown -R giftai:giftai "$APP_DIR/releases"

chmod o+x "$APP_DIR" "$APP_DIR/releases" "$APP_DIR/releases/storefront" "$APP_DIR/releases/admin"
find "$APP_DIR/releases/storefront" -type d -exec chmod o+rx {} \;
find "$APP_DIR/releases/storefront" -type f -exec chmod o+r {} \;
find "$APP_DIR/releases/admin" -type d -exec chmod o+rx {} \;
find "$APP_DIR/releases/admin" -type f -exec chmod o+r {} \;

nginx -t
systemctl reload nginx

echo "storefront index: $(ls -la "$APP_DIR/releases/storefront/current/index.html")"
echo "admin index: $(ls -la "$APP_DIR/releases/admin/current/index.html")"
echo "home=$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1/)"
echo "admin=$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1/admin/)"
