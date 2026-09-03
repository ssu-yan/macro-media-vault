---
id: CH-REAL-INCOME
label: 家庭實質所得下降
type: channel
domain: 經濟
status: 已緩解
aliases:
  - 實質所得
  - 購買力
edges:
  - to: OUT-EU-GDP
    sign: -1
    lag_months: [3, 18]
    confidence: 0.7
    mechanism: "消費是 GDP 最大組成"
    evidence: "已實現"
    breaks_if: "儲蓄釋出支撐消費"
---
# 家庭實質所得下降

`CH-REAL-INCOME` ｜ channel ｜ 經濟 ｜ 狀態：已緩解

通膨快於名目薪資成長時，實質購買力下降。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-EU-GDP]] | 抑制 ↓ | 3–18 | 0.7 | 消費是 GDP 最大組成 | 已實現 | 儲蓄釋出支撐消費 |

## ⚠️ 反向力量與已知限制

2022-23 年歐美的超額儲蓄顯著緩衝了這條邊。實質所得下降並沒有立刻造成消費崩跌——這一點跟本 vault 的 [[S5-情緒與支出脫鉤]] 觀察到的現象是同一件事。

## 觀察指標

- 實質可支配所得
- 儲蓄率

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
