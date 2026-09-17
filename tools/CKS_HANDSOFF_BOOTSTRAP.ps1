Clear-Host
# CKS HANDSOFF BOOTSTRAP
# Version: 1.2.4
# Universal entry point with locked repo context and collector download fallback.

$ErrorActionPreference = "Stop"
$RawBase = "https://raw.githubusercontent.com/rassvetpublic-spec/CKS/main"
$Tool = "tools/CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
$Temp = Join-Path $env:TEMP "CKS_HANDSOFF"
New-Item -ItemType Directory -Force -Path $Temp | Out-Null

Write-Host "CKS HANDSOFF BOOTSTRAP v1.2.4"
Write-Host "Discovering environment..."

$roots = @($env:CKS_WORKSPACE,(Get-Location).Path,"C:\git","C:\Irvis-UPG\GIT","C:\Projects") | Where-Object { $_ } | Select-Object -Unique
$repo = $null
foreach ($root in $roots) {
    if (Test-Path $root) {
        if ((Split-Path $root -Leaf) -eq "CKS" -and (Test-Path (Join-Path $root ".git"))) { $repo = Get-Item $root; break }
        $repo = Get-ChildItem -Path $root -Directory -Force -ErrorAction SilentlyContinue | Where-Object { $_.Name -eq "CKS" -and (Test-Path (Join-Path $_.FullName ".git")) } | Select-Object -First 1
        if ($repo) { break }
    }
}

if ($repo) {
    Write-Host "Local CKS found: $($repo.FullName)"
    Write-Host "Execution locked: $($repo.FullName)"
}

$download = Join-Path $Temp "CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
$ok = $false
foreach ($uri in @("$RawBase/$Tool?nocache=$(Get-Date -Format yyyyMMddHHmmss)","https://github.com/rassvetpublic-spec/CKS/raw/main/$Tool")) {
    try {
        Invoke-WebRequest -Uri $uri -OutFile $download
        $ok = $true
        break
    } catch {
        Write-Host "Download fallback failed: $uri"
    }
}
if (-not $ok) { throw "Collector download failed" }

Write-Host "Running collector..."
if ($repo) {
    powershell -ExecutionPolicy Bypass -File $download -RepoPath $repo.FullName
} else {
    powershell -ExecutionPolicy Bypass -File $download
}
Write-Host "DONE"
