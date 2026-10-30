"""Scrape the public contribution calendar into data/contributions.json."""
import json
import re
import sys
from collections import OrderedDict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = "syednafizreja"
URL = f"https://github.com/users/{USER}/contributions"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def fetch_days():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
    today = datetime.now(timezone.utc).date().isoformat()
    days = []
    for cell in soup.select("td.ContributionCalendar-day"):
        day = cell.get("data-date")
        if not day or day > today:
            continue
        match = re.search(r"([\d,]+) contribution", tips.get(cell.get("id"), ""))
        count = int(match.group(1).replace(",", "")) if match else 0
        days.append({"date": day, "count": count, "level": int(cell.get("data-level", 0))})
    days.sort(key=lambda d: d["date"])
    total = re.search(r"([\d,]+)\s+contributions?\s+in the last year", soup.get_text(" ", strip=True))
    return days, int(total.group(1).replace(",", "")) if total else sum(d["count"] for d in days)


def streaks(days):
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)
    tail = days[:-1] if days and days[-1]["count"] == 0 else days
    current = 0
    for d in reversed(tail):
        if not d["count"]:
            break
        current += 1
    return current, longest


def main():
    days, total = fetch_days()
    if len(days) < 300:
        sys.exit(f"Only {len(days)} days found; the page layout may have changed.")
    current, longest = streaks(days)
    months = OrderedDict()
    for d in days:
        months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["count"]
    best = max(days, key=lambda d: d["count"])
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({
        "username": USER,
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly_totals": months,
        "days": days,
    }, indent=1), encoding="utf-8")
    print(f"{len(days)} days, {total} contributions")


if __name__ == "__main__":
    main()
