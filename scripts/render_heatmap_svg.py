"""Render data/contributions.json to contrib-heatmap.svg. Set STATIC=1 for no animation."""
import json
import os
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 860, 170
CELL, STEP, LEFT, TOP = 12, 15, 42, 34
PALETTE = ["#161b22", "#0b3a4a", "#0e6377", "#14919b", "#2dd4bf", "#99f6e4"]
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def main():
    data = json.loads((ROOT / "data" / "contributions.json").read_text(encoding="utf-8"))
    days = data["days"]
    best = data["best_day"]
    start = date.fromisoformat(days[0]["date"])
    offset = (start.weekday() + 1) % 7  # Sunday is row 0
    rects, months, seen = [], [], None
    for i, d in enumerate(days):
        col, row = (i + offset) // 7, (i + offset) % 7
        level = 5 if d["date"] == best["date"] and best["count"] else d["level"]
        x, y = LEFT + col * STEP, TOP + row * STEP
        delay = (col + row) * 0.022
        rects.append(f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
                     f'fill="{PALETTE[level]}" style="animation-delay:{delay:.2f}s"/>')
        month = d["date"][:7]
        if month != seen and row == 0:
            seen = month
            label = date.fromisoformat(d["date"]).strftime("%b")
            if months and x - months[-1][0] < 30:
                months.pop()  # a partial first month would collide with the next label
            months.append((x, label))
    month_text = "".join(f'<text x="{x}" y="24">{label}</text>' for x, label in months)
    motion = "" if os.environ.get("STATIC") == "1" else (
        ".c{animation:s .5s ease-out both}"
        "@keyframes s{from{opacity:0;transform:translate(-10px,-10px)}to{opacity:1;transform:none}}")
    weekdays = "".join(f'<text x="14" y="{TOP + r * STEP + 10}">{n}</text>'
                       for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
    legend_x = W - 18 - 6 * STEP - 34
    legend = "".join(f'<rect x="{legend_x + i * STEP}" y="147" width="{CELL}" height="{CELL}" '
                     f'rx="3" fill="{c}"/>' for i, c in enumerate(PALETTE))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{data['total']} contributions in the last year">
<style>
text{{font-family:{FONT};font-size:11px;fill:#7d8b99}}
{motion}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="#0d1117" stroke="#1f3a44"/>
{month_text}{weekdays}{''.join(rects)}
<text x="{LEFT}" y="157" style="fill:#c9d1d9">{data['total']} contributions in the last year</text>
<text x="{legend_x - 34}" y="157">Less</text>{legend}<text x="{legend_x + 6 * STEP + 4}" y="157">More</text>
</svg>
'''
    (ROOT / "contrib-heatmap.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
