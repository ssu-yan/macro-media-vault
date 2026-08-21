---
id: CH-INPUT-PRICE
label: 投入品價格
type: channel
domain: 經濟
status: 進行中
aliases:
  - 投入品價格
  - 中間財成本
edges:
  - to: OUT-US-CPI
    sign: 1
    lag_months: [3, 18]
    confidence: 0.45
    mechanism: "生產者價格傳導至消費者"
    evidence: "已實現"
    breaks_if: "毛利吸收"
  - to: OUT-CORP-MARGINS
    sign: -1
    lag_months: [0, 18]
    confidence: 0.5
    mechanism: "成本上升壓縮毛利"
    evidence: "已實現"
    breaks_if: "可轉嫁"
---
# 投入品價格

`CH-INPUT-PRICE` ｜ channel ｜ 經濟 ｜ 狀態：進行中

中間財與關鍵原物料的價格。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-US-CPI]] | 推升 ↑ | 3–18 | 0.45 | 生產者價格傳導至消費者 | 已實現 | 毛利吸收 |
| [[OUT-CORP-MARGINS]] | 抑制 ↓ | 0–18 | 0.5 | 成本上升壓縮毛利 | 已實現 | 可轉嫁 |

## 觀察指標

- PPI
- PPI 對 CPI 傳導率

---

> 本檔由 `engine/seed_uschina.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
