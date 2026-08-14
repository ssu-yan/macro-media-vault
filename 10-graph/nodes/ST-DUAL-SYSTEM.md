---
id: ST-DUAL-SYSTEM
label: 技術與供應鏈雙軌化
type: state
domain: 政治
status: 進行中
aliases:
  - 雙軌化
  - 脫鉤
  - 技術分岔
edges:
  - to: CH-CAPEX-DUPLICATE
    sign: 1
    lag_months: [12, 60]
    confidence: 0.65
    mechanism: "兩套體系各自建設"
    evidence: "理論推導"
    breaks_if: "互通性維持"
  - to: OUT-GLOBAL-TRADE
    sign: -1
    lag_months: [24, 84]
    confidence: 0.45
    mechanism: "貿易密度下降"
    evidence: "理論推導 — 全球貿易佔 GDP 比重變化緩慢"
    breaks_if: "貿易轉向而非減少"
  - to: CH-RISK-PREMIUM
    sign: 1
    lag_months: [12, 60]
    confidence: 0.4
    mechanism: "制度不確定性上升"
    evidence: "理論推導"
    breaks_if: "制度化後不確定性反而下降"
---
# 技術與供應鏈雙軌化

`ST-DUAL-SYSTEM` ｜ state ｜ 政治 ｜ 狀態：進行中

標準、供應鏈、資本市場逐步分為兩套並行體系。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[CH-CAPEX-DUPLICATE]] | 推升 ↑ | 12–60 | 0.65 | 兩套體系各自建設 | 理論推導 | 互通性維持 |
| [[OUT-GLOBAL-TRADE]] | 抑制 ↓ | 24–84 | 0.45 | 貿易密度下降 | 理論推導 — 全球貿易佔 GDP 比重變化緩慢 | 貿易轉向而非減少 |
| [[CH-RISK-PREMIUM]] | 推升 ↑ | 12–60 | 0.4 | 制度不確定性上升 | 理論推導 | 制度化後不確定性反而下降 |

## ⚠️ 反向力量與已知限制

**「脫鉤」在資料上遠不如敘事上明顯。** 全球貿易佔 GDP 比重過去數年並未顯著下滑，多數變化是**流向重組**而非**總量萎縮**。這個節點的所有下游邊信心都壓在 0.45 以下，反映的是敘事與資料之間的落差。

## 觀察指標

- 全球貿易佔 GDP 比重
- 雙邊貿易佔比變化
- 技術標準組織的分歧

---

> 本檔由 `engine/seed_uschina.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
