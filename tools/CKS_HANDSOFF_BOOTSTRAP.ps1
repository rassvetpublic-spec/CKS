# CKS HANDSOFF BOOTSTRAP v3.0
# Single entry point. Core repository recovery.
param(
 [switch]$Quiet,
 [switch]$Repair,
 [switch]$E45
)

$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$OutputEncoding=[System.Text.Encoding]::UTF8

$RepoUrl='https://github.com/rassvetpublic-spec/CKS.git'
function Out($x){if(-not $Quiet){Write-Host $x}}

Out 'CKS HANDSOFF v3.0'
Out "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"

if(-not(Get-Command git -ErrorAction SilentlyContinue)){throw 'git missing'}
Out 'git PASS'

$start=(Get-Location).Path
$repoPath=$null
$scan=@($start,(Split-Path $start -Parent))|Select-Object -Unique
foreach($p in $scan){
 if(Test-Path (Join-Path $p '.git')){
  $url=(git -C $p remote get-url origin 2>$null)
  if($url -match 'rassvetpublic-spec/CKS'){$repoPath=$p;break}
 }
}

if(-not $repoPath){
 $repoPath=Join-Path (Split-Path $start -Parent) 'CKS'
 if(Test-Path $repoPath){throw "CKS path exists but is not repository: $repoPath"}
 git clone $RepoUrl $repoPath
 if($LASTEXITCODE){throw 'clone failed'}
}

Set-Location $repoPath
$remote=(git remote get-url origin).Trim()
if($remote -notmatch 'rassvetpublic-spec/CKS'){throw "repo identity failed: $remote"}

Out "repo PASS $repoPath"
git fetch origin main --quiet
git checkout main --quiet
git reset --hard origin/main --quiet

if($Repair){
 git clean -fdx --quiet
 Out 'repair PASS'
}

Out "branch PASS $(git branch --show-current)"
Out "HEAD PASS $(git rev-parse HEAD)"

$anchors=@('README.md','control/system-state.yaml','docs/CKS_CURRENT_WORKING_STATE_SNAPSHOT_2026-09-17.md')
foreach($a in $anchors){if(Test-Path $a){Out "anchor PASS $a"}else{Out "anchor MISSING $a"}}

Get-ChildItem (Split-Path $repoPath -Parent) -Directory -Filter 'CKS.__handsoff_clone_*' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Out 'SSOT DISCOVERY'
$hits=Get-ChildItem docs -Recurse -File -ErrorAction SilentlyContinue | Select-String 'GitHub `main`|recovery SSOT|CHAT_BOOTSTRAP|CURRENT_WORKING_STATE|ARCHITECTURE_DECISION'
$unique=@{}
foreach($h in $hits){
 $k="$($h.Path):$($h.LineNumber)"
 if(-not $unique.ContainsKey($k)){$unique[$k]=1;Out "SSOT $k"}
}
$primary=$hits|Where-Object{$_.Path -match 'CHAT_BOOTSTRAP'}|Select-Object -First 1
if($primary){Out "PRIMARY SSOT $($primary.Path):$($primary.LineNumber)"}else{Out 'PRIMARY SSOT UNKNOWN'}

if($E45){
 if(Test-Path 'issues') {Out 'E4.5 CHECK PASS'} else {Out 'E4.5 CHECK UNKNOWN'}
}

if($primary){Out 'STATUS READY'}else{Out 'STATUS BLOCKED'}
Out 'DONE'
