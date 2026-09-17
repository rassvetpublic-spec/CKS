# CKS E4.5 HANDSOFF COLLECTOR
# Version: 1.4.0
# Receives an exact repository path from bootstrap. It never switches to another repo.
# Fallback discovery is used only when RepoPath is not supplied.

param(
    [string]$RepoPath
)

$ErrorActionPreference = "Continue"
$ExpectedRemote = "github.com/rassvetpublic-spec/CKS"

function Test-CksRepo([string]$Path) {
    if (-not $Path) { return $false }
    if (-not (Test-Path (Join-Path $Path ".git"))) { return $false }
    try {
        $remote = git -C $Path remote get-url origin 2>$null
        if (-not $remote) { return $false }
        $normalized = ($remote -replace '\\.git$','') -replace '^git@github.com:','github.com/' -replace '^https://','' -replace '^http://',''
        return $normalized -eq $ExpectedRemote
    } catch {
        return $false
    }
}

if ($RepoPath) {
    if (-not (Test-CksRepo $RepoPath)) {
        Write-Host "FAILED: supplied RepoPath is not rassvetpublic-spec/CKS: $RepoPath"
        exit 11
    }
} else {
    $Roots = @(
        $env:CKS_WORKSPACE,
        $env:WORKSPACE,
        (Get-Location).Path,
        "C:\git",
        "C:\Irvis-UPG\GIT",
        "C:\Projects"
    ) | Where-Object { $_ } | Select-Object -Unique

    $found = $null
    foreach ($root in $Roots) {
        if (-not (Test-Path $root)) { continue }

        if (Test-CksRepo $root) {
            $found = (Get-Item $root).FullName
            break
        }

        $direct = Join-Path $root "CKS"
        if (Test-CksRepo $direct) {
            $found = (Get-Item $direct).FullName
            break
        }

        $candidate = Get-ChildItem -Path $root -Directory -Recurse -Force -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -eq "CKS" -and (Test-CksRepo $_.FullName) } |
            Select-Object -First 1
        if ($candidate) {
            $found = $candidate.FullName
            break
        }
    }

    if (-not $found) {
        Write-Host "FAILED: rassvetpublic-spec/CKS repository not found"
        exit 12
    }
    $RepoPath = $found
}

$RepoPath = (Resolve-Path $RepoPath).Path
Set-Location $RepoPath

$LogDir = Join-Path $env:TEMP "CKS_HANDSOFF\evidence"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir ("e45_collect_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log")

function Log($x) { $x | Tee-Object -FilePath $LogFile -Append }
function Run($name,$cmd) {
    Log ""
    Log "===== $name ====="
    Invoke-Expression $cmd 2>&1 | Tee-Object -FilePath $LogFile -Append
}

Log "CKS E4.5 HANDSOFF COLLECTOR v1.4.0"
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
Log "VERSION=1.4.0"
Log "REPOSITORY=$RepoPath"
Log "LOG=$LogFile"
Log "NEXT=python tools\cks_apply_branch_protection.py --dry-run"

Write-Host "VERSION=1.4.0"
Write-Host "REPOSITORY=$RepoPath"
Write-Host "LOG=$LogFile"
