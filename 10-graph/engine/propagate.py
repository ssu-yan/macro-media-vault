#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件傳導引擎

輸入一個事件（節點 id、標籤或別名），沿圖傳導，輸出可觀察結果的
方向、時序、信心，以及**反向路徑**與**已知限制**。

    python3 propagate.py 俄烏戰爭
    python3 propagate.py EV-RU-UA-2022 --depth 5 --min-conf 0.05
    python3 propagate.py --list

設計原則（每一條都是為了抑制過度輸出）
--------------------------------------------------------------
1. **信心隨路徑長度相乘衰減。** 三跳各 0.8 只剩 0.51。這是防止
   「六跳漂亮故事」的主要機制。
2. **同一結果的多條同向路徑取 max，不取 sum。** 多條路徑往往共用
   同一批底層機制，相加會系統性高估。取 max 是保守的選擇。
3. **反向路徑必須顯示。** 淨方向 = 支持 − 反向。若兩者接近，
   直接標示為「方向不明」而不是硬給一個方向。
4. **沿路節點的「反向力量與已知限制」一律列出。** 使用者必須看到
   這條推理鏈在哪裡可能斷掉。
5. **找不到節點就報錯，不猜。** 這是最重要的一條——寧可說
   「圖裡沒有這個事件」，也不要生成一條沒有記錄的因果鏈。
