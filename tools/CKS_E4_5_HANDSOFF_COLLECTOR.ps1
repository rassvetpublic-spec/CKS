# CKS E4.5 HANDSOFF COLLECTOR
# Version: 1.4.1

param(
    [string]$RepoPath
)

$ErrorActionPreference = "Continue"
$ExpectedRemote = "github.com/rassvetpublic-spec/CKS"

function Normalize-Remote([string]$Remote) {
    return (($Remote.Trim() `
        -replace '\.git$','' `
        -replace '^git@github\.com:','github.com/' `
        -replace '^https?://',''))
}

function Test-CksRepo([string]$Path) {
    if (-not $Path) { return $false }
    if (-not (Test-Path (Join-Path $Path '.git'))) { return $false }
    try {
        $remote = git -C $Path remote get-url origin 2>$null
        return (Normalize-Remote $remote) -eq $ExpectedRemote
    } catch {
        return $false
    }
}

if ($RepoPath -and -not (Test-CksRepo $RepoPath)) {
    Write-Host "FAILED: supplied RepoPath is not rassvetpublic-spec/CKS: $RepoPath"
    exit 11
}

if (-not $RepoPath) {
    $roots = @($env:CKS_WORKSPACE,$env:WORKSPACE,(Get-Location).Path,'C:\git','C:\Irvis-UPG\GIT') | Where-Object {$_} | Select-Object -Unique
    foreach ($root in $roots) {
        if (Test-CksRepo $root) { $RepoPath = $root; break }
        $candidate = Join-Path $root 'CKS'
        if (Test-CksRepo $candidate) { $RepoPath = $candidate; break }
    }
}

if (-not $RepoPath) {
    Write-Host 'FAILED: rassvetpublic-spec/CKS repository not found'
    exit 12
}

$RepoPath = (Resolve-Path $RepoPath).Path
Set-Location $RepoPath

$LogDir = Join-Path $env:TEMP 'CKS_HANDSOFF\evidence'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir ('e45_collect_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')

function Log($x) { $x | Tee-Object -FilePath $LogFile -Append }
function Run($n,$c) { Log ''; Log "===== $n ====="; Invoke-Expression $c 2>&1 | Tee-Object -FilePath $LogFile -Append }

Log 'CKS E4.5 HANDSOFF COLLECTOR v1.4.1'
Log "Repository: $RepoPath"
Run 'git status' 'git status'
Run 'branch' 'git branch --show-current'
Run 'sha' 'git rev-parse HEAD'
Run 'remote' 'git remote -v'
Run 'python' 'python --version'
Run 'helper' 'python tools\cks_apply_branch_protection.py --help'
if (Get-Command gh -ErrorAction SilentlyContinue) { Run 'gh auth' 'gh auth status' }
Log "VERSION=1.4.1"
Log "REPOSITORY=$RepoPath"
Log "LOG=$LogFile"
Log 'NEXT=python tools\cks_apply_branch_protection.py --dry-run'
Write-Host 'VERSION=1.4.1'
Write-Host "REPOSITORY=$RepoPath"
Write-Host "LOG=$LogFile"
