#!/usr/bin/env python3
"""Draw assets/hero.svg and assets/work.svg for the GitHub profile README.

GitHub shows the files through an img tag, so motion is CSS and SMIL inside
the SVG. The static drawing is the finished figure. Animation only brightens
the study that is on, and it stops under prefers-reduced-motion.

Numbers are the ones already printed on the profile and in the study files.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

PAPER = "#07090f"
PANEL = "#0c121b"
LINE = "#243246"
INK = "#f4f1ea"
MUTED = "#93a0b0"
DIM = "#66778a"
STEEL = "#7f93a3"
HOT = "#9fd8dc"
HOT_SOFT = "#d8f7f6"
SAND = "#d2c0a0"
SANS = '"Segoe UI", Helvetica, Arial, sans-serif'
SERIF = 'Georgia, Palatino, "Times New Roman", serif'
MONO = '"Segoe UI Mono", ui-monospace, Consolas, monospace'
CYCLE = "14s"


def poly(pts: list[tuple[float, float]]) -> str:
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def shell_mesh() -> tuple[list[str], str, list[tuple[float, float]]]:
    """Vault over the right bay, sprung clear of the beam. Lines, crown, nodes."""
    x0, x1 = 816.0, 988.0
    spring, rise = 172.0, 68.0
    nu, nv = 9, 4
    rows: list[list[tuple[float, float]]] = []
    for j in range(nv):
        v = j / (nv - 1)
        inset = (1 - v) * 12
        lift = (1 - v) * 14
        row = []
        for i in range(nu):
            u = i / (nu - 1)
            span = 1 - (2 * u - 1) ** 2
            x = x0 + inset + (x1 - x0 - 2 * inset) * u
            y = spring - lift - rise * span
            row.append((x, y))
        rows.append(row)
    lines = [poly(row) for row in rows]
    lines += [poly([rows[j][i] for j in range(nv)]) for i in range(nu)]
    crown = poly(rows[nv // 2])
    nodes = [point for row in rows for point in row]
    return lines, crown, nodes


# Closed NiTi flag, normalised. Two plateaus, a steep load, a steep unload.
FLAG = (
    (0.00, 0.78),
    (0.28, 0.86),
    (0.40, 0.12),
    (0.98, 0.00),
    (0.98, 0.34),
    (0.62, 0.46),
    (0.50, 0.96),
)


def flag(x: float, y: float, w: float, h: float) -> tuple[str, tuple[float, float]]:
    pts = [(x + px * w, y + py * h) for px, py in FLAG]
    return poly(pts) + " Z", pts[0]


def hero() -> str:
    mesh, crown, nodes = shell_mesh()
    _hero_flag, (_hx, _hy) = flag(656, 324, 196, 78)
    # Portal: left bay is the NiTi diagrid, right bay carries the vault.
    left, mid, right = 632.0, 812.0, 992.0
    beam, base, waist = 184.0, 292.0, 238.0
    braces = [
        poly([(left, waist), (mid, beam)]),
        poly([(left, beam), (mid, waist)]),
        poly([(left, base), (mid, waist)]),
        poly([(left, waist), (mid, base)]),
    ]
    frame = [
        poly([(left, base), (left, beam)]),
        poly([(mid, base), (mid, beam)]),
        poly([(right, base), (right, beam)]),
        poly([(left, beam), (right, beam)]),
        poly([(left - 22, base), (right + 28, base)]),
    ]
    pins = []
    for x in (left, mid, right):
        pins.append(
            f'<path d="M {x - 8:.0f} {base + 10:.0f} H {x + 8:.0f} L {x:.0f} {base:.0f} Z" class="pin"/>'
        )

    mesh_draw = "\n    ".join(f'<path d="{d}" class="steel"/>' for d in mesh)
    nodes_draw = "\n    ".join(
        f'<circle class="node" cx="{x:.1f}" cy="{y:.1f}" r="1.7" style="animation-delay:{i * 0.08:.2f}s"/>'
        for i, (x, y) in enumerate(nodes)
    )
    brace_draw = "\n    ".join(f'<path d="{d}" class="steel brace"/>' for d in braces)
    brace_hot = "\n    ".join(
        f'<path d="{d}" class="glint" style="animation-delay:{i * 0.35:.2f}s"/>' for i, d in enumerate(braces)
    )
    frame_draw = "\n    ".join(f'<path d="{d}" class="member"/>' for d in frame)

    tabs = [
        (620, "Alloy"),
        (760, "Surface"),
        (900, "Frame"),
        (1040, "Form"),
    ]
    tab_draw = "\n    ".join(
        f'<g class="phase p{i}">'
        f'<text class="tab" x="{x}" y="446">{name}</text>'
        f'<path d="M {x} 456 H {x + 52}" class="tabrule"/>'
        f"</g>"
        for i, (x, name) in enumerate(tabs)
    )
    lines = [
        (0, "0.0659% to 0.0175% residual"),
        (1, "Ribs \u221231.10% at equal volume"),
        (2, "Median carbon \u22125.7%"),
        (3, "79 of 84 pairs within 5%"),
    ]
    line_draw = "\n    ".join(
        f'<text class="result phase p{i}" x="48" y="{372 + 26 * i}">{text}</text>' for i, text in lines
    )
    pills = "\n    ".join(
        f'<g class="phase p{i}">'
        f'<rect x="{48 + i * 118}" y="300" width="108" height="32" rx="16" class="pill"/>'
        f'<text class="pilltext" x="{102 + i * 118}" y="321">0{i + 1}  {label}</text>'
        f"</g>"
        for i, label in enumerate(("Alloy", "Surface", "Frame", "Form"))
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 500" role="img" aria-labelledby="title desc">
  <title id="title">Syed Nafiz Reja Hasib. Mechanics, verification, and low-carbon design.</title>
  <desc id="desc">A two-bay frame. The left bay is a NiTi diagrid with a flag loop. The right bay carries a shell vault. Four studies take turns: residual drift 0.0659 percent to 0.0175 percent, ribs minus 31.10 percent, median carbon minus 5.7 percent, and 79 of 84 pairs within 5 percent.</desc>
  <defs>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0 H0 V28" fill="none" stroke="#121a26" stroke-width="1"/>
    </pattern>
    <radialGradient id="lamp" cx="78%" cy="28%" r="40%">
      <stop offset="0" stop-color="{HOT}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{HOT}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="board"><rect width="1200" height="500" rx="18"/></clipPath>
    <clipPath id="stage"><rect x="548" y="28" width="620" height="444" rx="14"/></clipPath>
  </defs>
  <style>
    .eye {{ fill: {HOT}; font-family: {MONO}; font-size: 12px; letter-spacing: 2.4px; }}
    .name {{ fill: {INK}; font-family: {SERIF}; font-size: 36px; }}
    .head {{ fill: {INK}; font-family: {SANS}; font-size: 20px; font-weight: 600; }}
    .sub {{ fill: {MUTED}; font-family: {SANS}; font-size: 14px; }}
    .result {{ fill: {MUTED}; font-family: {SANS}; font-size: 14px; }}
    .pill {{ fill: #101820; stroke: {LINE}; }}
    .pilltext {{ fill: {INK}; font-family: {MONO}; font-size: 12px; letter-spacing: 0.6px; text-anchor: middle; }}
    .steel {{ fill: none; stroke: {STEEL}; stroke-width: 1.15; stroke-linejoin: round; }}
    .brace {{ stroke-width: 1.35; }}
    .member {{ fill: none; stroke: #c5d0d8; stroke-width: 2.15; stroke-linejoin: round; stroke-linecap: square; }}
    .pin {{ fill: #101820; stroke: {STEEL}; stroke-width: 1; }}
    .joint {{ fill: {HOT_SOFT}; }}
    .glint {{ fill: none; stroke: {HOT_SOFT}; stroke-width: 1.7; stroke-linecap: round; stroke-dasharray: 18 160; animation: glide 5.6s linear infinite; }}
    .ridge {{ fill: none; stroke: {HOT}; stroke-width: 1.6; stroke-linecap: round; stroke-dasharray: 16 220; animation: glide 4.8s linear infinite; }}
    .node {{ fill: {HOT}; opacity: 0.45; animation: ripple 4.8s ease-in-out infinite; }}
    .flag {{ fill: none; stroke: {HOT}; stroke-width: 1.6; stroke-linejoin: round; stroke-linecap: round; }}
    .bead {{ fill: {HOT_SOFT}; }}
    .halo {{ fill: {HOT}; opacity: 0.28; }}
    .tab {{ fill: {INK}; font-family: {MONO}; font-size: 11px; letter-spacing: 1.4px; }}
    .tabrule {{ fill: none; stroke: {HOT}; stroke-width: 1.6; stroke-linecap: round; }}
    .tick {{ fill: none; stroke: #314458; stroke-width: 1; }}
    .phase {{ opacity: 0.38; }}
    .p0 {{ animation: ph0 {CYCLE} linear infinite; }}
    .p1 {{ animation: ph1 {CYCLE} linear infinite; }}
    .p2 {{ animation: ph2 {CYCLE} linear infinite; }}
    .p3 {{ animation: ph3 {CYCLE} linear infinite; }}
    @keyframes glide {{ to {{ stroke-dashoffset: -178; }} }}
    @keyframes ripple {{
      0%, 100% {{ opacity: 0.28; }}
      50% {{ opacity: 1; }}
    }}
    @keyframes ph0 {{
      0%, 20% {{ opacity: 1; }}
      28%, 94% {{ opacity: 0.34; }}
      100% {{ opacity: 1; }}
    }}
    @keyframes ph1 {{
      0%, 22% {{ opacity: 0.34; }}
      30%, 45% {{ opacity: 1; }}
      53%, 100% {{ opacity: 0.34; }}
    }}
    @keyframes ph2 {{
      0%, 47% {{ opacity: 0.34; }}
      55%, 70% {{ opacity: 1; }}
      78%, 100% {{ opacity: 0.34; }}
    }}
    @keyframes ph3 {{
      0%, 72% {{ opacity: 0.34; }}
      80%, 95% {{ opacity: 1; }}
      100% {{ opacity: 0.34; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .glint, .ridge, .node, .phase {{ animation: none; opacity: 1; }}
    }}
  </style>
  <g clip-path="url(#board)">
    <rect width="1200" height="500" fill="{PAPER}"/>
    <rect width="1200" height="500" fill="url(#grid)"/>
    <path class="tick" d="M28 28 H68 M28 28 V68 M1172 28 H1132 M1172 28 V68 M28 472 H68 M28 472 V432 M1172 472 H1132 M1172 472 V432"/>
    <text class="eye" x="48" y="78">COMPUTATIONAL MECHANICS</text>
    <text class="name" x="48" y="132">Syed Nafiz Reja Hasib</text>
    <text class="head" x="48" y="178">Mechanics, verification, and</text>
    <text class="head" x="48" y="206">low-carbon design in one workflow.</text>
    <text class="sub" x="48" y="244">Shells, superelastic NiTi, seismic carbon.</text>
    {pills}
    {line_draw}
    <g clip-path="url(#stage)">
      <rect x="548" y="28" width="620" height="444" fill="{PANEL}"/>
      <rect x="548" y="28" width="620" height="444" fill="url(#lamp)"/>
      <text class="eye" x="572" y="58">VIEW</text>
      <path d="M572 74 H1144" stroke="{LINE}" stroke-width="1"/>
      {frame_draw}
      {"".join(pins)}
      <g class="phase p2">
        {frame_draw.replace('class="member"', 'class="ridge"')}
      </g>
      {brace_draw}
      <g class="phase p0">
        {brace_hot}
      </g>
      {mesh_draw}
      <g class="phase p1">
        <path d="{crown}" class="ridge"/>
        {mesh_draw.replace('class="steel"', 'class="glint"')}
      </g>
      <g class="phase p3">
        {nodes_draw}
      </g>
      <circle class="joint" cx="{left:.0f}" cy="{beam:.0f}" r="2.4"/>
      <circle class="joint" cx="{mid:.0f}" cy="{beam:.0f}" r="2.4"/>
      <circle class="joint" cx="{right:.0f}" cy="{beam:.0f}" r="2.4"/>
      <text class="tab" x="572" y="360">NiTi</text>
      <path id="flag" class="flag" d="{_hero_flag}"/>
      <path d="{_hero_flag}" class="glint"/>
      <circle class="halo" r="7" cx="{_hx:.1f}" cy="{_hy:.1f}">
        <animateMotion dur="8.5s" repeatCount="indefinite" rotate="0">
          <mpath href="#flag" xlink:href="#flag"/>
        </animateMotion>
      </circle>
      <circle class="bead" r="3.1" cx="{_hx:.1f}" cy="{_hy:.1f}">
        <animateMotion dur="8.5s" repeatCount="indefinite">
          <mpath href="#flag" xlink:href="#flag"/>
        </animateMotion>
      </circle>
      <path d="M572 424 H1144" stroke="{LINE}" stroke-width="1"/>
      {tab_draw}
    </g>
  </g>
  <rect x="548.5" y="28.5" width="619" height="443" rx="14" fill="none" stroke="{LINE}"/>
  <rect x="0.5" y="0.5" width="1199" height="499" rx="18" fill="none" stroke="{LINE}"/>
</svg>
'''


def bars() -> str:
    """Equal-volume buckling change. Order is the study order, not the ranking."""
    specs = [
        ("ribs", -31.10, SAND),
        ("grid", 16.05, HOT),
        ("thick", 25.74, HOT),
        ("dent", 15.03, STEEL),
    ]
    zero = 100
    scale = 34 / 25.74
    parts = [f'<path d="M24 {zero} H256" stroke="{LINE}" stroke-width="1"/>']
    for i, (label, value, color) in enumerate(specs):
        height = abs(value) * scale
        x = 34 + i * 60
        y = zero if value < 0 else zero - height
        sign = "\u2212" if value < 0 else "+"
        parts.append(f'<rect x="{x}" y="{y:.1f}" width="32" height="{height:.1f}" rx="2" fill="{color}"/>')
        parts.append(
            f'<text class="tiny" x="{x + 16}" y="156" text-anchor="middle">{sign}{abs(value):.2f}</text>'
        )
        parts.append(f'<text class="tiny" x="{x + 16}" y="170" text-anchor="middle">{label}</text>')
    return "\n      ".join(parts)


def pips() -> str:
    parts = []
    for i in range(33):
        col, row = i % 11, i // 11
        x, y = 22 + col * 22, 86 + row * 24
        if i == 32:
            x += 4
        delay = "" if i == 32 else f' style="animation-delay:{i * 0.05:.2f}s"'
        klass = "pip last" if i == 32 else "pip"
        color = SAND if i == 32 else HOT
        parts.append(f'<rect class="{klass}"{delay} x="{x}" y="{y}" width="14" height="14" rx="2" fill="{color}"/>')
    return "\n      ".join(parts)


def cells() -> str:
    parts = []
    for i in range(84):
        col, row = i % 12, i // 12
        x, y = 18 + col * 21, 68 + row * 16
        dim = i >= 79
        delay = "" if dim else f' style="animation-delay:{i * 0.03:.2f}s"'
        klass = "cell dim" if dim else "cell"
        color = SAND if dim else HOT
        parts.append(f'<rect class="{klass}"{delay} x="{x}" y="{y}" width="15" height="11" rx="1.5" fill="{color}"/>')
    return "\n      ".join(parts)


def flag_card() -> str:
    d, (cx, cy) = flag(24, 68, 228, 72)
    return f'''<path id="cardflag" class="flag" d="{d}"/>
      <path d="{d}" class="glint"/>
      <circle class="bead" r="3" cx="{cx:.1f}" cy="{cy:.1f}">
        <animateMotion dur="6.5s" repeatCount="indefinite">
          <mpath href="#cardflag" xlink:href="#cardflag"/>
        </animateMotion>
      </circle>'''


def card(i: int, title: str, stat: str, lines: list[tuple[str, str]], diagram: str) -> str:
    x = 16 + i * 294
    body = "\n      ".join(
        f'<text class="{kind}" x="20" y="{226 + 22 * k}">{text}</text>' for k, (kind, text) in enumerate(lines)
    )
    return f'''<g transform="translate({x} 16)">
      <rect width="280" height="360" rx="16" fill="{PANEL}" stroke="{LINE}"/>
      <rect class="trace" width="280" height="360" rx="16" pathLength="100" style="animation-delay:{i * 0.6:.1f}s"/>
      <text class="idx" x="20" y="36">0{i + 1}</text>
      <text class="title" x="52" y="36">{title}</text>
      <path d="M20 52 H260" stroke="{LINE}"/>
      {diagram}
      <text class="stat" x="20" y="198">{stat}</text>
      {body}
    </g>'''


def work() -> str:
    cards = [
        card(
            0,
            "Alloy",
            "0.0659% to 0.0175%",
            [("body", "residual drift"), ("body", "Peak 1.79% to 3.40%"), ("body", "+620.9 kgCO2e"), ("limit", "1D, isothermal")],
            flag_card(),
        ),
        card(
            1,
            "Surface",
            "\u221231.10% ribs",
            [("body", "+16.05% grid"), ("body", "+25.74% thickness"), ("body", "+15.03% with a dent"), ("limit", "elastic only")],
            bars(),
        ),
        card(
            2,
            "Frame",
            "\u22125.7% median",
            [("body", "whole-building A1-A3"), ("body", "32 of 33 frames"), ("body", "5,184 designs"), ("limit", "frame dilutes the floor")],
            pips(),
        ),
        card(
            3,
            "Form",
            "79 / 84 within 5%",
            [("body", "seismic pairs"), ("body", "ShellForm, ShellLab"), ("body", "equilibrium to 1e-13 m"), ("limit", "buckling governs")],
            cells(),
        ),
    ]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 392" role="img" aria-labelledby="st sd">
  <title id="st">Four studies: alloy, surface, frame, form.</title>
  <desc id="sd">Residual drift 0.0659 percent to 0.0175 percent. Ribs minus 31.10 percent, orthogonal grid plus 16.05 percent, thickness plus 25.74 percent and plus 15.03 percent with a dent. Median carbon minus 5.7 percent on 32 of 33 frames. 79 of 84 pairs within 5 percent.</desc>
  <style>
    .idx {{ fill: {HOT}; font-family: {MONO}; font-size: 12px; letter-spacing: 1px; }}
    .title {{ fill: {INK}; font-family: {SERIF}; font-size: 20px; }}
    .stat {{ fill: {INK}; font-family: {SERIF}; font-size: 20px; }}
    .body {{ fill: {MUTED}; font-family: {SANS}; font-size: 14px; }}
    .limit {{ fill: {SAND}; font-family: {SANS}; font-size: 14px; }}
    .tiny {{ fill: {MUTED}; font-family: {MONO}; font-size: 10px; }}
    .flag {{ fill: none; stroke: {HOT}; stroke-width: 1.6; stroke-linejoin: round; stroke-linecap: round; }}
    .glint {{ fill: none; stroke: {HOT_SOFT}; stroke-width: 1.6; stroke-linecap: round; stroke-dasharray: 22 180; animation: glide 5.2s linear infinite; }}
    .bead {{ fill: {HOT_SOFT}; }}
    .trace {{ fill: none; stroke: {HOT}; stroke-width: 1.25; stroke-dasharray: 14 86; animation: march 9s linear infinite; }}
    .pip {{ animation: ripple 3.6s ease-in-out infinite; }}
    .pip.last {{ animation: none; }}
    .cell {{ animation: ripple 4.4s ease-in-out infinite; }}
    .cell.dim {{ animation: none; opacity: 0.95; }}
    @keyframes glide {{ to {{ stroke-dashoffset: -202; }} }}
    @keyframes march {{ to {{ stroke-dashoffset: -100; }} }}
    @keyframes ripple {{
      0%, 100% {{ opacity: 0.82; }}
      50% {{ opacity: 1; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .glint, .trace, .pip, .cell {{ animation: none; opacity: 1; }}
    }}
  </style>
  <rect width="1200" height="392" rx="18" fill="{PAPER}"/>
  {"".join(cards)}
  <rect x="0.5" y="0.5" width="1199" height="391" rx="18" fill="none" stroke="{LINE}"/>
</svg>
'''


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(hero(), encoding="utf-8", newline="\n")
    (ASSETS / "work.svg").write_text(work(), encoding="utf-8", newline="\n")
    print("[ok] assets/hero.svg assets/work.svg")


if __name__ == "__main__":
    main()
