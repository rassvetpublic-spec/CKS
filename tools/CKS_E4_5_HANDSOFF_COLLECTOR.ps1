# CKS E4.5 HANDSOFF COLLECTOR
# Universal fallback workspace discovery.
# No fixed machine path.

$ErrorActionPreference = "Continue"

$Roots = @(
    $env:CKS_WORKSPACE,
    "C:\git",
    "C:\Irvis-UPG\GIT",
    "C:\Projects",
    (Get-Location).Path
) | Where-Object { $_ }

$Repo = $null

foreach ($root in $Roots) {
    if (Test-Path $root) {
        $Repo = Get-ChildItem -Path $root -Directory -Recurse -Force -ErrorAction SilentlyContinue |
            Where-Object { Test-Path (Join-Path $_.FullName ".git") } |
            Select-Object -First 1
        if ($Repo) { break }
    }
}

if (-not $Repo) {
    Write-Host "FAILED: CKS repository not found"
    Write-Host "Set CKS_WORKSPACE or clone repository first"
    exit 1
}

$RepoPath = $Repo.FullName
Set-Location $RepoPath

$LogDir = Join-Path $RepoPath "e4.5-evidence"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir ("e45_collect_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log")

function Log($x) { $x | Tee-Object -FilePath $LogFile -Append }
function Run($name,$cmd) {
    Log ""
    Log "===== $name ====="
    Invoke-Expression $cmd 2>&1 | Tee-Object -FilePath $LogFile -Append
}

Log "CKS E4.5 HANDSOFF"
Log "Repository: $RepoPath"
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
Log "LOG=$LogFile"
Log "NEXT: python tools\cks_apply_branch_protection.py --dry-run"
