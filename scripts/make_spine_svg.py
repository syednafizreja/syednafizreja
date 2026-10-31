#!/usr/bin/env python3
"""Generate research-spine.svg from the "spine" block in data/profile.json.

Stages run left to right by structural scale. Each thread is a question that
carries through the stages it lists, so editing the data redraws the graphic.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from build_profile import load_profile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "research-spine.svg"

W, H = 510, 354
FONT = "-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"
INK = "#7dd3fc"
MUTED = "#94a3b8"
LINE = "#1e293b"
SPINE_Y = 136
THREAD_YS = [232, 272, 312]


def layers(cx: int) -> str:
    bands = "".join(
        f'<rect x="{cx - 44}" y="{y}" width="88" height="13" fill="{INK}" fill-opacity="{o}"/>'
        for y, o in ((72, 0.32), (85, 0.2), (98, 0.1))
    )
    grains = "".join(
        f'<circle cx="{cx - 38 + i * 11}" cy="{78 + (i % 2) * 3}" r="1.8" fill="{INK}"/>'
        for i in range(8)
    )
    return f'{bands}{grains}<rect x="{cx - 44}" y="72" width="88" height="39" fill="none" stroke="{INK}"/>'


def canopy(cx: int) -> str:
    return (
        f'<path d="M {cx - 46} 84 Q {cx} 44 {cx + 46} 84 Q {cx} 58 {cx - 46} 84 Z" '
        f'fill="{INK}" fill-opacity="0.2" stroke="{INK}"/>'
        f'<path d="M {cx - 22} 73 L {cx - 22} 114 M {cx + 22} 73 L {cx + 22} 114" stroke="{INK}" stroke-width="2"/>'
        f'<path d="M {cx - 46} 114 L {cx + 46} 114" stroke="{MUTED}"/>'
    )


def shell(cx: int) -> str:
    r, top, base = 46, 60, 112
    parts = [
        f"M {cx} {top} Q {cx + k * r / 2:.1f} {top + 2} {cx + k * r / 2:.1f} {base}"
        for k in (-2, -1, 1, 2)
    ]
    parts.append(f"M {cx} {top} L {cx} {base}")
    for t in (0.4, 0.7, 1.0):
        x = r * (2 * t * (1 - t) + t * t)
        y = (1 - t) ** 2 * top + 2 * t * (1 - t) * (top + 2) + t * t * base
        parts.append(f"M {cx - x:.1f} {y:.1f} Q {cx} {y + 9:.1f} {cx + x:.1f} {y:.1f}")
    return f'<path d="{" ".join(parts)}" fill="none" stroke="{INK}" stroke-width="0.9"/>'


def frame(cx: int) -> str:
    columns = "".join(f"M {cx - 39 + i * 26} 62 L {cx - 39 + i * 26} 114 " for i in range(4))
    floors = "".join(
        f"M {cx - 39 + i * 26} {y} Q {cx - 26 + i * 26} {y - 8} {cx - 13 + i * 26} {y} "
        for y in (62, 80, 98)
        for i in range(3)
    )
    return (
        f'<path d="{columns}" stroke="{INK}" stroke-width="1.6"/>'
        f'<path d="{floors}" fill="none" stroke="{INK}"/>'
        f'<path d="M {cx - 46} 114 L {cx + 46} 114" stroke="{MUTED}"/>'
    )


GLYPHS = {"layers": layers, "canopy": canopy, "shell": shell, "frame": frame}


def make_svg(profile: dict) -> str:
    spine = profile["spine"]
    stages = [stage["project"] for stage in spine["stages"]]
    known = {project["name"] for project in profile["projects"]}
    for name in stages:
        if name not in known:
            raise ValueError(f"spine stage {name!r} is not in projects")

    xs = {name: 75 + i * 120 for i, name in enumerate(stages)}
    left, right = xs[stages[0]], xs[stages[-1]]
    threads = list(zip(spine["threads"], THREAD_YS))

    body = []
    for name in stages:
        lowest = max(y for thread, y in threads if name in thread["stages"])
        body.append(
            f'<path d="M {xs[name]} 186 L {xs[name]} {lowest}" stroke="{LINE}" stroke-width="1.5" stroke-dasharray="3 4"/>'
        )

    body.append(
        f'<path id="spine" d="M {left} {SPINE_Y} L {right} {SPINE_Y}" stroke="#38bdf8" stroke-width="2"/>'
        f'<circle r="3" fill="#e2e8f0"><animateMotion dur="9s" repeatCount="indefinite" '
        f'path="M {left} {SPINE_Y} L {right} {SPINE_Y}"/></circle>'
    )

    for stage in spine["stages"]:
        cx = xs[stage["project"]]
        body.append(GLYPHS[stage["glyph"]](cx))
        body.append(
            f'<circle cx="{cx}" cy="{SPINE_Y}" r="5" fill="#090f17" stroke="#38bdf8" stroke-width="2"/>'
            f'<text x="{cx}" y="161" text-anchor="middle" font-size="12" font-weight="600" fill="#e2e8f0">{stage["project"]}</text>'
            f'<text x="{cx}" y="176" text-anchor="middle" font-size="10.5" fill="{MUTED}">{stage["scale"]}</text>'
        )

    for thread, y in threads:
        points = [xs[name] for name in stages if name in thread["stages"]]
        color = thread["color"]
        body.append(
            f'<path d="M {points[0]} {y} L {points[-1]} {y}" stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>'
            f'<text x="{points[0] - 6}" y="{y - 11}" font-size="11" font-weight="600" fill="{color}">{thread["label"]}</text>'
        )
        body.extend(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{color}"/>' for x in points)

    inner = "\n  ".join(body)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Research spine: {", ".join(stages)}" font-family="{FONT}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#090f17"/><stop offset="1" stop-color="#0d1726"/></linearGradient>
    <linearGradient id="head" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#111f30"/><stop offset="1" stop-color="#16273d"/></linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="url(#bg)" stroke="{LINE}"/>
  <path d="M 1 12 Q 1 1 12 1 L {W - 12} 1 Q {W - 1} 1 {W - 1} 12 L {W - 1} 44 L 1 44 Z" fill="url(#head)"/>
  <text x="24" y="27" font-size="14" font-weight="600" fill="#e2e8f0">Research spine</text>
  <text x="{W - 24}" y="27" text-anchor="end" font-size="11" fill="{MUTED}">{spine["caption"]}</text>
  {inner}
</svg>
'''


def main() -> int:
    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(make_svg(load_profile()))
    print(f"[ok] {OUTPUT.name} written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
