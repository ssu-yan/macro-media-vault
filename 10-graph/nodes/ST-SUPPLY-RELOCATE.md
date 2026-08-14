---
id: ST-SUPPLY-RELOCATE
label: 供應鏈重組
type: state
domain: 經濟
status: 進行中
aliases:
  - 供應鏈重組
  - 近岸外包
  - 友岸外包
  - 去風險
edges:
  - to: CH-CAPEX-DUPLICATE
    sign: 1
    lag_months: [6, 36]
    confidence: 0.7
    mechanism: "同樣的產能要蓋兩次"
    evidence: "已實現"
    breaks_if: "移轉為既有產能利用"
  - to: CH-TRADE-COST
    sign: 1
    lag_months: [6, 30]
    confidence: 0.55
    mechanism: "新產地的效率與規模較低"
    evidence: "理論推導"
    breaks_if: "新產地效率相當"
  - to: CH-RISK-PREMIUM
    sign: -1
    lag_months: [24, 60]
    confidence: 0.45
    mechanism: "多來源降低單點失效風險（適應性反向）"
    evidence: "理論推導 — 需數年才建成"
    breaks_if: "轉單但未真正分散"
---
# 供應鏈重組

`ST-SUPPLY-RELOCATE` ｜ state ｜ 經濟 ｜ 狀態：進行中

產能與採購從單一來源移向多來源、近岸或友岸。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[CH-CAPEX-DUPLICATE]] | 推升 ↑ | 6–36 | 0.7 | 同樣的產能要蓋兩次 | 已實現 | 移轉為既有產能利用 |
| [[CH-TRADE-COST]] | 推升 ↑ | 6–30 | 0.55 | 新產地的效率與規模較低 | 理論推導 | 新產地效率相當 |
| [[CH-RISK-PREMIUM]] | 抑制 ↓ | 24–60 | 0.45 | 多來源降低單點失效風險（適應性反向） | 理論推導 — 需數年才建成 | 轉單但未真正分散 |

## ⚠️ 反向力量與已知限制

**轉單不等於脫鉤。** 對美出口來源改變的同時，那些新來源國對中國中間財的依賴上升。所以這個節點抑制風險的效果很可能被高估——真正的分散要看**增值來源**而非**出口地**。

## 觀察指標

- 對美進口來源國結構
- 第三國對中國中間財進口
- 跨國企業產能投資公告

---

> 本檔由 `engine/seed_uschina.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
