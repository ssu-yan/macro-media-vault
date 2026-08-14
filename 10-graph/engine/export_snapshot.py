#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把整張圖 + 認識論設定匯出成單一 JSON 快照。

用途：讓**沒有 vault 的 session**（排程、無人值守）也能跑傳導引擎。
排程任務每次是全新雲端 session，裝置橋接不保證在——沒有這個快照，
G3 的每週掃描根本執行不了。

    python3 export_snapshot.py [輸出路徑]
"""
import os, re, sys, glob, json, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
NODES = os.path.normpath(os.path.join(HERE, "..", "nodes"))
EPIS = os.path.normpath(os.path.join(HERE, "..", "epistemic.yaml"))

nodes = []
for path in sorted(glob.glob(os.path.join(NODES, "*.md"))):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        continue
    fm = yaml.safe_load(m.group(1)) or {}
    if "id" not in fm:
        continue
    body = text[m.end():]
    cm = re.search(r"## ⚠️ 反向力量與已知限制\n(.*?)(?=\n## |\n---|\Z)", body, re.S)
    fm["_counter"] = cm.group(1).strip() if cm else ""
    fm["edges"] = fm.get("edges") or []
    nodes.append(fm)

snap = {
    "generated_note": "由 export_snapshot.py 產生；供無 vault 的排程 session 使用",
    "node_count": len(nodes),
    "nodes": nodes,
    "epistemic": yaml.safe_load(open(EPIS, encoding="utf-8")) if os.path.exists(EPIS) else None,
}
outp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "graph_snapshot.json")
json.dump(snap, open(outp, "w", encoding="utf-8"), ensure_ascii=False,
          indent=1, default=str)   # date 物件轉字串
print("已匯出 %d 個節點 → %s（%.0f KB）"
      % (len(nodes), outp, os.path.getsize(outp) / 1024))
