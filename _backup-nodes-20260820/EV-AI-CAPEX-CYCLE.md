---
id: EV-AI-CAPEX-CYCLE
label: 超大規模 AI 資本支出週期
type: event
domain: AI
status: 進行中
date: 2023-01-01
aliases:
  - ai 資本支出
  - ai capex
  - 資料中心投資
  - 超大規模投資
  - hyperscaler capex
edges:
  - to: ST-COMPUTE-DEMAND
    sign: 1
    lag_months: [0, 6]
    confidence: 0.9
    mechanism: "資本支出直接轉為算力採購"
    evidence: "已實現 — 2023-2026 加速器出貨與資料中心開工量"
    breaks_if: "資本支出計畫大幅下修"
  - to: CH-CAPEX-DEMAND
    sign: 1
    lag_months: [0, 12]
    confidence: 0.85
    mechanism: "營建、設備、電力設施的實體需求"
    evidence: "已實現"
    breaks_if: "投資轉為海外或閒置產能吸收"
  - to: ST-POWER-CONSTRAINT
    sign: 1
    lag_months: [6, 24]
    confidence: 0.8
    mechanism: "單一園區用電量級距躍升，超出既有電網規劃"
    evidence: "已實現 — 多國出現併網排隊"
    breaks_if: "電網容量充裕"
---
# 超大規模 AI 資本支出週期

`EV-AI-CAPEX-CYCLE` ｜ event ｜ AI ｜ 狀態：進行中

2023 年起大型雲端與模型商大幅上修資料中心與加速器資本支出。這是目前 AI 對實體經濟最直接、最可測量的傳導路徑——不是生產力，是水泥、銅、變壓器與電力。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[ST-COMPUTE-DEMAND]] | 推升 ↑ | 0–6 | 0.9 | 資本支出直接轉為算力採購 | 已實現 — 2023-2026 加速器出貨與資料中心開工量 | 資本支出計畫大幅下修 |
| [[CH-CAPEX-DEMAND]] | 推升 ↑ | 0–12 | 0.85 | 營建、設備、電力設施的實體需求 | 已實現 | 投資轉為海外或閒置產能吸收 |
| [[ST-POWER-CONSTRAINT]] | 推升 ↑ | 6–24 | 0.8 | 單一園區用電量級距躍升，超出既有電網規劃 | 已實現 — 多國出現併網排隊 | 電網容量充裕 |

## ⚠️ 反向力量與已知限制

**這條線最大的風險是它太容易測量，因而被過度重視。** 資本支出是實體、可見、可統計的，所以分析容易集中在這裡；但如果 AI 的經濟意義最終來自生產力而非建設，那麼把注意力放在 capex 就是在看錯地方。這張圖對 capex 通道的信心較高（已實現），對生產力通道的信心較低（理論推導）——**那反映的是證據狀態，不是重要性排序。**

## 觀察指標

- 主要雲端商季度資本支出指引
- 資料中心新開工面積
- 加速器出貨量

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
