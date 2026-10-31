#!/usr/bin/env python3
"""Generate an animated neofetch-style researcher profile card SVG.

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

WIDTH = 520
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
        # Top Terminal Window Bar
        f'<path d="M 1 12 Q 1 1 12 1 L {WIDTH-12} 1 Q {WIDTH-1} 1 {WIDTH-1} 12 L {WIDTH-1} 44 L 1 44 Z" fill="url(#headerGrad)"/>',
        f'<line x1="1" y1="44" x2="{WIDTH-1}" y2="44" stroke="#1e293b" stroke-width="1"/>',
        '<circle cx="22" cy="22" r="4.5" fill="#f87171"/>',
        '<circle cx="36" cy="22" r="4.5" fill="#fbbf24"/>',
        '<circle cx="50" cy="22" r="4.5" fill="#34d399"/>',
        '<text x="68" y="26" fill="#e2e8f0" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" font-weight="700">SYED NAFIZ REJA HASIB</text>',
        '<text x="245" y="26" fill="#64748b" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11">:: neofetch --profile</text>',
    ]

    y_pos = FIRST_ROW_Y
    base_delay = 0.15

    for i, row in enumerate(rows):
        label, lines, accent_col = row["label"], row["lines"], row["accent"]
        spacing = row_spacing(lines)
        anim_frag = ""
        if animated:
            d = base_delay + i * 0.12
            anim_frag = (
                f'<animateTransform attributeName="transform" type="translate" from="15,0" to="0,0" dur="0.35s" begin="{d:.2f}s" fill="freeze"/>'
                f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{d:.2f}s" fill="freeze"/>'
            )
            opacity_init = 'opacity="0"'
        else:
            opacity_init = 'opacity="1"'

        parts.append(f'<g transform="translate(24, {y_pos})" {opacity_init}>')
        if anim_frag:
            parts.append(anim_frag)
        
        # Key Label
        parts.append(
            f'<text x="0" y="0" fill="{accent_col}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
            f'font-size="11" font-weight="700" letter-spacing="0.08em">{escape(label)}</text>'
        )

        # Value Lines
        line_y = 0
        for l_idx, line_text in enumerate(lines):
            text_color = "#e2e8f0" if l_idx == 0 else "#94a3b8"
            weight = "600" if l_idx == 0 else "400"
            parts.append(
                f'<text x="110" y="{line_y}" fill="{text_color}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
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
