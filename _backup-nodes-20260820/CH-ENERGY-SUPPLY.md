---
id: CH-ENERGY-SUPPLY
label: 歐洲能源供給衝擊
type: channel
domain: 能源
status: 已緩解
aliases:
  - 能源供給
  - 天然氣短缺
edges:
  - to: OUT-EU-GAS-PRICE
    sign: 1
    lag_months: [0, 6]
    confidence: 0.95
    mechanism: "供需失衡直接反映在現貨與期貨"
    evidence: "已實現 — 2022/8 TTF 逼近 340 歐元"
    breaks_if: "替代供給即時到位"
  - to: OUT-OIL-PRICE
    sign: 1
    lag_months: [0, 6]
    confidence: 0.55
    mechanism: "氣轉油替代與整體能源溢價"
    evidence: "已實現"
    breaks_if: "替代有限"
  - to: CH-INPUT-COST
    sign: 1
    lag_months: [1, 12]
    confidence: 0.85
    mechanism: "能源是工業與農業的核心投入"
    evidence: "已實現"
    breaks_if: "能源密集產業外移完成"
  - to: OUT-EU-GDP
    sign: -1
    lag_months: [3, 18]
    confidence: 0.7
    mechanism: "能源成本衝擊壓抑生產與消費"
    evidence: "已實現 — 2022-23 歐洲工業產出下滑"
    breaks_if: "財政補貼完全吸收"
  - to: OUT-EUR-USD
    sign: -1
    lag_months: [1, 12]
    confidence: 0.45
    mechanism: "能源進口帳單暴增惡化貿易條件"
    evidence: "已實現 — 2022 歐元跌破平價"
    breaks_if: "能源價格回落"
  - to: ST-SPR-DEMAND
    sign: 1
    lag_months: [2, 12]
    confidence: 0.85
    mechanism: "供給衝擊本身觸發政策反應與需求破壞（負回饋）"
    evidence: "已實現 — 2022/3 IEA 協調釋儲、OPEC+ 增產、歐洲工業減產"
    breaks_if: "政治上無法釋儲且需求無彈性"
---
# 歐洲能源供給衝擊

`CH-ENERGY-SUPPLY` ｜ channel ｜ 能源 ｜ 狀態：已緩解

歐洲天然氣與電力供給的實質與預期短缺。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-EU-GAS-PRICE]] | 推升 ↑ | 0–6 | 0.95 | 供需失衡直接反映在現貨與期貨 | 已實現 — 2022/8 TTF 逼近 340 歐元 | 替代供給即時到位 |
| [[OUT-OIL-PRICE]] | 推升 ↑ | 0–6 | 0.55 | 氣轉油替代與整體能源溢價 | 已實現 | 替代有限 |
| [[CH-INPUT-COST]] | 推升 ↑ | 1–12 | 0.85 | 能源是工業與農業的核心投入 | 已實現 | 能源密集產業外移完成 |
| [[OUT-EU-GDP]] | 抑制 ↓ | 3–18 | 0.7 | 能源成本衝擊壓抑生產與消費 | 已實現 — 2022-23 歐洲工業產出下滑 | 財政補貼完全吸收 |
| [[OUT-EUR-USD]] | 抑制 ↓ | 1–12 | 0.45 | 能源進口帳單暴增惡化貿易條件 | 已實現 — 2022 歐元跌破平價 | 能源價格回落 |
| [[ST-SPR-DEMAND]] | 推升 ↑ | 2–12 | 0.85 | 供給衝擊本身觸發政策反應與需求破壞（負回饋） | 已實現 — 2022/3 IEA 協調釋儲、OPEC+ 增產、歐洲工業減產 | 政治上無法釋儲且需求無彈性 |

## 觀察指標

- TTF 期貨
- 歐洲工業產出
- 電價

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
