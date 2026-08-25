# -*- coding: utf-8 -*-
import io, sys, shutil
 
F = "seed_ruua.py"
s = io.open(F, encoding="utf-8").read()
 
if "ST-RU-EXPORT-INFRA-DAMAGE" in s:
    print("已經改過了，不需再改。"); sys.exit(0)
 
A1 = '"衝突降溫且平台介入有效")],'
NEW_EDGE = ('"衝突降溫且平台介入有效"),\n      '
            + '("ST-RU-EXPORT-INFRA-DAMAGE",1,[24,60],0.75,"長程打擊能力累積後，交戰方將對方能源出口與煉油設施列為目標。Novorossiysk 為俄羅斯最大黑海石油出口港，2025 年原油出口約 2.3 Mbd，其中 Sheskharis 終端約 830 kbd（占該港約 36%）；CPC 管線（設計運能約 1.4–1.7 Mbd）亦經此港區出海。單一港區集中度高，成規模打擊可抽走可定日期的一大塊出口量","已實現","停火，或防空使打擊無法奏效")],')
A2 = 'node("ST-DEDOLLAR"'
NEW_NODE = 'node("ST-RU-EXPORT-INFRA-DAMAGE","俄羅斯能源出口與煉油設施實體受損","state","能源","進行中",\n     ["俄油港受損","煉油廠被炸","Novorossiysk","俄羅斯出口設施"],\n     "交戰方以長程打擊破壞對方的油港、煉油與裝載設施。"\n     "補上既有俄烏子圖缺的一條機制：ST-SANCTIONS（制裁）與 ST-RU-ENERGY-REROUTE（轉向折價）"\n     "都不是「出口與煉油設施被實體摧毀」。2026-08-12 烏軍打擊 Novorossiysk 油港即落在此缺口。",\n     [("OUT-OIL-PRICE",1,[0,6],0.55,"Novorossiysk 單一港口原油出口約 2.3 Mbd（Kpler, 2025-10），裝載中斷使該部分供給短期無法出海","有先例","快速修復，或改由波羅的海與 ESPO 出海"),\n      ("ST-RU-ENERGY-REROUTE",-1,[0,12],0.50,"轉向亞洲的折價銷售同樣依賴黑海與波羅的海的裝運能力；裝載受阻會同時限制轉向量","理論推導","陸路管線（ESPO）吸收轉向量"),\n      ("CH-GRAIN-SUPPLY",1,[0,9],0.45,"Novorossiysk 同時是俄羅斯主要穀物出口港，估佔俄穀物出口 15–20%；油品與穀物裝載受同一組港口作業限制","理論推導","穀物泊位與油品泊位實際互不影響")],\n     counter=["**第二條邊（→ ST-RU-ENERGY-REROUTE，sign −1）是全圖少數會削弱既有反向力量的邊，要特別小心。** ST-RU-ENERGY-REROUTE 記錄了「制裁沒讓俄油退出市場，只改變流向與價差」這個 2022 年被大幅高估的教訓。本節點宣稱實體破壞會**限制轉向能力**，等於部分抵消那條教訓。**信心刻意壓在 0.50、證據等級誠實標為理論推導**：陸路管線（ESPO）與波羅的海港口確實可以吸收相當部分的轉向量，這條邊有可能根本不成立。",\n              "**修復速度是這個節點最大的不確定來源，而圖無法表達它。** 油港泊位與煉油裝置的修復期從數天到數月不等，取決於命中位置。同一個「被打擊」事件，修復三天與修復三個月的下游效果差一個量級，**圖只有一條邊、一組時滯**。",\n              "**穀物那條邊的數字來源最弱。** 「佔俄穀物出口 15–20%」目前只有次級來源，未升級到 USDA／IGC。信心 0.45、標理論推導已反映這點，但**若要拿這條邊做任何判斷，應先把數字換掉。**",\n              "**單一港口的集中度可能被高估。** Novorossiysk 重要，但俄羅斯尚有 Primorsk、Ust-Luga（波羅的海）與 Kozmino（ESPO／太平洋）等出口路徑。**「打掉一個港口 = 抽走等量出口」是錯的**——實際效果取決於其他港口的閒置運能，而圖沒有表達這個緩衝。"],\n     watch=["俄羅斯海運原油出口量","Novorossiysk 與 Sheskharis 裝載量","俄羅斯煉油產能利用率","黑海穀物出口量"])\n\n'
 
if s.count(A1) != 1:
    print("X 找不到改動 1 的位置，未動任何東西。"); sys.exit(1)
if s.count(A2) != 1:
    print("X 找不到改動 2 的位置，未動任何東西。"); sys.exit(1)
 
shutil.copy(F, F + ".bak")
s = s.replace(A1, NEW_EDGE).replace(A2, NEW_NODE + A2)
io.open(F, "w", encoding="utf-8", newline="\n").write(s)
n = s.count("ST-RU-EXPORT-INFRA-DAMAGE")
print("OK 改好了（舊檔備份為 seed_ruua.py.bak）")
print("   ST-RU-EXPORT-INFRA-DAMAGE 出現 %d 次（應為 2）" % n)
 