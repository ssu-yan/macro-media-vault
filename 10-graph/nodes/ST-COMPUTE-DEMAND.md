---
id: ST-COMPUTE-DEMAND
label: 算力需求擴張
type: state
domain: AI
status: 進行中
aliases:
  - 算力需求
  - compute demand
edges:
  - to: ST-CHIP-CONCENTRATION
    sign: 1
    lag_months: [0, 12]
    confidence: 0.85
    mechanism: "需求集中於少數能供應先進製程與封裝的廠商"
    evidence: "已實現"
    breaks_if: "製程競爭者追上"
  - to: CH-ELEC-COST
    sign: 1
    lag_months: [6, 24]
    confidence: 0.7
    mechanism: "算力即用電"
    evidence: "已實現"
    breaks_if: "效率提升抵消"
  - to: ST-EFFICIENCY-GAIN
    sign: 1
    lag_months: [12, 36]
    confidence: 0.7
    mechanism: "成本與供給壓力驅動效率研發（負回饋）"
    evidence: "已實現 — 推論成本持續下降"
    breaks_if: "無進一步效率空間"
---
# 算力需求擴張

`ST-COMPUTE-DEMAND` ｜ state ｜ AI ｜ 狀態：進行中

訓練與推論的算力需求。推論需求隨使用量成長，比訓練更持續。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[ST-CHIP-CONCENTRATION]] | 推升 ↑ | 0–12 | 0.85 | 需求集中於少數能供應先進製程與封裝的廠商 | 已實現 | 製程競爭者追上 |
| [[CH-ELEC-COST]] | 推升 ↑ | 6–24 | 0.7 | 算力即用電 | 已實現 | 效率提升抵消 |
| [[ST-EFFICIENCY-GAIN]] | 推升 ↑ | 12–36 | 0.7 | 成本與供給壓力驅動效率研發（負回饋） | 已實現 — 推論成本持續下降 | 無進一步效率空間 |

## ⚠️ 反向力量與已知限制

**Jevons 悖論在這裡是雙向的。** 效率提升會降低單位算力成本，但也會讓更多應用變得可行，總需求可能反而上升。所以 ST-EFFICIENCY-GAIN 對這個節點的抑制邊信心只給 0.40——**方向甚至可能是錯的。**

## 觀察指標

- 加速器出貨量
- 推論 vs 訓練的算力佔比
- 每 token 成本

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
