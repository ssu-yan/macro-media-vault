<#
    g3-vault-git-check.ps1
    ─────────────────────────────────────────────────────────────────────
    用途：檢查 macro-media-vault 有沒有「寫了但沒落地」的檔案。

    為什麼存在
      協議〈已知未解的問題〉第 9 條 v3.7 註：協議鏡像 2026-09-02 建立後
      兩天沒有進 Git，結論是「備份機制本身也會發生『寫了但沒落地』」。
      2026-09-28 查核發現同一種病第二次發作、規模大五倍——
      09-09／09-16／09-23 三份掃描紀錄與兩份媒體層提案全部 untracked。

      vault 自 2026-09-02 搬離 OneDrive 後，備份完全依賴 Git ＋ 私有 GitHub。
      untracked ＝ 沒有任何備份。

    用法
      pwsh -File .\sop\g3-vault-git-check.ps1
      或在 vault 內：  .\sop\g3-vault-git-check.ps1
      指定路徑：      .\sop\g3-vault-git-check.ps1 -Vault 'D:\somewhere\macro-media-vault'

    離開碼：0 = 全通過；1 = 有未落地項目；2 = 環境錯誤（找不到 vault 或 git）
#>

[CmdletBinding()]
param(
    [string] $Vault = 'C:\Users\Wendy\macro-media-vault'
)

$ErrorActionPreference = 'Stop'

$__oldOutEnc = [Console]::OutputEncoding
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

function Write-Head($t) { Write-Host ''; Write-Host $t -ForegroundColor Cyan }
function Write-OK($t)   { Write-Host "  [OK]   $t" -ForegroundColor Green }
function Write-Warn($t) { Write-Host "  [注意] $t" -ForegroundColor Yellow }
function Write-Bad($t)  { Write-Host "  [未落地] $t" -ForegroundColor Red }

