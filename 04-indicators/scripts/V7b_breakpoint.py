#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V7b：家計—市場脫鉤是「水準位移」還是「趨勢」？

判準見 04-indicators/V7b-預先登記.md —— **那份文件在本腳本執行前就已 commit**。
本腳本只負責產生數字，不負責決定怎樣算成功。

⚠️ 假說（2016 前後的斷點）是從 V7 的資料裡看出來的。
   因此本檢定的處置表刻意設計成**只能維持或下修 S6，不能上修**。
   要上修需要樣本外證據（另一個經濟體），那是 V7c。

--------------------------------------------------------------------
資料：沿用 V7 已下載的五個 FRED 序列，不需要新資料。
執行：python3 V7b_breakpoint.py
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

# ---- 全部由預先登記寫死，不得事後調整 ----
WINDOW = 60          # 與 V7 相同的滾動視窗
TRIM = 0.15          # 兩端各修剪 15%
BLOCK = 24           # 移動區塊 bootstrap 的區塊長度（月）
N_BOOT = 2000        # 重抽次數
ALPHA = 0.05         # 判準門檻
SEED = 20260904      # 固定亂數種子，讓結果可重現

# B2 的非媒體對照日期（事先寫死）
RIVAL_DATES = [("全球金融海嘯", "2008-09"),
               ("COVID 衝擊", "2020-03"),
               ("通膨衝擊起點", "2021-04")]
RIVAL_MONTHS = 12    # 相距 <= 12 個月即觸發反證


def load_fred(code):
    cands = [p for p in glob.glob(os.path.join(DATA_DIR, "*.csv"))
             if code.lower() in os.path.basename(p).lower()]
    if not cands:
        raise FileNotFoundError(f"在 {DATA_DIR} 找不到含「{code}」的 CSV")
    df = pd.read_csv(sorted(cands)[0])
    dc = next((c for c in df.columns
               if c.strip().lower() in ("date", "observation_date")), df.columns[0])
    vc = next(c for c in df.columns if c != dc)
    s = pd.Series(pd.to_numeric(df[vc], errors="coerce").values,
                  index=pd.to_datetime(df[dc]), name=code).dropna()
    if (s.index.to_series().diff().dt.days.median() or 31) < 20:
        s = s.resample("MS").mean()
    else:
        s = s.resample("MS").last()
    return s


def rolling_comovement(a, b, window=WINDOW):
    d = pd.concat([a.diff(), b.diff()], axis=1).dropna()
    d.columns = ["da", "db"]
    rows = []
    for i in range(window - 1, len(d)):
        w = d.iloc[i - window + 1: i + 1]
        if w["da"].std(ddof=1) == 0 or w["db"].std(ddof=1) == 0:
            continue
        rows.append({"end": d.index[i], "corr": float(w["da"].corr(w["db"]))})
    return pd.DataFrame(rows).dropna()


# ---------------- sup-Wald ----------------

def _ssr(y, X):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ beta
    return float(r @ r)


def sup_wald(y, t):
    """對 y ~ 1 + t 檢定水準位移（截距斷點）。回傳 (統計量, 斷點索引)。"""
    n = len(y)
    lo, hi = int(np.floor(TRIM * n)), int(np.ceil((1 - TRIM) * n))
    X0 = np.column_stack([np.ones(n), t])
    ssr0 = _ssr(y, X0)
    best, best_i = -np.inf, None
    for i in range(lo, hi):
        d = (np.arange(n) >= i).astype(float)
        X1 = np.column_stack([np.ones(n), t, d])
        ssr1 = _ssr(y, X1)
        if ssr1 <= 0:
            continue
        f = (ssr0 - ssr1) / (ssr1 / (n - 3))
        if f > best:
            best, best_i = f, i
    return best, best_i


def block_bootstrap_pvalue(y, t, stat, rng):
    """在「無斷點」的虛無下，用移動區塊 bootstrap 重建 sup-Wald 的分布。"""
    n = len(y)
    X0 = np.column_stack([np.ones(n), t])
    beta, *_ = np.linalg.lstsq(X0, y, rcond=None)
    fitted = X0 @ beta
    resid = y - fitted
    n_blocks = int(np.ceil(n / BLOCK))
    starts_max = n - BLOCK
    exceed = 0
    for _ in range(N_BOOT):
        starts = rng.integers(0, starts_max + 1, size=n_blocks)
        e = np.concatenate([resid[s:s + BLOCK] for s in starts])[:n]
        s_b, _ = sup_wald(fitted + e, t)
        if s_b >= stat:
            exceed += 1
    return (exceed + 1) / (N_BOOT + 1)


