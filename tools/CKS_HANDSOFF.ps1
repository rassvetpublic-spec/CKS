Clear-Host
# CKS HANDSOFF
# Version: 2.0.0
# Single-file bootstrap + health gate + fallback + SSOT/chat discovery.
# No helper scripts are downloaded or executed.

$ErrorActionPreference = 'Stop'

$Version = '2.0.0'
$RemoteRepoName = 'rassvetpublic-spec/CKS'
$RemoteHttpsUrl = 'https://github.com/rassvetpublic-spec/CKS.git'
$ExpectedRemoteNormalized = 'https://github.com/rassvetpublic-spec/cks'
$CurrentPath = (Get-Location).Path
$LogRoot = Join-Path $env:TEMP 'CKS_HANDSOFF'
New-Item -ItemType Directory -Force -Path $LogRoot | Out-Null
$LogFile = Join-Path $LogRoot ("cks_handsoff_{0}.log" -f (Get-Date -Format 'yyyyMMdd_HHmmss'))

function Write-Log {
    param([string]$Message)
    Write-Host $Message
    Add-Content -LiteralPath $LogFile -Value $Message -Encoding utf8
}

function Write-Step {
    param([string]$Name, [string]$Status, [string]$Detail)
    $line = ('{0,-24} {1,-8} {2}' -f $Name, $Status, $Detail)
    Write-Log $line
}

function Normalize-GitRemote {
    param([string]$Url)
    if ([string]::IsNullOrWhiteSpace($Url)) { return '' }

    $value = $Url.Trim()
    if ($value.StartsWith('git@github.com:', [System.StringComparison]::OrdinalIgnoreCase)) {
        $value = 'https://github.com/' + $value.Substring('git@github.com:'.Length)
    }
    elseif ($value.StartsWith('http://', [System.StringComparison]::OrdinalIgnoreCase)) {
        $value = 'https://' + $value.Substring('http://'.Length)
    }

    $value = $value.TrimEnd('/')
    if ($value.EndsWith('.git', [System.StringComparison]::OrdinalIgnoreCase)) {
        $value = $value.Substring(0, $value.Length - 4)
    }

    return $value.ToLowerInvariant()
}

function Test-CksRepository {
    param([string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path)) { return $false }
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) { return $false }
    if (-not (Test-Path -LiteralPath (Join-Path $Path '.git'))) { return $false }

    $inside = (& git -C $Path rev-parse --is-inside-work-tree 2>$null)
    if (($LASTEXITCODE -ne 0) -or (($inside | Select-Object -First 1) -ne 'true')) { return $false }

    $origin = (& git -C $Path remote get-url origin 2>$null)
    if ($LASTEXITCODE -ne 0) { return $false }
    if (-not $origin) { return $false }

    return ((Normalize-GitRemote ([string]($origin | Select-Object -First 1))) -eq $ExpectedRemoteNormalized)
}

function Get-UsdRubRate {
    try {
        $response = Invoke-WebRequest -Uri 'https://www.cbr.ru/scripts/XML_daily.asp' -TimeoutSec 8 -UseBasicParsing
        [xml]$xml = $response.Content
        $usd = $xml.ValCurs.Valute | Where-Object { $_.CharCode -eq 'USD' } | Select-Object -First 1
        if (($null -ne $usd) -and (-not [string]::IsNullOrWhiteSpace([string]$usd.Value))) {
            return [PSCustomObject]@{ Status = 'PASS'; Value = [string]$usd.Value; Source = 'CBR' }
        }
    }
    catch {
        # fallback below
    }

    try {
        $fallback = Invoke-RestMethod -Uri 'https://open.er-api.com/v6/latest/USD' -TimeoutSec 8
        if (($null -ne $fallback) -and ($null -ne $fallback.rates) -and ($null -ne $fallback.rates.RUB)) {
            return [PSCustomObject]@{ Status = 'PASS'; Value = [string]$fallback.rates.RUB; Source = 'ER-API fallback' }
        }
    }
    catch {
        # non-blocking informational check
    }

    return [PSCustomObject]@{ Status = 'WARN'; Value = 'N/A'; Source = 'unavailable' }
}

Write-Log "CKS HANDSOFF v$Version"
Write-Log "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Log "Start: $CurrentPath"
Write-Log ''

# --- Environment gate ---
$GitCommand = Get-Command git -ErrorAction SilentlyContinue
if (-not $GitCommand) {
    Write-Step 'git' 'BLOCKED' 'git.exe not found'
    throw 'git is required for CKS HANDSOFF'
}
Write-Step 'git' 'PASS' $GitCommand.Source

