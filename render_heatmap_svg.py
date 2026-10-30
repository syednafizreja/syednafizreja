#!/usr/bin/env python3
"""Render the 53 x 7 contribution calendar as a one-shot animated SVG."""
from __future__ import annotations

import json
from datetime import date
import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"
PALETTE = ["#101b2a", "#143c50", "#176078", "#2087a0", "#31a8bb", "#9de5e5"]


def render(payload: dict, animated: bool = True) -> str:
    days = payload.get("days", [])
    if len(days) != 371:
        raise ValueError(f"Expected 371 day records (53 weeks x 7 days), received {len(days)}")
    indexed = {date.fromisoformat(d["date"]): d for d in days}
    start = min(indexed)
    if start.weekday() != 6:
        raise ValueError("Calendar must start on Sunday")

    width, height = 1720, 400
    x0, y0 = 60, 112
    cell, gap = 20, 8
    stride = cell + gap
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="860" height="200" viewBox="0 0 {width} {height}" role="img" aria-label="53-week contribution calendar for syednafizreja">',
        '<title>GitHub contribution calendar — Syed Nafiz Reja Hasib</title>',
        '<defs><linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1623"/><stop offset="1" stop-color="#0e1f2e"/></linearGradient></defs>',
        '<rect x="1.5" y="1.5" width="1717" height="397" rx="22" fill="url(#panel)" stroke="#28485c" stroke-width="3"/>',
        '<text x="60" y="48" fill="#e4edf4" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="24" font-weight="700" letter-spacing="2">CONTRIBUTION ACTIVITY</text>',
        '<text x="1660" y="48" fill="#6f91a5" text-anchor="end" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="18">SYEDNAFIZREJA / 12 MONTHS</text>',
        '<path d="M60 65H1660" stroke="#29485a" stroke-width="1.5"/>',
    ]

    # Month labels follow the first day of each month in the Sunday-first grid.
    previous_month = None
    for col in range(53):
        week_date = start.fromordinal(start.toordinal() + col * 7)
        if week_date.month != previous_month:
            # The first month is usually only a few trailing days; omit that
            # partial label so it cannot collide with the following month.
            if not (col == 0 and week_date.day > 15):
                label = week_date.strftime("%b").upper()
                parts.append(f'<text x="{x0 + col * stride}" y="91" fill="#86a5b7" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="17">{label}</text>')
            previous_month = week_date.month

    for row, label in [(1, "MON"), (3, "WED"), (5, "FRI")]:
        parts.append(f'<text x="10" y="{y0 + row * stride + 15}" fill="#68899d" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="15">{label}</text>')

    for col in range(53):
        for row in range(7):
            day_date = start.fromordinal(start.toordinal() + col * 7 + row)
            record = indexed.get(day_date, {"count": 0, "level": 0})
            level = max(0, min(5, int(record.get("level", 0))))
            count = int(record.get("count", 0))
            x, y = x0 + col * stride, y0 + row * stride
            delay = col * 0.026 + row * 0.018
            tip = f'{day_date.isoformat()}: {count} contribution' + ("s" if count != 1 else "")
            parts.append(f'<g><title>{escape(tip)}</title>')
            opacity = '0' if animated else '1'
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="5" fill="{PALETTE[level]}" stroke="#1d394b" stroke-width="1.2" opacity="{opacity}">')
            if animated:
                parts.append(f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.48s" fill="freeze"/>')
                parts.append(f'<animateTransform attributeName="transform" type="translate" from="-4 -4" to="0 0" begin="{delay:.3f}s" dur="0.48s" fill="freeze"/>')
            parts.append('</rect></g>')

    legend_y = 348
    parts.append(f'<text x="60" y="{legend_y + 17}" fill="#86a5b7" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="18">LESS</text>')
    lx = 130
    for i, color in enumerate(PALETTE):
        parts.append(f'<rect x="{lx + i * 34}" y="{legend_y}" width="23" height="23" rx="5" fill="{color}" stroke="#29485a" stroke-width="1"/>')
    parts.append(f'<text x="{lx + 6 * 34 + 2}" y="{legend_y + 17}" fill="#86a5b7" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="18">MORE</text>')

    total = int(payload.get("total_contributions", sum(int(d.get("count", 0)) for d in days)))
    parts.append(f'<text x="1660" y="{legend_y + 17}" text-anchor="end" fill="#b5c8d4" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="19">{total:,} contributions in the last year</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def main() -> int:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    animated = os.getenv("STATIC", "0") != "1"
    OUTPUT.write_text(render(payload, animated=animated), encoding="utf-8")
    print(f"Wrote {OUTPUT} ({'animated' if animated else 'static preview'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
