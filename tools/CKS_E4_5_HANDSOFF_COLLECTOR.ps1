$ErrorActionPreference = "Continue"

$Root = "C:\Irvis-UPG\GIT\CKS"
$LogDir = Join-Path $Root "e4.5-evidence"
$LogFile = Join-Path $LogDir ("e45_collect_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log")

function Log($text) {
    $text | Tee-Object -FilePath $LogFile -Append
}

function Run-Step($title, $cmd) {
    Log ""
    Log "===== $title ====="
    try {
        Invoke-Expression $cmd 2>&1 | Tee-Object -FilePath $LogFile -Append
    } catch {
        Log ("ERROR: " + $_.Exception.Message)
    }
}

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
Log "CKS E4.5 Evidence Collector"
Log ("Time: " + (Get-Date))
Log ("Computer: " + $env:COMPUTERNAME)

if (Test-Path $Root) {
    Set-Location $Root
    Log "Repository found: $Root"
} else {
    Log "Repository missing: $Root"
    Log "Fallback search: C:\Irvis-UPG\GIT"
    $found = Get-ChildItem -Path C:\Irvis-UPG\GIT -Directory -Recurse -Force -ErrorAction SilentlyContinue |
        Where-Object { Test-Path (Join-Path $_.FullName ".git") } |
        Select-Object -First 1
    if ($found) {
        Set-Location $found.FullName
        Log ("Fallback repo: " + $found.FullName)
    } else {
        Log "FAILED: repository not found"
        exit 1
    }
}

Run-Step "git status" "git status"
Run-Step "branch" "git branch --show-current"
Run-Step "SHA" "git rev-parse HEAD"
Run-Step "remote" "git remote -v"
Run-Step "python" "python --version"
Run-Step "helper" "python tools\\cks_apply_branch_protection.py --help"

if (Get-Command gh -ErrorAction SilentlyContinue) {
    Run-Step "GitHub auth" "gh auth status"
} else {
    Log "gh CLI missing; fallback git auth info"
    Run-Step "git config" "git config --list"
}

Log ""
Log "NEXT:"
Log "python tools\\cks_apply_branch_protection.py --dry-run"
Log "python tools\\cks_apply_branch_protection.py --apply"
Log "python tools\\cks_apply_branch_protection.py"
Log ("Evidence log: " + $LogFile)
