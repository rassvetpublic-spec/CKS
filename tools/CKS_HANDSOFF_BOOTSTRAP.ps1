Clear-Host
# CKS HANDSOFF BOOTSTRAP
# Version: 1.2.1
# Universal one-command entry point with execution context lock.

$ErrorActionPreference = "Stop"

$RawBase = "https://raw.githubusercontent.com/rassvetpublic-spec/CKS/main"
$Tool = "tools/CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
$Temp = Join-Path $env:TEMP "CKS_HANDSOFF"

New-Item -ItemType Directory -Force -Path $Temp | Out-Null

Write-Host "CKS HANDSOFF BOOTSTRAP v1.2.1"
Write-Host "Discovering environment..."

$roots = @(
    $env:CKS_WORKSPACE,
    (Get-Location).Path,
    "C:\git",
    "C:\Irvis-UPG\GIT"
) | Where-Object { $_ } | Select-Object -Unique

$repo = $null

foreach ($root in $roots) {
    if (Test-Path $root) {
        $repo = Get-ChildItem -Path $root -Directory -Force -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -eq "CKS" -and (Test-Path (Join-Path $_.FullName ".git")) } |
            Select-Object -First 1

        if ($repo) { break }
    }
}

if ($repo) {
    Write-Host "Local CKS found: $($repo.FullName)"
    Set-Location $repo.FullName
    Write-Host "Execution locked: $((Get-Location).Path)"
}
else {
    Write-Host "Local CKS not found. Running standalone mode."
}

$download = Join-Path $Temp "CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
Invoke-WebRequest -Uri "$RawBase/$Tool" -OutFile $download

Write-Host "Running collector..."

if ($repo) {
    powershell -ExecutionPolicy Bypass -File $download -Workspace $repo.FullName
}
else {
    powershell -ExecutionPolicy Bypass -File $download
}

Write-Host "DONE"
