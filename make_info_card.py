#!/usr/bin/env python3
"""Generate an animated neofetch-style researcher profile card SVG.

Set STATIC=1 to write the same card with all rows in their final positions.
"""
from __future__ import annotations

import os
from pathlib import Path
from xml.sax.saxutils import escape

WIDTH, HEIGHT = 980, 784

ROWS = [
    ("NOW", ["Researcher · computational lightweight structures", "seismic / blast / pressure resilience · AI · low-carbon design"], "#63d4df", 78),
    ("PREV", ["Project Engineer, precision manufacturing and quality control"], "#79b8ff", 50),
    ("EDU", ["B.Eng. Civil Engineering · Southwest Petroleum University", "Chinese Government Scholarship"], "#c6a0f6", 65),
    ("STACK", ["Python · OpenSeesPy · CalculiX · AutoCAD", "Revit/BIM · JavaScript · Gmsh · GitHub Actions"], "#63d4df", 65),
    ("RESEARCH", ["Seismic RC design · shell form-finding · embodied carbon", "Structural optimisation · data-driven engineering"], "#f2cc60", 65),
    ("PROJECTS", ["ShellBench · ShellForm · thin-shell RC / concrete shells"], "#79b8ff", 50),
    ("CODE", ["parametric-canopy-carbon-optimization", "Interactive form–response–carbon design prototype"], "#63d4df", 65),
    ("PAPERS", ["3 peer-reviewed articles: BIM · nano-WMA · Edge AI/IoT"], "#c6a0f6", 50),
    ("PRACTICE", ["Benchmark validation · automated tests · reproducible code"], "#63d4df", 50),
    ("ORCID", ["0009-0002-7162-7890"], "#f2cc60", 45),
    ("CONNECT", ["syednafiz2811@gmail.com · LinkedIn · ResearchGate"], "#79b8ff", 55),
]


def make_svg(animated: bool) -> str:
    p = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="490" height="392" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="Research profile of Syed Nafiz Reja Hasib">',
        '<title>Syed Nafiz Reja Hasib — researcher profile</title>',
        '<defs>',
        '<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0c1b29"/><stop offset="1" stop-color="#101d2c"/></linearGradient>',
        '<linearGradient id="topbar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#132c3c"/><stop offset="1" stop-color="#142337"/></linearGradient>',
        '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#244154" stroke-width="1" opacity="0.20"/></pattern>',
        '</defs>',
        '<rect x="2" y="2" width="976" height="780" rx="24" fill="url(#panel)" stroke="#31536a" stroke-width="3"/>',
        '<rect x="4" y="4" width="972" height="776" rx="22" fill="url(#grid)"/>',
        '<path d="M5 84H975" stroke="#29475a" stroke-width="2"/>',
        '<path d="M5 24Q5 5 24 5H956Q975 5 975 24V82H5Z" fill="url(#topbar)"/>',
        '<circle cx="38" cy="43" r="9" fill="#f7768e"/><circle cx="68" cy="43" r="9" fill="#e0af68"/><circle cx="98" cy="43" r="9" fill="#9ece6a"/>',
        '<text x="132" y="39" fill="#e6edf3" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="27" font-weight="700">SYED NAFIZ REJA HASIB</text>',
        '<text x="132" y="65" fill="#83a9bb" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="17" letter-spacing="2.1">CIVIL ENGINEERING  /  COMPUTATIONAL STRUCTURES</text>',
        # Fine wireframe arch motif: a restrained nod to shell geometry.
        '<g transform="translate(852 15)" fill="none" stroke="#55c3cf" stroke-width="2.2" opacity="0.86">',
        '<path d="M0 52 Q44 -2 88 52"/><path d="M0 52 Q44 10 88 52" opacity=".6"/>',
        '<path d="M11 52L11 39M22 52L22 28M33 52L33 20M44 52L44 17M55 52L55 20M66 52L66 28M77 52L77 39" opacity=".8"/>',
        '<path d="M0 52H88" opacity=".8"/>',
        '</g>',
    ]
    y = 111
    for idx, (label, lines, color, row_h) in enumerate(ROWS):
        initial_opacity = '0' if animated else '1'
        initial_transform = 'translate(0 10)' if animated else 'translate(0 0)'
        p.append(f'<g class="row row-{idx}" opacity="{initial_opacity}" transform="{initial_transform}">')
        if animated:
            delay = idx * 0.105
            p.append(f'<animate attributeName="opacity" values="0;1" begin="{delay:.3f}s" dur="0.48s" fill="freeze"/>')
            p.append(f'<animateTransform attributeName="transform" type="translate" values="0 10;0 0" begin="{delay:.3f}s" dur="0.48s" fill="freeze"/>')
        p.append(f'<text x="58" y="{y + 26}" fill="{color}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="23" font-weight="700" letter-spacing="1.1">{escape(label)}</text>')
        line_y = y + 26
        for li, line in enumerate(lines):
            if li:
                line_y += 25
            p.append(f'<text x="228" y="{line_y}" fill="#d6e2ec" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="22">{escape(line)}</text>')
        p.append(f'<path d="M56 {y + row_h - 3}H924" stroke="#294253" stroke-width="1.2" opacity=".68"/>')
        p.append('</g>')
        y += row_h

    p.append('<text x="58" y="760" fill="#63869a" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="16" letter-spacing="1.1">OPEN METHODS  ·  VALIDATED MODELS  ·  LOWER-CARBON STRUCTURES</text>')
    p.append('</svg>')
    return "\n".join(p)


def main() -> int:
    animated = os.getenv("STATIC", "0") != "1"
    output = Path(__file__).resolve().parents[1] / "info-card.svg"
    output.write_text(make_svg(animated), encoding="utf-8")
    print(f"Wrote {output} ({'animated' if animated else 'static preview'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
