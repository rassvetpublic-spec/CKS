# CKS HANDSOFF LOG UPLOADER
# Fallback mode: works with local git even when GitHub is temporarily unavailable.

$ErrorActionPreference = "Continue"

$RepoCandidates = @(
    "C:\Irvis-UPG\GIT\CKS",
    (Get-Location).Path
)

$Repo = $RepoCandidates | Where-Object { Test-Path (Join-Path $_ ".git") } | Select-Object -First 1

if (-not $Repo) {
    Write-Host "FAILED: repository not found"
    exit 1
}

Set-Location $Repo

$Source = Join-Path $Repo "e4.5-evidence"

if (!(Test-Path $Source)) {
    Write-Host "No evidence folder: $Source"
    exit 1
}

$files = Get-ChildItem $Source -Filter "*.log" -File

if ($files.Count -eq 0) {
    Write-Host "No logs found"
    exit 0
}

$Archive = Join-Path $Source "uploaded"
New-Item -ItemType Directory -Force -Path $Archive | Out-Null

foreach ($f in $files) {
    Copy-Item $f.FullName $Archive -Force
}

git add e4.5-evidence/uploaded

git commit -m "evidence: upload CKS E4.5 hands-off logs"

$push = git push 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "PUSH FAILED - evidence saved locally"
    Write-Host $push
    exit 2
}

Write-Host "UPLOAD COMPLETE THROUGH GITHUB"
