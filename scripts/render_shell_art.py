"""Render shell-art.svg: a thin shell wireframe that draws, then sways once."""
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 370, 420
S, RISE, N, CX, CY = 95, 112, 14, 185, 192
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def point(u, v):
    x, y = u * S, v * S
    z = RISE * (1 - u * u) * (1 - v * v)
    return CX + (x - y) * 0.87, CY + (x + y) * 0.5 - z + 40


def grid_line(fixed, along_u):
    pts = []
    for k in range(41):
        t = -1 + k / 20
        pts.append(point(t, fixed) if along_u else point(fixed, t))
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def trace():
    pts = []
    for k in range(171):
        t = k / 170
        amp = 24 * math.exp(-3.5 * t) * math.sin(math.pi * min(t * 12, 1)) ** 2
        y = amp * math.sin(2 * math.pi * 9 * t) * math.sin(2 * math.pi * 2.3 * t + 0.6)
        pts.append(f"{30 + k * 1.82:.1f} {348 - y:.1f}")
    return "M" + "L".join(pts)


def main():
    static = os.environ.get("STATIC") == "1"
    lines = []
    for i in range(N + 1):
        fixed = -1 + 2 * i / N
        for along_u, color in ((True, "#2dd4bf"), (False, "#38bdf8")):
            lines.append(f'<path class="l" pathLength="1" d="{grid_line(fixed, along_u)}" stroke="{color}" '
                         f'style="animation-delay:{i * 0.05:.2f}s"/>')
    dots = "".join(f'<circle cx="{point(u, v)[0]:.1f}" cy="{point(u, v)[1]:.1f}" r="3" fill="#99f6e4"/>'
                   for u, v in ((-1, -1), (1, -1), (-1, 1), (1, 1)))
    motion = "" if static else (
        ".l{stroke-dasharray:1;animation:d 1.4s ease-out both}"
        ".q{animation:q 3.4s linear 2.8s both}"
        ".w{stroke-dasharray:1;animation:d 3.4s linear 2.8s both}"
        "@keyframes d{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}"
        "@keyframes q{0%,100%{transform:none}8%{transform:translateX(-6px)}16%{transform:translateX(7px)}"
        "26%{transform:translateX(-5px)}38%{transform:translateX(4px)}52%{transform:translateX(-2px)}"
        "68%{transform:translateX(1px)}}")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated wireframe of a thin concrete shell">
<style>
text{{font-family:{FONT}}}
.l{{fill:none;stroke-width:1;opacity:.85}}
.w{{fill:none;stroke:#2dd4bf;stroke-width:1.2}}
{motion}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="#0d1117" stroke="#1f3a44"/>
<circle cx="20" cy="18" r="5" fill="#ff5f56"/><circle cx="38" cy="18" r="5" fill="#ffbd2e"/><circle cx="56" cy="18" r="5" fill="#27c93f"/>
<text x="{W / 2}" y="22" text-anchor="middle" font-size="12" fill="#7d8b99">nafiz@github: ~/shell</text>
<path d="M0 35H{W}" stroke="#1f3a44"/>
<g class="q">{''.join(lines)}{dots}</g>
<path class="w" pathLength="1" d="{trace()}"/>
<text x="{W / 2}" y="398" text-anchor="middle" font-size="11" fill="#7d8b99">thin shell under ground motion (illustrative)</text>
</svg>
'''
    (ROOT / "shell-art.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
