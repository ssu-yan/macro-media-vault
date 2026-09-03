---
id: ST-LNG-SUBST
label: LNG 替代與接收站擴建
type: state
domain: 能源
status: 進行中
aliases:
  - lng 替代
  - 液化天然氣
edges:
  - to: OUT-EU-GAS-PRICE
    sign: -1
    lag_months: [12, 30]
    confidence: 0.8
    mechanism: "替代氣源補足缺口（接收站需先建成）"
    evidence: "已實現 — 2023 TTF 回落至戰前附近"
    breaks_if: "LNG 產能瓶頸"
  - to: OUT-US-LNG-EXPORT
    sign: 1
    lag_months: [3, 24]
    confidence: 0.85
    mechanism: "歐洲需求拉動美國出口與新建產能"
    evidence: "已實現"
    breaks_if: "出口設施審批受阻"
---
# LNG 替代與接收站擴建

`ST-LNG-SUBST` ｜ state ｜ 能源 ｜ 狀態：進行中

歐洲快速擴建 LNG 接收能力，美國與卡達出口增加。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-EU-GAS-PRICE]] | 抑制 ↓ | 12–30 | 0.8 | 替代氣源補足缺口（接收站需先建成） | 已實現 — 2023 TTF 回落至戰前附近 | LNG 產能瓶頸 |
| [[OUT-US-LNG-EXPORT]] | 推升 ↑ | 3–24 | 0.85 | 歐洲需求拉動美國出口與新建產能 | 已實現 | 出口設施審批受阻 |

## 觀察指標

- 歐洲 LNG 接收站產能
- 美國 LNG 出口量

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
