---
id: EV-RU-UA-2022
label: 俄羅斯全面入侵烏克蘭
type: event
domain: 戰爭
status: 已發生
date: 2022-02-24
aliases:
  - 俄烏戰爭
  - 烏俄戰爭
  - 烏克蘭戰爭
  - 俄羅斯入侵烏克蘭
  - russia ukraine war
  - ukraine invasion
edges:
  - to: ST-BLACKSEA
    sign: 1
    lag_months: [0, 1]
    confidence: 0.95
    mechanism: "黑海港口封鎖、航運保險費暴漲"
    evidence: "已實現 — 2022/2 敖德薩等港停擺"
    breaks_if: "黑海航道恢復通航且保險費正常化"
  - to: ST-SANCTIONS
    sign: 1
    lag_months: [0, 2]
    confidence: 0.95
    mechanism: "西方對俄金融、能源、技術制裁"
    evidence: "已實現 — 2022/2-6 多輪制裁"
    breaks_if: "制裁解除或普遍不執行"
  - to: ST-RU-GAS-CUT
    sign: 1
    lag_months: [1, 6]
    confidence: 0.85
    mechanism: "俄羅斯以減供作為反制槓桿"
    evidence: "已實現 — 2022 北溪流量降至零"
    breaks_if: "俄歐能源關係正常化"
  - to: ST-UA-FARMLAND
    sign: 1
    lag_months: [1, 12]
    confidence: 0.9
    mechanism: "耕地成戰場、勞動力徵召、機具與倉儲毀損"
    evidence: "已實現 — 2022 烏克蘭穀物產量大減"
    breaks_if: "戰事結束且農業重建完成"
  - to: CH-FISCAL
    sign: 1
    lag_months: [1, 12]
    confidence: 0.85
    mechanism: "國防預算上修與能源補貼同時擴張"
    evidence: "已實現 — 2022 起歐洲國防支出大幅上修"
    breaks_if: "財政緊縮壓過安全考量"
  - to: ST-INFO-WAR
    sign: 1
    lag_months: [0, 3]
    confidence: 0.8
    mechanism: "雙方資訊戰與平台演算法放大對立敘事"
    evidence: "有先例 — 2014 克里米亞"
    breaks_if: "衝突降溫且平台介入有效"
  - to: ST-RU-EXPORT-INFRA-DAMAGE
    sign: 1
    lag_months: [24, 60]
    confidence: 0.75
    mechanism: "長程打擊能力累積後，交戰方將對方能源出口與煉油設施列為目標。Novorossiysk 為俄羅斯最大黑海石油出口港，2025 年原油出口約 2.3 Mbd，其中 Sheskharis 終端約 830 kbd（占該港約 36%）；CPC 管線（設計運能約 1.4–1.7 Mbd）亦經此港區出海。單一港區集中度高，成規模打擊可抽走可定日期的一大塊出口量"
    evidence: "已實現"
    breaks_if: "停火，或防空使打擊無法奏效"
---
# 俄羅斯全面入侵烏克蘭

`EV-RU-UA-2022` ｜ event ｜ 戰爭 ｜ 狀態：已發生

2022-02-24 俄羅斯對烏克蘭發動全面軍事行動。本圖以此為根節點，示範一個事件如何沿多條通道傳導到可觀察的經濟與市場結果。

## 下游邊

| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |
|---|---|---|---|---|---|---|
| [[ST-BLACKSEA]] | 推升 ↑ | 0–1 | 0.95 | 黑海港口封鎖、航運保險費暴漲 | 已實現 — 2022/2 敖德薩等港停擺 | 黑海航道恢復通航且保險費正常化 |
| [[ST-SANCTIONS]] | 推升 ↑ | 0–2 | 0.95 | 西方對俄金融、能源、技術制裁 | 已實現 — 2022/2-6 多輪制裁 | 制裁解除或普遍不執行 |
| [[ST-RU-GAS-CUT]] | 推升 ↑ | 1–6 | 0.85 | 俄羅斯以減供作為反制槓桿 | 已實現 — 2022 北溪流量降至零 | 俄歐能源關係正常化 |
| [[ST-UA-FARMLAND]] | 推升 ↑ | 1–12 | 0.9 | 耕地成戰場、勞動力徵召、機具與倉儲毀損 | 已實現 — 2022 烏克蘭穀物產量大減 | 戰事結束且農業重建完成 |
| [[CH-FISCAL]] | 推升 ↑ | 1–12 | 0.85 | 國防預算上修與能源補貼同時擴張 | 已實現 — 2022 起歐洲國防支出大幅上修 | 財政緊縮壓過安全考量 |
| [[ST-INFO-WAR]] | 推升 ↑ | 0–3 | 0.8 | 雙方資訊戰與平台演算法放大對立敘事 | 有先例 — 2014 克里米亞 | 衝突降溫且平台介入有效 |
| [[ST-RU-EXPORT-INFRA-DAMAGE]] | 推升 ↑ | 24–60 | 0.75 | 長程打擊能力累積後，交戰方將對方能源出口與煉油設施列為目標。Novorossiysk 為俄羅斯最大黑海石油出口港，2025 年原油出口約 2.3 Mbd，其中 Sheskharis 終端約 830 kbd（占該港約 36%）；CPC 管線（設計運能約 1.4–1.7 Mbd）亦經此港區出海。單一港區集中度高，成規模打擊可抽走可定日期的一大塊出口量 | 已實現 | 停火，或防空使打擊無法奏效 |

## ⚠️ 反向力量與已知限制

戰爭本身不必然造成全球衝擊——關鍵在於交戰方在關鍵商品供應鏈上的份額。俄烏合計約佔全球小麥出口三成、俄羅斯佔歐洲天然氣進口約四成，這才是傳導的原因。同規模但非資源出口國的衝突，下游影響會小一個量級。

## 觀察指標

- 黑海航運量
- 北溪與烏克蘭過境管線流量
- 烏克蘭播種面積

---

> 本檔由 `engine/seed_ruua.py` 產生，**請勿直接編輯**。
> 要改內容請改該腳本再重跑。
