#!/usr/bin/env python3
"""Fetch the public GitHub contribution calendar and derive researcher stats.

No token or GraphQL API is used. Source: /users/<username>/contributions.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "syednafizreja"
URL = f"https://github.com/users/{USERNAME}/contributions"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "contributions.json"


def parse_cell(cell) -> tuple[date, int, int] | None:
    raw_date = cell.get("data-date")
    if not raw_date:
        return None
    try:
        day = date.fromisoformat(raw_date)
    except ValueError:
        return None

    raw_count = cell.get("data-count")
    count = None
    if raw_count is not None:
        try:
            count = int(raw_count)
        except (TypeError, ValueError):
            count = None
    if count is None:
        label = " ".join(str(cell.get("aria-label", "")).split())
        if not label:
            tooltip = cell.find(attrs={"class": re.compile(r"tool-tip|tooltip", re.I)})
            label = tooltip.get_text(" ", strip=True) if tooltip else cell.get_text(" ", strip=True)
        match = re.search(r"(\d[\d,]*)\s+contributions?", label, re.I)
        count = int(match.group(1).replace(",", "")) if match else 0
        if re.search(r"no contributions", label, re.I):
            count = 0

    # Preserve the GitHub level if available; the CSS palette supports 0..5.
    raw_level = cell.get("data-level")
    try:
        level = int(raw_level) if raw_level is not None else -1
    except ValueError:
        level = -1
    if level < 0:
        level = 0 if count == 0 else 1 if count <= 2 else 2 if count <= 5 else 3 if count <= 10 else 4 if count <= 20 else 5
    return day, max(0, count), min(5, max(0, level))


def streaks(days: list[dict]) -> tuple[int, int]:
    counts = {date.fromisoformat(d["date"]): int(d["count"]) for d in days}
    ordered_dates = sorted(counts)
    best = current_run = 0
    previous = None
    for d in ordered_dates:
        if counts[d] > 0:
            current_run = current_run + 1 if previous and d == previous + timedelta(days=1) else 1
            best = max(best, current_run)
            previous = d
        else:
            current_run = 0
            previous = d

    today = date.today()
    if counts.get(today, 0) > 0:
        cursor = today
    elif counts.get(today - timedelta(days=1), 0) > 0:
        cursor = today - timedelta(days=1)
    else:
        return 0, best
    current = 0
    while counts.get(cursor, 0) > 0:
        current += 1
        cursor -= timedelta(days=1)
    return current, best


def build_payload(days: list[dict], source_total: int | None = None) -> dict:
    monthly = defaultdict(int)
    for item in days:
        monthly[item["date"][:7]] += item["count"]
    current_streak, longest_streak = streaks(days)
    best_day = max(days, key=lambda d: (d["count"], d["date"])) if days else None
    total = sum(d["count"] for d in days)
    if source_total is not None and total != source_total:
        raise RuntimeError(f"Parsed day total {total} does not match page total {source_total}; refusing to write a misleading calendar")
    return {
        "username": USERNAME,
        "source": URL,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "period_days": len(days),
        "total_contributions": total,
        "days": days,
        "stats": {
            "current_streak_days": current_streak,
            "longest_streak_days": longest_streak,
            "best_day": ({"date": best_day["date"], "count": best_day["count"]} if best_day else None),
            "monthly_totals": dict(sorted(monthly.items())),
        },
    }


def main() -> int:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; NafizProfileContributionCalendar/1.0)",
        "Accept": "text/html,application/xhtml+xml",
    }
    try:
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Could not retrieve public GitHub contributions: {exc}", file=sys.stderr)
        return 2

    soup = BeautifulSoup(response.text, "html.parser")
    cells = soup.select("td[data-date], [data-date].ContributionCalendar-day")
    parsed = [record for cell in cells if (record := parse_cell(cell)) is not None]
    # Some GitHub markup revisions use an SVG title/aria-label nested in cells.
    by_date = {d.isoformat(): {"date": d.isoformat(), "count": c, "level": level} for d, c, level in parsed}
    if len(by_date) < 350:
        print(f"Expected a 53-week contribution calendar; parsed only {len(by_date)} dated cells.", file=sys.stderr)
        return 3

    dates = sorted(date.fromisoformat(d) for d in by_date)
    first = dates[0] - timedelta(days=(dates[0].weekday() + 1) % 7)
    calendar = []
    for offset in range(371):
        current = first + timedelta(days=offset)
        key = current.isoformat()
        calendar.append(by_date.get(key, {"date": key, "count": 0, "level": 0}))

    total_match = re.search(r"([\d,]+) contributions? in the last year", soup.get_text(" ", strip=True), re.I)
    page_total = int(total_match.group(1).replace(",", "")) if total_match else None
    payload = build_payload(calendar, page_total)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(calendar)} dated cells and {payload['total_contributions']:,} contributions to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
