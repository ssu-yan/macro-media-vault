---
id: ST-HORMUZ-DISRUPTION
label: 荷姆茲海峽通行受阻
type: state
domain: 能源
status: 進行中
aliases:
  - 荷姆茲海峽
  - 荷姆茲受阻
  - strait of hormuz
edges:
  - to: OUT-OIL-PRICE
    sign: 1
    lag_months: [0, 6]
    confidence: 0.8
    mechanism: "全球約五分之一石油液體消費須經此水道；沙國 East-West 與阿聯 Fujairah 繞道管線合計運能遠低於通過量，短期無等量替代"
    evidence: "有先例"
    breaks_if: "替代管線與協調釋儲補足缺口"
  - to: CH-SHIPPING-COST
    sign: 1
    lag_months: [0, 6]
    confidence: 0.7
    mechanism: "波灣裝運船舶的航程風險、待泊與繞行時間上升"
    evidence: "有先例"
    breaks_if: "通行恢復"
  - to: CH-ENERGY-SUPPLY
    sign: 1
    lag_months: [0, 9]
    confidence: 0.6
    mechanism: "全球約五分之一 LNG 貿易經荷姆茲（主要卡達），而歐洲自 2022 年後對 LNG 進口的依賴顯著上升"
    evidence: "有先例"
    breaks_if: "歐洲 LNG 來源已充分轉向大西洋盆地"
  - to: ST-SPR-DEMAND
    sign: 1
    lag_months: [2, 12]
    confidence: 0.7
    mechanism: "供給錯配本身觸發協調釋儲與需求端政策反應（負回饋）"
    evidence: "有先例"
    breaks_if: "政治上無法釋儲且需求無彈性"
  - to: CH-INPUT-COST
    sign: 1
    lag_months: [1, 12]
    confidence: 0.55
    mechanism: "能源是工業與農業核心投入，波灣供給錯配經到岸成本進入投入面"
    evidence: "理論推導"
    breaks_if: "能源價格未實質上升"
---
# 荷姆茲海峽通行受阻

`ST-HORMUZ-DISRUPTION` ｜ state ｜ 能源 ｜ 狀態：進行中

波灣原油與卡達 LNG 唯一的海上出口通道受軍事行動限制。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-OIL-PRICE]] | 推升 ↑ | 0–6 | 0.8 | 全球約五分之一石油液體消費須經此水道；沙國 East-West 與阿聯 Fujairah 繞道管線合計運能遠低於通過量，短期無等量替代 | 有先例 | 替代管線與協調釋儲補足缺口 |
| [[CH-SHIPPING-COST]] | 推升 ↑ | 0–6 | 0.7 | 波灣裝運船舶的航程風險、待泊與繞行時間上升 | 有先例 | 通行恢復 |
| [[CH-ENERGY-SUPPLY]] | 推升 ↑ | 0–9 | 0.6 | 全球約五分之一 LNG 貿易經荷姆茲（主要卡達），而歐洲自 2022 年後對 LNG 進口的依賴顯著上升 | 有先例 | 歐洲 LNG 來源已充分轉向大西洋盆地 |
| [[ST-SPR-DEMAND]] | 推升 ↑ | 2–12 | 0.7 | 供給錯配本身觸發協調釋儲與需求端政策反應（負回饋） | 有先例 | 政治上無法釋儲且需求無彈性 |
| [[CH-INPUT-COST]] | 推升 ↑ | 1–12 | 0.55 | 能源是工業與農業核心投入，波灣供給錯配經到岸成本進入投入面 | 理論推導 | 能源價格未實質上升 |

## ⚠️ 反向力量與已知限制

**指向 ST-SPR-DEMAND 那條邊是正向的，但它指向一個負回饋節點。** ST-SPR-DEMAND 既有的兩條出邊（→ OUT-OIL-PRICE −1、→ OUT-EU-GAS-PRICE −1）是負向的，所以荷姆茲受阻**同時**產生「推升油價」與「經釋儲／需求破壞壓低油價」兩條方向相反、時滯不同的路徑。時滯刻意錯開（主推力 0–6 個月、負回饋 2–12 個月）——這是 G1 的教訓：混在一起淨計會錯過「先漲後回」這個真實型態。

**替代管線的運能可能被低估。** 沙國 East-West 與阿聯 Fujairah 的繞道運能相對通過量是小的，但兩者確實存在且戰時會被優先使用。指向 OUT-OIL-PRICE 給 0.80 已考慮這點；若這條線出錯，最可能的錯法是**幅度高估**而非方向錯。

**指向 CH-ENERGY-SUPPLY 借用了一個語意是「歐洲」的節點。** 該節點既有的邊全部建在俄歐天然氣機制上。這裡指向它是合理的（卡達 LNG 經荷姆茲供歐），但**不得反過來拿 CH-ENERGY-SUPPLY 當荷姆茲事件的入口**——那等於改寫節點定義，2026-08-14 已判定過一次。

**地區異質性未處理。** 荷姆茲受阻對亞洲（尤其中、印、日、韓）的衝擊遠大於對美國；圖用單一 OUT-OIL-PRICE 節點代表全球油價是重大簡化。這是 G1 就發現、至今未解的結構性缺陷。

## 觀察指標

- 荷姆茲日通行量
- Brent 與 Dubai 價差
- 卡達 LNG 出港量
- IEA 釋儲決議

---

> 本檔由 `engine/seed_chokepoint.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
