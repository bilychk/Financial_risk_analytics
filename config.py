"""
config.py — all project constants in one place.
To change benchmark, dates, or paths — edit only this file.
"""

import os

# ── paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CHARTS_DIR = os.path.join(OUTPUT_DIR, "charts")

# ── analysis period ───────────────────────────────────────────────────────────
START_DATE = "2024-01-01"
END_DATE   = "2026-04-17"

# ── funds (pensionikeskus.ee fund IDs) ───────────────────────────────────────
# ID can be verified in the fund page URL:
# https://www.pensionikeskus.ee/en/ii-pillar/mandatory-pension-funds/fid/<ID>/
FUND_ID    = 48;  FUND_LABEL  = "Luminor 50-56"
BENCH_ID   = 38;  BENCH_LABEL = "LHV Julge"   # formerly LHV XL, renamed

# ── calculation parameters ────────────────────────────────────────────────────
RF_ANNUAL    = 0.03   # risk-free rate proxy, annual
PERIODS_YEAR = 52     # weekly data → 52 periods per year

# ── ESG profiles (from public reports / SFDR) ────────────────────────────────
# Pensionikeskus does not publish numeric ESG scores in NAV tables,
# so we use qualitative SFDR classification instead.
ESG_PROFILES = {
    FUND_LABEL: {
        "sfdr_article": "Article 8",
        "description":  "Promotes ESG characteristics; excludes controversial weapons & tobacco",
    },
    BENCH_LABEL: {
        "sfdr_article": "Article 6",
        "description":  "No formal ESG screen; broad active equity mandate",
    },
}
