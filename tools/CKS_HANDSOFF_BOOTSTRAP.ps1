# CKS HANDSOFF BOOTSTRAP v2.1
# Single entry point. No secondary downloads.
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$OutputEncoding=[System.Text.Encoding]::UTF8
$Repo='rassvetpublic-spec/CKS'
$RepoUrl='https://github.com/rassvetpublic-spec/CKS.git'

Write-Host 'CKS HANDSOFF v2.1'
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"

function Has-Cmd($name){[bool](Get-Command $name -ErrorAction SilentlyContinue)}
if(Has-Cmd git){Write-Host 'git PASS'}else{throw 'git missing'}
if(Has-Cmd gh){Write-Host 'gh PASS'}else{Write-Host 'gh SKIP'}

$start=(Get-Location).Path
$repoPath=Join-Path $start 'CKS'
$tmpDirs=Get-ChildItem $start -Directory -Filter 'CKS.__handsoff_clone_*' -ErrorAction SilentlyContinue
foreach($d in $tmpDirs){Remove-Item $d.FullName -Recurse -Force}

if(-not(Test-Path(Join-Path $repoPath '.git'))){
 $tmp="$repoPath.__handsoff_clone_$PID"
 git clone $RepoUrl $tmp
 if($LASTEXITCODE -ne 0){throw 'clone failed'}
 Move-Item $tmp $repoPath
}

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

try{
 $cbr=Invoke-RestMethod 'https://www.cbr-xml-daily.ru/daily_json.js' -TimeoutSec 5
 Write-Host "USD/RUB PASS $($cbr.Valute.USD.Value) RUB"
}catch{Write-Host 'USD/RUB SKIP'}

Write-Host 'SSOT DISCOVERY'
$patterns=@('GitHub `main`','recovery SSOT','CHAT_BOOTSTRAP','CURRENT_WORKING_STATE','ARCHITECTURE_DECISION')
foreach($p in $patterns){
 Get-ChildItem docs -Recurse -File -ErrorAction SilentlyContinue | Select-String $p | Select-Object -First 3 | ForEach-Object {Write-Host "SSOT $($_.Path):$($_.LineNumber)"}
}

Write-Host 'DONE'
