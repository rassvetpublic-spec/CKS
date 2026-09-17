Clear-Host
# CKS HANDSOFF BOOTSTRAP
# Version: 1.3.0
# Universal entry point with GitHub API content fallback.

$ErrorActionPreference = "Stop"
$Repo = "rassvetpublic-spec/CKS"
$ToolPath = "tools/CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
$Temp = Join-Path $env:TEMP "CKS_HANDSOFF"
New-Item -ItemType Directory -Force -Path $Temp | Out-Null

Write-Host "CKS HANDSOFF BOOTSTRAP v1.3.0"
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
$api = "https://api.github.com/repos/$Repo/contents/$ToolPath"

try {
    $headers = @{ Accept = "application/vnd.github+json" }
    $data = Invoke-RestMethod -Uri $api -Headers $headers
    $bytes = [Convert]::FromBase64String($data.content)
    [IO.File]::WriteAllBytes($download,$bytes)
}
catch {
    throw "GitHub API collector download failed"
}

Write-Host "Running collector..."
if($repo){ powershell -ExecutionPolicy Bypass -File $download -RepoPath $repo.FullName }
else { powershell -ExecutionPolicy Bypass -File $download }
Write-Host "DONE"
