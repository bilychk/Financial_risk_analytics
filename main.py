"""
main.py — entry point.
Run: python main.py

"""

import os

from config import OUTPUT_DIR, CHARTS_DIR, ESG_PROFILES, FUND_LABEL, BENCH_LABEL
from data import load_weekly
from metrics import build_metrics_table
from charts import save_all

os.makedirs(CHARTS_DIR, exist_ok=True)


def save_summary(metrics, weekly, returns) -> None:
    lines = [
        f"Period : {weekly.index.min().date()} → {weekly.index.max().date()}",
        f"Weeks  : {len(returns)}",
        "",
        "─── Metrics ────────────────────────────────────────",
    ]
    for metric in metrics.index:
        fv = metrics.loc[metric, FUND_LABEL]
        bv = metrics.loc[metric, BENCH_LABEL]
        fv_str = f"{fv:.4f}" if isinstance(fv, float) else str(fv)
        bv_str = f"{bv:.4f}" if isinstance(bv, float) else str(bv)
        lines.append(f"  {metric:<28} {FUND_LABEL}: {fv_str:<10}  {BENCH_LABEL}: {bv_str}")

    lines += ["", "─── ESG Profiles ───────────────────────────────────"]
    for fund, profile in ESG_PROFILES.items():
        lines.append(f"  {fund}")
        lines.append(f"    SFDR: {profile['sfdr_article']}")
        lines.append(f"    {profile['description']}")

    path = os.path.join(OUTPUT_DIR, "summary.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nSummary saved: {path}")


def main() -> None:
    # 1. data
    weekly, returns = load_weekly()

    # 2. metrics
    fr, br = returns[FUND_LABEL], returns[BENCH_LABEL]
    metrics = build_metrics_table(fr, br)

    print("\nMetrics:")
    print(metrics.applymap(lambda x: f"{x:.4f}" if isinstance(x, float) else x))

    # 3. save CSV
    metrics.to_csv(os.path.join(OUTPUT_DIR, "metrics.csv"))
    returns.to_csv(os.path.join(OUTPUT_DIR, "weekly_returns.csv"))

    # 4. charts
    save_all(weekly, returns, metrics)

    # 5. text summary
    save_summary(metrics, weekly, returns)

    print("\nDone.")
    print(f"  Charts  → {CHARTS_DIR}")
    print(f"  Metrics → {os.path.join(OUTPUT_DIR, 'metrics.csv')}")


if __name__ == "__main__":
    main()