"""

import os
import re
import sys
import glob
import json
import argparse

try:
    import yaml
except ImportError:
    print("需要 pyyaml：pip install pyyaml")
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
NODES_DIR = os.path.normpath(os.path.join(HERE, "..", "nodes"))
EPIS_FILE = os.path.normpath(os.path.join(HERE, "..", "epistemic.yaml"))

DEFAULT_EPIS = {
    "evidence_caps": {"已實現": 1.00, "有先例": 0.75, "理論推導": 0.50},
    "status_caps": {"事實": 1.00, "進行中": 0.80, "證據混雜": 0.50,
                    "未檢驗": 0.45, "難以檢驗": 0.35, "已證偽": 0.00},
    "nodes": {},
}


def load_epistemic(path=EPIS_FILE):
    if not os.path.exists(path):
        return dict(DEFAULT_EPIS)
    d = yaml.safe_load(open(path, encoding="utf-8")) or {}
    for k, v in DEFAULT_EPIS.items():
        d.setdefault(k, v)
    return d


def cap_for(epis, ends, evidence):
    """回傳 (上限, 綁定原因)。

    規則：**對一條邊的信心，不可能高於你對它兩端的信心。**
    上限 = min(證據等級, 起點節點狀態, 終點節點狀態)
    """
    ev = str(evidence).split("—")[0].strip()
    caps = [(epis["evidence_caps"].get(ev, 1.0), "證據等級「%s」" % ev)]
    for nid, role in ends:
        st = epis.get("nodes", {}).get(nid)
        if st:
            caps.append((epis["status_caps"].get(st, 1.0),
                         "%s節點 %s 為「%s」" % (role, nid, st)))
    return min(caps, key=lambda x: x[0])

HORIZONS = [(0, 3, "立即（0–3 個月）"),
            (3, 12, "短期（3–12 個月）"),
            (12, 36, "中期（1–3 年）"),
            (36, 999, "長期（3 年以上）")]


# ---------------- 載入 ----------------

def load_graph(nodes_dir):
    nodes = {}
    for path in sorted(glob.glob(os.path.join(nodes_dir, "*.md"))):
        text = open(path, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as e:
            print(f"⚠️ {os.path.basename(path)} 的 YAML 解析失敗：{e}")
            continue
        if "id" not in fm:
            continue
        body = text[m.end():]
        cm = re.search(r"## ⚠️ 反向力量與已知限制\n(.*?)(?=\n## |\n---|\Z)", body, re.S)
        fm["_counter"] = cm.group(1).strip() if cm else ""
        fm["_file"] = os.path.basename(path)
        fm["edges"] = fm.get("edges") or []
        nodes[fm["id"]] = fm

    # 補上「圖外節點」：被指到但沒有自己的檔案（例如媒體沙盤的 S3）
    for n in list(nodes.values()):
        for e in n["edges"]:
            if e["to"] not in nodes:
                nodes[e["to"]] = {"id": e["to"], "label": e["to"], "type": "external",
                                  "domain": "圖外", "status": "未建檔",
                                  "aliases": [], "edges": [], "_counter": "",
                                  "_file": "(圖外)"}
    return nodes


def find_node(nodes, query):
    q = query.strip().lower()
    for nid, n in nodes.items():
        if nid.lower() == q:
            return nid
    for nid, n in nodes.items():
        if str(n.get("label", "")).lower() == q:
            return nid
        for a in (n.get("aliases") or []):
            if str(a).lower() == q:
                return nid
    hits = [nid for nid, n in nodes.items()
            if q in str(n.get("label", "")).lower()
            or any(q in str(a).lower() for a in (n.get("aliases") or []))]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        return hits
    return None


# ---------------- 傳導 ----------------

def apply_caps(nodes, epis):
    """把認識論狀態套用成邊的信心上限，就地寫入 e['_eff']。

    這是圖譜層與沙盤層的接縫：沙盤裡某個節點被證偽或標為證據混雜之後，
    **圖譜這邊指向它的邊必須自動跟著降**，否則兩層會脫節。
    """
    capped, killed = [], []
    for n in nodes.values():
        for e in n["edges"]:
            declared = float(e.get("confidence", 0))
            lim, why = cap_for(epis, [(n["id"], "起點"), (e["to"], "終點")],
                               e.get("evidence", ""))
            eff = min(declared, lim)
            e["_eff"] = eff
            if eff <= 0:
                killed.append((n["id"], e["to"], declared, why))
            elif eff < declared:
                capped.append((n["id"], e["to"], declared, eff, why))

    # 守門：指向「圖外且未評狀態」的節點，等於一條沒有上限的邊。
    # 這是最容易讓兩層脫節的漏洞，所以要主動報出來。
    unlisted = sorted({e["to"] for n in nodes.values() for e in n["edges"]
                       if nodes.get(e["to"], {}).get("type") == "external"
                       and e["to"] not in epis.get("nodes", {})})
    for u in unlisted:
        print(f"⚠️ {u} 指向圖外且未在 epistemic.yaml 評定狀態——這條邊沒有上限保護。")
    return capped, killed


def propagate(nodes, root, max_depth=5, min_conf=0.05):
    """深度優先列舉所有路徑，回傳 {target_id: [path, ...]}。"""
    results = {}

    def walk(nid, path, conf, sign, lo, hi, seen):
        if len(path) - 1 >= max_depth:
            return
        for e in nodes[nid]["edges"]:
            tgt = e["to"]
            if tgt in seen:          # 防環
                continue
            ec = e.get("_eff", float(e.get("confidence", 0)))
            if ec <= 0:              # 下游已證偽：整條邊移除
                continue
            c = conf * ec
            if c < min_conf:
                continue
            lag = e.get("lag_months") or [0, 0]
            s = sign * int(e.get("sign", 1))
            p = path + [(tgt, e)]
            rec = {"path": p, "conf": c, "sign": s,
                   "lag": (lo + lag[0], hi + lag[1])}
            results.setdefault(tgt, []).append(rec)
            walk(tgt, p, c, s, lo + lag[0], hi + lag[1], seen | {tgt})

    walk(root, [(root, None)], 1.0, 1, 0, 0, {root})
    return results


def horizon_of(months):
    for i, (lo, hi, name) in enumerate(HORIZONS):
        if lo <= months < hi:
            return i
    return len(HORIZONS) - 1


def summarize(nodes, results):
    """
    **按時間分層淨計**，而不是把所有路徑一次相抵。

    這是必要的：反向力量的時滯常常比主推力長很多。俄烏戰爭對歐洲天然氣
    價格就是典型案例——供給衝擊 0–6 個月，LNG 替代 6–24 個月。混在一起
    淨計會得到「小幅推升」，完全錯過「先暴漲再崩回」這個真實型態。

    所以同一個結果節點可以在不同時間層出現不同方向。
    """
    out = []
    for tgt, paths in results.items():
        buckets = {}
        for p in paths:
            buckets.setdefault(horizon_of(p["lag"][0]), []).append(p)
        for hi, ps in buckets.items():
            up = [p for p in ps if p["sign"] > 0]
            dn = [p for p in ps if p["sign"] < 0]
            s_up = max([p["conf"] for p in up], default=0.0)
            s_dn = max([p["conf"] for p in dn], default=0.0)
            net = s_up - s_dn
            pool = up if net >= 0 else dn
            dom = max(pool or ps, key=lambda p: p["conf"])
            out.append({
                "id": tgt, "label": nodes[tgt].get("label", tgt),
                "type": nodes[tgt].get("type", "?"),
                "domain": nodes[tgt].get("domain", "?"),
                "h": hi, "net": net, "up": s_up, "dn": s_dn,
                "n_up": len(up), "n_dn": len(dn),
                "lag": dom["lag"], "best": dom,
            })
    return sorted(out, key=lambda r: (r["h"], -abs(r["net"])))


# ---------------- 輸出 ----------------

def fmt_path(nodes, rec):
    ids = [p[0] for p in rec["path"]]
    labels = [nodes[i].get("label", i) for i in ids]
    return " → ".join(labels)


def report(nodes, root, summ, results, max_depth, min_conf, capped, killed):
    r = nodes[root]
    print()
    print("=" * 78)
    print(f"事件：{r.get('label', root)}  [{root}]")
    if r.get("date"):
        print(f"發生時間：{r['date']}")
    print(f"領域：{r.get('domain','?')} ｜ 狀態：{r.get('status','?')}")
    print(f"參數：最大深度 {max_depth} 跳、信心下限 {min_conf}")
    print("=" * 78)

    outcomes = [s for s in summ if s["type"] in ("outcome", "external")]
    inter = [s for s in summ if s["type"] not in ("outcome", "external")]

    print()
    print(f"■ 可觀察結果（{len({s['id'] for s in outcomes})} 個節點，"
          f"{len(outcomes)} 個時間層判斷）")
    print("  ※ 同一結果在不同時間層可能方向相反——反向力量的時滯常比主推力長。")
    for hidx, (lo, hi, name) in enumerate(HORIZONS):
        band = [s for s in outcomes if s["h"] == hidx]
        if not band:
            continue
        print()
        print(f"── {name} " + "─" * (60 - len(name)))
        for s in band:
            if abs(s["net"]) < 0.10:
                arrow, verdict = "?", "方向不明（支持與反向力量接近）"
            elif s["net"] > 0:
                arrow, verdict = "↑", f"推升   淨信心 {s['net']:.2f}"
            else:
                arrow, verdict = "↓", f"抑制   淨信心 {abs(s['net']):.2f}"
            print(f"  {arrow} {s['label']:<22}{verdict}")
            print(f"      時窗 {s['lag'][0]}–{s['lag'][1]} 個月 ｜ "
                  f"支持 {s['n_up']} 條(最強 {s['up']:.2f}) / "
                  f"反向 {s['n_dn']} 條(最強 {s['dn']:.2f})")
            print(f"      主路徑：{fmt_path(nodes, s['best'])}")
            if s["type"] == "external":
                print(f"      ⚠️ 此節點不在圖中（{s['id']}），無法再往下傳導")

    print()
    print(f"■ 中間狀態與通道（{len(inter)} 個，摘要）")
    for s in inter[:10]:
        d = "↑" if s["net"] > 0 else ("↓" if s["net"] < 0 else "?")
        print(f"  {d} {s['label']:<24}信心 {abs(s['net']):.2f}  "
              f"時窗 {s['lag'][0]}–{s['lag'][1]}m")

    # 沿路節點的反向力量
    touched = {root} | set(results.keys())
    warns = [(nodes[i].get("label", i), nodes[i]["_counter"])
             for i in touched if nodes.get(i, {}).get("_counter")]
    print()
    print("■ ⚠️ 反向力量與已知限制（沿路節點）")
    print()
    for lab, txt in warns:
        print(f"  【{lab}】")
        for line in txt.split("\n"):
            if line.strip():
                print(f"    {line.strip()}")
        print()

    if capped or killed:
        print()
        print("■ 🔒 認識論上限生效的邊")
        print()
        print("  規則：對一條邊的信心，不可能高於你對它兩端的信心。")
        print("  上限 = min(證據等級, 起點節點狀態, 終點節點狀態)")
        print()
        for a_, b_, d_, e_, why in capped:
            print("  %s → %s" % (a_, b_))
            print("      宣告 %.2f → 生效 %.2f　（受限於%s）" % (d_, e_, why))
        for a_, b_, d_, why in killed:
            print("  %s → %s" % (a_, b_))
            print("      宣告 %.2f → ❌ 整條邊移除（%s）" % (d_, why))

    print()
    print("=" * 78)
    print("讀法")
    print("=" * 78)
    print("  · 信心沿路徑相乘衰減；三跳各 0.8 只剩 0.51。跳數越多越不可信。")
    print("  · 同一結果的多條同向路徑取最大值而非加總——多條路徑常共用底層")
    print("    機制，相加會系統性高估。")
    print("  · 淨信心 < 0.10 一律標為「方向不明」，不硬給方向。")
    print("  · **這張圖是手寫的，絕大多數邊未經實證檢驗。** 它輸出的是")
    print("    「圖中存在這些路徑」，不是「這些事會發生」。")
    print("  · 已知結構性缺陷：沒有處理地區異質性；沒有處理事件規模；")
    print("    邊的信心值是判斷而非估計。")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("event", nargs="?", help="事件 id、標籤或別名")
    ap.add_argument("--depth", type=int, default=5)
    ap.add_argument("--min-conf", type=float, default=0.05)
    ap.add_argument("--nodes", default=NODES_DIR)
    ap.add_argument("--list", action="store_true", help="列出圖中所有節點")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    nodes = load_graph(a.nodes)
    if not nodes:
        print(f"在 {a.nodes} 找不到任何節點")
        sys.exit(1)

    if a.list or not a.event:
        print(f"圖中共 {len(nodes)} 個節點：\n")
        for t in ("event", "state", "channel", "outcome", "external"):
            g = [n for n in nodes.values() if n.get("type") == t]
            if not g:
                continue
            print(f"[{t}]")
            for n in sorted(g, key=lambda x: x["id"]):
                al = "、".join(str(x) for x in (n.get("aliases") or [])[:3])
                print(f"  {n['id']:<24}{n.get('label','')}" + (f"　（{al}）" if al else ""))
            print()
        if not a.event:
            print("用法：python3 propagate.py <事件>")
        return

    hit = find_node(nodes, a.event)
    if hit is None:
        print(f"\n❌ 圖中沒有「{a.event}」這個節點。\n")
        print("引擎不會替沒有記錄的事件生成因果鏈——那正是這個系統要避免的事。")
        print("要加入它，請在 nodes/ 新增一個檔案，或告訴我，我幫你建。")
        print("\n用 --list 看現有節點。")
        sys.exit(2)
    if isinstance(hit, list):
        print(f"\n「{a.event}」對應到多個節點，請指定其中一個：\n")
        for h in hit:
            print(f"  {h:<24}{nodes[h].get('label','')}")
        sys.exit(3)

    epis = load_epistemic()
    capped, killed = apply_caps(nodes, epis)
    results = propagate(nodes, hit, a.depth, a.min_conf)
    summ = summarize(nodes, results)
    if a.json:
        print(json.dumps({"root": hit, "results": [
            {k: v for k, v in s.items() if k != "best"} for s in summ]},
            ensure_ascii=False, indent=2))
    else:
        report(nodes, hit, summ, results, a.depth, a.min_conf, capped, killed)


if __name__ == "__main__":
    main()
