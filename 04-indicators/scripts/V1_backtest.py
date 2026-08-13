#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1 驗證任務：消費者信心對後續實質消費支出的預測力，是否隨時間衰退？

對應節點：01-nodes-short/S5-情緒與支出脫鉤.md
判準：若「情緒的增量解釋力」逐段下降 → 支持沙盤主線
      若三段穩定 → 整張沙盤可信度大幅下修

--------------------------------------------------------------------
需要的資料（從 FRED 下載 CSV，放到本檔同層的 data/ 資料夾）
    https://fred.stlouisfed.org/series/UMCSENT   → data/UMCSENT.csv
    https://fred.stlouisfed.org/series/PCEC96    → data/PCEC96.csv
    https://fred.stlouisfed.org/series/UNRATE    → data/UNRATE.csv
    https://fred.stlouisfed.org/series/FEDFUNDS  → data/FEDFUNDS.csv
    https://fred.stlouisfed.org/series/DSPIC96   → data/DSPIC96.csv
每個頁面右上角 Download → CSV，檔名不用改。

執行：  python3 V1_backtest.py
相依：  pandas, numpy（不需要 statsmodels，OLS 與 Newey-West 都自己算）
--------------------------------------------------------------------

方法要點（為什麼這樣設計）：
1. 用「增量 R²」而非「總 R²」。單看總 R² 會被控制變數主導，看不出情緒本身
   的貢獻。增量 R² = 完整模型 R² − 只有控制變數的模型 R²，這才是「情緒多告訴
   了我們什麼」。
2. 重疊樣本（overlapping windows）造成殘差自相關，OLS 標準誤會嚴重低估，
   所以用 Newey-West HAC 修正，lag 設為 h（預測期數）。
3. COVID 必須單獨處理。2020 年 3–5 月的消費崩跌與反彈是史上最大的離群值，
   會完全主導 2013–2020 這一段。所以每段都跑「含 / 不含 2020」兩個版本；
   兩者結論不一致時，以排除版為準，並在筆記中註明。
