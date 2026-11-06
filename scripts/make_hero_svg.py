#!/usr/bin/env python3
"""Generate hero.svg from the "hero" block in data/profile.json.

Left: a chain under equal point loads hangs as a funicular polygon in pure
tension, then inverts into the arch that carries the same loads in pure
compression (Hooke's principle). Right: the research question and pillars.
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).parent))

from build_profile import load_profile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "hero.svg"

W, H = 940, 300
FONT = "-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"
MUTED = "#94a3b8"
LINE = "#1e293b"
TENSION = "#f59e0b"
COMPRESSION = "#38bdf8"

# Chain geometry: supports at X0, X1 on BASE; SAG is the rise or sag at midspan.
X0, X1, BASE, SAG, N = 70, 400, 172, 70, 10
DUR = "10s"
KEY_TIMES = "0;0.3;0.5;0.8;1"
SPLINES = "0 0 1 1;0.45 0 0.55 1;0 0 1 1;0.45 0 0.55 1"
ANIM = f'dur="{DUR}" repeatCount="indefinite" keyTimes="{KEY_TIMES}" calcMode="spline" keySplines="{SPLINES}"'


def shape(u: float) -> float:
    """Equal loads at equal spacing give a parabolic funicular (1 at midspan)."""
    return 1 - u * u


def nodes(sign: int) -> list[tuple[float, float]]:
    pts = []
    for i in range(N + 1):
        u = -1 + 2 * i / N
        x = X0 + (X1 - X0) * i / N
        pts.append((x, BASE + sign * SAG * shape(u)))
    return pts


def path(pts: list[tuple[float, float]]) -> str:
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def chain() -> str:
    hang, arch = path(nodes(+1)), path(nodes(-1))
    cx = (X0 + X1) / 2
    out = [
        # ground and pin supports
        f'<path d="M {X0 - 30} {BASE + 12} L {X1 + 30} {BASE + 12}" stroke="#334155"/>',
        *(f'<path d="M {x} {BASE} L {x - 9} {BASE + 12} L {x + 9} {BASE + 12} Z" fill="#0d1726" stroke="{MUTED}"/>' for x in (X0, X1)),
        # ghost of the opposite state, so both forms read at a glance
        f'<path d="{hang}" fill="none" stroke="{TENSION}" stroke-opacity="0.14" stroke-dasharray="3 4"/>',
        f'<path d="{arch}" fill="none" stroke="{COMPRESSION}" stroke-opacity="0.14" stroke-dasharray="3 4"/>',
        f'<path d="{hang}" fill="none" stroke-width="2.6" stroke-linejoin="round">'
        f'<animate attributeName="d" values="{hang};{hang};{arch};{arch};{hang}" {ANIM}/>'
        f'<animate attributeName="stroke" values="{TENSION};{TENSION};{COMPRESSION};{COMPRESSION};{TENSION}" {ANIM}/>'
        f'</path>',
    ]
    for i in range(1, N):
        x = X0 + (X1 - X0) * i / N
        dy = SAG * shape(-1 + 2 * i / N)
        out.append(
            f'<g transform="translate(0 {dy:.1f})">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 {dy:.1f};0 {dy:.1f};0 {-dy:.1f};0 {-dy:.1f};0 {dy:.1f}" {ANIM}/>'
            f'<path d="M {x:.1f} {BASE - 22} L {x:.1f} {BASE - 7} M {x - 3:.1f} {BASE - 11} L {x:.1f} {BASE - 6} L {x + 3:.1f} {BASE - 11}" '
            f'stroke="#cbd5e1" stroke-opacity="0.75" fill="none" stroke-width="1.2"/>'
            f'<circle cx="{x:.1f}" cy="{BASE}" r="3.4" fill="#e2e8f0"/></g>'
        )
    for label, color, values in (
        ("Hanging chain · pure tension", TENSION, "1;1;0;0;1"),
        ("Inverted arch · pure compression", COMPRESSION, "0;0;1;1;0"),
    ):
        out.append(
            f'<text x="{cx}" y="66" text-anchor="middle" font-size="12" font-weight="600" fill="{color}" opacity="{values[0]}">'
            f'{label}<animate attributeName="opacity" values="{values}" {ANIM}/></text>'
        )
    return "\n  ".join(out)


def question(hero: dict) -> str:
    x = 500
    out = [
        f'<text x="{x}" y="80" font-size="11" font-weight="700" letter-spacing="1.6" fill="{COMPRESSION}">{escape(hero["eyebrow"].upper())}</text>'
    ]
    for k, line in enumerate(textwrap.wrap(hero["question"], 38, break_on_hyphens=False)):
        out.append(f'<text x="{x}" y="{110 + 28 * k}" font-size="21" font-weight="600" fill="#e2e8f0">{escape(line)}</text>')
    col = 142
    for j, pillar in enumerate(hero["pillars"]):
        px = x + j * col
        lines = textwrap.wrap(pillar["text"], 24)
        out.append(f'<rect x="{px}" y="216" width="3" height="{20 + 14 * len(lines)}" rx="1.5" fill="{pillar["color"]}"/>')
        out.append(f'<text x="{px + 12}" y="228" font-size="12.5" font-weight="700" fill="{pillar["color"]}">{escape(pillar["label"])}</text>')
        out.extend(
            f'<text x="{px + 12}" y="{245 + 14 * k}" font-size="10.5" fill="{MUTED}">{escape(t)}</text>'
            for k, t in enumerate(lines)
        )
    return "\n  ".join(out)


def make_svg(profile: dict) -> str:
    hero = profile["hero"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(hero["eyebrow"])}: {escape(hero["question"])}" font-family="{FONT}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#090f17"/><stop offset="1" stop-color="#0d1726"/></linearGradient>
    <linearGradient id="head" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#111f30"/><stop offset="1" stop-color="#16273d"/></linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="url(#bg)" stroke="{LINE}"/>
  <path d="M 1 12 Q 1 1 12 1 L {W - 12} 1 Q {W - 1} 1 {W - 1} 12 L {W - 1} 44 L 1 44 Z" fill="url(#head)"/>
  <text x="24" y="27" font-size="14" font-weight="600" fill="#e2e8f0">{escape(hero["title"])}</text>
  <text x="{W - 24}" y="27" text-anchor="end" font-size="11" fill="{MUTED}">{escape(hero["caption"])}</text>
  <path d="M 468 64 L 468 276" stroke="{LINE}"/>
  {chain()}
  <text x="{(X0 + X1) / 2}" y="282" text-anchor="middle" font-size="10.5" font-style="italic" fill="{MUTED}">“{escape(hero["quote"])}”</text>
  {question(hero)}
</svg>
'''


def main() -> int:
    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(make_svg(load_profile()))
    print(f"[ok] {OUTPUT.name} written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
