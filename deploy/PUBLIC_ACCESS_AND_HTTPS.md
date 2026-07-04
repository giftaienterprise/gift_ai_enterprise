# Public Access and HTTPS

This guide covers opening the site to mobile/public users and enabling HTTPS on Alibaba Cloud ECS.

Replace placeholders:

- `112.125.89.10` — current ECS public IP
- `example.com` — your domain
- `YOUR_ADMIN_IP/32` — your office/home public IP for SSH

## Part 1: Security group (fix mobile access)

### 1.1 Open the Alibaba Cloud console

1. Go to **ECS** → **Instances**
2. Select instance `iZ2zegkwsojyx1s4j79styZ`
3. Open the **Security Group** tab → click the linked security group
4. Choose **Inbound Rules** → **Manual Add**

### 1.2 Recommended inbound rules

| Priority | Protocol | Port | Source | Purpose |
|----------|----------|------|--------|---------|
| 1 | TCP | 22 | `YOUR_ADMIN_IP/32` | SSH (admin only) |
| 1 | TCP | 80 | `0.0.0.0/0` | HTTP storefront/admin/API |
| 1 | TCP | 443 | `0.0.0.0/0` | HTTPS (after Part 2) |

Do **not** open: `8000`, `3306`, `5432`, `6379`.

### 1.3 Verify from a phone (mobile data, not Wi‑Fi)

```text
http://112.125.89.10/health
```

Expected: `{"status":"healthy"}`

Then open:

```text
http://112.125.89.10/
http://112.125.89.10/admin/
```

### 1.4 Optional: allow one phone IP only (testing)

1. On the phone, visit https://ip.cn/ and note the public IP
2. Add inbound rule: TCP 80 → `PHONE_IP/32`
3. Remove `0.0.0.0/0` on port 80 if you do not want full public access yet

---

## Part 2: Domain and HTTPS

HTTPS requires a domain. IP-only Let's Encrypt certificates are not supported.

### 2.1 Point DNS to the ECS IP

At your domain registrar or Alibaba Cloud DNS:

| Type | Host | Value |
|------|------|-------|
| A | `@` | `112.125.89.10` |
| A | `www` | `112.125.89.10` |

Wait until DNS resolves:

```bash
ping example.com
```

### 2.2 Update Nginx `server_name`

On the ECS, edit `/etc/nginx/conf.d/gift-ai.conf`:

```nginx
server_name example.com www.example.com;
```

Or install from the repo after updating `deploy/nginx/gift-ai.conf`, then:

```bash
nginx -t && systemctl reload nginx
```

### 2.3 Install Certbot (Alibaba Cloud Linux 3)

```bash
dnf install -y certbot python3-certbot-nginx
```

Ensure port 80 is reachable from the internet before running Certbot.

### 2.4 Issue certificate and configure Nginx

```bash
certbot --nginx \
  -d example.com \
  -d www.example.com \
  --email your-email@example.com \
  --agree-tos \
  --no-eff-email \
  --redirect
```

Certbot will:

- Obtain a Let's Encrypt certificate
- Add a `listen 443 ssl` server block
- Redirect HTTP → HTTPS

### 2.5 Confirm security group allows 443

Add inbound rule **TCP 443 → 0.0.0.0/0** if not already present.

### 2.6 Verify HTTPS

```bash
curl -I https://example.com/
curl -I https://example.com/admin/
curl -I https://example.com/health
```

From a phone:

```text
https://example.com/
```

### 2.7 Auto-renewal

```bash
systemctl enable --now certbot-renew.timer
certbot renew --dry-run
```

---

## Part 3: Post-go-live security checklist

- [ ] Change default admin password (`admin` / initial password)
- [ ] Confirm `backend/.env` uses a unique random `SECRET_KEY`
- [ ] Keep SSH (22) restricted to admin IP only
- [ ] Do not expose port 8000 publicly
- [ ] Configure contact info in admin **Settings**
- [ ] Add `DEEPSEEK_API_KEY` in `.env` if AI advisor is required

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Phone timeout, PC works | Security group blocks phone IP | Open 80 to `0.0.0.0/0` or add phone IP |
| `500` on `/` or `/admin/` | Static files not published | Run `bash deploy/scripts/publish_static_local.sh` |
| Certbot fails | DNS not pointing to ECS | Fix A record, wait for propagation |
| WeChat browser warning | HTTP without SSL | Complete Part 2 (HTTPS) |
| `403` on static pages | Nginx cannot read releases | Re-run publish script (sets permissions) |

---

## Aliyun documentation

- Security group rules: https://help.aliyun.com/document_detail/416274.html
- DNS A record: Alibaba Cloud DNS console
- Free SSL (alternative): Alibaba Cloud **SSL Certificates** service
