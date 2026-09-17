# CKS HANDSOFF LOG UPLOADER
# Uploads local diagnostic evidence back into repository without chat copy/paste.

$ErrorActionPreference = "Continue"

$Repo = "C:\Irvis-UPG\GIT\CKS"
$Source = Join-Path $Repo "e4.5-evidence"
$Target = Join-Path $Repo "e4.5-evidence\uploaded"

if (!(Test-Path $Source)) {
    Write-Host "No evidence directory found: $Source"
    exit 1
}

New-Item -ItemType Directory -Force -Path $Target | Out-Null

$files = Get-ChildItem $Source -Filter "*.log" -File

if ($files.Count -eq 0) {
    Write-Host "No logs found"
    exit 0
}

foreach ($file in $files) {
    Copy-Item $file.FullName $Target -Force
}

Set-Location $Repo

git add e4.5-evidence/uploaded
git commit -m "evidence: upload CKS E4.5 hands-off logs"
git push

Write-Host "Uploaded logs through GitHub"
