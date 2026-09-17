# CKS HANDSOFF BOOTSTRAP v2.0.0
# One file entry point. No secondary downloads.
$ErrorActionPreference='Stop'
$Repo='rassvetpublic-spec/CKS'
$RepoUrl='https://github.com/rassvetpublic-spec/CKS.git'
Write-Host "CKS HANDSOFF v2.0.0"
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"

function Test-Cmd($n){ if(Get-Command $n -ErrorAction SilentlyContinue){'PASS'}else{'FAIL'} }

Write-Host "git $(Test-Cmd git)"
Write-Host "gh $(Test-Cmd gh)"

$root=(Get-Location).Path
$repoPath=Join-Path $root 'CKS'
if(-not (Test-Path (Join-Path $repoPath '.git'))){
  $tmp="$repoPath.__handsoff_clone_$PID"
  if(Test-Path $tmp){Remove-Item $tmp -Recurse -Force}
  git clone $RepoUrl $tmp
  if($LASTEXITCODE -ne 0){throw 'clone failed'}
  Move-Item $tmp $repoPath
}

Set-Location $repoPath
$remote=(git remote get-url origin).Trim()
if($remote -notmatch 'rassvetpublic-spec/CKS'){throw "repo identity failed: $remote"}

$head=(git rev-parse HEAD).Trim()
$branch=(git branch --show-current).Trim()
Write-Host "repo PASS $repoPath"
Write-Host "branch PASS $branch"
Write-Host "HEAD PASS $head"

git fetch origin main --quiet
git checkout main --quiet

git reset --hard origin/main --quiet

$anchors=@('README.md','control/system-state.yaml','docs/CKS_CURRENT_WORKING_STATE_SNAPSHOT_2026-09-17.md')
foreach($a in $anchors){ if(Test-Path $a){Write-Host "anchor PASS $a"}else{Write-Host "anchor MISSING $a"}}

try{
 $cbr=Invoke-RestMethod 'https://www.cbr-xml-daily.ru/daily_json.js' -TimeoutSec 5
 Write-Host "USD/RUB PASS $($cbr.Valute.USD.Value) RUB"
}catch{Write-Host 'USD/RUB SKIP'}

Write-Host 'SSOT DISCOVERY'
Get-ChildItem docs -Recurse -File -ErrorAction SilentlyContinue | Select-String 'SSOT|Single Source of Truth' | Select-Object -First 20

Write-Host 'DONE'
