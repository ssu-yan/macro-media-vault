---
id: OUT-SEMI-STOCKS
label: 半導體類股
type: outcome
domain: 市場
status: 可觀察
aliases:
  - 半導體
  - 晶片股
  - semis
edges:
  - to: CH-INDEX-CONCENTRATION
    sign: 1
    lag_months: [0, 18]
    confidence: 0.75
    mechanism: "權值上升推高指數集中度"
    evidence: "已實現"
    breaks_if: "漲幅落後"
---
# 半導體類股

`OUT-SEMI-STOCKS` ｜ outcome ｜ 市場 ｜ 狀態：可觀察

先進製程、加速器、記憶體、設備廠商。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[CH-INDEX-CONCENTRATION]] | 推升 ↑ | 0–18 | 0.75 | 權值上升推高指數集中度 | 已實現 | 漲幅落後 |

## ⚠️ 反向力量與已知限制

這是全圖信心最高的一組邊（多為已實現），但也是**最可能已被定價**的一組。圖能告訴你路徑存在，不能告訴你市場是否已經反映。**這張圖沒有任何估值或預期的概念。**

## 觀察指標

- 半導體類股相對表現
- 前瞻本益比
- 資本支出指引修正

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
