# Internal Test Deployment

This deployment targets Alibaba Cloud Linux 3 on a 2 vCPU, 2 GiB ECS instance.

## Before connecting

Configure the ECS security group:

- TCP 22: allow only the administrator public IP.
- TCP 80: allow only internal tester public IPs.
- Do not expose 8000, 3306, 5432, or 6379.

Verify the SSH host-key fingerprint against the ECS console before accepting it.

## 1. Inspect the server

```bash
cat /etc/os-release
uname -m
nproc
free -h
df -h /
ss -lntup
```

Expected: Alibaba Cloud Linux 3, x86_64, 2 CPUs, about 2 GiB RAM, and no unexpected listeners.

## 2. Bootstrap

Clone the reviewed branch, then run the bootstrap script as root:

```bash
dnf install -y git
git clone --branch codex/project-stability https://github.com/giftaienterprise/gift_ai_enterprise.git /opt/gift_ai_enterprise
bash /opt/gift_ai_enterprise/deploy/scripts/bootstrap_alinux3.sh
chown -R giftai:giftai /opt/gift_ai_enterprise
python3.11 --version
```

## 3. Create the server environment

Create `/opt/gift_ai_enterprise/backend/.env` directly on the server. Start from `deploy/internal.env.example`, replace `SECRET_KEY` with a random value generated on the server, and add the DeepSeek key only when AI integration testing is required.

```bash
cp /opt/gift_ai_enterprise/deploy/internal.env.example /opt/gift_ai_enterprise/backend/.env
python3 -c "from pathlib import Path; import secrets; p=Path('/opt/gift_ai_enterprise/backend/.env'); p.write_text(p.read_text().replace('replace-on-server', secrets.token_urlsafe(48)))"
chown giftai:giftai /opt/gift_ai_enterprise/backend/.env
chmod 600 /opt/gift_ai_enterprise/backend/.env
```

Never copy the resulting file into Git, logs, screenshots, or chat.

## 4. Deploy

```bash
bash /opt/gift_ai_enterprise/deploy/scripts/deploy_internal.sh codex/project-stability
```

## 5. Verify

```bash
systemctl is-active gift-ai nginx
nginx -t
curl --fail http://127.0.0.1:8000/health
curl --fail http://127.0.0.1/health
journalctl -u gift-ai --no-pager -n 50
```

From an IP allowed by the security group, verify:

```text
http://SERVER_IP/health
http://SERVER_IP/openapi.json
http://SERVER_IP/api/gifts/
http://SERVER_IP/api/categories/
http://SERVER_IP/api/brands/
```

Direct access to `http://SERVER_IP:8000` must fail.

## 6. Reboot verification

```bash
reboot
```

After reconnecting:

```bash
systemctl is-active gift-ai nginx
curl --fail http://127.0.0.1/health
swapon --show
```

## Logs and backups

```bash
journalctl -u gift-ai -f
ls -la /opt/gift-ai-backups
```

The deployment script creates timestamped data backups before changing code.

## Rollback

Choose a previously verified commit. Rollback does not overwrite or delete the database automatically.

```bash
bash /opt/gift_ai_enterprise/deploy/scripts/rollback_internal.sh VERIFIED_COMMIT
```
