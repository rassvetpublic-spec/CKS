# CKS HANDSOFF BOOTSTRAP
# Version: 1.0.0
# Universal one-command entry point.

$ErrorActionPreference = "Stop"

$Repo = "rassvetpublic-spec/CKS"
$RawBase = "https://raw.githubusercontent.com/rassvetpublic-spec/CKS/main"
$Tool = "tools/CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
$Temp = Join-Path $env:TEMP "CKS_HANDSOFF"

New-Item -ItemType Directory -Force -Path $Temp | Out-Null

Write-Host "CKS HANDSOFF BOOTSTRAP v1.0.0"
Write-Host "Discovering environment..."

$roots = @(
    $env:CKS_WORKSPACE,
    "C:\git",
    "C:\Irvis-UPG\GIT",
    "C:\Projects",
    (Get-Location).Path
) | Where-Object { $_ }

$repo = $null
foreach ($root in $roots) {
    if (Test-Path $root) {
        $repo = Get-ChildItem -Path $root -Directory -Recurse -Force -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -eq "CKS" -and (Test-Path (Join-Path $_.FullName ".git")) } |
            Select-Object -First 1
        if ($repo) { break }
    }
}

if ($repo) {
    Write-Host "Local CKS found: $($repo.FullName)"
}
else {
    Write-Host "Local CKS not found. Running standalone bootstrap mode."
}

$download = Join-Path $Temp "CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
Invoke-WebRequest -Uri "$RawBase/$Tool" -OutFile $download

Write-Host "Running collector..."
powershell -ExecutionPolicy Bypass -File $download

Write-Host "DONE"
