---
id: OUT-EU-GAS-PRICE
label: 歐洲天然氣價格 (TTF)
type: outcome
domain: 能源
status: 可觀察
aliases:
  - 天然氣
  - ttf
  - 歐洲天然氣
edges:
  - to: OUT-EU-CPI
    sign: 1
    lag_months: [1, 9]
    confidence: 0.8
    mechanism: "能源直接進入 CPI 並透過電價二次傳導"
    evidence: "已實現"
    breaks_if: "價格管制"
---
# 歐洲天然氣價格 (TTF)

`OUT-EU-GAS-PRICE` ｜ outcome ｜ 能源 ｜ 狀態：可觀察

2022/8 一度逼近 340 歐元/MWh，2023 年回落至戰前水準附近。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-EU-CPI]] | 推升 ↑ | 1–9 | 0.8 | 能源直接進入 CPI 並透過電價二次傳導 | 已實現 | 價格管制 |

## 觀察指標

- TTF 現貨與期貨曲線
- 歐洲庫存率

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
