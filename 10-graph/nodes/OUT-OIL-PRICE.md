---
id: OUT-OIL-PRICE
label: 原油價格
type: outcome
domain: 能源
status: 可觀察
aliases:
  - 油價
  - 原油
  - brent
edges:
  - to: OUT-EU-CPI
    sign: 1
    lag_months: [1, 9]
    confidence: 0.7
    mechanism: "運輸與化工成本傳導"
    evidence: "已實現"
    breaks_if: "稅制吸收"
  - to: OUT-ENERGY-STOCKS
    sign: 1
    lag_months: [0, 6]
    confidence: 0.8
    mechanism: "上游獲利直接連動油價"
    evidence: "已實現 — 2022 能源類股表現最強"
    breaks_if: "稅制或政治干預壓縮獲利"
---
# 原油價格

`OUT-OIL-PRICE` ｜ outcome ｜ 能源 ｜ 狀態：可觀察

Brent。2022/3 一度突破 120 美元，年底回落至 80 附近。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-EU-CPI]] | 推升 ↑ | 1–9 | 0.7 | 運輸與化工成本傳導 | 已實現 | 稅制吸收 |
| [[OUT-ENERGY-STOCKS]] | 推升 ↑ | 0–6 | 0.8 | 上游獲利直接連動油價 | 已實現 — 2022 能源類股表現最強 | 稅制或政治干預壓縮獲利 |

## 觀察指標

- Brent 期貨
- OPEC+ 產量決議

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
