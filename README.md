# Luminor 50-56 vs LHV Julge — Pension Fund Analysis

A Python tool for comparing two Estonian II pillar pension funds using publicly available NAV data from [pensionikeskus.ee](https://www.pensionikeskus.ee).

---

## What it does

- Fetches historical NAV data directly from pensionikeskus.ee
- Resamples daily data to weekly frequency
- Computes a full set of performance and risk metrics
- Generates five charts as PNG files
- Saves a text summary and CSV exports

---

## Funds compared

| | Fund | Benchmark |
|---|---|---|
| **Name** | Luminor 50-56 | LHV Julge (formerly LHV XL) |
| **Pensionikeskus ID** | 48 | 38 |
| **SFDR** | Article 8 | Article 6 |

The fund and benchmark can be changed in `config.py` — just update the IDs and labels.

---

## Metrics calculated

| Metric | Description |
|---|---|
| Annualized Return | Geometric annualized return |
| Annualized Volatility | Annualized standard deviation of weekly returns |
| Sharpe Ratio | Excess return per unit of total risk (RF = 3%) |
| Sortino Ratio | Excess return per unit of downside risk |
| Calmar Ratio | Annualized return divided by max drawdown |
| Max Drawdown | Largest peak-to-trough decline |
| Beta vs Benchmark | Sensitivity of the fund to benchmark moves |
| Tracking Error | Annualized std of active returns |
| Information Ratio | Active return per unit of tracking error |

---

## Charts generated

| File | Description |
|---|---|
| `chart1_nav.png` | NAV levels over time |
| `chart2_cumulative.png` | Cumulative return comparison |
| `chart3_drawdowns.png` | Drawdown comparison |
| `chart4_risk_return.png` | Risk / Return scatter |
| `chart5_metrics_grouped.png` | All metrics as grouped bar charts |

---

## Project structure

```
Luminor/
├── main.py          # Entry point — run this
├── config.py        # All settings: fund IDs, dates, risk-free rate
├── data.py          # Data fetching from pensionikeskus.ee
├── metrics.py       # Financial metrics calculations
├── charts.py        # Chart generation (matplotlib)
└── output/
    ├── charts/      # PNG charts (auto-created)
    ├── metrics.csv  # Metrics table
    ├── weekly_returns.csv
    └── summary.txt  # Human-readable summary
```

---

## Configuration

All parameters are in `config.py`:

```python
START_DATE   = "2024-01-01"   # analysis start
END_DATE     = "2026-04-17"   # analysis end
FUND_ID      = 48             # pensionikeskus.ee fund ID
BENCH_ID     = 38             # benchmark fund ID
RF_ANNUAL    = 0.03           # risk-free rate (annual)
PERIODS_YEAR = 52             # weekly data
```

Fund IDs can be found in the URL of any fund page on pensionikeskus.ee:
`https://www.pensionikeskus.ee/en/ii-pillar/mandatory-pension-funds/fid/<ID>/`

---

## Notes

- pensionikeskus.ee returns data as a UTF-16 tab-separated file despite the `.xls` extension — `data.py` handles this automatically
- Missing dates (holidays, no trading) are forward-filled before resampling
- Benchmark-relative metrics (Beta, Tracking Error, Information Ratio) are only meaningful for the fund column; benchmark values are set to `1.0`, `0.0`, and `NaN` respectively
