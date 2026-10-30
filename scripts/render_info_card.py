"""Render info-card.svg. Set STATIC=1 for a frozen version with no animation."""
import os
import sys
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
W, H = 490, 420
LINE, SIZE, KEY_X, VAL_X = 19, 13, 22, 104
CHARS = int((W - VAL_X - 18) / (SIZE * 0.62))
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

ROWS = [
    ("Name", "Syed Nafiz Reja Hasib"),
    ("Now", "Researcher, lightweight structures that resist earthquakes, blast and pressure while cutting carbon, using computation and AI"),
    ("Prev", "Project Engineer, precision manufacturing and quality control"),
    ("Edu", "B.Eng Civil Engineering, Southwest Petroleum University (Chinese Government Scholarship)"),
    ("Stack", "Python · AutoCAD · Revit/BIM · JavaScript"),
    ("Research", "3 review papers (BIM; nano-modified warm-mix asphalt; Edge AI + IoT for structural health monitoring)"),
    ("Code", "parametric-canopy-carbon-optimization"),
    ("ORCID", "0009-0002-7162-7890"),
    ("LinkedIn", "linkedin.com/in/syednafizreja"),
    ("Email", "syednafiz2811@gmail.com"),
]


def main():
    static = os.environ.get("STATIC") == "1"
    y, parts = 62, []
    for i, (key, value) in enumerate(ROWS):
        lines = textwrap.wrap(value, CHARS)
        body = f'<text class="k" x="{KEY_X}" y="{y}">{key}</text>'
        for n, line in enumerate(lines):
            body += f'<text class="v" x="{VAL_X}" y="{y + n * LINE}">{escape(line)}</text>'
        parts.append(f'<g class="r" style="animation-delay:{0.25 + i * 0.09:.2f}s">{body}</g>')
        y += len(lines) * LINE + 5
    if y - LINE > H - 12:
        sys.exit(f"Card overflow: last line at {y - LINE}, height {H}")
    motion = "" if static else (
        ".r{animation:f .5s ease-out both}"
        "@keyframes f{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:none}}")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Profile summary for Syed Nafiz Reja Hasib">
<style>
text{{font-family:{FONT};font-size:{SIZE}px}}
.k{{fill:#2dd4bf;font-weight:600}}.v{{fill:#c9d1d9}}.t{{fill:#7d8b99;font-size:12px}}
{motion}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="#0d1117" stroke="#1f3a44"/>
<circle cx="20" cy="18" r="5" fill="#ff5f56"/><circle cx="38" cy="18" r="5" fill="#ffbd2e"/><circle cx="56" cy="18" r="5" fill="#27c93f"/>
<text class="t" x="{W / 2}" y="22" text-anchor="middle">nafiz@github: ~/whoami</text>
<path d="M0 35H{W}" stroke="#1f3a44"/>
{''.join(parts)}
</svg>
'''
    (ROOT / "info-card.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
