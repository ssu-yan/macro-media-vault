---
id: OUT-ECB-RATE
label: ECB 政策利率
type: outcome
domain: 經濟
status: 可觀察
aliases:
  - ecb
  - 歐洲央行
  - 政策利率
edges:
  - to: OUT-EU-GDP
    sign: -1
    lag_months: [6, 24]
    confidence: 0.7
    mechanism: "利率上升抑制投資與耐久財消費"
    evidence: "已實現"
    breaks_if: "傳導受阻"
  - to: OUT-EUR-USD
    sign: 1
    lag_months: [0, 6]
    confidence: 0.45
    mechanism: "利差收斂支撐歐元"
    evidence: "有先例 — 但 2022 年被避險需求蓋過"
    breaks_if: "美元避險需求主導"
---
# ECB 政策利率

`OUT-ECB-RATE` ｜ outcome ｜ 經濟 ｜ 狀態：可觀察

2022/7 起結束負利率並連續升息。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-EU-GDP]] | 抑制 ↓ | 6–24 | 0.7 | 利率上升抑制投資與耐久財消費 | 已實現 | 傳導受阻 |
| [[OUT-EUR-USD]] | 推升 ↑ | 0–6 | 0.45 | 利差收斂支撐歐元 | 有先例 — 但 2022 年被避險需求蓋過 | 美元避險需求主導 |

## 觀察指標

- ECB 存款利率
- OIS 隱含路徑

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
