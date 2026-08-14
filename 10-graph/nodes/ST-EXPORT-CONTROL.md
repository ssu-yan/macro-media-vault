---
id: ST-EXPORT-CONTROL
label: 半導體出口管制
type: state
domain: 政治
status: 進行中
aliases:
  - 出口管制
  - 晶片管制
  - export control
edges:
  - to: ST-MODEL-COMMODITIZE
    sign: 1
    lag_months: [12, 48]
    confidence: 0.45
    mechanism: "受限方轉向效率路線與開源生態"
    evidence: "理論推導 — 已有跡象但因果難分"
    breaks_if: "受限方無法追上"
  - to: OUT-SEMI-STOCKS
    sign: -1
    lag_months: [0, 18]
    confidence: 0.4
    mechanism: "市場被切割，部分營收失去"
    evidence: "已實現 — 特定廠商中國營收下滑"
    breaks_if: "豁免或替代市場補足"
---
# 半導體出口管制

`ST-EXPORT-CONTROL` ｜ state ｜ 政治 ｜ 狀態：進行中

先進晶片與設備的跨國流動限制。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[ST-MODEL-COMMODITIZE]] | 推升 ↑ | 12–48 | 0.45 | 受限方轉向效率路線與開源生態 | 理論推導 — 已有跡象但因果難分 | 受限方無法追上 |
| [[OUT-SEMI-STOCKS]] | 抑制 ↓ | 0–18 | 0.4 | 市場被切割，部分營收失去 | 已實現 — 特定廠商中國營收下滑 | 豁免或替代市場補足 |

## ⚠️ 反向力量與已知限制

管制的效果高度不確定，而且可能與意圖相反：它同時抑制對手取得算力、又逼對手往效率與開源方向走。**俄烏子圖的制裁節點給過一模一樣的教訓——制裁沒讓俄油退出市場，只改變了流向與價差。**

## 觀察指標

- 管制清單變動
- 受限地區的模型能力追趕速度

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
