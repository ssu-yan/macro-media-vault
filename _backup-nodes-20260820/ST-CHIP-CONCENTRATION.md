---
id: ST-CHIP-CONCENTRATION
label: 先進製程與加速器供給集中
type: state
domain: AI
status: 已發生
aliases:
  - 晶片集中
  - 先進製程
  - 加速器供給
edges:
  - to: OUT-SEMI-STOCKS
    sign: 1
    lag_months: [0, 18]
    confidence: 0.8
    mechanism: "議價能力與毛利率提升"
    evidence: "已實現"
    breaks_if: "產能大幅擴張稀釋議價力"
  - to: CH-INDEX-CONCENTRATION
    sign: 1
    lag_months: [0, 24]
    confidence: 0.7
    mechanism: "少數公司市值佔比上升"
    evidence: "已實現 — 指數集中度創數十年新高"
    breaks_if: "漲勢擴散至其他類股"
  - to: ST-EXPORT-CONTROL
    sign: 1
    lag_months: [0, 12]
    confidence: 0.6
    mechanism: "戰略物資屬性引發管制"
    evidence: "已實現"
    breaks_if: "地緣政治緩和"
---
# 先進製程與加速器供給集中

`ST-CHIP-CONCENTRATION` ｜ state ｜ AI ｜ 狀態：已發生

先進邏輯製程、先進封裝、高頻寬記憶體的產能集中在極少數供應商與地理位置。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-SEMI-STOCKS]] | 推升 ↑ | 0–18 | 0.8 | 議價能力與毛利率提升 | 已實現 | 產能大幅擴張稀釋議價力 |
| [[CH-INDEX-CONCENTRATION]] | 推升 ↑ | 0–24 | 0.7 | 少數公司市值佔比上升 | 已實現 — 指數集中度創數十年新高 | 漲勢擴散至其他類股 |
| [[ST-EXPORT-CONTROL]] | 推升 ↑ | 0–12 | 0.6 | 戰略物資屬性引發管制 | 已實現 | 地緣政治緩和 |

## ⚠️ 反向力量與已知限制

**集中度上升同時是報酬來源與風險來源。** 同一個事實既支撐半導體類股的重評價，也讓整個市場對單一供應鏈事件的脆弱度上升。這兩條邊方向相反卻同源——**任何只講其中一邊的分析都是不完整的。**

## 觀察指標

- 先進製程產能份額
- 前十大成分股市值佔比
- HBM 供需

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
