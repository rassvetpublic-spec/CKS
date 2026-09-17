Clear-Host
# CKS HANDSOFF BOOTSTRAP
# Version: 1.3.1
# Universal one-command entry point. Uses authenticated GitHub CLI for internal delivery.

$ErrorActionPreference = "Stop"
$Repo = "rassvetpublic-spec/CKS"
$ToolPath = "tools/CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
$Temp = Join-Path $env:TEMP "CKS_HANDSOFF"
New-Item -ItemType Directory -Force -Path $Temp | Out-Null

Write-Host "CKS HANDSOFF BOOTSTRAP v1.3.1"
Write-Host "Discovering environment..."

$roots = @(
    $env:CKS_WORKSPACE,
    (Get-Location).Path,
    "C:\git",
    "C:\Irvis-UPG\GIT"
) | Where-Object { $_ } | Select-Object -Unique

$repo = $null
foreach ($root in $roots) {
    if (-not (Test-Path $root)) { continue }

    if ((Split-Path $root -Leaf) -eq "CKS" -and (Test-Path (Join-Path $root ".git"))) {
        $repo = Get-Item $root
        break
    }

    $candidate = Join-Path $root "CKS"
    if (Test-Path (Join-Path $candidate ".git")) {
        $repo = Get-Item $candidate
        break
    }
}

if (-not $repo) {
    throw "Local CKS repository not found inside configured git roots"
}

Write-Host "Local CKS found: $($repo.FullName)"
Write-Host "Execution locked: $($repo.FullName)"

$download = Join-Path $Temp "CKS_E4_5_HANDSOFF_COLLECTOR.ps1"
Remove-Item $download -Force -ErrorAction SilentlyContinue

if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "Delivery: authenticated gh api"
    $raw = & gh api "repos/$Repo/contents/$ToolPath" -H "Accept: application/vnd.github.raw+json" 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "gh api collector download failed: $($raw -join ' ')"
    }
    [IO.File]::WriteAllText($download, ($raw -join [Environment]::NewLine), [Text.UTF8Encoding]::new($false))
}
else {
    Write-Host "Delivery: anonymous GitHub API fallback"
    $api = "https://api.github.com/repos/$Repo/contents/$ToolPath"
    try {
        $headers = @{ Accept = "application/vnd.github+json"; "User-Agent" = "CKS-HANDSOFF" }
        $data = Invoke-RestMethod -Uri $api -Headers $headers
        $payload = ($data.content -replace '\s','')
        $bytes = [Convert]::FromBase64String($payload)
        [IO.File]::WriteAllBytes($download, $bytes)
    }
    catch {
        throw "GitHub API collector download failed: $($_.Exception.Message)"
    }
}

if (-not (Test-Path $download) -or (Get-Item $download).Length -eq 0) {
    throw "Collector delivery produced an empty file"
}

Write-Host "Running collector..."
& $download -RepoPath $repo.FullName
if ($LASTEXITCODE -ne 0) {
    throw "Collector failed with exit code $LASTEXITCODE"
}

Write-Host "DONE"
