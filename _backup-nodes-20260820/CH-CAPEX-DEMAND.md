---
id: CH-CAPEX-DEMAND
label: 資本支出的需求乘數
type: channel
domain: 經濟
status: 進行中
aliases:
  - 資本支出乘數
edges:
  - to: OUT-GDP-CAPEX
    sign: 1
    lag_months: [0, 24]
    confidence: 0.75
    mechanism: "直接計入固定投資"
    evidence: "已實現 — 已成為部分經濟體成長的顯著貢獻項"
    breaks_if: "投資轉往海外"
  - to: OUT-DC-REIT
    sign: 1
    lag_months: [0, 18]
    confidence: 0.7
    mechanism: "資料中心資產需求與租金"
    evidence: "已實現"
    breaks_if: "供給過剩"
  - to: OUT-REAL-RATES
    sign: 1
    lag_months: [12, 48]
    confidence: 0.4
    mechanism: "大規模投資需求推升資金需求"
    evidence: "理論推導 — 效果可能被儲蓄過剩淹沒"
    breaks_if: "資金供給充裕"
---
# 資本支出的需求乘數

`CH-CAPEX-DEMAND` ｜ channel ｜ 經濟 ｜ 狀態：進行中

資料中心建設對營建、電力設備、工業的實體需求。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-GDP-CAPEX]] | 推升 ↑ | 0–24 | 0.75 | 直接計入固定投資 | 已實現 — 已成為部分經濟體成長的顯著貢獻項 | 投資轉往海外 |
| [[OUT-DC-REIT]] | 推升 ↑ | 0–18 | 0.7 | 資料中心資產需求與租金 | 已實現 | 供給過剩 |
| [[OUT-REAL-RATES]] | 推升 ↑ | 12–48 | 0.4 | 大規模投資需求推升資金需求 | 理論推導 — 效果可能被儲蓄過剩淹沒 | 資金供給充裕 |

## ⚠️ 反向力量與已知限制

**資本支出的貢獻有一個內建的反轉風險：它是水準效應，不是成長效應。** 一旦資本支出停在高原期，它對 GDP 成長的貢獻就歸零，即使絕對金額仍然很高。這一點在討論「AI 撐起經濟成長」時經常被搞混。

## 觀察指標

- 固定投資對 GDP 成長的貢獻度
- 資料中心空置率

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
