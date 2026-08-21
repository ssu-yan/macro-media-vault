---
id: CH-INDEX-CONCENTRATION
label: 指數集中度上升
type: channel
domain: 市場
status: 已發生
aliases:
  - 指數集中度
  - 市值集中
edges:
  - to: OUT-EQUITY-CONCENTRATION
    sign: 1
    lag_months: [0, 24]
    confidence: 0.85
    mechanism: "直接定義關係"
    evidence: "已實現"
    breaks_if: "漲勢擴散"
  - to: OUT-REAL-RATES
    sign: 1
    lag_months: [12, 48]
    confidence: 0.25
    mechanism: "估值對利率敏感度上升是結果非原因"
    evidence: "理論推導 — 因果方向可疑"
    breaks_if: "無關"
---
# 指數集中度上升

`CH-INDEX-CONCENTRATION` ｜ channel ｜ 市場 ｜ 狀態：已發生

少數大型公司佔指數市值比重上升。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-EQUITY-CONCENTRATION]] | 推升 ↑ | 0–24 | 0.85 | 直接定義關係 | 已實現 | 漲勢擴散 |
| [[OUT-REAL-RATES]] | 推升 ↑ | 12–48 | 0.25 | 估值對利率敏感度上升是結果非原因 | 理論推導 — 因果方向可疑 | 無關 |

## ⚠️ 反向力量與已知限制

**集中度上升與本 vault 沙盤層的 [[S3-信念離散度上升]] 方向相反。** S3 預測離散度上升、相關性下降；指數集中度上升通常伴隨相關性上升。V6 的結果（2005 年後相關性回升至 0.55）與集中度敘事一致，與 S3 的媒體敘事不一致。**這是兩層之間一個真實的張力，不是矛盾——但值得記著。**

## 觀察指標

- 前十大成分股市值佔比
- 等權 vs 市值加權指數的表現差

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
