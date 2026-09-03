---
id: ST-SANCTIONS
label: 西方對俄金融與能源制裁
type: state
domain: 政治
status: 進行中
aliases:
  - 對俄制裁
  - 制裁俄羅斯
  - sanctions russia
edges:
  - to: ST-RU-ENERGY-REROUTE
    sign: 1
    lag_months: [1, 9]
    confidence: 0.85
    mechanism: "俄油氣轉向中印等買家並以折價成交"
    evidence: "已實現 — Urals 對 Brent 折價擴大"
    breaks_if: "制裁解除"
  - to: CH-ENERGY-SUPPLY
    sign: 1
    lag_months: [0, 6]
    confidence: 0.7
    mechanism: "西方自我限制採購造成短期供給錯配"
    evidence: "已實現"
    breaks_if: "替代供給到位"
  - to: OUT-GOLD
    sign: 1
    lag_months: [0, 12]
    confidence: 0.55
    mechanism: "央行資產遭凍結促使部分國家分散儲備至黃金"
    evidence: "有先例 — 2022 後各國央行購金創高"
    breaks_if: "儲備體系信任未受影響"
  - to: ST-DEDOLLAR
    sign: 1
    lag_months: [6, 60]
    confidence: 0.4
    mechanism: "非西方國家尋求降低美元結算依賴"
    evidence: "理論推導 — 進展緩慢且規模有限"
    breaks_if: "美元結算份額維持穩定"
---
# 西方對俄金融與能源制裁

`ST-SANCTIONS` ｜ state ｜ 政治 ｜ 狀態：進行中

包含部分銀行排除於 SWIFT、央行資產凍結、油價上限、技術出口管制。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[ST-RU-ENERGY-REROUTE]] | 推升 ↑ | 1–9 | 0.85 | 俄油氣轉向中印等買家並以折價成交 | 已實現 — Urals 對 Brent 折價擴大 | 制裁解除 |
| [[CH-ENERGY-SUPPLY]] | 推升 ↑ | 0–6 | 0.7 | 西方自我限制採購造成短期供給錯配 | 已實現 | 替代供給到位 |
| [[OUT-GOLD]] | 推升 ↑ | 0–12 | 0.55 | 央行資產遭凍結促使部分國家分散儲備至黃金 | 有先例 — 2022 後各國央行購金創高 | 儲備體系信任未受影響 |
| [[ST-DEDOLLAR]] | 推升 ↑ | 6–60 | 0.4 | 非西方國家尋求降低美元結算依賴 | 理論推導 — 進展緩慢且規模有限 | 美元結算份額維持穩定 |

## ⚠️ 反向力量與已知限制

制裁的能源效果被大幅高估過。俄羅斯原油出口量在制裁後並未崩跌，只是流向改變、折價擴大。對全球供給總量的影響遠小於對價差結構的影響。

## 觀察指標

- Urals 對 Brent 折價
- 俄羅斯原油海運出口量
- 各國央行黃金購買量

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
