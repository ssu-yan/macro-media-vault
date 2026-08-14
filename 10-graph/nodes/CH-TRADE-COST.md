---
id: CH-TRADE-COST
label: 貿易成本
type: channel
domain: 經濟
status: 進行中
aliases:
  - 貿易成本
  - 到岸成本
edges:
  - to: OUT-US-CPI
    sign: 1
    lag_months: [3, 18]
    confidence: 0.5
    mechanism: "成本傳導至消費者物價"
    evidence: "已實現但幅度有爭議 — 承擔方分配長期未有定論"
    breaks_if: "由進口商或出口商吸收"
  - to: CH-INPUT-PRICE
    sign: 1
    lag_months: [0, 12]
    confidence: 0.65
    mechanism: "中間財成本上升"
    evidence: "已實現"
    breaks_if: "可替代來源"
---
# 貿易成本

`CH-TRADE-COST` ｜ channel ｜ 經濟 ｜ 狀態：進行中

關稅、運輸、合規、重組帶來的成本。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-US-CPI]] | 推升 ↑ | 3–18 | 0.5 | 成本傳導至消費者物價 | 已實現但幅度有爭議 — 承擔方分配長期未有定論 | 由進口商或出口商吸收 |
| [[CH-INPUT-PRICE]] | 推升 ↑ | 0–12 | 0.65 | 中間財成本上升 | 已實現 | 可替代來源 |

## ⚠️ 反向力量與已知限制

關稅的最終負擔分配是**實證上長期爭議**的問題。0.50 的信心反映爭議本身，不是我的猶豫。

## 觀察指標

- 進口物價指數
- 有效關稅稅率
- 企業毛利率

---

> 本檔由 `engine/seed_uschina.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
