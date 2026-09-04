---
id: CH-GRAIN-SUPPLY
label: 穀物供給衝擊
type: channel
domain: 糧食
status: 已緩解
aliases:
  - 小麥供給
  - 穀物供給
edges:
  - to: OUT-WHEAT-PRICE
    sign: 1
    lag_months: [0, 3]
    confidence: 0.9
    mechanism: "供給預期下修推升期貨價格"
    evidence: "已實現 — 2022/3 小麥期貨創高"
    breaks_if: "其他產區增產補足"
  - to: CH-FOOD-PRICE
    sign: 1
    lag_months: [1, 9]
    confidence: 0.8
    mechanism: "穀物是食品價格的上游投入"
    evidence: "已實現"
    breaks_if: "傳導被補貼吸收"
---
# 穀物供給衝擊

`CH-GRAIN-SUPPLY` ｜ channel ｜ 糧食 ｜ 狀態：已緩解

俄烏合計約佔全球小麥出口三成、葵花油約七成。供給預期的改變先於實際短缺反映在價格上。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-WHEAT-PRICE]] | 推升 ↑ | 0–3 | 0.9 | 供給預期下修推升期貨價格 | 已實現 — 2022/3 小麥期貨創高 | 其他產區增產補足 |
| [[CH-FOOD-PRICE]] | 推升 ↑ | 1–9 | 0.8 | 穀物是食品價格的上游投入 | 已實現 | 傳導被補貼吸收 |

## ⚠️ 反向力量與已知限制

價格在 2022 年 3 月見高後於年內大幅回落。**期貨市場對供給衝擊的反應通常在數週內就過度反映，然後修正。** 這條邊的方向可靠，持續性不可靠。

## 觀察指標

- CBOT 小麥期貨
- USDA 期末庫存比

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
