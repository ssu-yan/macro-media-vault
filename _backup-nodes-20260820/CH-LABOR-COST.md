---
id: CH-LABOR-COST
label: 勞動成本
type: channel
domain: 經濟
status: 進行中
aliases:
  - 勞動成本
  - 工資
edges:
  - to: OUT-CORP-MARGINS
    sign: -1
    lag_months: [0, 24]
    confidence: 0.55
    mechanism: "工資是最大的成本項"
    evidence: "已實現"
    breaks_if: "生產力同步提升"
---
# 勞動成本

`CH-LABOR-COST` ｜ channel ｜ 經濟 ｜ 狀態：進行中

工資成長率與單位勞動成本。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-CORP-MARGINS]] | 抑制 ↓ | 0–24 | 0.55 | 工資是最大的成本項 | 已實現 | 生產力同步提升 |

## 觀察指標

- 單位勞動成本
- 工資成長率

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
