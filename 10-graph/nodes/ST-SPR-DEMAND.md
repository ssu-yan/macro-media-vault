---
id: ST-SPR-DEMAND
label: 戰略儲備釋出與需求破壞
type: state
domain: 能源
status: 已發生
aliases:
  - 戰略儲備
  - spr
  - 需求破壞
edges:
  - to: OUT-OIL-PRICE
    sign: -1
    lag_months: [0, 12]
    confidence: 0.7
    mechanism: "供給增加與需求減少同時作用"
    evidence: "已實現 — 2022H2 油價回落"
    breaks_if: "儲備耗盡且需求剛性"
  - to: OUT-EU-GAS-PRICE
    sign: -1
    lag_months: [3, 18]
    confidence: 0.65
    mechanism: "工業減產與家庭節能降低用氣"
    evidence: "已實現 — 歐洲工業用氣顯著下降"
    breaks_if: "需求無彈性"
---
# 戰略儲備釋出與需求破壞

`ST-SPR-DEMAND` ｜ state ｜ 能源 ｜ 狀態：已發生

IEA 協調釋出戰略石油儲備、OPEC+ 增產、以及高價本身造成的需求減少。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-OIL-PRICE]] | 抑制 ↓ | 0–12 | 0.7 | 供給增加與需求減少同時作用 | 已實現 — 2022H2 油價回落 | 儲備耗盡且需求剛性 |
| [[OUT-EU-GAS-PRICE]] | 抑制 ↓ | 3–18 | 0.65 | 工業減產與家庭節能降低用氣 | 已實現 — 歐洲工業用氣顯著下降 | 需求無彈性 |

## ⚠️ 反向力量與已知限制

需求破壞是雙面刃：它壓低價格，但方式是透過抑制實體經濟活動。價格回落本身可能是壞消息。

## 觀察指標

- 歐洲工業用氣量
- OECD 石油庫存

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