Write-Host '=============================================='
Write-Host ' G3 vault ↔ Git 落地檢查'
Write-Host '=============================================='
Write-Host ("vault：{0}" -f $Vault)
Write-Host ("時間：{0}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))

# ── 0. 環境 ──────────────────────────────────────────────────────────
if (-not (Test-Path -LiteralPath $Vault)) {
    Write-Host ''
    Write-Host ("找不到 vault：{0}" -f $Vault) -ForegroundColor Red
    exit 2
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host ''
    Write-Host '找不到 git，無法檢查。' -ForegroundColor Red
    exit 2
}

Push-Location -LiteralPath $Vault
try {
    $inside = (git rev-parse --is-inside-work-tree 2>$null)
    if ($LASTEXITCODE -ne 0 -or $inside -ne 'true') {
        Write-Host ''
        Write-Host ("{0} 不是一個 Git 工作區。" -f $Vault) -ForegroundColor Red
        exit 2
    }

    $problems = 0

    # ── 1. 未追蹤與未提交 ─────────────────────────────────────────────
    Write-Head '1. 工作區狀態（untracked／modified／staged）'

    $porcelain = @(git -c core.quotepath=false status --porcelain)
    if ($porcelain.Count -eq 0) {
        Write-OK '工作區乾淨，沒有任何未提交的變更。'
    }
    else {
        $untracked = @()
        $modified  = @()
        foreach ($line in $porcelain) {
            if ($line.Length -lt 4) { continue }
            $code = $line.Substring(0, 2)
            $path = $line.Substring(3).Trim('"')
            if ($code -eq '??') { $untracked += $path } else { $modified += ,@($code, $path) }
        }

        if ($untracked.Count -gt 0) {
            Write-Host ("  未追蹤（從未進 Git，目前沒有任何備份）：{0} 個" -f $untracked.Count) -ForegroundColor Red
            foreach ($p in $untracked) { Write-Bad $p }
            $problems += $untracked.Count
        }
        if ($modified.Count -gt 0) {
            Write-Host ("  已追蹤但有未提交的改動：{0} 個" -f $modified.Count) -ForegroundColor Yellow
            foreach ($m in $modified) { Write-Warn ("{0}  {1}" -f $m[0], $m[1]) }
            $problems += $modified.Count
        }
    }

    # ── 2. 已提交但未推送 ─────────────────────────────────────────────
    Write-Head '2. 是否已推送到遠端'

    $branch = (git rev-parse --abbrev-ref HEAD 2>$null)
    $upstream = (git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>$null)
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($upstream)) {
        Write-Warn ("分支 {0} 沒有設定上游，無法判斷是否已推送。" -f $branch)
        $problems += 1
    }
    else {
        $ahead = @(git log --oneline "$upstream..HEAD" 2>$null)
        if ($ahead.Count -eq 0) {
            Write-OK ("{0} 與 {1} 同步。" -f $branch, $upstream)
        }
        else {
            Write-Host ("  有 {0} 個 commit 尚未推送到 {1}（遠端沒有備份）：" -f $ahead.Count, $upstream) -ForegroundColor Red
            foreach ($c in $ahead) { Write-Bad $c }
            $problems += $ahead.Count
        }
    }

    # ── 3. 被 .gitignore 排除、因此沒有備份的重要檔 ───────────────────
    Write-Head '3. 被 .gitignore 排除的檔（Git 不會備份它們）'

    $watch = @()
    $engine = Join-Path (Join-Path $Vault '10-graph') 'engine'
    if (Test-Path -LiteralPath $engine) {
        $watch += @(Get-ChildItem -LiteralPath $engine -Filter 'graph_snapshot*.json' -File -ErrorAction SilentlyContinue |
                    ForEach-Object { $_.FullName })
    }

    if ($watch.Count -eq 0) {
        Write-Warn '在 10-graph/engine 找不到任何 graph_snapshot*.json，請確認快照是否還在。'
        $problems += 1
    }
    else {
        foreach ($f in $watch) {
            $rel = $f.Substring($Vault.Length).TrimStart('\','/').Replace('\','/')
            git check-ignore -q -- $rel 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Warn ("{0} 被 .gitignore 排除——唯一的跨機器副本在 Project，弄丟就沒有了。" -f $rel)
            }
            else {
                Write-OK ("{0} 有納入 Git。" -f $rel)
            }
        }
    }

    # ── 4. 協議鏡像的版本與檔名是否一致 ───────────────────────────────
    Write-Head '4. 協議鏡像'

    $mirrors = @(Get-ChildItem -LiteralPath (Join-Path $Vault '10-graph') -Filter 'G3-每週掃描協議-mirror-v*.md' -File -ErrorAction SilentlyContinue)
    if ($mirrors.Count -eq 0) {
        Write-Warn '找不到協議鏡像檔（10-graph 底下的 G3-每週掃描協議-mirror-vX.Y.md）。'
        $problems += 1
    }
    else {
        foreach ($m in $mirrors) {
            $declared = $null
            foreach ($line in (Get-Content -LiteralPath $m.FullName -Encoding UTF8 -TotalCount 80)) {
                if ($line -match '^\*\*版本：v([0-9]+\.[0-9]+)') { $declared = $Matches[1]; break }
            }
            $inName = $null
            if ($m.Name -match 'mirror-v([0-9]+\.[0-9]+)\.md$') { $inName = $Matches[1] }

            if ($null -eq $declared) {
                Write-Warn ("{0}：檔案裡找不到「**版本：vX.Y」那一行，無法核對。" -f $m.Name)
                $problems += 1
            }
            elseif ($declared -eq $inName) {
                Write-OK ("{0}：檔名與內文都是 v{1}。" -f $m.Name, $declared)
            }
            else {
                Write-Bad ("{0}：檔名寫 v{1}，內文宣告 v{2} —— 不一致。" -f $m.Name, $inName, $declared)
                $problems += 1
            }
        }
    }

    # ── 結論 ─────────────────────────────────────────────────────────
    Write-Host ''
    Write-Host '=============================================='
    if ($problems -eq 0) {
        Write-Host ' 全部通過：磁碟上的東西都已進 Git 並推送。' -ForegroundColor Green
        Write-Host '=============================================='
        exit 0
    }
    else {
        Write-Host (" 有 {0} 項未落地，見上面紅字與黃字。" -f $problems) -ForegroundColor Red
        Write-Host ' 提醒：vault 已無雲端同步，未進 Git ＝ 沒有備份。' -ForegroundColor Red
        Write-Host '=============================================='
        exit 1
    }
}
finally {
    Pop-Location
    try { [Console]::OutputEncoding = $__oldOutEnc } catch { }
}
