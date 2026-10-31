#!/usr/bin/env python3
"""Render the 53 x 7 contribution calendar as a one-shot animated SVG.

Style: FEA Structural Blue-Steel & Cyan palette, diagonal SMIL cascade,
terminal header with live stats footer.
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
    svg_width = 860
    svg_height = 242

    parts: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" '
        f'viewBox="0 0 {svg_width} {svg_height}" role="img" aria-label="Syed Nafiz Reja Hasib contributions">',
        '<title>Syed Nafiz Reja Hasib — 53-week computational &amp; structural engineering commit timeline</title>',
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
        # Terminal Header Bar
        f'<path d="M 1 10 Q 1 1 10 1 L {svg_width-10} 1 Q {svg_width-1} 1 {svg_width-1} 10 L {svg_width-1} 40 L 1 40 Z" fill="url(#topbarGrad)"/>',
        '<line x1="1" y1="40" x2="859" y2="40" stroke="#1e293b" stroke-width="1"/>',
        '<circle cx="24" cy="21" r="5" fill="#f87171"/>',
        '<circle cx="42" cy="21" r="5" fill="#fbbf24"/>',
        '<circle cx="60" cy="21" r="5" fill="#34d399"/>',
        '<text x="82" y="25" fill="#64748b" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" letter-spacing="0.05em">LIVE DISPATCH :: git log --graph --all (FEA Stress Contour Palette)</text>',
        '<text x="836" y="25" fill="#38bdf8" text-anchor="end" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" font-weight="600">CONTINUOUS RESEARCH CI</text>',
    ]

    # Day of week labels on left (Mon, Wed, Fri)
    day_labels = [("", 0), ("Mon", 1), ("", 2), ("Wed", 3), ("", 4), ("Fri", 5), ("", 6)]
    for lbl, idx in day_labels:
        if lbl:
            y = top_pad + idx * (cell_size + cell_gap) + 9
            parts.append(
                f'<text x="44" y="{y:.1f}" text-anchor="end" fill="#475569" '
                f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5">{lbl}</text>'
            )

    # Compute month label positions along the 53 weeks
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    seen_months = set()
    for col in range(53):
        first_day_idx = col * 7
        d_str = days[first_day_idx].get("date", "")
        if d_str and len(d_str) >= 10:
            m_idx = int(d_str[5:7]) - 1
            y_str = d_str[:4]
            key = f"{y_str}-{m_idx}"
            if key not in seen_months:
                seen_months.add(key)
                x = left_pad + col * (cell_size + cell_gap)
                parts.append(
                    f'<text x="{x:.1f}" y="{top_pad - 12:.1f}" fill="#64748b" '
                    f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10">{month_names[m_idx]}</text>'
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

        if animated:
            # Diagonal cascade reveal: col + row
            delay = 0.05 + (col + row) * 0.016
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2.5" '
                f'fill="{color}" opacity="0">'
                f'<title>{escape(tip)}</title>'
                f'<animate attributeName="opacity" from="0" to="1" dur="0.32s" begin="{delay:.3f}s" fill="freeze"/>'
                f'</rect>'
            )
        else:
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2.5" '
                f'fill="{color}"><title>{escape(tip)}</title></rect>'
            )

    # Footer with Live Research Engineering Stats & Legend
    footer_y = top_pad + grid_height + 28
    parts.append(
        f'<text x="{left_pad}" y="{footer_y:.1f}" fill="#94a3b8" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11">'
        f'<tspan fill="#38bdf8" font-weight="700">{total:,}</tspan> verified contributions  ·  '
        f'<tspan fill="#38bdf8" font-weight="700">{active}</tspan> active days  ·  '
        f'current streak: <tspan fill="#38bdf8" font-weight="700">{streak}</tspan>d  ·  '
        f'longest: <tspan fill="#38bdf8" font-weight="700">{longest}</tspan>d'
        f'</text>'
    )

    # Legend on right side of footer
    legend_right = svg_width - 34
    parts.append(
        f'<text x="{legend_right - 92}" y="{footer_y:.1f}" fill="#64748b" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10">Less</text>'
    )
    for i, colr in enumerate(PALETTE[:5]):
        lx = (legend_right - 62) + i * 14
        ly = footer_y - 9
        parts.append(f'<rect x="{lx}" y="{ly}" width="10" height="10" rx="2" fill="{colr}"/>')
    parts.append(
        f'<text x="{legend_right + 12}" y="{footer_y:.1f}" fill="#64748b" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10">More</text>'
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
