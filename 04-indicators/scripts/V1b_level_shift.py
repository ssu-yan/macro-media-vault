#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1b：區分「預測力消失」與「校準漂移」

V1 的結果顯示情緒指標的**增量預測力沒有衰退**（2021–2026 反而是三段最高）。
但這跟「信心跌到 49.5、消費卻沒崩」的觀察並不矛盾——因為那是**水準**的脫鉤，
不是**共變**的消失。

兩者是可以分開檢驗的：
  - 共變還在  → 情緒的「變化」仍能預測消費的「變化」（V1 已證實）
  - 水準漂移  → 用歷史關係外推，會系統性低估近年的消費

檢驗方法：用 2019 年以前的資料估計關係，外推到 2021 年以後，看預測誤差是否
系統性偏向一邊。若近年的實際消費**持續高於**模型預測 → 校準漂移成立。

執行：python3 V1b_level_shift.py（需與 V1_backtest.py 同層，共用 data/）
"""

import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from V1_backtest import build_dataset, ols_hac, COVID  # noqa: E402

TRAIN_END = "2019-12"
TEST_START = "2021-01"
HORIZONS = [3, 6, 12]
CONTROLS = ["pce_g_lag", "inc_g_lag", "unrate_chg", "ff_lvl"]


def run(df, h, use_controls=True):
    cols = [f"y{h}", "sent_lvl"] + (CONTROLS if use_controls else [])
    d = df[cols].dropna()

    train = d.loc[:TRAIN_END]
    train = train.drop(train.loc[COVID[0]:COVID[1]].index, errors="ignore")
    test = d.loc[TEST_START:]
    if len(train) < 40 or len(test) < 12:
        return None

    xcols = ["sent_lvl"] + (CONTROLS if use_controls else [])
    ytr = train[f"y{h}"].to_numpy(float)
    Xtr = train[xcols].to_numpy(float)
    beta, se, r2, n = ols_hac(ytr, Xtr, lag=h)

    Xte = np.column_stack([np.ones(len(test)), test[xcols].to_numpy(float)])
    pred = Xte @ beta
    actual = test[f"y{h}"].to_numpy(float)
    err = actual - pred

    # 誤差是否系統性偏向一邊：對常數做 HAC 檢定
    b0, se0, _, n0 = ols_hac(err, np.zeros((len(err), 0)), lag=h)
    return {
        "n_train": n, "n_test": len(test),
        "bias": float(err.mean()),
        "t_bias": float(b0[0] / se0[0]) if se0[0] > 0 else np.nan,
        "pos_share": float((err > 0).mean()),
        "r2_train": r2,
    }


def main():
    df = build_dataset()
    for label, uc in [("完整模型（情緒＋控制變數）", True), ("僅情緒（無控制變數）", False)]:
        print()
        print("=" * 76)
        print(f"樣本外偏誤檢定 — {label}")
        print(f"訓練：起點 ~ {TRAIN_END}（排除 COVID） ｜ 測試：{TEST_START} ~ 迄今")
        print("=" * 76)
        print(f"{'h':>3}{'N訓練':>7}{'N測試':>7}{'訓練R²':>9}"
              f"{'平均誤差(pp)':>14}{'t(HAC)':>9}{'低估比例':>10}")
        print("-" * 76)
        for h in HORIZONS:
            r = run(df, h, uc)
            if r is None:
                print(f"{h:>3}{'樣本不足':>14}")
                continue
            print(f"{h:>3}{r['n_train']:>7}{r['n_test']:>7}{r['r2_train']:>9.3f}"
                  f"{r['bias']:>14.2f}{r['t_bias']:>9.2f}{r['pos_share']*100:>9.0f}%")
        print("-" * 76)

    print()
    print("判讀：")
    print("  平均誤差 = 實際消費成長 − 模型預測（年化 pp）。")
    print("  **顯著為正** → 近年實際消費持續高於情緒所預示 → 校準漂移成立，")
    print("                  「信心 50 = 衰退」這個歷史對應關係已經失效。")
    print("  接近零     → 沒有水準漂移，脫鉤的觀察需要別的解釋。")
    print("  低估比例   = 模型低估的月份佔比；越接近 100% 表示偏誤越系統性。")


if __name__ == "__main__":
    main()
