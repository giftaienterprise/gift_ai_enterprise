# Remote fix for Gift AI static sites on ECS.
# Requires SSH key at $env:USERPROFILE\.ssh\gift_ai_ecs

$ErrorActionPreference = "Stop"

$Server = "112.125.89.10"
$User = "root"
$Key = Join-Path $env:USERPROFILE ".ssh\gift_ai_ecs"
$RemoteScript = "/opt/gift_ai_enterprise/deploy/scripts/publish_static_local.sh"

if (-not (Test-Path $Key)) {
  Write-Error "Missing SSH key: $Key. Run deploy\scripts\setup_local_ssh.ps1 first."
}

$sshArgs = @(
  "-i", $Key,
  "-o", "StrictHostKeyChecking=accept-new",
  "-o", "BatchMode=yes",
  "${User}@${Server}"
)

Write-Host "Publishing static sites on $Server ..."
ssh @sshArgs "bash $RemoteScript"
if ($LASTEXITCODE -ne 0) {
  Write-Error "Publish failed. Ensure the public key is installed on the server."
}

Write-Host "Creating admin account (skip if already exists) ..."
ssh @sshArgs @"
sudo -u giftai bash -c 'cd /opt/gift_ai_enterprise/backend && PYTHONPATH=/opt/gift_ai_enterprise/backend /opt/gift_ai_enterprise/.venv/bin/python scripts/create_admin.py admin --password 1235678Ab' || true
"@

Write-Host "Verification:"
ssh @sshArgs "curl -s -o /dev/null -w 'health=%{http_code} home=%{http_code} admin=%{http_code}\n' http://127.0.0.1/health http://127.0.0.1/ http://127.0.0.1/admin/"
Write-Host "Done. Storefront: http://${Server}/  Admin: http://${Server}/admin/"
