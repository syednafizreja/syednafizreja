#!/usr/bin/env python3
"""Fetch the public GitHub contribution calendar and derive researcher stats.

No token or GraphQL API is used. Source: /users/<username>/contributions.
Outputs clean structured JSON for reproducible rendering.
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


def parse_calendar(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict] = []
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        raw_date = td.get("data-date")
        if not raw_date:
            continue
        level = int(td.get("data-level", 0))
        text = td.get_text(strip=True)
        count = 0
        match = re.search(r"(\d+)\s+contribution", text)
        if match:
            count = int(match.group(1))
        elif "No contributions" in text:
            count = 0
        else:
            id_val = td.get("id")
            if id_val:
                tip = soup.find("tool-tip", attrs={"for": id_val})
                if tip:
                    tip_match = re.search(r"(\d+)\s+contribution", tip.get_text())
                    if tip_match:
                        count = int(tip_match.group(1))
        rows.append({"date": raw_date, "count": count, "level": level})

    # Deduplicate and sort
    by_date: dict[str, dict] = {}
    for r in rows:
        by_date[r["date"]] = r
    sorted_days = [by_date[k] for k in sorted(by_date.keys())]

    # Normalize to exactly 53 weeks (371 days) ending at the latest Sunday
    if not sorted_days:
        return []
    end = datetime.strptime(sorted_days[-1]["date"], "%Y-%m-%d").date()
    days_to_sat = (5 - end.weekday()) % 7
    calendar_end = end + timedelta(days=days_to_sat)
    calendar_start = calendar_end - timedelta(days=371 - 1)

    lookup = {r["date"]: r for r in sorted_days}
    grid: list[dict] = []
    cur = calendar_start
    while cur <= calendar_end:
        iso = cur.isoformat()
        if iso in lookup:
            grid.append(lookup[iso])
        else:
            grid.append({"date": iso, "count": 0, "level": 0})
        cur += timedelta(days=1)
    return grid[-371:]


def derive_stats(days: list[dict]) -> dict:
    if not days:
        return {
            "total_contributions": 0,
            "active_days": 0,
            "longest_streak": 0,
            "current_streak": 0,
            "max_day_count": 0,
            "by_month": {},
            "by_weekday": [0] * 7,
        }

    total = sum(d["count"] for d in days)
    active = sum(1 for d in days if d["count"] > 0)
    max_day = max(d["count"] for d in days)

    longest = 0
    cur_streak = 0
    for d in days:
        if d["count"] > 0:
            cur_streak += 1
            if cur_streak > longest:
                longest = cur_streak
        else:
            cur_streak = 0

    tail_streak = 0
    for d in reversed(days):
        if d["count"] > 0:
            tail_streak += 1
        elif tail_streak > 0:
            break

    by_month: dict[str, int] = defaultdict(int)
    by_weekday = [0] * 7
    for d in days:
        dt = datetime.strptime(d["date"], "%Y-%m-%d").date()
        by_month[dt.strftime("%Y-%m")] += d["count"]
        by_weekday[dt.weekday()] += d["count"]

    return {
        "total_contributions": total,
        "active_days": active,
        "longest_streak": longest,
        "current_streak": tail_streak,
        "max_day_count": max_day,
        "by_month": dict(by_month),
        "by_weekday": by_weekday,
    }


def main() -> int:
    try:
        resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        resp.raise_for_status()
        html = resp.text
    except Exception as exc:
        print(f"[warn] Failed to fetch {URL}: {exc}", file=sys.stderr)
        if OUT.exists():
            print("[info] Keeping existing data cache.")
            return 0
        html = ""

    days = parse_calendar(html) if html else []
    if not days and OUT.exists():
        print("[info] Parsed 0 days; retaining previous cache.")
        return 0

    stats = derive_stats(days)
    payload = {
        "user": USERNAME,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_days": len(days),
        "stats": stats,
        "days": days,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"[ok] Cached {len(days)} days -> {OUT} (total={stats['total_contributions']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
