---
id: OUT-EM-FOOD-STRESS
label: 新興市場糧食壓力與社會動盪
type: outcome
domain: 政治
status: 可觀察
aliases:
  - 糧食危機
  - 新興市場糧食
edges:
  - to: OUT-EM-INSTABILITY
    sign: 1
    lag_months: [6, 24]
    confidence: 0.55
    mechanism: "糧價與燃料價格是歷史上動盪的可靠前導"
    evidence: "有先例 — 2008、2011"
    breaks_if: "補貼與援助到位"
---
# 新興市場糧食壓力與社會動盪

`OUT-EM-FOOD-STRESS` ｜ outcome ｜ 政治 ｜ 狀態：可觀察

糧食進口依賴國的財政壓力與社會不穩。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-EM-INSTABILITY]] | 推升 ↑ | 6–24 | 0.55 | 糧價與燃料價格是歷史上動盪的可靠前導 | 有先例 — 2008、2011 | 補貼與援助到位 |

## 觀察指標

- FAO 食品價格指數
- 進口國補貼支出
- IMF 紓困申請

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
