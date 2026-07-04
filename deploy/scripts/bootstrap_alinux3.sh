#!/usr/bin/env bash
set -Eeuo pipefail

if [[ ${EUID} -ne 0 ]]; then
  echo "Run this script as root." >&2
  exit 1
fi

dnf install -y git python3.11 gcc nginx curl tar rsync sudo nodejs npm

if ! id giftai >/dev/null 2>&1; then
  useradd --system --home-dir /opt/gift_ai_enterprise --shell /sbin/nologin giftai
fi

install -d -o giftai -g giftai -m 0750 /opt/gift_ai_enterprise
install -d -o giftai -g giftai -m 0750 /opt/gift-ai-backups

if ! swapon --show=NAME --noheadings | grep -qx '/swapfile'; then
  if [[ ! -f /swapfile ]]; then
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
  fi
  swapon /swapfile
fi

if ! grep -qF '/swapfile none swap sw 0 0' /etc/fstab; then
  printf '%s\n' '/swapfile none swap sw 0 0' >> /etc/fstab
fi

systemctl enable nginx

echo "Bootstrap complete. Swap status:"
swapon --show
