---
id: ST-DOMESTIC-SUBSIDY
label: 各國產業補貼競賽
type: state
domain: 政治
status: 進行中
aliases:
  - 產業補貼
  - 晶片法案
  - 產業政策
edges:
  - to: CH-CAPEX-DUPLICATE
    sign: 1
    lag_months: [6, 36]
    confidence: 0.75
    mechanism: "補貼驅動的重複產能"
    evidence: "已實現"
    breaks_if: "補貼未落實"
  - to: OUT-SEMI-STOCKS
    sign: -1
    lag_months: [36, 84]
    confidence: 0.45
    mechanism: "產能大幅擴張最終侵蝕議價能力（適應性反向）"
    evidence: "有先例 — 半導體週期史上多次"
    breaks_if: "需求成長吸收新增產能"
---
# 各國產業補貼競賽

`ST-DOMESTIC-SUBSIDY` ｜ state ｜ 政治 ｜ 狀態：進行中

半導體、電池、關鍵礦物的本土化補貼。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[CH-CAPEX-DUPLICATE]] | 推升 ↑ | 6–36 | 0.75 | 補貼驅動的重複產能 | 已實現 | 補貼未落實 |
| [[OUT-SEMI-STOCKS]] | 抑制 ↓ | 36–84 | 0.45 | 產能大幅擴張最終侵蝕議價能力（適應性反向） | 有先例 — 半導體週期史上多次 | 需求成長吸收新增產能 |

## ⚠️ 反向力量與已知限制

**補貼建成的產能會在數年後同時到位，這是半導體週期的經典劇本。** 反向邊的時滯下界設在 36 個月是刻意的（G1 教訓）：晶圓廠從動土到量產約 3–5 年。

## 觀察指標

- 各國補貼落實金額
- 新建晶圓廠產能與投產時程
- 產能利用率

---

> 本檔由 `engine/seed_uschina.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
