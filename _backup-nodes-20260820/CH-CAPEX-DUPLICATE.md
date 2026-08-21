---
id: CH-CAPEX-DUPLICATE
label: 重複建設的資本支出
type: channel
domain: 經濟
status: 進行中
aliases:
  - 重複建設
  - 產能重複
edges:
  - to: OUT-GDP-CAPEX
    sign: 1
    lag_months: [6, 36]
    confidence: 0.6
    mechanism: "短期計入固定投資，推升成長"
    evidence: "已實現"
    breaks_if: "投資未落實"
  - to: OUT-CAPITAL-EFFICIENCY
    sign: -1
    lag_months: [24, 84]
    confidence: 0.55
    mechanism: "長期看是同樣產出用了更多資本"
    evidence: "理論推導"
    breaks_if: "重複產能被需求成長吸收"
---
# 重複建設的資本支出

`CH-CAPEX-DUPLICATE` ｜ channel ｜ 經濟 ｜ 狀態：進行中

同樣的產能在多個地區各建一次。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-GDP-CAPEX]] | 推升 ↑ | 6–36 | 0.6 | 短期計入固定投資，推升成長 | 已實現 | 投資未落實 |
| [[OUT-CAPITAL-EFFICIENCY]] | 抑制 ↓ | 24–84 | 0.55 | 長期看是同樣產出用了更多資本 | 理論推導 | 重複產能被需求成長吸收 |

## ⚠️ 反向力量與已知限制

**這條通道的短期與長期方向相反，而且這不是矛盾，是同一件事的兩面：** 重複建設在建的時候是 GDP 的加項，建完之後是資本效率的減項。圖用兩條不同時滯的邊表達，但**讀的人很容易只看到自己想看的那一條。**

## 觀察指標

- 固定投資佔 GDP
- 產能利用率
- 資本報酬率

---

> 本檔由 `engine/seed_uschina.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
