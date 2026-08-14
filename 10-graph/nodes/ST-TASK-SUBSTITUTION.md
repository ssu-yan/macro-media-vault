---
id: ST-TASK-SUBSTITUTION
label: 特定白領任務被替代
type: state
domain: 經濟
status: 進行中
aliases:
  - 任務替代
  - 白領替代
  - 工作自動化
edges:
  - to: OUT-WHITE-COLLAR-JOBS
    sign: -1
    lag_months: [12, 48]
    confidence: 0.45
    mechanism: "入門職缺最先受影響"
    evidence: "理論推導 — 目前證據混雜且難與景氣區分"
    breaks_if: "需求擴張吸收釋出的勞動力"
  - to: CH-LABOR-COST
    sign: -1
    lag_months: [18, 60]
    confidence: 0.4
    mechanism: "議價能力下降抑制工資成長"
    evidence: "理論推導"
    breaks_if: "勞動市場仍緊俏"
  - to: CH-PRODUCTIVITY
    sign: 1
    lag_months: [12, 60]
    confidence: 0.45
    mechanism: "單位產出所需人時下降"
    evidence: "理論推導"
    breaks_if: "組織調整跟不上"
---
# 特定白領任務被替代

`ST-TASK-SUBSTITUTION` ｜ state ｜ 經濟 ｜ 狀態：進行中

注意是**任務**層級而非職業層級——多數職業由多個任務組成，替代通常先發生在任務層。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-WHITE-COLLAR-JOBS]] | 抑制 ↓ | 12–48 | 0.45 | 入門職缺最先受影響 | 理論推導 — 目前證據混雜且難與景氣區分 | 需求擴張吸收釋出的勞動力 |
| [[CH-LABOR-COST]] | 抑制 ↓ | 18–60 | 0.4 | 議價能力下降抑制工資成長 | 理論推導 | 勞動市場仍緊俏 |
| [[CH-PRODUCTIVITY]] | 推升 ↑ | 12–60 | 0.45 | 單位產出所需人時下降 | 理論推導 | 組織調整跟不上 |

## ⚠️ 反向力量與已知限制

**這是整張圖裡最容易被過度解讀的節點。** 入門職缺減少同時可以用升息、後疫情正常化、產業週期解釋，而且這幾個解釋在時間上高度重疊。**要把 AI 的貢獻分離出來，需要的識別策略目前沒有人有。** 這跟沙盤 [[S5-情緒與支出脫鉤]] 死掉的原因是同一類：現象存在，歸因無法識別。

## 觀察指標

- 軟體業入門職缺數
- 任務層級的自動化研究
- 單位勞動成本

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
