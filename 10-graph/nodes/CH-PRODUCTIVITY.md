---
id: CH-PRODUCTIVITY
label: 生產力傳導
type: channel
domain: 經濟
status: 假設
aliases:
  - 生產力傳導
edges:
  - to: OUT-PRODUCTIVITY-STAT
    sign: 1
    lag_months: [24, 84]
    confidence: 0.4
    mechanism: "效率提升最終進入統計"
    evidence: "理論推導 — 歷史上通用技術的生產力效果遲到數十年"
    breaks_if: "統計無法捕捉或效果不存在"
  - to: OUT-CORP-MARGINS
    sign: 1
    lag_months: [18, 60]
    confidence: 0.45
    mechanism: "同樣產出所需成本下降"
    evidence: "理論推導"
    breaks_if: "競爭把節省的成本讓渡給客戶"
---
# 生產力傳導

`CH-PRODUCTIVITY` ｜ channel ｜ 經濟 ｜ 狀態：假設

AI 若真的提升產出效率，最終應該出現在總要素生產力與勞動生產力統計中。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-PRODUCTIVITY-STAT]] | 推升 ↑ | 24–84 | 0.4 | 效率提升最終進入統計 | 理論推導 — 歷史上通用技術的生產力效果遲到數十年 | 統計無法捕捉或效果不存在 |
| [[OUT-CORP-MARGINS]] | 推升 ↑ | 18–60 | 0.45 | 同樣產出所需成本下降 | 理論推導 | 競爭把節省的成本讓渡給客戶 |

## ⚠️ 反向力量與已知限制

**這個節點是整張圖裡最重要、也最沒有證據的一個。** 如果 AI 的總體意義最終來自生產力，那麼上面所有 capex 通道都只是序曲；但生產力效果目前**完全沒有出現在統計裡**，而且歷史先例（電力、電腦）顯示它可能遲到數十年。時滯下界設 24 個月已經是樂觀的。

## 觀察指標

- 勞動生產力年增率
- TFP 估計
- 產業別生產力分歧

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
