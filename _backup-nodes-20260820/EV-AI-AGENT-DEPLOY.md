---
id: EV-AI-AGENT-DEPLOY
label: AI 代理人進入生產環境
type: event
domain: AI
status: 進行中
date: 2025-01-01
aliases:
  - ai 代理人
  - ai agent
  - agentic ai
  - 自主代理
edges:
  - to: ST-TASK-SUBSTITUTION
    sign: 1
    lag_months: [6, 36]
    confidence: 0.55
    mechanism: "特定白領任務可被端到端替代"
    evidence: "理論推導 — 目前僅有零星個案"
    breaks_if: "代理人可靠度不足以承擔責任"
  - to: CH-PRODUCTIVITY
    sign: 1
    lag_months: [12, 60]
    confidence: 0.45
    mechanism: "若替代成立，單位產出所需人時下降"
    evidence: "理論推導"
    breaks_if: "生產力統計捕捉不到"
  - to: S4-敘事加速
    sign: 1
    lag_months: [0, 24]
    confidence: 0.3
    mechanism: "大量資金由讀相似資訊源的代理人管理"
    evidence: "理論推導 — S4 在沙盤中未檢驗"
    breaks_if: "代理人策略高度分化"
---
# AI 代理人進入生產環境

`EV-AI-AGENT-DEPLOY` ｜ event ｜ AI ｜ 狀態：進行中

從輔助工具轉為可自主完成多步驟工作流程的系統。與上一個節點的差別：capex 是投入，這個是產出開始接觸真實工作流程的時點。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[ST-TASK-SUBSTITUTION]] | 推升 ↑ | 6–36 | 0.55 | 特定白領任務可被端到端替代 | 理論推導 — 目前僅有零星個案 | 代理人可靠度不足以承擔責任 |
| [[CH-PRODUCTIVITY]] | 推升 ↑ | 12–60 | 0.45 | 若替代成立，單位產出所需人時下降 | 理論推導 | 生產力統計捕捉不到 |
| [[S4-敘事加速]] | 推升 ↑ | 0–24 | 0.3 | 大量資金由讀相似資訊源的代理人管理 | 理論推導 — S4 在沙盤中未檢驗 | 代理人策略高度分化 |

## ⚠️ 反向力量與已知限制

**歷史上通用技術的生產力效果幾乎都遲到很久。** 電力、電腦都出現過數十年的「生產力悖論」。Solow 那句「電腦時代到處看得見，就是不在生產力統計裡」講的正是這個。所以這個節點下游的所有邊，時滯都設得很長、信心都設得很低——**如果它們錯，最可能的錯法是「方向對但太早」。**

## 觀察指標

- 企業導入率調查
- 軟體業入門職缺數
- 單位勞動成本

---

> 本檔由 `engine/seed_ai.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
