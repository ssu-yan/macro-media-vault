---
id: ST-MODEL-COMMODITIZE
label: 模型能力商品化
type: state
domain: AI
status: 進行中
aliases:
  - 開源模型
  - 模型商品化
  - 能力追趕
edges:
  - to: OUT-SEMI-STOCKS
    sign: -1
    lag_months: [12, 36]
    confidence: 0.4
    mechanism: "若模型層不賺錢，算力採購的持續性受質疑"
    evidence: "理論推導"
    breaks_if: "推論需求成長蓋過"
  - to: OUT-CORP-MARGINS
    sign: 1
    lag_months: [12, 48]
    confidence: 0.4
    mechanism: "使用者端以低成本取得能力，成本下降"
    evidence: "理論推導"
    breaks_if: "能力仍集中於少數供應商"
  - to: L4-集中化vs碎片化
    sign: -1
    lag_months: [12, 60]
    confidence: 0.45
    mechanism: "開源普及推向碎片化那一端"
    evidence: "理論推導 — L4 在沙盤中標為難以檢驗"
    breaks_if: "前沿與開源差距重新拉大"
---
# 模型能力商品化

`ST-MODEL-COMMODITIZE` ｜ state ｜ AI ｜ 狀態：進行中

開源與次級供應商的能力與前沿差距縮小，模型層本身的議價能力下降。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-SEMI-STOCKS]] | 抑制 ↓ | 12–36 | 0.4 | 若模型層不賺錢，算力採購的持續性受質疑 | 理論推導 | 推論需求成長蓋過 |
| [[OUT-CORP-MARGINS]] | 推升 ↑ | 12–48 | 0.4 | 使用者端以低成本取得能力，成本下降 | 理論推導 | 能力仍集中於少數供應商 |
| [[L4-集中化vs碎片化]] | 抑制 ↓ | 12–60 | 0.45 | 開源普及推向碎片化那一端 | 理論推導 — L4 在沙盤中標為難以檢驗 | 前沿與開源差距重新拉大 |

## ⚠️ 反向力量與已知限制

**這個節點與 [[L4-集中化vs碎片化]] 是同一個問題的兩個面向**，但沙盤把 L4 標為「難以檢驗」，所以那條邊的上限是 0.35。這是刻意的：跨層的邊不應該比它指向的節點更確定。

## 觀察指標

- 開源與前沿模型的 benchmark 落差
- 模型 API 價格趨勢
- 推論市場份額分布

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
