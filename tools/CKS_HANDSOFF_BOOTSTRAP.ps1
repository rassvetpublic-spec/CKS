Clear-Host
# CKS HANDSOFF BOOTSTRAP
# Version: 1.2.6
# Universal entry point. Locked repo context.

$ErrorActionPreference = "Stop"
$Temp = Join-Path $env:TEMP "CKS_HANDSOFF"
New-Item -ItemType Directory -Force -Path $Temp | Out-Null

Write-Host "CKS HANDSOFF BOOTSTRAP v1.2.6"
Write-Host "Discovering environment..."

$roots = @($env:CKS_WORKSPACE,(Get-Location).Path,"C:\git","C:\Irvis-UPG\GIT","C:\Projects") | Where-Object { $_ } | Select-Object -Unique
$repo = $null
foreach ($root in $roots) {
    if (Test-Path $root) {
        if ((Split-Path $root -Leaf) -eq "CKS" -and (Test-Path (Join-Path $root ".git"))) { $repo = Get-Item $root; break }
        $candidate = Join-Path $root "CKS"
        if (Test-Path (Join-Path $candidate ".git")) { $repo = Get-Item $candidate; break }
    }
}

if ($repo) {
    Write-Host "Local CKS found: $($repo.FullName)"
    Write-Host "Execution locked: $($repo.FullName)"
}

$download = Join-Path $Temp "CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
$urls = @(
"https://raw.githubusercontent.com/rassvetpublic-spec/CKS/main/tools/CKS_E4_5_HANDSOFF_COLLECTOR.ps1",
"https://github.com/rassvetpublic-spec/CKS/raw/main/tools/CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
)

$ok=$false
foreach($uri in $urls){
    try { Invoke-WebRequest -Uri "$uri?x=$(Get-Random)" -OutFile $download; $ok=$true; break } catch { }
}
if(-not $ok){ throw "Collector download failed" }

Write-Host "Running collector..."
if($repo){ powershell -ExecutionPolicy Bypass -File $download -RepoPath $repo.FullName }
else { powershell -ExecutionPolicy Bypass -File $download }
Write-Host "DONE"
