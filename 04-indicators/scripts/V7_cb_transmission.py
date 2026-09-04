#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V7：檢驗 S6-央行溝通失效

判準見 04-indicators/V7-預先登記.md —— **那份文件在本腳本執行前、
且在任何資料被下載之前就已 commit**。
本腳本只負責產生數字，不負責決定怎樣算成功。

--------------------------------------------------------------------
需要的資料（由 Wendy 從 FRED 下載，放進 scripts/data/）

    MICH        密西根 1 年期通膨預期（月）        1978-01 起
    T5YIFR      5 年 5 年後遠期通膨預期（日）      2003-01 起
    T10YIE      10 年損益兩平通膨率（日）          2003-01 起   ← 安慰劑
    EXPINF1YR   克里夫蘭 Fed 1 年期預期通膨（月）  1982-01 起   ← 長樣本
    CPIAUCSL    CPI 全項目（月）                   1947-01 起   ← 控制變數

    下載：FRED 序列頁面右上 DOWNLOAD -> CSV，檔名保留代號即可。

執行：python3 V7_cb_transmission.py
相依：pandas, numpy
--------------------------------------------------------------------
"""

import os
import sys
import glob
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")

WINDOW = 60          # 滾動視窗（月）——預先登記寫死
HAC_LAG = 24         # 預先登記寫死
T_CRIT = 2.0         # |t| > 2 算顯著——預先登記寫死

SEG_MAIN = [("2003-01", "2009-12", "2003–2009 前社群"),
            ("2010-01", "2015-12", "2010–2015 社群普及"),
            ("2016-01", "2021-12", "2016–2021 演算法／極化"),
            ("2022-01", "2026-12", "2022–2026 AI／通膨衝擊")]

SEG_LONG = [("1982-01", "1994-12", "1982–1994 三大電視網末期"),
            ("1995-01", "2004-12", "1995–2004 有線＋早期網路"),
            ("2005-01", "2014-12", "2005–2014 社群興起"),
            ("2015-01", "2026-12", "2015–2026 演算法／AI")]


# ---------------- 讀 FRED CSV ----------------

def load_fred(code):
    """FRED 的 CSV 有兩種欄位命名（DATE/observation_date），兩種都吃。"""
    cands = [p for p in glob.glob(os.path.join(DATA_DIR, "*.csv"))
             if code.lower() in os.path.basename(p).lower()]
    if not cands:
        raise FileNotFoundError(f"在 {DATA_DIR} 找不到含「{code}」的 CSV")
    path = sorted(cands)[0]
    df = pd.read_csv(path)
    datecol = next((c for c in df.columns
                    if c.strip().lower() in ("date", "observation_date")), df.columns[0])
    valcol = next((c for c in df.columns if c != datecol))
    s = pd.Series(pd.to_numeric(df[valcol], errors="coerce").values,
                  index=pd.to_datetime(df[datecol]), name=code).dropna()
    # 日頻 -> 月平均
    if len(s) > 0 and (s.index.to_series().diff().dt.days.median() or 31) < 20:
        s = s.resample("MS").mean()
    else:
        s = s.resample("MS").last()
    print(f"  {code:<10} {len(s):>5} 個月  {s.index.min().date()} → {s.index.max().date()}")
    return s


# 預先登記寫死的樣本起點。**這是護欄，不是判準**——
# 它只確認拿到的資料真的涵蓋預先登記所說的期間，不改變任何假說或門檻。
#
# 為什麼要有它：2026-09-04 第一次下載時，T5YIFR 與 T10YIE 只拿到
# 2021-09 起的 61 個月（FRED 的圖預設只顯示近 5 年，DOWNLOAD 會跟著那個範圍走）。
# 60 個月的滾動視窗只能產生 **2 個視窗**，主要規格與 H4 安慰劑都跑不了。
# 若沒有這道護欄，腳本會安靜地在 2 個視窗上算出一組毫無意義的 t 值。
#
# 這與 V1 的 PCEC96 是同一種失敗：**檔案存在、格式正確、程式跑得動，只是序列被截斷了。**
# 那一次的截斷產生了一個**方向相反**的結論。
REQUIRED_START = {
    "MICH": "1985-01",
    "T5YIFR": "2003-06",
    "T10YIE": "2003-06",
    "EXPINF1YR": "1985-01",
    "CPIAUCSL": "1985-01",
}


def check_coverage(series_map):
    bad = []
    for code, s in series_map.items():
        need = pd.Timestamp(REQUIRED_START[code])
        if s.index.min() > need:
            bad.append((code, s.index.min().date(), need.date(), len(s)))
    if bad:
        print()
        print("=" * 78)
        print("⛔ 停止：有序列的涵蓋期間短於預先登記所要求的樣本")
        print("=" * 78)
        print(f"{'序列':<12}{'實際起點':>12}{'需要不晚於':>14}{'月數':>8}{'60月視窗數':>12}")
        print("-" * 78)
        for code, got, need, n in bad:
            print(f"{code:<12}{str(got):>12}{str(need):>14}{n:>8}{max(0, n - WINDOW + 1):>12}")
        print("-" * 78)
        print()
        print("原因幾乎一定是：FRED 的圖預設只顯示近 5 年，DOWNLOAD 會跟著那個範圍走。")
        print()
        print("修法：到該序列的 FRED 頁面，把圖上方的**起始日期框**改成該序列的最早日期")
        print("     （或按圖右上的時間範圍選單選 MAX），**再**按 DOWNLOAD → CSV。")
        print()
        print("⚠️ 這道檢查刻意讓腳本停下來，而不是在短樣本上算出一組沒有意義的數字。")
        print("   V1 的 PCEC96 就是同一種失敗（序列被截斷），而那次產生了方向相反的結論。")
        sys.exit(1)


# ---------------- 統計工具（沿用 V1/V6 的 HAC 實作） ----------------

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


def rolling_comovement(a, b, infl_vol, window=WINDOW):
    """回傳 DataFrame：視窗結束日 / 共動相關係數 / 該視窗的通膨波動。"""
    d = pd.concat([a.diff(), b.diff(), infl_vol], axis=1).dropna()
    d.columns = ["da", "db", "vol"]
    rows = []
    for i in range(window - 1, len(d)):
        w = d.iloc[i - window + 1: i + 1]
        if w["da"].std(ddof=1) == 0 or w["db"].std(ddof=1) == 0:
            continue
        rows.append({"end": d.index[i],
                     "corr": float(w["da"].corr(w["db"])),
                     "vol": float(w["vol"].mean())})
    return pd.DataFrame(rows).dropna()


# ---------------- 三個迴歸假說 ----------------

def h1_h2(res, label):
    print()
    print("=" * 78)
    print(f"H1／H2：{label}")
    print("  H1 判準 — 時間係數顯著為負（|t(HAC)| > 2）")
    print("  H2 判準 — 控制通膨波動後，時間係數仍顯著為負  ⭐ 這條是裁判")
    print("=" * 78)
    if len(res) < 24:
        print("  視窗數不足，無法判定")
        return None, None
    t = ((res["end"] - res["end"].iloc[0]).dt.days / 365.25).to_numpy()
    y = res["corr"].to_numpy(float)

    b1, se1, r21, n1 = ols_hac(y, t.reshape(-1, 1), HAC_LAG)
    tv1 = b1[1] / se1[1] if se1[1] > 0 else np.nan
    h1 = (b1[1] < 0) and abs(tv1) > T_CRIT

    X2 = np.column_stack([t, res["vol"].to_numpy(float)])
    b2, se2, r22, n2 = ols_hac(y, X2, HAC_LAG)
    tv2 = b2[1] / se2[1] if se2[1] > 0 else np.nan
    tvv = b2[2] / se2[2] if se2[2] > 0 else np.nan
    h2 = (b2[1] < 0) and abs(tv2) > T_CRIT

    print(f"  視窗數 {len(res)}　期間 {res['end'].min().date()} → {res['end'].max().date()}")
    print(f"{'規格':<18}{'時間係數/年':>15}{'t(HAC)':>10}{'R²':>8}{'判定':>12}")
    print("-" * 78)
    print(f"{'單獨':<18}{b1[1]:>+15.5f}{tv1:>10.2f}{r21:>8.3f}"
          f"{('H1 通過' if h1 else 'H1 未過'):>12}")
    print(f"{'控制通膨波動':<18}{b2[1]:>+15.5f}{tv2:>10.2f}{r22:>8.3f}"
          f"{('H2 通過' if h2 else 'H2 未過'):>12}")
    print(f"{'  （波動係數）':<18}{b2[2]:>+15.5f}{tvv:>10.2f}")
    return h1, h2


def h3_segments(res, segs, label):
    print()
    print("=" * 78)
    print(f"H3：分段對比 — {label}   ⭐ 這條殺死過 S5 與 S3")
    print("  判準 — 共動逐段下降，且最早一段必須是最高的")
    print("=" * 78)
    idx = res.set_index("end")["corr"]
    rows = []
    print(f"{'期間':<30}{'N':>6}{'共動平均':>12}")
    print("-" * 78)
    for s, e, lab in segs:
        sub = idx.loc[s:e]
        if len(sub) < 12:
            print(f"{lab:<30}{'樣本不足':>12}")
            continue
        rows.append((lab, float(sub.mean())))
        print(f"{lab:<30}{len(sub):>6}{sub.mean():>12.3f}")
    print("-" * 78)
    if len(rows) < 4:
        print("  H3 無法判定")
        return False
    v = [x[1] for x in rows]
    mono = all(v[i] > v[i + 1] for i in range(len(v) - 1))
    first_highest = v[0] == max(v)
    print(f"  逐段下降：{'✓' if mono else '✗'}"
          f"   最早段最高：{'✓' if first_highest else '✗ ← S5 與 S3 都死在這'}")
    passed = mono and first_highest
    print(f"  H3 {'通過' if passed else '未通過'}")
    return passed


def main():
    print()
    print("V7：檢驗 S6-央行溝通失效")
    print("判準見 04-indicators/V7-預先登記.md（於資料下載前已 commit）")
    print()
    print("讀取資料：")
    try:
        mich = load_fred("MICH")
        t5y = load_fred("T5YIFR")
        t10 = load_fred("T10YIE")
        cle = load_fred("EXPINF1YR")
        cpi = load_fred("CPIAUCSL")
    except FileNotFoundError as e:
        print()
        print(e)
        print()
        print("請先從 FRED 下載這五個序列的 CSV 放進 scripts/data/：")
        print("  MICH / T5YIFR / T10YIE / EXPINF1YR / CPIAUCSL")
        sys.exit(1)

    check_coverage({"MICH": mich, "T5YIFR": t5y, "T10YIE": t10,
                    "EXPINF1YR": cle, "CPIAUCSL": cpi})

    # 已實現通膨波動（控制變數）：CPI 年增率的滾動標準差
    infl = cpi.pct_change(12) * 100
    infl_vol = infl.rolling(WINDOW).std(ddof=1).rename("vol")

    # ---------- 主要規格：家計（MICH）vs 金融（T5YIFR），2003 起 ----------
    main_res = rolling_comovement(mich, t5y, infl_vol)
    h1a, h2a = h1_h2(main_res, "主要規格：Δ家計預期(MICH) vs Δ市場預期(T5YIFR)")
    h3a = h3_segments(main_res, SEG_MAIN, "主要規格")

    # ---------- H4 安慰劑：市場內部（T5YIFR vs T10YIE） ----------
    plac_res = rolling_comovement(t5y, t10, infl_vol)
    print()
    print("=" * 78)
    print("H4：安慰劑 — 市場內部共動（ΔT5YIFR vs ΔT10YIE）  ⭐ 這條是 S6 特有的")
    print("  判準 — 市場內部**不得**出現同樣顯著的下降趨勢")
    print("        若市場也在下降，代表退化的是整個通膨預期環境，不是實體通道")
    print("=" * 78)
    h1p, h2p = h1_h2(plac_res, "安慰劑：市場內部共動")
    h4 = not bool(h1p)          # 市場內部沒有顯著下降 -> H4 通過
    print(f"\n  H4 {'通過（市場內部沒有同樣的下降）' if h4 else '未通過（市場內部也在下降）'}")

    # ---------- 次要規格：長樣本 ----------
    long_res = rolling_comovement(mich, cle, infl_vol)
    h1b, h2b = h1_h2(long_res, "次要規格（長樣本）：Δ家計預期(MICH) vs Δ克里夫蘭 Fed(EXPINF1YR)")
    h3b = h3_segments(long_res, SEG_LONG, "次要規格（長樣本）")

    # ---------- 處置表 ----------
    print()
    print("=" * 78)
    print("依 V7-預先登記.md 第 5 節的處置表（以主要規格為準）")
    print("=" * 78)
    print(f"  H1={h1a}　H2={h2a}　H3={h3a}　H4={h4}")
    print()
    if h1a and h2a and h3a and h4:
        print("  四條全過 → S6：未檢驗 → **有支持**（上限 0.45 → 0.75）")
    elif h1a and not h2a:
        print("  H1 ✓ H2 ✗ → **不算通過。** 有趨勢，但控制通膨波動後消失。")
        print("  這與 S5 的死法一模一樣。S6：未檢驗 → **證據混雜**（0.50）")
    elif h1a and h2a and not h3a:
        print("  H3 ✗ → 有趨勢，但最早一段不是最高的。")
        print("  這與 S3 的死法一模一樣。S6：未檢驗 → **證據混雜**（0.50）")
    elif h1a and h2a and h3a and not h4:
        print("  H4 ✗ → 有退化，但**市場內部也在退化**，不是家計通道特有。")
        print("  S6 主張的不對稱不成立。S6：未檢驗 → **證據混雜**（0.50）")
    else:
        print("  H1 ✗ → **S6 證偽。** 上限 0.00。")
        print("  S6 → S7 與 S6 → OUT-EQUITY-VOL 兩條邊生效信心歸零，")
        print("  媒體 → 總體那條四跳鏈整段斷掉。")

    print()
    print("  次要規格（長樣本）僅供對照，不改變上述處置：")
    print(f"    H1={h1b}　H2={h2b}　H3={h3b}")
    print()
    print("  ⚠️ 不論結果如何：S7-政策不確定性溢價 仍是「未檢驗」，")
    print("     那條四跳鏈在本檢定之後**仍然跨不過 0.10**（硬天花板 0.1155）。")
    print("  ⚠️ 狀態變更要走協議第 8 節的調參流程，不是跑完就自動生效。")
    print("  ⚠️ 本檢定測的是**共動**不是**傳導**；MICH 是中位數不是離散度。")
    print("     限制見預先登記第 6 節，不得事後拿來解釋結果。")

    out = os.path.join(HERE, "V7_comovement.csv")
    main_res.assign(spec="main").to_csv(out, index=False)
    print(f"\n主要規格的滾動序列已存成 {os.path.basename(out)}")


if __name__ == "__main__":
    main()
