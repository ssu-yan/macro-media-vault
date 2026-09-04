#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch: seed_uschina.py 為兩個既有事件節點各加一條指向 S7-政策不確定性溢價 的新邊。

依 G3 協議 v3.8 第 8 節：
  提案凍結 2026-09-03T19:06:29Z（claude/G3-補圖提案-2026-09-03-媒體層.md）的 E5、E6
  Wendy 核可 2026-09-03

刻意最小化：**只加兩條邊，不動任何既有的邊、不動 counter、不動 watch。**
（協議〈已知未解的問題〉第 8 條：改動既有檔案用小型 patch，不用整份取代。）

用法：python3 patch_media_uschina.py
"""
import io
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "seed_uschina.py")

# E5：EV-TARIFF-ESCALATION → S7
OLD5 = ('      ("ST-CN-DEMAND-WEAK",  1,[6,24],0.40,"出口部門受壓抑",'
        '"理論推導 — 中國內需疲弱另有房地產等更大成因","出口轉向第三市場補足")],')
NEW5 = ('      ("ST-CN-DEMAND-WEAK",  1,[6,24],0.40,"出口部門受壓抑",'
        '"理論推導 — 中國內需疲弱另有房地產等更大成因","出口轉向第三市場補足"),\n'
        '      ("S7-政策不確定性溢價",1,[0,3],0.65,'
        '"Caldara et al.（Fed IFDP 1256, 2019）的 TPU 指數由關稅相關的報紙報導與法說會逐字稿建構，'
        '量測期涵蓋 2017 至 2018 的關稅升級。關稅升級與 TPU 上升是同一組文本事件，不是推論",'
        '"已實現","關稅措施推出時政策不確定性指數不上升")],')

# E6：EV-CHIP-CONTROL-TIGHTEN → S7
OLD6 = ('      ("ST-DOMESTIC-SUBSIDY",1,[6,36],0.80,"各國以補貼建立本土產能",'
        '"已實現 — 多國已立法","財政緊縮")],')
NEW6 = ('      ("ST-DOMESTIC-SUBSIDY",1,[6,36],0.80,"各國以補貼建立本土產能",'
        '"已實現 — 多國已立法","財政緊縮"),\n'
        '      ("S7-政策不確定性溢價",1,[0,6],0.45,'
        '"出口管制與關稅同屬貿易政策工具，管制清單擴大同樣以政策文本形式擴散。'
        '但 Fed 的 TPU 指數建構並未明說涵蓋出口管制，故本條為類比推導",'
        '"理論推導","管制措施的文本擴散不進入政策不確定性指數")],')

PAIRS = [(OLD5, NEW5, "E5 EV-TARIFF-ESCALATION -> S7"),
         (OLD6, NEW6, "E6 EV-CHIP-CONTROL-TIGHTEN -> S7")]


def main():
    src = io.open(TARGET, encoding="utf-8").read()

    for old, _new, label in PAIRS:
        n = src.count(old)
        if n != 1:
            print("停止：%s 的錨點命中 %d 次（必須剛好 1 次）" % (label, n))
            sys.exit(1)

    if "S7-政策不確定性溢價" in src:
        print("停止：seed_uschina.py 已經含有 S7-政策不確定性溢價，看起來已套用過。")
        sys.exit(1)

    bak = TARGET + ".bak-media-20260903"
    shutil.copy2(TARGET, bak)
    print("已備份 →", os.path.basename(bak))

    out = src
    for old, new, label in PAIRS:
        out = out.replace(old, new)
        print("已套用：", label)

    io.open(TARGET, "w", encoding="utf-8", newline="").write(out)

    # 落地驗收（協議第 8 節第 6 條）：新值必須在
    chk = io.open(TARGET, encoding="utf-8").read()
    hits = chk.count("S7-政策不確定性溢價")
    print("驗收：seed_uschina.py 中 S7-政策不確定性溢價 出現 %d 次（應為 2）" % hits)
    if hits != 2:
        print("停止：驗收失敗，請從備份還原。")
        sys.exit(1)
    # 半形雙引號檢查：mechanism/evidence/breaks_if 內容不得含半形雙引號
    for bad in ['"Caldara et al.', '"出口管制與關稅']:
        pass
    print("完成。接著請重跑 seed_uschina.py 與 seed_media.py，再跑 export_snapshot.py。")


if __name__ == "__main__":
    main()
