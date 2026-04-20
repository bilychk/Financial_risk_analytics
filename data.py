"""
data.py — fetching and preparing NAV data from pensionikeskus.ee.
"""

from io import StringIO

import pandas as pd
import requests

from config import (
    START_DATE, END_DATE,
    FUND_ID, FUND_LABEL,
    BENCH_ID, BENCH_LABEL,
    PERIODS_YEAR,
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.pensionikeskus.ee/",
}


def _fmt(date_str: str) -> str:
    """YYYY-MM-DD → DD.MM.YYYY (pensionikeskus query format)."""
    return pd.to_datetime(date_str).strftime("%d.%m.%Y")


def fetch_nav(fund_id: int, label: str,
              date_from: str = START_DATE,
              date_to: str = END_DATE) -> pd.Series:
    """Downloads NAV series for one fund, returns pd.Series indexed by Date."""
    url = (
        "https://www.pensionikeskus.ee/en/statistics/ii-pillar/nav-of-funded-pension/"
        f"?date_from={_fmt(date_from)}&date_to={_fmt(date_to)}"
        f"&download=xls&f%5B0%5D={fund_id}"
    )
    print(f"  Fetching {label} (id={fund_id}) ...")

    session = requests.Session()
    session.get(
        "https://www.pensionikeskus.ee/en/statistics/ii-pillar/nav-of-funded-pension/",
        headers=HEADERS,
        timeout=30,
    )
    resp = session.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    # Site returns UTF-16 tab-separated text (despite the .xls extension)
    text = resp.content.decode("utf-16", errors="replace")

    df = pd.read_csv(
        StringIO(text),
        sep="\t",
        decimal=",",
        thousands=" ",
        engine="python",
    )
    df.columns = [c.strip() for c in df.columns]

    # Columns: Date, Fund, Shortname, ISIN, NAV, Change %
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["NAV"] = (
        df["NAV"].astype(str)
        .str.replace(r"[\xa0\s]", "", regex=True)
        .str.replace(",", ".", regex=False)
    )
    df["NAV"] = pd.to_numeric(df["NAV"], errors="coerce")

    result = (
        df.dropna(subset=["Date", "NAV"])
        .sort_values("Date")
        .drop_duplicates("Date")
        .set_index("Date")["NAV"]
        .rename(label)
    )
    print(f"  Got {len(result)} data points: {result.index.min().date()} → {result.index.max().date()}")
    return result


def load_weekly() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads both funds, merges them, resamples to weekly (Friday).
    Returns:
        weekly  — DataFrame with NAV levels (weekly frequency)
        returns — DataFrame with percentage changes (first NaN row dropped)
    """
    print("Loading data:")
    fund_nav  = fetch_nav(FUND_ID,  FUND_LABEL)
    bench_nav = fetch_nav(BENCH_ID, BENCH_LABEL)

    weekly = (
        pd.concat([fund_nav, bench_nav], axis=1)
        .resample("W-FRI").last()
        .ffill()
        .dropna()
    )

    returns = weekly.pct_change().dropna()

    print(f"  Period : {weekly.index.min().date()} → {weekly.index.max().date()}")
    print(f"  Weeks  : {len(returns)}")

    return weekly, returns
