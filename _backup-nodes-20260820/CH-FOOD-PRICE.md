---
id: CH-FOOD-PRICE
label: 全球糧價傳導
type: channel
domain: 糧食
status: 已緩解
aliases:
  - 糧價
  - 食品價格
edges:
  - to: OUT-EU-CPI
    sign: 1
    lag_months: [3, 12]
    confidence: 0.75
    mechanism: "食品是 CPI 的重要分項"
    evidence: "已實現"
    breaks_if: "補貼與價格管制"
  - to: OUT-EM-FOOD-STRESS
    sign: 1
    lag_months: [3, 18]
    confidence: 0.7
    mechanism: "糧食進口國的財政與社會壓力"
    evidence: "有先例 — 2008、2011 阿拉伯之春"
    breaks_if: "國際援助與補貼到位"
---
# 全球糧價傳導

`CH-FOOD-PRICE` ｜ channel ｜ 糧食 ｜ 狀態：已緩解

穀物與植物油價格傳導至零售食品價格，時滯約 6–12 個月。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-EU-CPI]] | 推升 ↑ | 3–12 | 0.75 | 食品是 CPI 的重要分項 | 已實現 | 補貼與價格管制 |
| [[OUT-EM-FOOD-STRESS]] | 推升 ↑ | 3–18 | 0.7 | 糧食進口國的財政與社會壓力 | 有先例 — 2008、2011 阿拉伯之春 | 國際援助與補貼到位 |

## ⚠️ 反向力量與已知限制

糧價對已開發國家 CPI 的影響遠小於對進口依賴型新興市場的影響。同一條邊在不同地區的強度差三倍以上——**這張圖目前沒有處理地區異質性，是已知的結構性缺陷。**

## 觀察指標

- FAO 食品價格指數
- 進口依賴國的糧食補貼支出

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
