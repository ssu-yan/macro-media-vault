#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1c：把「狀態相依」從說法變成檢定

V1 的四段結果（增量 R²，h=6）：
    1978–1999  0.029
    2000–2012  0.167
    2013–2020  0.002
    2021–2026  0.134

沒有時間趨勢。我的解釋是「狀態相依」——情緒的解釋力跟著**總體波動**走，
波動大的時期強、平靜期弱。但這只是看四個數字講故事，需要真的檢定。

做法：滾動 10 年視窗，每個視窗算兩個東西——
  (a) 情緒的增量 R²
  (b) 該視窗內消費成長的標準差（總體波動的直接測量）
然後問三個問題：
  1. 兩者相關嗎？（狀態相依假說）
  2. 增量 R² 對時間有趨勢嗎？（媒體衰退假說的直接檢定）
  3. **控制住波動之後**，時間趨勢還在嗎？← 這題才是真正的裁判

若第 3 題的時間係數不顯著 → 沒有獨立於波動的媒體衰退效應，S5 的原始主張死透。
若仍顯著為負 → 波動之外還有東西在侵蝕，媒體假說重新活過來。

執行：python3 V1c_state_dependence.py
"""

import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from V1_backtest import build_dataset, ols_hac, COVID  # noqa: E402

WINDOW = 120          # 滾動視窗長度（月）
STEP = 3              # 每 3 個月推進一次
H = 6                 # 預測期
CONTROLS = ["pce_g_lag", "inc_g_lag", "unrate_chg", "ff_lvl"]


def incr_r2(d, h):
    y = d[f"y{h}"].to_numpy(float)
    Xc = d[CONTROLS].to_numpy(float)
    Xf = d[["sent_lvl"] + CONTROLS].to_numpy(float)
    _, _, r2c, _ = ols_hac(y, Xc, lag=h)
    _, _, r2f, _ = ols_hac(y, Xf, lag=h)
    return r2f - r2c


def main():
    df = build_dataset()
    cols = [f"y{H}", "sent_lvl"] + CONTROLS
    d = df[cols].dropna()
    d = d.drop(d.loc[COVID[0]:COVID[1]].index, errors="ignore")

    rows = []
    for i in range(0, len(d) - WINDOW + 1, STEP):
        w = d.iloc[i:i + WINDOW]
        try:
            r = incr_r2(w, H)
        except Exception:
            continue
        rows.append({
            "end": w.index[-1],
            "incr_r2": r,
            "vol": float(w[f"y{H}"].std(ddof=1)),
        })

    res = pd.DataFrame(rows).dropna()
    if len(res) < 20:
        print("視窗數不足")
        return

    res["t_idx"] = (res["end"] - res["end"].iloc[0]).dt.days / 365.25

    print()
    print("=" * 70)
    print(f"滾動 {WINDOW} 個月視窗，h={H}，共 {len(res)} 個視窗")
    print(f"視窗結束日範圍：{res['end'].min().date()} → {res['end'].max().date()}")
    print("=" * 70)

    # 每十年看一眼，確認資料長相
    print(f"\n{'視窗結束':<12}{'增量R²':>10}{'消費成長sd':>12}")
    print("-" * 34)
    for _, r in res.iloc[::max(len(res) // 12, 1)].iterrows():
        print(f"{str(r['end'].date()):<12}{r['incr_r2']:>10.3f}{r['vol']:>12.2f}")

    print()
    print("=" * 70)
    print("問題 1：增量 R² 與總體波動相關嗎？（狀態相依假說）")
    print("=" * 70)
    c = res["incr_r2"].corr(res["vol"])
    print(f"  相關係數 = {c:+.3f}")
    print(f"  → {'支持狀態相依' if c > 0.3 else ('不支持' if c < 0.1 else '弱')}")

    print()
    print("=" * 70)
    print("問題 2：增量 R² 對時間有下降趨勢嗎？（媒體衰退假說）")
    print("=" * 70)
    y = res["incr_r2"].to_numpy(float)
    b1, se1, r2_1, n1 = ols_hac(y, res[["t_idx"]].to_numpy(float), lag=40)
    print(f"  時間係數 = {b1[1]:+.5f}/年   t(HAC) = {b1[1]/se1[1]:+.2f}   R² = {r2_1:.3f}")
    print(f"  → {'顯著下降' if b1[1] < 0 and abs(b1[1]/se1[1]) > 2 else '無顯著下降趨勢'}")

    print()
    print("=" * 70)
    print("問題 3：控制波動之後，時間趨勢還在嗎？  ← 裁判")
    print("=" * 70)
    X = res[["t_idx", "vol"]].to_numpy(float)
    b2, se2, r2_2, n2 = ols_hac(y, X, lag=40)
    t_time = b2[1] / se2[1]
    t_vol = b2[2] / se2[2]
    print(f"  時間係數 = {b2[1]:+.5f}/年   t(HAC) = {t_time:+.2f}")
    print(f"  波動係數 = {b2[2]:+.5f}      t(HAC) = {t_vol:+.2f}")
    print(f"  R² = {r2_2:.3f}")
    print()
    if b2[1] < 0 and abs(t_time) > 2:
        print("  → 時間趨勢**顯著為負**：波動之外還有東西在侵蝕情緒指標的資訊含量")
        print("    → 媒體假說重新活過來。")
    elif b2[1] > 0 and abs(t_time) > 2:
        print("  → 時間趨勢**顯著為正**。不只是沒有衰退，情緒指標的增量資訊含量")
        print("    在控制波動後還略為**上升**。S5 的原始主張（媒體侵蝕預測力）死透。")
    else:
        print("  → 時間趨勢**不顯著**：沒有獨立於總體波動的衰退效應。")
        print("    S5 的原始主張（媒體侵蝕預測力）不成立。")

    if c < 0:
        print()
        print("  ⚠️ 附帶結果：增量 R² 與波動的相關是**負的**，與「波動期解釋力較強」")
        print("     的直覺相反。所以「狀態相依」這個補救解釋，方向也錯了。")

    print()
    print("注意：滾動視窗高度重疊，這些檢定的有效自由度遠低於視窗數。")
    print("     HAC lag 已設為 40（約 10 年 × 4 個 step），但仍應把 t 值當作")
    print("     方向性參考而非嚴格推論。")

    res.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "V1c_rolling.csv"), index=False)
    print("\n滾動結果已存成 V1c_rolling.csv")


if __name__ == "__main__":
    main()
