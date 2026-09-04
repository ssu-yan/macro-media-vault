---
id: CH-SHIPPING-COST
label: 航運與保險成本
type: channel
domain: 經濟
status: 已緩解
aliases:
  - 航運成本
  - 保險費
edges:
  - to: CH-INPUT-COST
    sign: 1
    lag_months: [0, 6]
    confidence: 0.6
    mechanism: "運輸成本進入商品到岸價"
    evidence: "已實現"
    breaks_if: "運費回落"
---
# 航運與保險成本

`CH-SHIPPING-COST` ｜ channel ｜ 經濟 ｜ 狀態：已緩解

戰爭風險區的保險費與繞道成本。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[CH-INPUT-COST]] | 推升 ↑ | 0–6 | 0.6 | 運輸成本進入商品到岸價 | 已實現 | 運費回落 |

## 觀察指標

- 戰爭風險保險費率
- 波羅的海乾散貨指數

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
