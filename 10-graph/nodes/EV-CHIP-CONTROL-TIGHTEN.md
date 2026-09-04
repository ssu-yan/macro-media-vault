---
id: EV-CHIP-CONTROL-TIGHTEN
label: 半導體出口管制收緊
type: event
domain: 政治
status: 進行中
date: 2022-10-07
aliases:
  - 晶片管制收緊
  - 出口管制
  - entity list
  - 半導體管制
edges:
  - to: ST-EXPORT-CONTROL
    sign: 1
    lag_months: [0, 6]
    confidence: 0.9
    mechanism: "直接的法規效果"
    evidence: "已實現"
    breaks_if: "管制放寬"
  - to: ST-DUAL-SYSTEM
    sign: 1
    lag_months: [12, 60]
    confidence: 0.6
    mechanism: "技術標準與供應鏈分岔為兩套"
    evidence: "理論推導 — 目前僅部分領域出現"
    breaks_if: "互通性維持"
  - to: ST-TW-CONCENTRATION
    sign: 1
    lag_months: [0, 24]
    confidence: 0.45
    mechanism: "管制強化了既有樞紐的不可替代性"
    evidence: "理論推導"
    breaks_if: "替代產能建成"
  - to: ST-DOMESTIC-SUBSIDY
    sign: 1
    lag_months: [6, 36]
    confidence: 0.8
    mechanism: "各國以補貼建立本土產能"
    evidence: "已實現 — 多國已立法"
    breaks_if: "財政緊縮"
  - to: S7-政策不確定性溢價
    sign: 1
    lag_months: [0, 6]
    confidence: 0.45
    mechanism: "出口管制與關稅同屬貿易政策工具，管制清單擴大同樣以政策文本形式擴散。但 Fed 的 TPU 指數建構並未明說涵蓋出口管制，故本條為類比推導"
    evidence: "理論推導"
    breaks_if: "管制措施的文本擴散不進入政策不確定性指數"
---
# 半導體出口管制收緊

`EV-CHIP-CONTROL-TIGHTEN` ｜ event ｜ 政治 ｜ 狀態：進行中

先進運算晶片、半導體設備與相關技術的出口限制逐步擴大。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[ST-EXPORT-CONTROL]] | 推升 ↑ | 0–6 | 0.9 | 直接的法規效果 | 已實現 | 管制放寬 |
| [[ST-DUAL-SYSTEM]] | 推升 ↑ | 12–60 | 0.6 | 技術標準與供應鏈分岔為兩套 | 理論推導 — 目前僅部分領域出現 | 互通性維持 |
| [[ST-TW-CONCENTRATION]] | 推升 ↑ | 0–24 | 0.45 | 管制強化了既有樞紐的不可替代性 | 理論推導 | 替代產能建成 |
| [[ST-DOMESTIC-SUBSIDY]] | 推升 ↑ | 6–36 | 0.8 | 各國以補貼建立本土產能 | 已實現 — 多國已立法 | 財政緊縮 |
| [[S7-政策不確定性溢價]] | 推升 ↑ | 0–6 | 0.45 | 出口管制與關稅同屬貿易政策工具，管制清單擴大同樣以政策文本形式擴散。但 Fed 的 TPU 指數建構並未明說涵蓋出口管制，故本條為類比推導 | 理論推導 | 管制措施的文本擴散不進入政策不確定性指數 |

## ⚠️ 反向力量與已知限制

**俄烏子圖的制裁節點給過完全一樣的教訓：管制改變流向與價差，不必然改變總量。** 那次我高估了制裁對石油供給的效果。這裡的對應風險是高估管制對算力取得的效果——受限方會轉向效率路線、走私、或第三地採購。已在 AI 子圖的 `ST-EXPORT-CONTROL` 節點寫明。

## 觀察指標

- 管制清單變動
- 設備出口許可核發率
- 受限地區的先進製程進展

---

> 本檔由 `engine/seed_uschina.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