$selfTestUrls = @(
    'https://github.com/rassvetpublic-spec/CKS.git',
    'git@github.com:rassvetpublic-spec/CKS.git',
    'http://github.com/rassvetpublic-spec/CKS/'
)
$selfTestFailed = $false
foreach ($selfTestUrl in $selfTestUrls) {
    if ((Normalize-GitRemote $selfTestUrl) -ne $ExpectedRemoteNormalized) {
        $selfTestFailed = $true
    }
}
if ($selfTestFailed) {
    Write-Step 'self-test' 'BLOCKED' 'remote normalization failed'
    throw 'CKS HANDSOFF self-test failed'
}
Write-Step 'self-test' 'PASS' 'remote normalization + fallback primitives'

$GhCommand = Get-Command gh -ErrorAction SilentlyContinue
if ($GhCommand) {
    & gh auth status *> $null
    if ($LASTEXITCODE -eq 0) {
        Write-Step 'gh auth' 'PASS' 'authenticated'
    }
    else {
        Write-Step 'gh auth' 'WARN' 'gh exists but authentication is unavailable; git fallback remains active'
    }
}
else {
    Write-Step 'gh' 'WARN' 'not found; git fallback remains active'
}

$fx = Get-UsdRubRate
Write-Step 'USD/RUB' $fx.Status ("{0} RUB per USD [{1}]" -f $fx.Value, $fx.Source)

# --- Find a valid CKS repository ---
$CandidatePaths = @(
    $CurrentPath,
    (Join-Path $CurrentPath 'CKS'),
    'C:\Irvis-UPG\GIT\CKS',
    'C:\git\CKS'
) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique

$LocalRepoPath = $null
foreach ($candidatePath in $CandidatePaths) {
    if (Test-CksRepository $candidatePath) {
        $LocalRepoPath = (Resolve-Path -LiteralPath $candidatePath).Path
        break
    }
}

# --- Clone fallback when CKS is absent ---
if (-not $LocalRepoPath) {
    $CloneRoot = $null

    if (((Split-Path $CurrentPath -Leaf) -ieq 'GIT') -and (Test-Path -LiteralPath $CurrentPath -PathType Container)) {
        $CloneRoot = $CurrentPath
    }
    elseif (Test-Path -LiteralPath 'C:\Irvis-UPG\GIT' -PathType Container) {
        $CloneRoot = 'C:\Irvis-UPG\GIT'
    }
    elseif (Test-Path -LiteralPath 'C:\git' -PathType Container) {
        $CloneRoot = 'C:\git'
    }
    else {
        $CloneRoot = $CurrentPath
    }

    $CloneTarget = Join-Path $CloneRoot 'CKS'
    if (Test-Path -LiteralPath $CloneTarget) {
        Write-Step 'repo fallback' 'BLOCKED' "Path exists but is not a valid CKS repo: $CloneTarget"
        throw "Refusing to overwrite invalid path: $CloneTarget"
    }

    $StagingTarget = Join-Path $CloneRoot ("CKS.__handsoff_clone_{0}" -f $PID)
    if (Test-Path -LiteralPath $StagingTarget) {
        Remove-Item -LiteralPath $StagingTarget -Recurse -Force
    }

    Write-Step 'repo fallback' 'RUN' "clone -> $CloneTarget"
    $cloneSucceeded = $false

    if ($GhCommand) {
        $cloneOutput = @(& gh repo clone $RemoteRepoName $StagingTarget 2>&1)
        foreach ($cloneLine in $cloneOutput) { Write-Log ([string]$cloneLine) }
        if ($LASTEXITCODE -eq 0) { $cloneSucceeded = $true }
    }

    if ((-not $cloneSucceeded) -and (Test-Path -LiteralPath $StagingTarget)) {
        Remove-Item -LiteralPath $StagingTarget -Recurse -Force
    }

    if (-not $cloneSucceeded) {
        $cloneOutput = @(& git clone $RemoteHttpsUrl $StagingTarget 2>&1)
        foreach ($cloneLine in $cloneOutput) { Write-Log ([string]$cloneLine) }
        if ($LASTEXITCODE -eq 0) { $cloneSucceeded = $true }
    }

    if (-not $cloneSucceeded) {
        if (Test-Path -LiteralPath $StagingTarget) {
            Remove-Item -LiteralPath $StagingTarget -Recurse -Force
        }
        Write-Step 'repo fallback' 'BLOCKED' 'both gh clone and git clone failed'
        throw 'Unable to restore CKS repository'
    }

    if (-not (Test-CksRepository $StagingTarget)) {
        Remove-Item -LiteralPath $StagingTarget -Recurse -Force
        Write-Step 'repo identity' 'BLOCKED' 'cloned directory failed CKS identity validation'
        throw 'Cloned repository is not valid CKS'
    }

    Move-Item -LiteralPath $StagingTarget -Destination $CloneTarget
    $LocalRepoPath = (Resolve-Path -LiteralPath $CloneTarget).Path
}

