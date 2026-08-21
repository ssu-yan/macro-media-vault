---
id: ST-EFFICIENCY-GAIN
label: 演算法與硬體效率提升
type: state
domain: AI
status: 進行中
aliases:
  - 效率提升
  - 推論成本下降
edges:
  - to: ST-COMPUTE-DEMAND
    sign: -1
    lag_months: [12, 36]
    confidence: 0.4
    mechanism: "同樣能力需要更少算力"
    evidence: "理論推導 — 但 Jevons 悖論方向可能相反"
    breaks_if: "總需求隨可行應用擴張而上升"
  - to: OUT-ELEC-PRICE
    sign: -1
    lag_months: [18, 48]
    confidence: 0.35
    mechanism: "單位運算耗電下降"
    evidence: "理論推導"
    breaks_if: "總量成長蓋過效率"
---
# 演算法與硬體效率提升

`ST-EFFICIENCY-GAIN` ｜ state ｜ AI ｜ 狀態：進行中

每單位能力所需的算力與電力持續下降。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[ST-COMPUTE-DEMAND]] | 抑制 ↓ | 12–36 | 0.4 | 同樣能力需要更少算力 | 理論推導 — 但 Jevons 悖論方向可能相反 | 總需求隨可行應用擴張而上升 |
| [[OUT-ELEC-PRICE]] | 抑制 ↓ | 18–48 | 0.35 | 單位運算耗電下降 | 理論推導 | 總量成長蓋過效率 |

## ⚠️ 反向力量與已知限制

**這條反向邊的方向本身就不確定。** 歷史上效率提升經常擴大而非縮小總消耗（Jevons 悖論）。我把它放進圖裡並給低信心，是為了標示「這裡有一股方向未定的力量」，不是為了主張它會壓低需求。

## 觀察指標

- 每 token 推論成本
- 資料中心 PUE
- 單位能力的訓練算力

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
