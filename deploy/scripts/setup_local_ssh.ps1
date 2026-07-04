# One-time local SSH setup for Gift AI ECS deployment.

$ErrorActionPreference = "Stop"

$Key = Join-Path $env:USERPROFILE ".ssh\gift_ai_ecs"
$Pub = "$Key.pub"
$Server = "112.125.89.10"
$User = "root"

if (-not (Test-Path (Split-Path $Key))) {
  New-Item -ItemType Directory -Path (Split-Path $Key) | Out-Null
}

if (-not (Test-Path $Key)) {
  ssh-keygen -t ed25519 -f $Key -N '""' -C "gift-ai-deploy"
}

Write-Host ""
Write-Host "=== Step 1: Add this public key on the ECS (Aliyun Workbench) ==="
Write-Host ""
Get-Content $Pub
Write-Host ""
Write-Host "Run on ECS as root:"
Write-Host ""
Write-Host @"
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo '$(Get-Content $Pub -Raw).Trim()' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
"@
Write-Host ""
Write-Host "=== Step 2: Test from this PC ==="
Write-Host "ssh -i `"$Key`" ${User}@${Server} echo ok"
Write-Host ""
Write-Host "=== Step 3: Run remote fix ==="
Write-Host "powershell -ExecutionPolicy Bypass -File deploy\scripts\remote_fix.ps1"