Write-Step 'repo path' 'PASS' $LocalRepoPath

# --- Repository health / "lice check" ---
$originUrl = [string]((& git -C $LocalRepoPath remote get-url origin) | Select-Object -First 1)
$originNormalized = Normalize-GitRemote $originUrl
if ($originNormalized -ne $ExpectedRemoteNormalized) {
    Write-Step 'repo identity' 'BLOCKED' $originUrl
    throw 'CKS remote identity mismatch'
}
Write-Step 'repo identity' 'PASS' $originUrl

$headSha = [string]((& git -C $LocalRepoPath rev-parse HEAD) | Select-Object -First 1)
if ($LASTEXITCODE -ne 0) { throw 'Cannot read repository HEAD' }
Write-Step 'HEAD' 'PASS' $headSha

$branchName = [string]((& git -C $LocalRepoPath branch --show-current) | Select-Object -First 1)
if ([string]::IsNullOrWhiteSpace($branchName)) { $branchName = '(detached)' }
Write-Step 'branch' 'PASS' $branchName

$dirty = @(& git -C $LocalRepoPath status --porcelain)
if ($dirty.Count -gt 0) {
    Write-Step 'worktree' 'WARN' ("dirty: {0} change(s); search uses canonical ref, no files will be changed" -f $dirty.Count)
}
else {
    Write-Step 'worktree' 'PASS' 'clean'
}

& git -C $LocalRepoPath fsck --no-dangling --no-progress *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Step 'git fsck' 'BLOCKED' 'repository object integrity check failed'
    throw 'CKS repository integrity check failed'
}
Write-Step 'git fsck' 'PASS' 'object database healthy'

# --- Refresh canonical ref, with local fallback ---
$CanonicalRef = 'HEAD'
& git -C $LocalRepoPath fetch origin main --quiet 2>$null
if ($LASTEXITCODE -eq 0) {
    & git -C $LocalRepoPath rev-parse --verify origin/main *> $null
    if ($LASTEXITCODE -eq 0) {
        $CanonicalRef = 'origin/main'
        Write-Step 'canonical ref' 'PASS' 'origin/main refreshed'
    }
    else {
        Write-Step 'canonical ref' 'WARN' 'fetch completed but origin/main unavailable; using HEAD'
    }
}
else {
    Write-Step 'canonical ref' 'WARN' 'remote fetch unavailable; using local HEAD fallback'
}

# --- Required current-state anchors ---
$RequiredAnchors = @(
    'README.md',
    'control/system-state.yaml',
    'docs/CKS_CURRENT_WORKING_STATE_SNAPSHOT_2026-09-17.md'
)

$AnchorFailure = $false
foreach ($anchor in $RequiredAnchors) {
    & git -C $LocalRepoPath cat-file -e "${CanonicalRef}:$anchor" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Step ('anchor ' + $anchor) 'PASS' $CanonicalRef
    }
    else {
        Write-Step ('anchor ' + $anchor) 'BLOCKED' 'missing from canonical ref'
        $AnchorFailure = $true
    }
}

if ($AnchorFailure) {
    throw 'Required CKS current-state anchors are incomplete'
}

Write-Log ''
Write-Log 'ALL CORE CHECKS PASS -> SSOT/CHAT DISCOVERY STARTED'
Write-Log ''

# --- SSOT/chat discovery in canonical repository content ---
$Pattern = 'SSOT|single source of truth|source of truth|источник истины|единственный источник|единого источника|chat|чат|bootstrap|context pack|context snapshot|current working state|текущее фактическое состояние|канон|canonical'
$RawMatches = @(& git -C $LocalRepoPath grep -n -I -i -E $Pattern $CanonicalRef -- '*.md' '*.yaml' '*.yml' '*.json' '*.txt' 2>$null)
$GrepExit = $LASTEXITCODE
if (($GrepExit -ne 0) -and ($GrepExit -ne 1)) {
    throw "git grep failed with exit code $GrepExit"
}

$Results = @()
foreach ($matchLine in $RawMatches) {
    $lineText = [string]$matchLine
    if ($lineText -match '^[^:]+:(?<path>[^:]+):(?<line>\d+):(?<text>.*)$') {
        $path = [string]$Matches['path']
        $lineNumber = [int]$Matches['line']
        $text = ([string]$Matches['text']).Trim()
        $haystack = ($path + ' ' + $text).ToLowerInvariant()
        $score = 0

        if ($haystack -match 'ssot|single source of truth|source of truth|источник истины|единственный источник|единого источника') { $score += 12 }
        if ($haystack -match 'chat|чат') { $score += 8 }
        if ($haystack -match 'current working state|текущее фактическое состояние|system-state') { $score += 7 }
        if ($haystack -match 'bootstrap|context pack|context snapshot|snapshot') { $score += 5 }
        if ($haystack -match 'канон|canonical') { $score += 3 }
        if ($path -match 'README|system-state|CURRENT_WORKING_STATE|BOOTSTRAP|CONTEXT') { $score += 4 }

        $Results += [PSCustomObject]@{
            Score = $score
            Path = $path
            Line = $lineNumber
            Text = $text
        }
    }
}

