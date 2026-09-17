# CKS HANDSOFF BOOTSTRAP v2.5
# Single entry point. Core repository recovery only.
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$OutputEncoding=[System.Text.Encoding]::UTF8

$RepoUrl='https://github.com/rassvetpublic-spec/CKS.git'

Write-Host 'CKS HANDSOFF v2.5'
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"

if(-not (Get-Command git -ErrorAction SilentlyContinue)){throw 'git missing'}
Write-Host 'git PASS'

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

Write-Host "repo PASS $repoPath"
git fetch origin main --quiet
git checkout main --quiet
git reset --hard origin/main --quiet

Write-Host "branch PASS $(git branch --show-current)"
Write-Host "HEAD PASS $(git rev-parse HEAD)"

foreach($a in @('README.md','control/system-state.yaml','docs/CKS_CURRENT_WORKING_STATE_SNAPSHOT_2026-09-17.md')){
 if(Test-Path $a){Write-Host "anchor PASS $a"}else{Write-Host "anchor MISSING $a"}
}

Write-Host 'SSOT DISCOVERY'
$patterns=@('GitHub `main`','recovery SSOT','CHAT_BOOTSTRAP','CURRENT_WORKING_STATE','ARCHITECTURE_DECISION')
foreach($p in $patterns){
 Get-ChildItem docs -Recurse -File -ErrorAction SilentlyContinue |
 Select-String $p |
 Select-Object -First 3 |
 ForEach-Object {Write-Host "SSOT $($_.Path):$($_.LineNumber)"}
}

Write-Host 'DONE'
