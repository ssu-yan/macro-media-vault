---
id: CH-FISCAL
label: 財政擴張：能源補貼與國防支出
type: channel
domain: 政治
status: 進行中
aliases:
  - 財政擴張
  - 國防支出
  - 能源補貼
edges:
  - to: OUT-DEFENSE-STOCKS
    sign: 1
    lag_months: [0, 36]
    confidence: 0.85
    mechanism: "國防預算上修的直接受益"
    evidence: "已實現 — 2022 後歐洲國防股大漲"
    breaks_if: "預算承諾未落實為訂單"
  - to: OUT-EU-CPI
    sign: 1
    lag_months: [6, 24]
    confidence: 0.35
    mechanism: "財政擴張的需求側推力"
    evidence: "理論推導 — 效果小且有爭議"
    breaks_if: "財政乘數低"
  - to: OUT-EU-GDP
    sign: 1
    lag_months: [3, 18]
    confidence: 0.55
    mechanism: "補貼支撐可支配所得與需求"
    evidence: "已實現"
    breaks_if: "補貼規模不足"
---
# 財政擴張：能源補貼與國防支出

`CH-FISCAL` ｜ channel ｜ 政治 ｜ 狀態：進行中

各國以補貼吸收能源衝擊，同時大幅上修國防預算。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-DEFENSE-STOCKS]] | 推升 ↑ | 0–36 | 0.85 | 國防預算上修的直接受益 | 已實現 — 2022 後歐洲國防股大漲 | 預算承諾未落實為訂單 |
| [[OUT-EU-CPI]] | 推升 ↑ | 6–24 | 0.35 | 財政擴張的需求側推力 | 理論推導 — 效果小且有爭議 | 財政乘數低 |
| [[OUT-EU-GDP]] | 推升 ↑ | 3–18 | 0.55 | 補貼支撐可支配所得與需求 | 已實現 | 補貼規模不足 |

## 觀察指標

- 各國國防支出佔 GDP 比
- 能源補貼財政成本

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