$Ranked = @($Results | Sort-Object -Property @{Expression={$_.Score};Descending=$true}, Path, Line | Select-Object -First 30)

# --- Optional GitHub issues/PR discovery; local search remains authoritative fallback ---
$RemoteHits = @()
if ($GhCommand) {
    try {
        $issueJson = & gh issue list --repo $RemoteRepoName --state all --limit 100 --json number,title,body,url 2>$null
        if (($LASTEXITCODE -eq 0) -and (-not [string]::IsNullOrWhiteSpace([string]$issueJson))) {
            $issues = $issueJson | ConvertFrom-Json
            foreach ($item in $issues) {
                $combined = ([string]$item.title + ' ' + [string]$item.body)
                if ($combined -match '(?i)SSOT|single source of truth|source of truth|источник истины|чат|chat|bootstrap|context') {
                    $RemoteHits += [PSCustomObject]@{ Type='ISSUE'; Number=$item.number; Title=$item.title; Url=$item.url }
                }
            }
        }
    }
    catch {
        Write-Step 'issue search' 'WARN' 'GitHub issue search unavailable'
    }

    try {
        $prJson = & gh pr list --repo $RemoteRepoName --state all --limit 100 --json number,title,body,url 2>$null
        if (($LASTEXITCODE -eq 0) -and (-not [string]::IsNullOrWhiteSpace([string]$prJson))) {
            $prs = $prJson | ConvertFrom-Json
            foreach ($item in $prs) {
                $combined = ([string]$item.title + ' ' + [string]$item.body)
                if ($combined -match '(?i)SSOT|single source of truth|source of truth|источник истины|чат|chat|bootstrap|context') {
                    $RemoteHits += [PSCustomObject]@{ Type='PR'; Number=$item.number; Title=$item.title; Url=$item.url }
                }
            }
        }
    }
    catch {
        Write-Step 'PR search' 'WARN' 'GitHub PR search unavailable'
    }
}

Write-Log '=== SSOT / CHAT CANDIDATES (canonical repository) ==='
if ($Ranked.Count -eq 0) {
    Write-Log 'No keyword candidates found in canonical repository content.'
}
else {
    foreach ($row in $Ranked) {
        Write-Log ("[{0,2}] {1}:{2} | {3}" -f $row.Score, $row.Path, $row.Line, $row.Text)
    }
}

Write-Log ''
Write-Log '=== CURRENT-STATE ANCHORS FROM CKS README CONTRACT ==='
Write-Log '1. control/system-state.yaml'
Write-Log '2. docs/CKS_CURRENT_WORKING_STATE_SNAPSHOT_2026-09-17.md'
Write-Log '3. reports/CKS_CI_VERIFIED_2026-09-17.md (verification summary, if present)'

if ($RemoteHits.Count -gt 0) {
    Write-Log ''
    Write-Log '=== RELATED GITHUB ISSUES / PRs ==='
    foreach ($hit in ($RemoteHits | Select-Object -First 20)) {
        Write-Log ("{0} #{1} | {2} | {3}" -f $hit.Type, $hit.Number, $hit.Title, $hit.Url)
    }
}

$ExplicitChatSsot = @($Ranked | Where-Object {
    $hasSsotMarker = (($_.Text -match '(?i)SSOT|single source of truth|source of truth|источник истины|единственный источник|единого источника') -or ($_.Path -match '(?i)SSOT'))
    $hasChatMarker = (($_.Text -match '(?i)chat|чат') -or ($_.Path -match '(?i)chat|чат'))
    return ($hasSsotMarker -and $hasChatMarker)
})

Write-Log ''
Write-Log '=== RESULT ==='
if ($ExplicitChatSsot.Count -gt 0) {
    $winner = $ExplicitChatSsot | Select-Object -First 1
    Write-Log ("EXPLICIT CHAT SSOT CANDIDATE: {0}:{1}" -f $winner.Path, $winner.Line)
    Write-Log ("EVIDENCE: {0}" -f $winner.Text)
}
else {
    Write-Log 'EXPLICIT CHAT SSOT MARKER: NOT FOUND'
    Write-Log 'Fallback conclusion: use CKS current-state anchors above as the canonical factual-state chain; do not invent a separate chat SSOT.'
}

Write-Log ''
Write-Log "LOG=$LogFile"
Write-Log "REPOSITORY=$LocalRepoPath"
Write-Log "CANONICAL_REF=$CanonicalRef"
Write-Log 'DONE'
