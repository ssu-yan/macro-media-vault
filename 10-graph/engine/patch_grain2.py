# -*- coding: utf-8 -*-
"""
G3 調參落地腳本（第二次）
 
依據：claude/G3-調參提案-2026-09-01.md（凍結於 2026-09-01T22:55:43Z）
核可：Wendy，2026-09-01
 
只改一條邊：ST-RU-EXPORT-INFRA-DAMAGE -> CH-GRAIN-SUPPLY
  confidence  0.70 -> 0.60
  mechanism   運能數字改為與來源一致的「逾 2,000 萬噸」，移除推算出來的份額
  breaks_if   改寫為目前真正未解的機制變數
  evidence / sign / lag_months  刻意不動
並在該節點的 _counter 追加一段變更沿革（含 Wendy 要求的備註）。
 
用法（在 10-graph/engine/ 底下執行）：
    python patch_grain2.py            # 預覽，不寫檔
    python patch_grain2.py --apply    # 實際寫檔（會先備份）
 
⚠️ 這支腳本寫好之後**必須真的執行**。
   2026-08-21 的 patch_grain.py 寫好、存檔、被提案引用為「已修正」，
   但從未在 vault 跑過，8/25 才發現。跑完請務必做第 6 步的 grep 落地驗收。
"""
 
import io
import os
import re
import sys
import shutil
import datetime
 
PATH = "seed_ruua.py"
 
# --- 新的邊（7-tuple 的後半段全部重寫；sign 與 lag_months 維持 1 與 [0,9]）---
NEW_TUPLE = (
    '("CH-GRAIN-SUPPLY",1,[0,9],0.60,'
    '"Novorossiysk 同時是俄羅斯最大穀物出口港，三個穀物碼頭（NKHP、NZT、KSK）'
    '合計年運能逾 2,000 萬噸，其中 NKHP 單座 710 萬噸；該國上一季海運穀物出口 5,270 萬噸，'
    '其中經亞速—黑海盆地 4,630 萬噸、佔其海運穀物 88%，'
    '而黑海與亞速海港口原佔全部穀物出口 70%；'
    '油品與穀物裝載受同一組港口作業限制",'
    '"已實現",'
    '"Delo Group 與 Demetra 的碼頭在 NKHP 修復期內回到常態吞吐，'
    '或 Tuapse、波羅的海與陸路路線補足 NKHP 的 710 萬噸缺口")'
)
 
# --- 追加到 _counter 末尾的變更沿革 ---
COUNTER_ADD = (
    "**本次（2026-09-01 提案）調整**：confidence 0.70→0.60、"
    "mechanism 的運能數字改為與來源一致的「逾 2,000 萬噸」並移除推算出來的份額、"
    "breaks_if 改寫；evidence、sign、lag_months 刻意不動。"
    "起因是 2026-08-26 NKHP 的陳述顯示損害不均："
    "NKHP（710 萬噸／年）重損、修復最長 4 個月，Demetra 的碼頭損害較輕，"
    "Delo Group 的未受損——長期受阻量約當全國海運 13%，而非四到五成。"
    "**0.60 這個數字是 Lucas 編出來的判斷，不是任何來源的估計**，"
    "Wendy 於 2026-09-01 核可時要求明確標註此點。"
    "原本寫的「約 2,500 萬噸／40-50%」在來源中找不到，來源說的是逾 2,000 萬噸；"
    "運能與吞吐的口徑不同，故本次不寫任何推算出來的百分比。"
    "提案見 claude/G3-調參提案-2026-09-01.md（凍結於 2026-09-01T22:55:43Z）。"
)
 
# _counter 末段的錨點（取自現行圖，應唯一）
COUNTER_ANCHOR = "而圖沒有表達這個緩衝。"
 
TUPLE_RE = re.compile(r'\(\s*"CH-GRAIN-SUPPLY"\s*,.*?\)', re.S)
 
 
def fail(msg):
    print("\n[中止] " + msg)
    print("       檔案未被修改。請把這段訊息貼回對話，不要自己手改 seed_ruua.py。")
    sys.exit(1)
 
 
