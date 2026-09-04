---
id: ST-RU-GAS-CUT
label: 俄羅斯對歐天然氣供應削減
type: state
domain: 能源
status: 已發生
aliases:
  - 北溪
  - 俄羅斯斷氣
  - 天然氣減供
edges:
  - to: CH-ENERGY-SUPPLY
    sign: 1
    lag_months: [0, 3]
    confidence: 0.95
    mechanism: "歐洲最大單一氣源退出"
    evidence: "已實現"
    breaks_if: "管線恢復輸送"
  - to: ST-LNG-SUBST
    sign: 1
    lag_months: [3, 18]
    confidence: 0.85
    mechanism: "歐洲轉向美國與卡達 LNG 並加建接收站"
    evidence: "已實現 — 2022-23 歐洲 LNG 進口創高"
    breaks_if: "LNG 供給無法擴張"
  - to: OUT-EU-RENEW-CAPEX
    sign: 1
    lag_months: [6, 36]
    confidence: 0.75
    mechanism: "能源安全成為政治優先，加速再生能源與電網投資"
    evidence: "已實現 — REPowerEU"
    breaks_if: "政策轉向或財政受限"
---
# 俄羅斯對歐天然氣供應削減

`ST-RU-GAS-CUT` ｜ state ｜ 能源 ｜ 狀態：已發生

2022 年俄對歐管線氣量逐步降至接近零，北溪一號於 9 月停止輸送。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[CH-ENERGY-SUPPLY]] | 推升 ↑ | 0–3 | 0.95 | 歐洲最大單一氣源退出 | 已實現 | 管線恢復輸送 |
| [[ST-LNG-SUBST]] | 推升 ↑ | 3–18 | 0.85 | 歐洲轉向美國與卡達 LNG 並加建接收站 | 已實現 — 2022-23 歐洲 LNG 進口創高 | LNG 供給無法擴張 |
| [[OUT-EU-RENEW-CAPEX]] | 推升 ↑ | 6–36 | 0.75 | 能源安全成為政治優先，加速再生能源與電網投資 | 已實現 — REPowerEU | 政策轉向或財政受限 |

## ⚠️ 反向力量與已知限制

這條邊的短期強度極高，但它同時觸發了兩股強力的反向力量（LNG 替代、再生能源投資），使得中期效果反轉——2023 年歐洲天然氣價格已回落至戰前水準附近。**衝擊越大，誘發的適應反應也越大。**

## 觀察指標

- 歐洲天然氣庫存率
- LNG 進口量
- TTF 期貨曲線

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
