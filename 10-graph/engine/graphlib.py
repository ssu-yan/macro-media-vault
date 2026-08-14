# -*- coding: utf-8 -*-
"""圖譜節點產生器（各領域種子腳本共用）。

格式改一次就好，不用改每一支種子腳本。
"""
import os


class Graph:
    def __init__(self, source="種子腳本"):
        self.N = []
        self.source = source

    def node(self, id, label, type, domain, status, aliases, body,
             edges=(), date=None, counter=(), watch=()):
        self.N.append(dict(
            id=id, label=label, type=type, domain=domain, status=status,
            date=date, aliases=list(aliases), body=body,
            edges=[dict(zip(("to", "s", "lag", "c", "why", "ev", "breaks"), e))
                   for e in edges],
            counter=list(counter), watch=list(watch)))

    def out(self, id, label, domain, body, edges=(), counter=(), watch=(),
            aliases=()):
        self.node(id, label, "outcome", domain, "可觀察", list(aliases), body,
                  edges, counter=counter, watch=watch)

    def write(self, outdir):
        os.makedirs(outdir, exist_ok=True)
        for n in self.N:
            fm = ["---", "id: %s" % n["id"], "label: %s" % n["label"],
                  "type: %s" % n["type"], "domain: %s" % n["domain"],
                  "status: %s" % n["status"]]
            if n["date"]:
                fm.append("date: %s" % n["date"])
            fm.append("aliases:" + (" []" if not n["aliases"] else
                                    "\n" + "\n".join("  - %s" % a for a in n["aliases"])))
            if n["edges"]:
                fm.append("edges:")
                for e in n["edges"]:
                    fm += ["  - to: %s" % e["to"],
                           "    sign: %s" % e["s"],
                           "    lag_months: [%s, %s]" % (e["lag"][0], e["lag"][1]),
                           "    confidence: %s" % e["c"],
                           '    mechanism: "%s"' % e["why"],
                           '    evidence: "%s"' % e["ev"],
                           '    breaks_if: "%s"' % e["breaks"]]
            else:
                fm.append("edges: []")
            fm.append("---")

            body = ["", "# %s" % n["label"], "",
                    "`%s` ｜ %s ｜ %s ｜ 狀態：%s" % (n["id"], n["type"], n["domain"], n["status"]),
                    "", n["body"], ""]
            if n["edges"]:
                body += ["## 下游邊", "",
                         "| 指向 | 方向 | 時滯(月) | 信心 | 機制 | 證據 | 何時不成立 |",
                         "|---|---|---|---|---|---|---|"]
                for e in n["edges"]:
                    body.append("| [[%s]] | %s | %s–%s | %s | %s | %s | %s |" % (
                        e["to"], "推升 ↑" if e["s"] > 0 else "抑制 ↓",
                        e["lag"][0], e["lag"][1], e["c"], e["why"], e["ev"], e["breaks"]))
                body.append("")
            if n["counter"]:
                body += ["## ⚠️ 反向力量與已知限制", ""] + ["%s\n" % c for c in n["counter"]]
            if n["watch"]:
                body += ["## 觀察指標", ""] + ["- %s" % w for w in n["watch"]] + [""]
            body += ["---", "", "> 本檔由 `engine/%s` 產生，**請勿直接編輯**。" % self.source,
                     "> 要改內容請改該腳本再重跑。", ""]

            with open(os.path.join(outdir, "%s.md" % n["id"]), "w",
                      encoding="utf-8") as f:
                f.write("\n".join(fm) + "\n".join(body))
        print("已產生 %d 個節點 → %s" % (len(self.N), outdir))
        ids = {n["id"] for n in self.N}
        dangling = sorted({e["to"] for n in self.N for e in n["edges"]} - ids)
        if dangling:
            print("⚠️ 指向圖外的邊（若指向沙盤節點屬正常）：", dangling)
