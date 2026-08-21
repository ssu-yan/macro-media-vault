---
id: CH-ELEC-COST
label: 電力成本傳導
type: channel
domain: 能源
status: 進行中
aliases:
  - 電力成本
edges:
  - to: OUT-CORP-MARGINS
    sign: -1
    lag_months: [6, 30]
    confidence: 0.45
    mechanism: "電力密集產業成本上升"
    evidence: "理論推導 — 電力佔多數產業成本比重不高"
    breaks_if: "可轉嫁或佔比太小"
  - to: OUT-ELEC-PRICE
    sign: 1
    lag_months: [0, 12]
    confidence: 0.6
    mechanism: "需求增量直接反映"
    evidence: "有先例"
    breaks_if: "供給彈性充足"
---
# 電力成本傳導

`CH-ELEC-COST` ｜ channel ｜ 能源 ｜ 狀態：進行中

電價上升傳導至工業與家庭。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-CORP-MARGINS]] | 抑制 ↓ | 6–30 | 0.45 | 電力密集產業成本上升 | 理論推導 — 電力佔多數產業成本比重不高 | 可轉嫁或佔比太小 |
| [[OUT-ELEC-PRICE]] | 推升 ↑ | 0–12 | 0.6 | 需求增量直接反映 | 有先例 | 供給彈性充足 |

## ⚠️ 反向力量與已知限制

電力佔多數產業成本的比重其實很低（通常個位數百分比），所以這條通道對總體毛利率的影響**可能小到測不出來**。放進圖裡是為了完整性，不是因為它重要。

## 觀察指標

- 工業電價
- 電力密集產業毛利率

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
