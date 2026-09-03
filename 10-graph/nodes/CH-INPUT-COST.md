---
id: CH-INPUT-COST
label: 企業投入成本上升
type: channel
domain: 經濟
status: 已緩解
aliases:
  - 投入成本
  - 生產成本
edges:
  - to: OUT-EU-CPI
    sign: 1
    lag_months: [3, 12]
    confidence: 0.85
    mechanism: "成本推動型通膨"
    evidence: "已實現 — 2022 歐元區 HICP 破 10%"
    breaks_if: "企業吸收毛利不轉嫁"
  - to: CH-REAL-INCOME
    sign: -1
    lag_months: [3, 18]
    confidence: 0.75
    mechanism: "物價上漲侵蝕實質購買力"
    evidence: "已實現"
    breaks_if: "名目薪資同步上漲"
---
# 企業投入成本上升

`CH-INPUT-COST` ｜ channel ｜ 經濟 ｜ 狀態：已緩解

能源、運輸、化肥、原物料成本上升傳導至終端價格。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-EU-CPI]] | 推升 ↑ | 3–12 | 0.85 | 成本推動型通膨 | 已實現 — 2022 歐元區 HICP 破 10% | 企業吸收毛利不轉嫁 |
| [[CH-REAL-INCOME]] | 抑制 ↓ | 3–18 | 0.75 | 物價上漲侵蝕實質購買力 | 已實現 | 名目薪資同步上漲 |

## 觀察指標

- PPI 對 CPI 的傳導率
- 企業毛利率

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
