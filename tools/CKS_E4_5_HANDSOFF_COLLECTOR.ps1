# CKS E4.5 HANDSOFF COLLECTOR
# Context-driven fallback collector. No fixed machine path.

$ErrorActionPreference = "Continue"

function Find-Repo {
    $roots = @()
    if ($env:CKS_REPO) { $roots += $env:CKS_REPO }
    $roots += (Get-Location).Path
    $roots += "C:\Irvis-UPG\GIT"
    $roots += "C:\git"
    $roots += "C:\Projects"

    foreach ($root in $roots) {
        if (Test-Path $root) {
            $repo = Get-ChildItem $root -Directory -Recurse -Force -ErrorAction SilentlyContinue |
                Where-Object { Test-Path (Join-Path $_.FullName '.git') } |
                Select-Object -First 1
            if ($repo) { return $repo.FullName }
        }
    }
    return $null
}

$Repo = Find-Repo
if (-not $Repo) { Write-Host 'FAILED: repository not found'; exit 1 }
Set-Location $Repo

$LogDir = Join-Path $Repo 'e4.5-evidence'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir ("e45_collect_" + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')

function Run($name,$cmd) {
    "===== $name =====" | Tee-Object -FilePath $LogFile -Append
    Invoke-Expression $cmd 2>&1 | Tee-Object -FilePath $LogFile -Append
}

"CKS E4.5 HANDSOFF" | Tee-Object -FilePath $LogFile
"Repo=$Repo" | Tee-Object -FilePath $LogFile -Append
Run 'git status' 'git status'
Run 'branch' 'git branch --show-current'
Run 'sha' 'git rev-parse HEAD'
Run 'remote' 'git remote -v'
Run 'python' 'python --version'
Run 'helper' 'python tools\cks_apply_branch_protection.py --help'

Write-Host "LOG=$LogFile"
