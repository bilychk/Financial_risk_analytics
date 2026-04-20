"""
metrics.py — financial metrics.
All functions accept pd.Series of weekly returns.
"""

import numpy as np
import pandas as pd

from config import RF_ANNUAL, PERIODS_YEAR, FUND_LABEL, BENCH_LABEL


# ── helper ────────────────────────────────────────────────────────────────────

def _rf_per_period() -> float:
    return (1 + RF_ANNUAL) ** (1 / PERIODS_YEAR) - 1


# ── single-series metrics ─────────────────────────────────────────────────────

def ann_return(r: pd.Series) -> float:
    """Annualized return (geometric)."""
    return (1 + r).prod() ** (PERIODS_YEAR / len(r)) - 1


def ann_vol(r: pd.Series) -> float:
    """Annualized volatility."""
    return r.std() * PERIODS_YEAR ** 0.5


def sharpe(r: pd.Series) -> float:
    """Sharpe ratio."""
    excess = r - _rf_per_period()
    return (excess.mean() / r.std()) * PERIODS_YEAR ** 0.5


def sortino(r: pd.Series) -> float:
    """Sortino ratio (denominator uses downside deviation only)."""
    excess = r - _rf_per_period()
    downside_std = r[r < 0].std() * PERIODS_YEAR ** 0.5
    if downside_std == 0:
        return np.nan
    return excess.mean() * PERIODS_YEAR / downside_std


def calmar(r: pd.Series) -> float:
    """Calmar ratio = annualized return / |max drawdown|."""
    dd = abs(max_drawdown(r))
    return ann_return(r) / dd if dd else np.nan


def max_drawdown(r: pd.Series) -> float:
    """Maximum drawdown (negative number)."""
    wealth = (1 + r).cumprod()
    return ((wealth - wealth.cummax()) / wealth.cummax()).min()


def drawdown_series(r: pd.Series) -> pd.Series:
    """Time series of drawdowns."""
    wealth = (1 + r).cumprod()
    return (wealth - wealth.cummax()) / wealth.cummax()


# ── benchmark-relative metrics ────────────────────────────────────────────────

def beta(fr: pd.Series, br: pd.Series) -> float:
    """Beta of fund relative to benchmark."""
    arr = pd.concat([fr, br], axis=1).dropna().values
    return np.cov(arr.T)[0, 1] / np.var(arr[:, 1])


def tracking_error(fr: pd.Series, br: pd.Series) -> float:
    """Annualized tracking error."""
    return (fr - br).std() * PERIODS_YEAR ** 0.5


def information_ratio(fr: pd.Series, br: pd.Series) -> float:
    """Information ratio."""
    active = fr - br
    te = active.std() * PERIODS_YEAR ** 0.5
    return active.mean() * PERIODS_YEAR / te if te else np.nan


# ── summary table ─────────────────────────────────────────────────────────────

def build_metrics_table(fr: pd.Series, br: pd.Series) -> pd.DataFrame:
    """Returns a DataFrame with all metrics for both funds."""
    return pd.DataFrame({
        FUND_LABEL: {
            "Annualized Return":     ann_return(fr),
            "Annualized Volatility": ann_vol(fr),
            "Sharpe Ratio":          sharpe(fr),
            "Sortino Ratio":         sortino(fr),
            "Calmar Ratio":          calmar(fr),
            "Max Drawdown":          max_drawdown(fr),
            "Beta vs Benchmark":     beta(fr, br),
            "Tracking Error":        tracking_error(fr, br),
            "Information Ratio":     information_ratio(fr, br),
        },
        BENCH_LABEL: {
            "Annualized Return":     ann_return(br),
            "Annualized Volatility": ann_vol(br),
            "Sharpe Ratio":          sharpe(br),
            "Sortino Ratio":         sortino(br),
            "Calmar Ratio":          calmar(br),
            "Max Drawdown":          max_drawdown(br),
            "Beta vs Benchmark":     1.0,
            "Tracking Error":        0.0,
            "Information Ratio":     np.nan,
        },
    })
