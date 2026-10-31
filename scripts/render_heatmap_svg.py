#!/usr/bin/env python3
"""Render the 53 x 7 contribution calendar as a static SVG.

Blue-steel to cyan palette, plain header and a stats footer.
"""
from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"

# FEA Blue-Steel to Cyan contour gradient
PALETTE = ["#0e1724", "#133854", "#18638b", "#0284c7", "#38bdf8", "#a5f3fc"]


def render(payload: dict, animated: bool = True) -> str:
    days = payload.get("days", [])
    if len(days) != 371:
        # Fallback padding if data not exactly 371 days
        days = (days + [{"count": 0, "level": 0}] * 371)[:371]

    stats = payload.get("stats", {})
    total = stats.get("total_contributions", sum(d.get("count", 0) for d in days))
    active = stats.get("active_days", sum(1 for d in days if d.get("count", 0) > 0))
    streak = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)

    # Grid constants
    cell_size = 11.0
    cell_gap = 3.0
    left_pad = 52.0
    top_pad = 78.0
    grid_width = 53 * cell_size + 52 * cell_gap
    grid_height = 7 * cell_size + 6 * cell_gap
    svg_width = 815
    svg_height = 224

    parts: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" '
        f'viewBox="0 0 {svg_width} {svg_height}" role="img" aria-label="Syed Nafiz Reja Hasib contributions">',
        '<title>Syed Nafiz Reja Hasib — contribution activity over the past 53 weeks</title>',
        '<defs>',
        '<linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">',
        '  <stop offset="0%" stop-color="#090f17"/>',
        '  <stop offset="100%" stop-color="#0e1724"/>',
        '</linearGradient>',
        '<linearGradient id="topbarGrad" x1="0" y1="0" x2="1" y2="0">',
        '  <stop offset="0%" stop-color="#111f30"/>',
        '  <stop offset="100%" stop-color="#16273d"/>',
        '</linearGradient>',
        '</defs>',
        # Background frame
        f'<rect width="{svg_width}" height="{svg_height}" rx="10" fill="url(#bgGrad)" stroke="#1e293b" stroke-width="1.2"/>',
        # Header bar
        f'<path d="M 1 10 Q 1 1 10 1 L {svg_width-10} 1 Q {svg_width-1} 1 {svg_width-1} 10 L {svg_width-1} 40 L 1 40 Z" fill="url(#topbarGrad)"/>',
        '<line x1="1" y1="40" x2="814" y2="40" stroke="#1e293b" stroke-width="1"/>',
        '<text x="24" y="26" fill="#e2e8f0" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="13.5" font-weight="600">Contribution activity</text>',
        '<text x="791" y="26" fill="#64748b" text-anchor="end" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="11.5">Past 53 weeks</text>',
    ]

    # Day of week labels on left (Mon, Wed, Fri)
    day_labels = [("", 0), ("Mon", 1), ("", 2), ("Wed", 3), ("", 4), ("Fri", 5), ("", 6)]
    for lbl, idx in day_labels:
        if lbl:
            y = top_pad + idx * (cell_size + cell_gap) + 9
            parts.append(
                f'<text x="44" y="{y:.1f}" text-anchor="end" fill="#475569" '
                f'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="9.5">{lbl}</text>'
            )

    # Compute month label positions along the 53 weeks
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # Collect the first column of each month, then drop a label that would
    # collide with the next one (a partial month at the left edge of the grid).
    month_labels = []
    seen_months = set()
    for col in range(53):
        d_str = days[col * 7].get("date", "")
        if d_str and len(d_str) >= 10:
            key = d_str[:7]
            if key not in seen_months:
                seen_months.add(key)
                month_labels.append((col, month_names[int(d_str[5:7]) - 1]))

    for i, (col, label) in enumerate(month_labels):
        if i + 1 < len(month_labels) and month_labels[i + 1][0] - col < 3:
            continue
        x = left_pad + col * (cell_size + cell_gap)
        parts.append(
            f'<text x="{x:.1f}" y="{top_pad - 12:.1f}" fill="#64748b" '
            f'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="10">{label}</text>'
        )

    # Heatmap Grid Cells
    for idx, day in enumerate(days):
        col = idx // 7
        row = idx % 7
        x = left_pad + col * (cell_size + cell_gap)
        y = top_pad + row * (cell_size + cell_gap)

        level = day.get("level", 0)
        count = day.get("count", 0)
        # Select color based on level or count
        color_idx = min(level, 4)
        if count >= 10:
            color = PALETTE[5]
        else:
            color = PALETTE[color_idx]

        dt = day.get("date", "")
        tip = f"{dt}: {count} contribution{'s' if count != 1 else ''}"

        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2.5" '
            f'fill="{color}"><title>{escape(tip)}</title></rect>'
        )

    # Footer with stats and legend
    footer_y = top_pad + grid_height + 28
    parts.append(
        f'<text x="{left_pad}" y="{footer_y:.1f}" fill="#94a3b8" '
        f'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="11">'
        f'<tspan fill="#38bdf8" font-weight="700">{total:,}</tspan> verified contributions  ·  '
        f'<tspan fill="#38bdf8" font-weight="700">{active}</tspan> active days  ·  '
        f'current streak: <tspan fill="#38bdf8" font-weight="700">{streak}</tspan>d  ·  '
        f'longest: <tspan fill="#38bdf8" font-weight="700">{longest}</tspan>d'
        f'</text>'
    )

    # Legend on right side of footer
    legend_right = left_pad + grid_width
    parts.append(
        f'<text x="{legend_right - 104}" y="{footer_y:.1f}" fill="#64748b" text-anchor="end" '
        f'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="10">Less</text>'
    )
    for i, colr in enumerate(PALETTE[:5]):
        lx = (legend_right - 98) + i * 14
        ly = footer_y - 9
        parts.append(f'<rect x="{lx}" y="{ly}" width="10" height="10" rx="2" fill="{colr}" stroke="#334155" stroke-width="0.5"/>')
    parts.append(
        f'<text x="{legend_right}" y="{footer_y:.1f}" fill="#64748b" text-anchor="end" '
        f'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="10">More</text>'
    )

    parts.append('</svg>')
    return "\n".join(parts)


def main() -> int:
    if not DATA.exists():
        print(f"[error] {DATA} does not exist. Run fetch_contributions.py first.", file=sys.stderr)
        return 1

    with open(DATA, "r", encoding="utf-8") as f:
        payload = json.load(f)

    svg_content = render(payload, animated=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[ok] Heatmap rendered -> {OUTPUT}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
