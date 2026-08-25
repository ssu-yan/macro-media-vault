# -*- coding: utf-8 -*-
"""依 claude/G3-調參提案-2026-08-25.md（時間戳 2026-08-25T14:57:10Z）調整
   ST-RU-EXPORT-INFRA-DAMAGE -> CH-GRAIN-SUPPLY 一條邊。
   Wendy 於 2026-08-25 核可。

   變更：mechanism 文字、confidence 0.45->0.70、evidence 理論推導->已實現、
        breaks_if 改寫。sign 與 lag_months 不動。
"""
import io, sys, shutil

F = "seed_ruua.py"
s = io.open(F, encoding="utf-8").read()

OLD_EDGE = '("CH-GRAIN-SUPPLY",1,[0,9],0.45,"Novorossiysk 同時是俄羅斯主要穀物出口港，估佔俄穀物出口 15–20%；油品與穀物裝載受同一組港口作業限制","理論推導","穀物泊位與油品泊位實際互不影響")'
NEW_EDGE = '("CH-GRAIN-SUPPLY",1,[0,9],0.70,"Novorossiysk 同時是俄羅斯最大穀物出口港，三個穀物碼頭（NKHP、NZT、KSK）合計年吞吐約 2,500 萬噸，約當俄羅斯海運穀物出口的 40–50%（該國上一季經亞速—黑海盆地出口 4,630 萬噸、佔其海運穀物 88%）；油品與穀物裝載受同一組港口作業限制","已實現","Tuapse 與波羅的海或陸路替代路線在數週內補足受阻運能，或受損碼頭快速復工")'

OLD_CNT = '"**穀物那條邊的數字來源最弱。** 「佔俄穀物出口 15–20%」目前只有次級來源，未升級到 USDA／IGC。信心 0.45、標理論推導已反映這點，但**若要拿這條邊做任何判斷，應先把數字換掉。**"'
NEW_CNT = '"**穀物那條邊的參數於 2026-08-25 依提案調整**（`claude/G3-調參提案-2026-08-25.md`，時間戳 2026-08-25T14:57:10Z，Wendy 核可）。原為 conf 0.45／理論推導／「估佔俄穀物出口 15–20%」，來源是次級商業網站。2026-08 的事實把三項都推翻了：Novorossiysk 三座穀物碼頭（NKHP、NZT、KSK，合計年吞吐約 2,500 萬噸）全部停擺，約當俄羅斯海運穀物出口的 40–50%；原 breaks_if「穀物泊位與油品泊位實際互不影響」**已被證偽**——兩者同時停。evidence 改為已實現，**等於移除這條邊的認識論上限保護**（0.50 → 1.00），所以 confidence 只給 0.70 而非更高，保留三個尚未排除的機制緩衝：**Tuapse 仍在運作**、2026 年約 1.4 億噸強收成、以及**停擺持續時間未知而圖只有一組時滯**。來源等級為產業權威（SovEcon、俄羅斯穀物聯盟），仍非 USDA／IGC 官方統計。"'

if NEW_EDGE in s:
    print("已經改過了，不需再改。"); sys.exit(0)

miss = []
if s.count(OLD_EDGE) != 1: miss.append("edge tuple (找到 %d 次)" % s.count(OLD_EDGE))
if s.count(OLD_CNT)  != 1: miss.append("counter 文字 (找到 %d 次)" % s.count(OLD_CNT))
if miss:
    print("X 找不到：" + "、".join(miss) + " — 未動任何東西。"); sys.exit(1)

shutil.copy(F, F + ".bak3")
s = s.replace(OLD_EDGE, NEW_EDGE).replace(OLD_CNT, NEW_CNT)
io.open(F, "w", encoding="utf-8", newline="\n").write(s)
print("OK 已套用調參（舊檔備份 seed_ruua.py.bak3）")
print("   conf 0.45 -> 0.70 ｜ evidence 理論推導 -> 已實現 ｜ mechanism 與 breaks_if 已改寫")
print("   未動：sign=1、lag_months=[0,9]")