def run_break(res, label, rng):
    print()
    print("=" * 78)
    print(f"B1：sup-Wald 斷點檢定 — {label}")
    print(f"  修剪 {TRIM:.0%}　區塊長度 {BLOCK} 個月　重抽 {N_BOOT} 次　種子 {SEED}")
    print(f"  判準 — bootstrap p < {ALPHA} 即為「有斷點」")
    print("=" * 78)
    y = res["corr"].to_numpy(float)
    t = ((res["end"] - res["end"].iloc[0]).dt.days / 365.25).to_numpy()
    stat, i = sup_wald(y, t)
    if i is None:
        print("  無法計算")
        return None, None, None
    date = res["end"].iloc[i]
    p = block_bootstrap_pvalue(y, t, stat, rng)
    print(f"  視窗數 {len(res)}　期間 {res['end'].min().date()} → {res['end'].max().date()}")
    print(f"  sup-Wald 統計量 = {stat:.3f}")
    print(f"  估計斷點        = {date.date()}")
    print(f"  bootstrap p 值  = {p:.4f}")
    sig = p < ALPHA
    print(f"  → {'顯著（有斷點）' if sig else '不顯著（沒有斷點證據）'}")
    # 斷點前後的平均，純描述
    print(f"  斷點前平均 {y[:i].mean():.3f}　斷點後平均 {y[i:].mean():.3f}")
    return sig, date, p


def main():
    rng = np.random.default_rng(SEED)
    print()
    print("V7b：家計—市場脫鉤是水準位移還是趨勢？")
    print("判準見 04-indicators/V7b-預先登記.md（於本次執行前已 commit）")
    print()
    print("⚠️ 假說來自 V7 同一份資料。處置表只能維持或下修 S6，不能上修。")

    try:
        mich = load_fred("MICH")
        t5y = load_fred("T5YIFR")
        t10 = load_fred("T10YIE")
    except FileNotFoundError as e:
        print(); print(e); sys.exit(1)

    main_res = rolling_comovement(mich, t5y)
    plac_res = rolling_comovement(t5y, t10)

    sig, date, p = run_break(main_res, "家計 vs 市場（Δ MICH vs Δ T5YIFR）", rng)

    # ---- B2 ----
    print()
    print("=" * 78)
    print("B2：斷點落在哪裡（**反證用，不作為支持**）")
    print(f"  判準 — 斷點與任一非媒體對照日期相距 <= {RIVAL_MONTHS} 個月即觸發反證")
    print("=" * 78)
    b2_triggered = False
    if date is not None:
        print(f"{'對照事件':<18}{'日期':>10}{'相距(月)':>12}{'反證':>8}")
        print("-" * 78)
        for name, d in RIVAL_DATES:
            rd = pd.Timestamp(d)
            months = abs((date.year - rd.year) * 12 + (date.month - rd.month))
            hit = months <= RIVAL_MONTHS
            b2_triggered = b2_triggered or hit
            print(f"{name:<18}{d:>10}{months:>12}{('觸發' if hit else '—'):>8}")
        print("-" * 78)
        print(f"  B2 {'**觸發反證**：斷點更可能來自總體衝擊' if b2_triggered else '未觸發'}")

    # ---- B3 ----
    print()
    print("=" * 78)
    print("B3：安慰劑 — 市場內部（Δ T5YIFR vs Δ T10YIE）")
    print(f"  判準 — 市場內部也在同一時點 ±{RIVAL_MONTHS} 個月顯著斷裂即觸發反證")
    print("=" * 78)
    sig_p, date_p, p_p = run_break(plac_res, "市場內部", rng)
    b3_triggered = False
    if sig_p and date is not None and date_p is not None:
        months = abs((date.year - date_p.year) * 12 + (date.month - date_p.month))
        b3_triggered = months <= RIVAL_MONTHS
        print(f"\n  與主要規格斷點相距 {months} 個月"
              f" → B3 {'**觸發反證**：斷點非家計通道特有' if b3_triggered else '未觸發'}")
    else:
        print("\n  市場內部沒有顯著斷點 → B3 未觸發")

    # ---- 處置 ----
    print()
    print("=" * 78)
    print("依 V7b-預先登記.md 第 3 節的處置表")
    print("=" * 78)
    print(f"  B1 顯著={sig}　B2 反證={b2_triggered}　B3 反證={b3_triggered}")
    print()
    if not sig:
        print("  B1 不顯著 → **維持證據混雜**，並記下「水準位移的說法未獲支持」。")
        print("  那個 2016 斷點很可能只是四段平均值的雜訊。")
    elif b2_triggered:
        print("  B1 顯著但 B2 觸發 → **維持證據混雜**，並記下")
        print("  「斷點更可能來自總體衝擊而非媒體結構」。對媒體故事不利。")
    elif b3_triggered:
        print("  B1 顯著但 B3 觸發 → **維持證據混雜**，並記下")
        print("  「斷點非家計通道特有」。直接打擊 S6 的不對稱主張。")
    else:
        print("  B1 顯著、B2 與 B3 都沒觸發 → **維持證據混雜**，並記下")
        print("  「水準位移的說法通過了本輪反證，但仍是樣本內」。")
    print()
    print("  ⚠️ 四種結果都**不會**讓 S6 升到「有支持」——假說來自同一份資料。")
    print("     上修需要樣本外證據（例如歐元區的家計 vs 市場預期），那是 V7c。")
    print("  ⚠️ 區塊長度 24 低估了重疊視窗誘發的相依，偏向於「找到斷點」。")
    print("     這個偏誤的方向對本檢定不利，讀結果時要記住。")
    print("  ⚠️ 斷點日期的估計本身有很大不確定性，不得當成精確日期來講故事。")


if __name__ == "__main__":
    main()
