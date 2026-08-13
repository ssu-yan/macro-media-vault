#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V6：直接檢驗 S3（信念離散度）與 S9（市場二階量）

判準見 04-indicators/V6-預先登記.md —— **那份文件在本腳本執行前就已 commit**。
本腳本只負責產生數字，不負責決定怎樣算成功。

--------------------------------------------------------------------
需要的資料
    Ken French Data Library → "49 Industry Portfolios"（月頻）
    https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
    下載 CSV（會是 zip），解壓後把 CSV 放進 data/，檔名含 "49_Industry" 即可。
執行：python3 V6_dispersion.py
相依：pandas, numpy
--------------------------------------------------------------------
"""

import os
import re
import sys
import glob
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")

START = "1960-01"
CORR_WINDOW = 60      # 滾動相關係數視窗（月）
VOL_WINDOW = 12       # 市場波動視窗（月）

SEGMENTS = [
    ("1960-01", "1989-12", "1960–1989 三大電視網"),
    ("1990-01", "2004-12", "1990–2004 有線＋早期網路"),
    ("2005-01", "2014-12", "2005–2014 社群興起"),
    ("2015-01", "2026-12", "2015–2026 演算法/AI"),
]


# ---------- 讀 Ken French 的檔案 ----------

def load_french_49():
    """
    French 的 CSV 有多個表格疊在一起（平均加權報酬、等權報酬、公司數、平均市值），
    中間用空白行分隔，開頭有一段說明文字。這裡只取**第一個**表格
    （Average Value Weighted Returns — Monthly），並把 -99.99 / -999 視為缺值。
    """
    cands = glob.glob(os.path.join(DATA_DIR, "*49_Industry*.csv")) + \
            glob.glob(os.path.join(DATA_DIR, "*49_Industry*.CSV"))
    if not cands:
        raise FileNotFoundError(
            f"在 {DATA_DIR} 找不到 49 Industry Portfolios 的 CSV。\n"
            "請到 Ken French Data Library 下載「49 Industry Portfolios」的月頻 CSV，\n"
            "解壓後把檔案放進 data/（檔名含 49_Industry 即可）。"
        )
    path = sorted(cands)[0]
    print(f"讀取：{os.path.basename(path)}")

    with open(path, "r", encoding="latin-1") as f:
        lines = f.read().splitlines()

    # 找出表頭列：第一欄空白、後面是產業名稱
    hdr_i = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith(",") and len(ln.split(",")) > 40:
            hdr_i = i
            break
    if hdr_i is None:
        raise ValueError("找不到表頭列，French 的檔案格式可能改了")

    cols = [c.strip() for c in lines[hdr_i].split(",")]
    cols[0] = "date"

    rows = []
    for ln in lines[hdr_i + 1:]:
        parts = [p.strip() for p in ln.split(",")]
        if len(parts) != len(cols):
            continue
        if not re.fullmatch(r"\d{6}", parts[0]):   # 只收 YYYYMM，遇到年頻或下一個表格就停
            if rows:
                break
            continue
        rows.append(parts)

    df = pd.DataFrame(rows, columns=cols)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m")
    df = df.set_index("date").astype(float)
    df = df.mask(df <= -99)          # -99.99 / -999.99 = 缺值
    print(f"  {len(df)} 個月，{df.shape[1]} 個產業，"
          f"{df.index.min().date()} → {df.index.max().date()}")
    return df


# ---------- 統計工具 ----------

def ols_hac(y, X, lag):
    n = len(y)
    X = np.column_stack([np.ones(n), X])
    k = X.shape[1]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    XtX_inv = np.linalg.pinv(X.T @ X)
    Xu = X * resid[:, None]
    S = Xu.T @ Xu
    for L in range(1, lag + 1):
        w = 1.0 - L / (lag + 1.0)
        G = Xu[L:].T @ Xu[:-L]
        S += w * (G + G.T)
    cov = XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.maximum(np.diag(cov) * (n / max(n - k, 1)), 0))
    ss_res = float(resid @ resid)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return beta, se, (1 - ss_res / ss_tot if ss_tot > 0 else np.nan), n


def build_measures(ind):
    """產生 disp / mktvol / ratio / corr 四個月頻序列。"""
    mkt = ind.mean(axis=1)                             # 等權市場報酬
    disp = ind.std(axis=1, ddof=1)                     # 橫斷面標準差
    mktvol = mkt.rolling(VOL_WINDOW).std(ddof=1)
    ratio = disp / mktvol                              # ⬅️ 主要變數

    # 滾動平均兩兩相關（off-diagonal 平均）
    corr = pd.Series(index=ind.index, dtype=float)
    vals = ind.to_numpy()
    for i in range(CORR_WINDOW - 1, len(ind)):
        w = vals[i - CORR_WINDOW + 1: i + 1]
        w = w[:, ~np.isnan(w).any(axis=0)]
        if w.shape[1] < 20:
            continue
        c = np.corrcoef(w, rowvar=False)
        m = ~np.eye(c.shape[0], dtype=bool)
        corr.iloc[i] = np.nanmean(c[m])

    out = pd.DataFrame({"disp": disp, "mktvol": mktvol,
                        "ratio": ratio, "corr": corr}).loc[START:]
    return out.dropna()


# ---------- 三個假說 ----------

def h1_trend(df):
    print()
    print("=" * 74)
    print("H1：時間趨勢（1960–2026）")
    print("  判準 — S3 成立：ratio 係數顯著為正、corr 係數顯著為負")
    print("=" * 74)
    t = (df.index - df.index[0]).days / 365.25
    print(f"{'變數':<10}{'規格':<16}{'時間係數/年':>14}{'t(HAC)':>10}{'判定':>12}")
    print("-" * 74)
    res = {}
    for var, want in [("ratio", "+"), ("corr", "-")]:
        y = df[var].to_numpy(float)
        for spec, X in [("單獨", t.to_numpy().reshape(-1, 1)),
                        ("控制 mktvol", np.column_stack([t, df["mktvol"]]))]:
            b, se, _, n = ols_hac(y, X, lag=24)
            tv = b[1] / se[1]
            ok = (b[1] > 0 if want == "+" else b[1] < 0) and abs(tv) > 2
            if spec == "控制 mktvol":
                res[var] = ok
            print(f"{var:<10}{spec:<16}{b[1]:>+14.5f}{tv:>10.2f}"
                  f"{('符合 ✓' if ok else '不符 ✗'):>12}")
    print("-" * 74)
    passed = res.get("ratio") and res.get("corr")
    print(f"  H1 {'通過' if passed else '未通過'}（以控制 mktvol 的規格為準）")
    return passed


def h2_segments(df):
    print()
    print("=" * 74)
    print("H2：碎片化前後對比 ⭐ 這條殺死過 S5")
    print("  判準 — S3 成立：ratio 逐段上升、corr 逐段下降")
    print("        且最早一段的 ratio 必須是最低的")
    print("=" * 74)
    print(f"{'期間':<26}{'N':>5}{'ratio 平均':>12}{'corr 平均':>12}")
    print("-" * 74)
    rows = []
    for s, e, lab in SEGMENTS:
        sub = df.loc[s:e]
        if len(sub) < 24:
            print(f"{lab:<26}{'樣本不足':>10}")
            continue
        rows.append((lab, sub["ratio"].mean(), sub["corr"].mean()))
        print(f"{lab:<26}{len(sub):>5}{sub['ratio'].mean():>12.3f}"
              f"{sub['corr'].mean():>12.3f}")
    print("-" * 74)
    if len(rows) < 4:
        print("  H2 無法判定")
        return False
    r = [x[1] for x in rows]
    c = [x[2] for x in rows]
    mono_r = all(r[i] < r[i + 1] for i in range(3))
    mono_c = all(c[i] > c[i + 1] for i in range(3))
    first_lowest = r[0] == min(r)
    print(f"  ratio 逐段上升：{'✓' if mono_r else '✗'}"
          f"   corr 逐段下降：{'✓' if mono_c else '✗'}"
          f"   最早段 ratio 最低：{'✓' if first_lowest else '✗ ← S5 就是死在這'}")
    passed = mono_r and mono_c and first_lowest
    print(f"  H2 {'通過' if passed else '未通過'}")
    return passed


def h3_robust(df):
    print()
    print("=" * 74)
    print("H3：穩健性 — 趨勢是否由少數危機期驅動")
    print("=" * 74)
    t_all = (df.index - df.index[0]).days / 365.25
    # 剔除 mktvol 最高的 10% 月份（危機期代理）
    thr = df["mktvol"].quantile(0.90)
    calm = df[df["mktvol"] < thr]
    t_calm = (calm.index - calm.index[0]).days / 365.25
    print(f"{'樣本':<22}{'N':>6}{'ratio 斜率':>13}{'t':>8}{'corr 斜率':>13}{'t':>8}")
    print("-" * 74)
    for lab, d, t in [("全樣本", df, t_all), ("剔除高波動 10%", calm, t_calm)]:
        out = []
        for var in ["ratio", "corr"]:
            b, se, _, _ = ols_hac(d[var].to_numpy(float),
                                  np.column_stack([t, d["mktvol"]]), lag=24)
            out += [b[1], b[1] / se[1]]
        print(f"{lab:<22}{len(d):>6}{out[0]:>+13.5f}{out[1]:>8.2f}"
              f"{out[2]:>+13.5f}{out[3]:>8.2f}")
    print("-" * 74)
    print("  兩列方向與顯著性一致 → 趨勢不是危機期造成的")


def main():
    try:
        ind = load_french_49()
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)

    df = build_measures(ind)
    print(f"分析期間：{df.index.min().date()} → {df.index.max().date()}"
          f"（{len(df)} 個月）")

    h1 = h1_trend(df)
    h2 = h2_segments(df)
    h3_robust(df)

    print()
    print("=" * 74)
    print("依 V6-預先登記.md 的處置表")
    print("=" * 74)
    if h1 and h2:
        print("  H1 ✓ H2 ✓ → S3 從「未檢驗」升為「有支持」。")
        print("  這是恢復 vault 預測定位所需兩個節點中的第一個。")
    elif h1 and not h2:
        print("  H1 ✓ H2 ✗ → **不算通過。** 有趨勢，但碎片化之前的水準沒有比較低。")
        print("  這跟 S5 的死法一模一樣。S3 標記為「證據混雜」。")
    else:
        print("  H1 ✗ → **S3 證偽。**")
        print("  S9 的兩條條件式含意一併失效，vault 的可操作產出歸零。")
        print("  應考慮從「推理工具」再降級為「歷史紀錄」。")
    print()
    print("  ⚠️ 不論結果如何：本測量是**產業層級**，不是個股層級。")
    print("     它測的是 S3 的必要條件，不是充分條件。")

    df.to_csv(os.path.join(HERE, "V6_measures.csv"))
    print("\n月頻序列已存成 V6_measures.csv")


if __name__ == "__main__":
    main()
