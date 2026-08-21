---
id: ST-CHINA-RETALIATE
label: 中國反制措施
type: state
domain: 政治
status: 進行中
aliases:
  - 中國反制
  - 稀土管制
  - 關鍵礦物
edges:
  - to: OUT-RARE-EARTH
    sign: 1
    lag_months: [0, 12]
    confidence: 0.7
    mechanism: "供給集中度極高，管制立即反映在價格"
    evidence: "已實現 — 多次公告後價格跳升"
    breaks_if: "替代來源或庫存充足"
  - to: CH-INPUT-PRICE
    sign: 1
    lag_months: [3, 18]
    confidence: 0.5
    mechanism: "關鍵礦物進入電動車、風電、國防供應鏈"
    evidence: "理論推導 — 佔終端成本比重通常不高"
    breaks_if: "佔比太小或可替代"
  - to: ST-DUAL-SYSTEM
    sign: 1
    lag_months: [12, 48]
    confidence: 0.5
    mechanism: "反制強化雙軌化動能"
    evidence: "理論推導"
    breaks_if: "談判緩和"
---
# 中國反制措施

`ST-CHINA-RETALIATE` ｜ state ｜ 政治 ｜ 狀態：進行中

關鍵礦物出口管制、市場准入限制、反壟斷調查等非關稅手段。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-RARE-EARTH]] | 推升 ↑ | 0–12 | 0.7 | 供給集中度極高，管制立即反映在價格 | 已實現 — 多次公告後價格跳升 | 替代來源或庫存充足 |
| [[CH-INPUT-PRICE]] | 推升 ↑ | 3–18 | 0.5 | 關鍵礦物進入電動車、風電、國防供應鏈 | 理論推導 — 佔終端成本比重通常不高 | 佔比太小或可替代 |
| [[ST-DUAL-SYSTEM]] | 推升 ↑ | 12–48 | 0.5 | 反制強化雙軌化動能 | 理論推導 | 談判緩和 |

## ⚠️ 反向力量與已知限制

**稀土的故事經常被誇大。** 中國在**精煉**環節份額極高，但礦源分布其實較分散，而且過往每次管制都催生了境外精煉產能。價格衝擊通常劇烈但短暫——**這是典型的適應性反向力量案例，時滯約 2–5 年。**

## 觀察指標

- 稀土與關鍵礦物價格
- 境外精煉產能建設
- 管制清單變動

---

> 本檔由 `engine/seed_uschina.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
