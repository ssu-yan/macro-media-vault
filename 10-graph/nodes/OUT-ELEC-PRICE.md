---
id: OUT-ELEC-PRICE
label: 電價
type: outcome
domain: 能源
status: 可觀察
aliases:
  - 電價
  - 電力價格
edges:
  - to: OUT-CORP-MARGINS
    sign: -1
    lag_months: [6, 24]
    confidence: 0.4
    mechanism: "成本上升"
    evidence: "理論推導"
    breaks_if: "佔比太小"
---
# 電價

`OUT-ELEC-PRICE` ｜ outcome ｜ 能源 ｜ 狀態：可觀察

批發與零售電價。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-CORP-MARGINS]] | 抑制 ↓ | 6–24 | 0.4 | 成本上升 | 理論推導 | 佔比太小 |

## ⚠️ 反向力量與已知限制

電價的地區差異極大，全國平均幾乎沒有意義。**這張圖用單一節點代表電價是重大簡化。**

## 觀察指標

- 主要電網區批發電價
- 零售電價
- 尖峰負載

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