def main():
    apply = "--apply" in sys.argv
 
    if not os.path.exists(PATH):
        fail("找不到 %s。請在 10-graph/engine/ 目錄底下執行這支腳本。" % PATH)
 
    with io.open(PATH, encoding="utf-8") as f:
        src = f.read()
 
    # graphlib 產生 YAML 時這三個欄位用半形雙引號包起來，內容裡不能有半形雙引號
    for name, s in (("NEW_TUPLE", NEW_TUPLE), ("COUNTER_ADD", COUNTER_ADD)):
        body = s[s.index("(") + 1:] if name == "NEW_TUPLE" else s
        if name == "COUNTER_ADD" and '"' in body:
            fail("%s 含半形雙引號，會弄壞 frontmatter。" % name)
 
    # ---- 1. 邊 ----
    # CH-GRAIN-SUPPLY 在 seed_ruua.py 裡會出現多次：
    #   · 節點本身的定義
    #   · ST-BLACKSEA -> CH-GRAIN-SUPPLY
    #   · ST-UA-FARMLAND -> CH-GRAIN-SUPPLY
    #   · ST-RU-EXPORT-INFRA-DAMAGE -> CH-GRAIN-SUPPLY  ← 只有這條要改
    # 所以不能只靠 id 篩選，必須再用 Novorossiysk 這個只出現在目標邊的字串。
    all_hits = TUPLE_RE.findall(src)
    hits = [h for h in all_hits if "Novorossiysk" in h]
 
    if len(hits) != 1:
        print("\n在 %s 找到 %d 處 CH-GRAIN-SUPPLY，其中含 Novorossiysk 的有 %d 處："
              % (PATH, len(all_hits), len(hits)))
        for i, h in enumerate(all_hits, 1):
            flag = "  <== 含 Novorossiysk" if "Novorossiysk" in h else ""
            print("  [%d] %s%s" % (i, h[:110].replace("\n", " "), flag))
        fail("預期剛好 1 處含 Novorossiysk 的邊。")
 
    old_tuple = hits[0]
 
    if "0.60" in old_tuple and "逾 2,000 萬噸" in old_tuple:
        print("[略過] 這條邊看起來已經套用過本次變更，檔案未修改。")
        return
    if "0.70" not in old_tuple:
        fail("目標邊的 confidence 不是 0.70，與提案第 1 節記載的現況不符。\n       現況：" + old_tuple[:200])
 
    # ---- 2. _counter ----
    n_anchor = src.count(COUNTER_ANCHOR)
    if n_anchor != 1:
        fail("_counter 的錨點「%s」出現 %d 次，預期剛好 1 次。" % (COUNTER_ANCHOR, n_anchor))
 
    new_src = src.replace(old_tuple, NEW_TUPLE, 1)
    new_src = new_src.replace(
        COUNTER_ANCHOR,
        COUNTER_ANCHOR + "\\n\\n" + COUNTER_ADD,
        1,
    )
 
    if new_src == src:
        fail("替換後內容沒有變化，邏輯有問題，請回報。")
 
    print("=" * 70)
    print("舊的邊：")
    print(old_tuple)
    print("-" * 70)
    print("新的邊：")
    print(NEW_TUPLE)
    print("-" * 70)
    print("_counter 追加：")
    print(COUNTER_ADD)
    print("=" * 70)
 
    if not apply:
        print("\n這是預覽，沒有寫檔。確認無誤後執行：")
        print("    python patch_grain2.py --apply")
        return
 
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = "%s.bak-%s" % (PATH, stamp)
    shutil.copy2(PATH, backup)
    with io.open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(new_src)
 
    print("\n[完成] 已寫入 %s，備份在 %s" % (PATH, backup))
    print("""
接下來一定要做（協議第 8 節的六件事）：
 
  1. python seed_ruua.py
     python export_snapshot.py
     然後把新的 graph_snapshot.json 上傳到 Project 的 claude/graph-snapshot.json
     （連字號，不是底線）
 
  2. 確認協議第 1 步寫死的數字（本次 81 / 140 不變，仍要確認一次）
 
  3. grep 落地驗收（新值必須在、舊值只能在 _counter 的沿革裡）：
       Select-String -Path seed_ruua.py -Pattern "逾 2,000 萬噸"
       Select-String -Path seed_ruua.py,..\\nodes\\*.md -Pattern "2,500 萬噸"
     第二條會在 _counter 命中，那是刻意保留的沿革；
     若在別處命中，停下來回報。
 
  4. memory/decisions/ 留 after-action，更新 memory-summary.md 的重要決策索引
 
  5. 確認 Git 已同步
""")
 
 
if __name__ == "__main__":
    main()
 