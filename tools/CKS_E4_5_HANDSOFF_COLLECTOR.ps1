# CKS E4.5 HANDSOFF COLLECTOR
# Fallback first: works when GitHub/network is unavailable.
# Collects local evidence and prepares GitHub upload.

$ErrorActionPreference = "Continue"

$Candidates = @(
    "C:\Irvis-UPG\GIT\CKS",
    (Get-Location).Path
)

$Repo = $null
foreach ($c in $Candidates) {
    if (Test-Path (Join-Path $c ".git")) {
        $Repo = $c
        break
    }
}

if (-not $Repo) {
    $found = Get-ChildItem -Path C:\Irvis-UPG\GIT -Directory -Recurse -Force -ErrorAction SilentlyContinue |
        Where-Object { Test-Path (Join-Path $_.FullName ".git") } |
        Select-Object -First 1
    if ($found) { $Repo = $found.FullName }
}

if (-not $Repo) {
    Write-Host "FAILED: repository not found"
    exit 1
}

Set-Location $Repo

$LogDir = Join-Path $Repo "e4.5-evidence"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir ("e45_collect_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log")

function Log($x) { $x | Tee-Object -FilePath $LogFile -Append }
function Run($name,$cmd) {
    Log ""
    Log "===== $name ====="
    Invoke-Expression $cmd 2>&1 | Tee-Object -FilePath $LogFile -Append
}

Log "CKS E4.5 HANDSOFF"
Log "Repo: $Repo"
Log "Time: $(Get-Date)"

Run "git status" "git status"
Run "branch" "git branch --show-current"
Run "sha" "git rev-parse HEAD"
Run "remote" "git remote -v"
Run "python" "python --version"
Run "helper" "python tools\cks_apply_branch_protection.py --help"

if (Get-Command gh -ErrorAction SilentlyContinue) {
    Run "gh auth" "gh auth status"
} else {
    Log "gh unavailable - fallback mode"
}

Log ""
Log "NEXT"
Log "python tools\cks_apply_branch_protection.py --dry-run"
Log "python tools\cks_apply_branch_protection.py --apply"
Log "python tools\cks_apply_branch_protection.py"
Log "UPLOAD: tools\CKS_HANDSOFF_LOG_UPLOAD.ps1"
Log "LOG=$LogFile"
