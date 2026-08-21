---
id: ST-RU-EXPORT-INFRA-DAMAGE
label: 俄羅斯能源出口與煉油設施實體受損
type: state
domain: 能源
status: 進行中
aliases:
  - 俄油港受損
  - 煉油廠被炸
  - Novorossiysk
  - 俄羅斯出口設施
edges:
  - to: OUT-OIL-PRICE
    sign: 1
    lag_months: [0, 6]
    confidence: 0.55
    mechanism: "Novorossiysk 單一港口原油出口約 2.3 Mbd（Kpler, 2025-10），裝載中斷使該部分供給短期無法出海"
    evidence: "有先例"
    breaks_if: "快速修復，或改由波羅的海與 ESPO 出海"
  - to: ST-RU-ENERGY-REROUTE
    sign: -1
    lag_months: [0, 12]
    confidence: 0.5
    mechanism: "轉向亞洲的折價銷售同樣依賴黑海與波羅的海的裝運能力；裝載受阻會同時限制轉向量"
    evidence: "理論推導"
    breaks_if: "陸路管線（ESPO）吸收轉向量"
  - to: CH-GRAIN-SUPPLY
    sign: 1
    lag_months: [0, 9]
    confidence: 0.45
    mechanism: "Novorossiysk 同時是俄羅斯主要穀物出口港，估佔俄穀物出口 15–20%；油品與穀物裝載受同一組港口作業限制"
    evidence: "理論推導"
    breaks_if: "穀物泊位與油品泊位實際互不影響"
---
# 俄羅斯能源出口與煉油設施實體受損

`ST-RU-EXPORT-INFRA-DAMAGE` ｜ state ｜ 能源 ｜ 狀態：進行中

交戰方以長程打擊破壞對方的油港、煉油與裝載設施。補上既有俄烏子圖缺的一條機制：ST-SANCTIONS（制裁）與 ST-RU-ENERGY-REROUTE（轉向折價）都不是「出口與煉油設施被實體摧毀」。2026-08-12 烏軍打擊 Novorossiysk 油港即落在此缺口。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[OUT-OIL-PRICE]] | 推升 ↑ | 0–6 | 0.55 | Novorossiysk 單一港口原油出口約 2.3 Mbd（Kpler, 2025-10），裝載中斷使該部分供給短期無法出海 | 有先例 | 快速修復，或改由波羅的海與 ESPO 出海 |
| [[ST-RU-ENERGY-REROUTE]] | 抑制 ↓ | 0–12 | 0.5 | 轉向亞洲的折價銷售同樣依賴黑海與波羅的海的裝運能力；裝載受阻會同時限制轉向量 | 理論推導 | 陸路管線（ESPO）吸收轉向量 |
| [[CH-GRAIN-SUPPLY]] | 推升 ↑ | 0–9 | 0.45 | Novorossiysk 同時是俄羅斯主要穀物出口港，估佔俄穀物出口 15–20%；油品與穀物裝載受同一組港口作業限制 | 理論推導 | 穀物泊位與油品泊位實際互不影響 |

## ⚠️ 反向力量與已知限制

**第二條邊（→ ST-RU-ENERGY-REROUTE，sign −1）是全圖少數會削弱既有反向力量的邊，要特別小心。** ST-RU-ENERGY-REROUTE 記錄了「制裁沒讓俄油退出市場，只改變流向與價差」這個 2022 年被大幅高估的教訓。本節點宣稱實體破壞會**限制轉向能力**，等於部分抵消那條教訓。**信心刻意壓在 0.50、證據等級誠實標為理論推導**：陸路管線（ESPO）與波羅的海港口確實可以吸收相當部分的轉向量，這條邊有可能根本不成立。

**修復速度是這個節點最大的不確定來源，而圖無法表達它。** 油港泊位與煉油裝置的修復期從數天到數月不等，取決於命中位置。同一個「被打擊」事件，修復三天與修復三個月的下游效果差一個量級，**圖只有一條邊、一組時滯**。

**穀物那條邊的數字來源最弱。** 「佔俄穀物出口 15–20%」目前只有次級來源，未升級到 USDA／IGC。信心 0.45、標理論推導已反映這點，但**若要拿這條邊做任何判斷，應先把數字換掉。**

**單一港口的集中度可能被高估。** Novorossiysk 重要，但俄羅斯尚有 Primorsk、Ust-Luga（波羅的海）與 Kozmino（ESPO／太平洋）等出口路徑。**「打掉一個港口 = 抽走等量出口」是錯的**——實際效果取決於其他港口的閒置運能，而圖沒有表達這個緩衝。

## 觀察指標

- 俄羅斯海運原油出口量
- Novorossiysk 與 Sheskharis 裝載量
- 俄羅斯煉油產能利用率
- 黑海穀物出口量

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
