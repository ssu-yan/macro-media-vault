---
id: CH-RISK-PREMIUM
label: 地緣風險溢價
type: channel
domain: 市場
status: 進行中
aliases:
  - 地緣風險溢價
  - 風險溢價
edges:
  - to: OUT-GOLD
    sign: 1
    lag_months: [0, 18]
    confidence: 0.55
    mechanism: "避險資產需求"
    evidence: "有先例"
    breaks_if: "實質利率主導"
  - to: OUT-DEFENSE-STOCKS
    sign: 1
    lag_months: [0, 36]
    confidence: 0.7
    mechanism: "國防預算與訂單預期"
    evidence: "已實現"
    breaks_if: "預算未落實"
  - to: OUT-TW-EQUITY
    sign: -1
    lag_months: [0, 12]
    confidence: 0.55
    mechanism: "風險溢價直接壓縮本地估值"
    evidence: "有先例 — 歷次緊張期已觀察到"
    breaks_if: "已充分定價"
  - to: OUT-SEMI-STOCKS
    sign: -1
    lag_months: [0, 12]
    confidence: 0.4
    mechanism: "供應鏈單點風險被重新定價"
    evidence: "有先例"
    breaks_if: "市場忽略"
---
# 地緣風險溢價

`CH-RISK-PREMIUM` ｜ channel ｜ 市場 ｜ 狀態：進行中

市場對地緣事件的定價。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-GOLD]] | 推升 ↑ | 0–18 | 0.55 | 避險資產需求 | 有先例 | 實質利率主導 |
| [[OUT-DEFENSE-STOCKS]] | 推升 ↑ | 0–36 | 0.7 | 國防預算與訂單預期 | 已實現 | 預算未落實 |
| [[OUT-TW-EQUITY]] | 抑制 ↓ | 0–12 | 0.55 | 風險溢價直接壓縮本地估值 | 有先例 — 歷次緊張期已觀察到 | 已充分定價 |
| [[OUT-SEMI-STOCKS]] | 抑制 ↓ | 0–12 | 0.4 | 供應鏈單點風險被重新定價 | 有先例 | 市場忽略 |

## ⚠️ 反向力量與已知限制

**地緣風險溢價的半衰期通常很短。** 歷史上多數地緣事件的市場影響在數週到數月內消退，除非它實際改變了現金流。這條通道的所有邊都應該預期**幅度大但持續性差**——而圖沒有表達持續性的能力。

## 觀察指標

- 黃金
- 區域股市風險溢價
- 選擇權隱含波動

---

> 本檔由 `engine/seed_uschina.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
