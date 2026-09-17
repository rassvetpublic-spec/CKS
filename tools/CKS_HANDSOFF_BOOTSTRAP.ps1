# CKS HANDSOFF BOOTSTRAP v2.7
# Single entry point. Core repository recovery only.
param([switch]$Quiet)

$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$OutputEncoding=[System.Text.Encoding]::UTF8

$RepoUrl='https://github.com/rassvetpublic-spec/CKS.git'

function Out($x){ if(-not $Quiet){ Write-Host $x } }

Out 'CKS HANDSOFF v2.7'
Out "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"

if(-not (Get-Command git -ErrorAction SilentlyContinue)){throw 'git missing'}
Out 'git PASS'

$start=(Get-Location).Path
$repoPath=$null

$scan=@($start,(Split-Path $start -Parent)) | Select-Object -Unique
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
 if($LASTEXITCODE -ne 0){throw 'clone failed'}
}

if((Split-Path $repoPath -Leaf) -ne 'CKS'){throw "invalid repo path: $repoPath"}
Set-Location $repoPath

$remote=(git remote get-url origin).Trim()
if($remote -notmatch 'rassvetpublic-spec/CKS'){throw "repo identity failed: $remote"}

Out "repo PASS $repoPath"
git fetch origin main --quiet
git checkout main --quiet
git reset --hard origin/main --quiet

Out "branch PASS $(git branch --show-current)"
Out "HEAD PASS $(git rev-parse HEAD)"

foreach($a in @('README.md','control/system-state.yaml','docs/CKS_CURRENT_WORKING_STATE_SNAPSHOT_2026-09-17.md')){
 if(Test-Path $a){Out "anchor PASS $a"}else{Out "anchor MISSING $a"}
}

# remove temporary clones from previous handsoff runs
Get-ChildItem (Split-Path $repoPath -Parent) -Directory -Filter 'CKS.__handsoff_clone_*' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Out 'SSOT DISCOVERY'
$patterns=@('GitHub `main`','recovery SSOT','CHAT_BOOTSTRAP','CURRENT_WORKING_STATE','ARCHITECTURE_DECISION')
$seen=@()
$candidates=@()
foreach($p in $patterns){
 Get-ChildItem docs -Recurse -File -ErrorAction SilentlyContinue |
 Select-String $p |
 ForEach-Object {
  $key="$($_.Path):$($_.LineNumber)"
  if($seen -notcontains $key){
   $seen += $key
   $candidates += $_
   Out "SSOT $key"
  }
 }
}

$primary=$candidates | Where-Object {$_.Path -match 'CHAT_BOOTSTRAP'} | Select-Object -First 1
if($primary){
 Out "PRIMARY SSOT $($primary.Path):$($primary.LineNumber)"
}else{
 Out 'PRIMARY SSOT UNKNOWN'
}

Out 'DONE'