"""

import os
import sys
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

SEGMENTS = [
    ("2000-01", "2012-12", "2000–2012"),
    ("2013-01", "2020-12", "2013–2020"),
    ("2021-01", "2026-12", "2021–2026"),
]
HORIZONS = [3, 6, 12]          # 預測未來幾個月
COVID = ("2020-02", "2020-09")  # 排除版要拿掉的區間


# ---------- 資料讀取 ----------

def load_fred(series_id):
    """讀 FRED 匯出的 CSV。FRED 的欄位名稱格式改過好幾次，這裡一律取前兩欄。"""
    path = os.path.join(DATA_DIR, f"{series_id}.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"缺少 {path}\n"
            f"請到 https://fred.stlouisfed.org/series/{series_id} 下載 CSV 放進 data/"
        )
    df = pd.read_csv(path)
    df = df.iloc[:, :2]
    df.columns = ["date", series_id]
    df["date"] = pd.to_datetime(df["date"])
    df[series_id] = pd.to_numeric(df[series_id], errors="coerce")
    s = df.dropna().set_index("date")[series_id]
    # 統一成月初，避免不同序列的日期標記對不上
    s.index = s.index.to_period("M").to_timestamp()
    return s


def build_dataset():
    umc = load_fred("UMCSENT")      # 密西根消費者信心（指數）
    pce = load_fred("PCEC96")       # 實質個人消費支出（月，chained $）
    unrate = load_fred("UNRATE")    # 失業率
    ff = load_fred("FEDFUNDS")      # 聯邦資金利率
    inc = load_fred("DSPIC96")      # 實質可支配所得

    df = pd.concat([umc, pce, unrate, ff, inc], axis=1).sort_index()

    # 解釋變數：信心的水準（標準化）與 12 個月變化
    df["sent_lvl"] = df["UMCSENT"]
    df["sent_chg"] = df["UMCSENT"] - df["UMCSENT"].shift(12)

    # 控制變數：都必須是「當期已知」的資訊，不能用到未來
    df["pce_g_lag"] = np.log(df["PCEC96"]).diff(12) * 100      # 過去 12 個月消費成長（動能）
    df["inc_g_lag"] = np.log(df["DSPIC96"]).diff(12) * 100     # 過去 12 個月實質所得成長
    df["unrate_chg"] = df["UNRATE"] - df["UNRATE"].shift(12)   # 失業率 12 個月變化
    df["ff_lvl"] = df["FEDFUNDS"]

    # 被解釋變數：未來 h 個月的實質消費成長（年化 %）
    logpce = np.log(df["PCEC96"])
    for h in HORIZONS:
        df[f"y{h}"] = (logpce.shift(-h) - logpce) * (12.0 / h) * 100

    return df


# ---------- OLS + Newey-West ----------

def ols_hac(y, X, lag):
    """回傳 (beta, se_hac, r2, n)。X 不含常數項，函式內部自己加。"""
    n = len(y)
    X = np.column_stack([np.ones(n), X])
    k = X.shape[1]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    ss_res = float(resid @ resid)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    # Newey-West HAC 共變異數
    XtX_inv = np.linalg.pinv(X.T @ X)
    S = (X * resid[:, None]).T @ (X * resid[:, None])
    for L in range(1, lag + 1):
        w = 1.0 - L / (lag + 1.0)
        Xu = X * resid[:, None]
        G = Xu[L:].T @ Xu[:-L]
        S += w * (G + G.T)
    cov = XtX_inv @ S @ XtX_inv
    dof_adj = n / max(n - k, 1)
    se = np.sqrt(np.maximum(np.diag(cov) * dof_adj, 0))
    return beta, se, r2, n


def run_one(sub, h, sent_col):
    """對一個子樣本、一個預測期，跑控制模型與完整模型，回傳比較結果。"""
    controls = ["pce_g_lag", "inc_g_lag", "unrate_chg", "ff_lvl"]
    cols = [f"y{h}", sent_col] + controls
    d = sub[cols].dropna()
    if len(d) < 40:
        return None

    y = d[f"y{h}"].to_numpy(float)
    Xc = d[controls].to_numpy(float)
    Xf = d[[sent_col] + controls].to_numpy(float)

    # 標準化情緒變數，讓係數可跨期比較（單位＝1 個標準差）
    s = Xf[:, 0]
    Xf = Xf.copy()
    Xf[:, 0] = (s - s.mean()) / (s.std(ddof=1) if s.std(ddof=1) > 0 else 1)

    _, _, r2_c, _ = ols_hac(y, Xc, lag=h)
    beta, se, r2_f, n = ols_hac(y, Xf, lag=h)

    t = beta[1] / se[1] if se[1] > 0 else np.nan
    return {
        "n": n,
        "r2_controls": r2_c,
        "r2_full": r2_f,
        "incr_r2": r2_f - r2_c,
        "beta": beta[1],
        "t_hac": t,
    }


# ---------- 主流程 ----------

def report(df, sent_col, drop_covid, title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)
    print(f"{'期間':<12}{'h':>3}{'N':>6}{'R²(控制)':>11}{'R²(完整)':>11}"
          f"{'增量R²':>10}{'β(1sd)':>10}{'t(HAC)':>9}")
    print("-" * 78)

    table = {}
    for start, end, label in SEGMENTS:
        sub = df.loc[start:end]
        if drop_covid:
            sub = sub.drop(sub.loc[COVID[0]:COVID[1]].index, errors="ignore")
        for h in HORIZONS:
            r = run_one(sub, h, sent_col)
            if r is None:
                print(f"{label:<12}{h:>3}{'樣本不足':>12}")
                continue
            table[(label, h)] = r
            print(f"{label:<12}{h:>3}{r['n']:>6}{r['r2_controls']:>11.3f}"
                  f"{r['r2_full']:>11.3f}{r['incr_r2']:>10.3f}"
                  f"{r['beta']:>10.2f}{r['t_hac']:>9.2f}")
        print("-" * 78)
    return table


def verdict(table):
    print()
    print("=" * 78)
    print("判準檢查：情緒的增量解釋力是否逐段下降？")
    print("=" * 78)
    labels = [s[2] for s in SEGMENTS]
    declining = 0
    total = 0
    for h in HORIZONS:
        vals = [table.get((lb, h), {}).get("incr_r2") for lb in labels]
        if any(v is None for v in vals):
            continue
        total += 1
        mono = vals[0] > vals[1] > vals[2]
        last_lowest = vals[2] == min(vals)
        if mono:
            declining += 1
        print(f"  h={h:>2}m  增量R²: " +
              " → ".join(f"{v:.3f}" for v in vals) +
              f"   {'單調下降 ✓' if mono else ('末段最低 ~' if last_lowest else '未下降 ✗')}")
    print()
    if total == 0:
        print("  無法判定：樣本不足")
    elif declining == total:
        print("  → 三個預測期都單調下降：支持「情緒指標預測力衰退」")
        print("    沙盤 S5 分岔 B 成立，主線可信度上調。")
    elif declining > 0:
        print("  → 部分預測期下降：證據混雜。")
        print("    不足以確認，也不足以推翻。建議加做 V2（分政黨信心差距）再判斷。")
    else:
        print("  → 沒有下降：**這是對沙盤主線不利的結果**。")
        print("    依照 L5-長期市場均衡 的自我檢驗設計，整張沙盤可信度應大幅下修。")
        print("    請照實記錄，不要事後找理由解釋掉。")


def main():
    try:
        df = build_dataset()
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    print(f"資料範圍：{df.index.min().date()} → {df.index.max().date()}")
    print(f"UMCSENT 最新值：{df['UMCSENT'].dropna().iloc[-1]:.1f} "
          f"({df['UMCSENT'].dropna().index[-1].date()})")

    t1 = report(df, "sent_lvl", drop_covid=True,
                title="【主要規格】信心水準，排除 COVID (2020-02 ~ 2020-09)")
    verdict(t1)

    report(df, "sent_lvl", drop_covid=False,
           title="【穩健性 1】信心水準，含 COVID（預期 2013–2020 段被離群值主導）")

    report(df, "sent_chg", drop_covid=True,
           title="【穩健性 2】信心的 12 個月變化，排除 COVID")

    print()
    print("註：增量 R² = 完整模型 R² − 只含控制變數的模型 R²，")
    print("    也就是「信心指數在利率、失業、所得、消費動能之外，多解釋了多少」。")
    print("    t 值為 Newey-West HAC 修正（lag = h），已處理重疊樣本的自相關。")


if __name__ == "__main__":
    main()
