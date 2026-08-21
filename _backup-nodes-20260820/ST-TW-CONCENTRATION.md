---
id: ST-TW-CONCENTRATION
label: 先進製程的地理集中
type: state
domain: AI
status: 已發生
aliases:
  - 台灣集中度
  - 先進製程集中
edges:
  - to: CH-RISK-PREMIUM
    sign: 1
    lag_months: [0, 24]
    confidence: 0.55
    mechanism: "單點失效風險被市場認知"
    evidence: "已實現 — 已進入主要機構的風險報告"
    breaks_if: "風險被視為已定價"
  - to: OUT-SEMI-STOCKS
    sign: 1
    lag_months: [0, 24]
    confidence: 0.45
    mechanism: "不可替代性支撐議價能力"
    evidence: "已實現"
    breaks_if: "替代產能建成"
  - to: OUT-TW-EQUITY
    sign: 1
    lag_months: [0, 24]
    confidence: 0.5
    mechanism: "樞紐地位支撐本地企業獲利"
    evidence: "已實現"
    breaks_if: "地位被稀釋"
---
# 先進製程的地理集中

`ST-TW-CONCENTRATION` ｜ state ｜ AI ｜ 狀態：已發生

最先進邏輯製程與先進封裝產能高度集中於單一地理區域。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[CH-RISK-PREMIUM]] | 推升 ↑ | 0–24 | 0.55 | 單點失效風險被市場認知 | 已實現 — 已進入主要機構的風險報告 | 風險被視為已定價 |
| [[OUT-SEMI-STOCKS]] | 推升 ↑ | 0–24 | 0.45 | 不可替代性支撐議價能力 | 已實現 | 替代產能建成 |
| [[OUT-TW-EQUITY]] | 推升 ↑ | 0–24 | 0.5 | 樞紐地位支撐本地企業獲利 | 已實現 | 地位被稀釋 |

## ⚠️ 反向力量與已知限制

**集中度同時是獲利來源與風險來源**——與 AI 子圖 `ST-CHIP-CONCENTRATION` 的結構完全相同。任何只講其中一面的分析都不完整。

## 觀察指標

- 先進製程產能地理分布
- 海外新廠投產進度
- 半導體庫存天數

---

> 本檔由 `engine/seed_uschina.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
