#!/usr/bin/env python3
"""Generate the researcher profile card SVG.

Tuned with structural blue-steel / FEA cyan highlights and authoritative academic metadata.
"""
from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).parent))
from build_profile import card_rows, derive, load_profile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "info-card.svg"

WIDTH = 510
FIRST_ROW_Y = 72
BOTTOM_PADDING = 30


def row_spacing(lines: list[str]) -> int:
    return 44 if len(lines) > 1 else 36


def make_svg(rows: list[dict], animated: bool = True) -> str:
    HEIGHT = FIRST_ROW_Y + sum(row_spacing(r["lines"]) for r in rows) + BOTTOM_PADDING
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="Research profile of Syed Nafiz Reja Hasib">',
        '<title>Syed Nafiz Reja Hasib — Structural Engineering Researcher Profile</title>',
        '<defs>',
        '<linearGradient id="cardBg" x1="0" y1="0" x2="1" y2="1">',
        '  <stop offset="0%" stop-color="#090f17"/>',
        '  <stop offset="100%" stop-color="#0d1726"/>',
        '</linearGradient>',
        '<linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">',
        '  <stop offset="0%" stop-color="#111f30"/>',
        '  <stop offset="100%" stop-color="#16273d"/>',
        '</linearGradient>',
        '</defs>',
        # Card Background Frame
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="12" fill="url(#cardBg)" stroke="#1e293b" stroke-width="1.2"/>',
        # Header bar
        f'<path d="M 1 12 Q 1 1 12 1 L {WIDTH-12} 1 Q {WIDTH-1} 1 {WIDTH-1} 12 L {WIDTH-1} 44 L 1 44 Z" fill="url(#headerGrad)"/>',
        f'<line x1="1" y1="44" x2="{WIDTH-1}" y2="44" stroke="#1e293b" stroke-width="1"/>',
        '<text x="24" y="27" fill="#e2e8f0" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="14" font-weight="600">Syed Nafiz Reja Hasib</text>',
    ]

    y_pos = FIRST_ROW_Y

    for i, row in enumerate(rows):
        label, lines, accent_col = row["label"], row["lines"], row["accent"]
        spacing = row_spacing(lines)
        parts.append(f'<g transform="translate(24, {y_pos})">')

        # Key Label
        parts.append(
            f'<text x="0" y="0" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" '
            f'font-size="11" font-weight="700" letter-spacing="0.08em">{escape(label)}</text>'
        )

        # Value Lines
        line_y = 0
        for l_idx, line_text in enumerate(lines):
            text_color = "#e2e8f0" if l_idx == 0 else "#94a3b8"
            weight = "600" if l_idx == 0 else "400"
            parts.append(
                f'<text x="110" y="{line_y}" fill="{text_color}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" '
                f'font-size="10.5" font-weight="{weight}">{escape(line_text)}</text>'
            )
            line_y += 15

        parts.append('</g>')
        y_pos += spacing

    parts.append('</svg>')
    return "\n".join(parts)


def main() -> int:
    profile = load_profile()
    content = make_svg(card_rows(profile, derive(profile)), animated=True)
    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"[ok] Profile info card rendered -> {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
