Clear-Host
# CKS HANDSOFF BOOTSTRAP
# Version: 1.3.3
# Universal one-command entry point. Uses authenticated GitHub API content delivery.

$ErrorActionPreference = "Stop"
$Repo = "rassvetpublic-spec/CKS"
$ToolPath = "tools/CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
$Temp = Join-Path $env:TEMP "CKS_HANDSOFF"
New-Item -ItemType Directory -Force -Path $Temp | Out-Null

Write-Host "CKS HANDSOFF BOOTSTRAP v1.3.3"
Write-Host "Discovering environment..."

$roots = @($env:CKS_WORKSPACE,(Get-Location).Path,"C:\git","C:\Irvis-UPG\GIT") | Where-Object { $_ } | Select-Object -Unique
$repo = $null
foreach ($root in $roots) {
    if ((Test-Path (Join-Path $root ".git")) -and ((Split-Path $root -Leaf) -eq "CKS")) { $repo = Get-Item $root; break }
    $candidate = Join-Path $root "CKS"
    if (Test-Path (Join-Path $candidate ".git")) { $repo = Get-Item $candidate; break }
}

if (-not $repo) { throw "Local CKS repository not found" }

Write-Host "Local CKS found: $($repo.FullName)"
Write-Host "Execution locked: $($repo.FullName)"

$download = Join-Path $Temp "CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
Remove-Item $download -Force -ErrorAction SilentlyContinue

Write-Host "Delivery: GitHub API content"
$data = gh api "repos/$Repo/contents/$ToolPath" | ConvertFrom-Json
if (-not $data.content) { throw "Collector content missing" }

$bytes = [Convert]::FromBase64String(($data.content -replace '\s',''))
[IO.File]::WriteAllBytes($download,$bytes)

if ((Get-Item $download).Length -eq 0) { throw "Collector empty" }

Write-Host "Running collector..."
& $download -RepoPath $repo.FullName
if ($LASTEXITCODE -ne 0) { throw "Collector failed: $LASTEXITCODE" }
Write-Host "DONE"
