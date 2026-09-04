---
id: EV-TARIFF-ESCALATION
label: 美中關稅升級
type: event
domain: 政治
status: 進行中
date: 2018-07-06
aliases:
  - 關稅升級
  - 美中關稅
  - 貿易戰
  - tariff
  - trade war
edges:
  - to: CH-TRADE-COST
    sign: 1
    lag_months: [0, 6]
    confidence: 0.9
    mechanism: "關稅直接進入到岸成本"
    evidence: "已實現"
    breaks_if: "豁免或轉單吸收"
  - to: ST-SUPPLY-RELOCATE
    sign: 1
    lag_months: [6, 36]
    confidence: 0.75
    mechanism: "成本與政策風險驅動產能外移"
    evidence: "已實現 — 對美出口的來源國結構已明顯改變"
    breaks_if: "移轉成本高於關稅"
  - to: ST-CHINA-RETALIATE
    sign: 1
    lag_months: [0, 12]
    confidence: 0.7
    mechanism: "對等反制與非關稅手段"
    evidence: "已實現"
    breaks_if: "談判達成緩和"
  - to: ST-CN-DEMAND-WEAK
    sign: 1
    lag_months: [6, 24]
    confidence: 0.4
    mechanism: "出口部門受壓抑"
    evidence: "理論推導 — 中國內需疲弱另有房地產等更大成因"
    breaks_if: "出口轉向第三市場補足"
  - to: S7-政策不確定性溢價
    sign: 1
    lag_months: [0, 3]
    confidence: 0.65
    mechanism: "Caldara et al.（Fed IFDP 1256, 2019）的 TPU 指數由關稅相關的報紙報導與法說會逐字稿建構，量測期涵蓋 2017 至 2018 的關稅升級。關稅升級與 TPU 上升是同一組文本事件，不是推論"
    evidence: "已實現"
    breaks_if: "關稅措施推出時政策不確定性指數不上升"
---
# 美中關稅升級

`EV-TARIFF-ESCALATION` ｜ event ｜ 政治 ｜ 狀態：進行中

2018 年起的多輪關稅措施與其後的反覆調整。這是本子圖最容易定日期、也最容易觀察後果的入口。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[CH-TRADE-COST]] | 推升 ↑ | 0–6 | 0.9 | 關稅直接進入到岸成本 | 已實現 | 豁免或轉單吸收 |
| [[ST-SUPPLY-RELOCATE]] | 推升 ↑ | 6–36 | 0.75 | 成本與政策風險驅動產能外移 | 已實現 — 對美出口的來源國結構已明顯改變 | 移轉成本高於關稅 |
| [[ST-CHINA-RETALIATE]] | 推升 ↑ | 0–12 | 0.7 | 對等反制與非關稅手段 | 已實現 | 談判達成緩和 |
| [[ST-CN-DEMAND-WEAK]] | 推升 ↑ | 6–24 | 0.4 | 出口部門受壓抑 | 理論推導 — 中國內需疲弱另有房地產等更大成因 | 出口轉向第三市場補足 |
| [[S7-政策不確定性溢價]] | 推升 ↑ | 0–3 | 0.65 | Caldara et al.（Fed IFDP 1256, 2019）的 TPU 指數由關稅相關的報紙報導與法說會逐字稿建構，量測期涵蓋 2017 至 2018 的關稅升級。關稅升級與 TPU 上升是同一組文本事件，不是推論 | 已實現 | 關稅措施推出時政策不確定性指數不上升 |

## ⚠️ 反向力量與已知限制

**關稅的最終負擔由誰承擔，實證上長期有爭議。** 早期研究多半發現主要由進口國的進口商與消費者承擔，但後續也有匯率與供應商讓價部分吸收的證據。這張圖把 `CH-TRADE-COST → OUT-US-CPI` 的信心設在 0.50，反映的正是這個爭議，不是我的猶豫。

另一個常被忽略的事實：**轉單不等於脫鉤**。對美出口來源從中國轉向第三國，但那些國家對中國中間財的依賴反而上升。所以 `ST-SUPPLY-RELOCATE` 抑制風險的效果被高估的可能性很大。

## 觀察指標

- 有效關稅稅率
- 對美進口的來源國結構
- 第三國對中國中間財進口

---

> 本檔由 `engine/seed_uschina.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
