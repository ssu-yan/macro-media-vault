# SOP — 收工前 Git 檢查

> 每次結束工作、關閉 Obsidian 前跑一遍。三十秒的事。
> 建立：2026-09-01（Lucas）｜起因見下方「為什麼有這條」

## 為什麼有這條

Obsidian Git 外掛的自動 commit **只在 Obsidian 開著的時候跑**。
關掉 app，計時器就停——那之後寫的東西、或關閉前不到 10 分鐘寫的東西，
全部只存在於本機硬碟，沒有任何版本紀錄、沒有任何遠端備份。

2026-09-01 這件事就是這樣發生的：一天寫了 1,109 行（含一份 579 行的掃描紀錄），
一行都沒 commit。當天因為調整雲端同步設定，本機檔案被清空。
救回來靠的不是 Git，是雲端剛好還留著一份。**那是運氣，不是機制。**

## 收工前檢查（三步）

**1. 看狀態**

```powershell
git status --short
```

- 沒有輸出 → 乾淨，可以關了
- 有輸出 → 繼續第 2 步

**2. 提交並推送**

```powershell
git add -A
git commit -m "描述今天做了什麼"
git push
```

commit 訊息寫**做了什麼**，不要寫 `update` 或 `backup`。
半年後你要靠這行字找回某次修改。

**3. 確認推上去了**

```powershell
git log origin/main..main --oneline
```

沒有輸出 = 全部已推送。有輸出 = 還有 commit 卡在本機，`git push` 再跑一次。

## 判斷「今天值不值得 commit」

不需要判斷。**有變更就 commit。**
Git 的成本是三十秒，遺失的成本是一整天。

## 常見狀況

| 狀況 | 處理 |
|---|---|
| `Unable to create '.git/index.lock': File exists` | 沒有 git 程序在跑，是殘留鎖。`Remove-Item ".git\index.lock" -Force` 後重試 |
| `cannot lock ref 'HEAD'` | 同上，清掉 `.git` 底下所有 `*.lock`：`Get-ChildItem .git -Recurse -Filter *.lock \| Remove-Item -Force` |
| `git push` 要求帳密 | Git Credential Manager 的權杖過期，重新登入 GitHub 即可 |
| 大量檔案顯示 modified 但內容沒改 | 行尾 CRLF/LF 差異，正常，照常 commit |

## 鐵則

- **Vault 不放進任何雲端同步資料夾**（OneDrive／Dropbox／iCloud）。
  雲端同步會與 Git 爭搶 `.git/` 的寫入權，造成 lock 殘留、ref 被還原、物件損毀。
  備份由 Git ＋ 私有 GitHub repo 負責，一套就夠。
- **要把 vault 移出雲端資料夾，用「剪下貼上」把資料夾搬出去**，
  絕對不要用「取消勾選同步資料夾」——那個動作會把本機檔案收走。
- **多台裝置輪流用**：離開前先 commit + push，另一台開始前先 `git pull`。
  不要兩台同時編輯。
