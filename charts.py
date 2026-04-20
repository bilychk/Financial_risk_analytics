"""
charts.py — all charts.
Each function takes the required data and saves a PNG to CHARTS_DIR.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

from config import FUND_LABEL, BENCH_LABEL, CHARTS_DIR
from metrics import ann_return, ann_vol, drawdown_series

COLORS = {FUND_LABEL: "#1f77b4", BENCH_LABEL: "#ff7f0e"}


def _style(ax: plt.Axes, title: str, ylabel: str) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_title(title, fontweight="bold", fontsize=12)
    ax.set_ylabel(ylabel)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")


def _save(name: str) -> None:
    path = os.path.join(CHARTS_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


def chart_nav(weekly: pd.DataFrame) -> None:
    """NAV levels for both funds."""
    fig, ax = plt.subplots(figsize=(11, 5))
    for lbl, ls in [(FUND_LABEL, "-"), (BENCH_LABEL, "--")]:
        ax.plot(weekly.index, weekly[lbl], lw=2, color=COLORS[lbl], ls=ls, label=lbl)
    _style(ax, "NAV levels", "EUR")
    ax.legend()
    _save("chart1_nav.png")


def chart_cumulative(returns: pd.DataFrame) -> None:
    """Cumulative return chart."""
    cum = (1 + returns).cumprod() - 1
    fig, ax = plt.subplots(figsize=(11, 5))
    for lbl, ls in [(FUND_LABEL, "-"), (BENCH_LABEL, "--")]:
        ax.plot(cum.index, cum[lbl] * 100, lw=2, color=COLORS[lbl], ls=ls, label=lbl)
    ax.axhline(0, color="gray", lw=0.8)
    _style(ax, "Cumulative return", "%")
    ax.legend()
    _save("chart2_cumulative.png")


def chart_drawdowns(returns: pd.DataFrame) -> None:
    """Drawdown chart."""
    fig, ax = plt.subplots(figsize=(11, 5))
    for lbl, ls in [(FUND_LABEL, "-"), (BENCH_LABEL, "--")]:
        dd = drawdown_series(returns[lbl]) * 100
        ax.plot(returns.index, dd, lw=2, color=COLORS[lbl], ls=ls, label=f"{lbl} drawdown")
    ax.axhline(0, color="gray", lw=0.8)
    _style(ax, "Drawdown comparison", "%")
    ax.legend()
    _save("chart3_drawdowns.png")


def chart_risk_return(returns: pd.DataFrame) -> None:
    """Risk / Return scatter plot."""
    fig, ax = plt.subplots(figsize=(7, 5))
    for lbl in [FUND_LABEL, BENCH_LABEL]:
        r = returns[lbl]
        x, y = ann_vol(r) * 100, ann_return(r) * 100
        ax.scatter(x, y, s=180, color=COLORS[lbl], zorder=5, label=lbl)
        ax.annotate(lbl, (x, y), textcoords="offset points", xytext=(8, 4), fontsize=9)
    ax.set_xlabel("Annualized Volatility (%)")
    ax.set_ylabel("Annualized Return (%)")
    ax.set_title("Risk / Return", fontweight="bold", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(linestyle="--", alpha=0.3)
    ax.legend()
    _save("chart4_risk_return.png")


def chart_metrics_grouped(returns: pd.DataFrame, metrics: pd.DataFrame) -> None:
    """
    Three grouped bar charts with compatible units:
      - Return & Risk (%)
      - Ratios (dimensionless)
      - Relative metrics
    """
    groups = [
        ("Return & Risk (%)",   ["Annualized Return", "Annualized Volatility", "Max Drawdown"]),
        ("Ratios",              ["Sharpe Ratio", "Sortino Ratio", "Calmar Ratio", "Information Ratio"]),
        ("Relative metrics",    ["Beta vs Benchmark", "Tracking Error"]),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    x = np.arange(2)

    for ax, (title, keys) in zip(axes, groups):
        width = 0.8 / len(keys)
        for i, key in enumerate(keys):
            vals = metrics.loc[key].values.astype(float)
            # convert to % where applicable
            if any(k in key for k in ("Return", "Volatility", "Drawdown", "Error")):
                vals = vals * 100
            offset = (i - len(keys) / 2 + 0.5) * width
            ax.bar(x + offset, vals, width * 0.9, label=key)
        ax.set_xticks(x)
        ax.set_xticklabels([FUND_LABEL, BENCH_LABEL], rotation=0)
        ax.set_title(title, fontweight="bold", fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.legend(fontsize=7)

    _save("chart5_metrics_grouped.png")


def save_all(weekly: pd.DataFrame, returns: pd.DataFrame, metrics: pd.DataFrame) -> None:
    """Generates and saves all five charts."""
    print("\nGenerating charts:")
    chart_nav(weekly)
    chart_cumulative(returns)
    chart_drawdowns(returns)
    chart_risk_return(returns)
    chart_metrics_grouped(returns, metrics)
