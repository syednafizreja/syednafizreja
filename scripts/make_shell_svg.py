#!/usr/bin/env python3
"""Generate a standalone animated SVG depicting a parametric funicular shell

with a finite element mesh motif. Illustrative art, not solver output.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "structural-shell.svg"


def generate_shell_svg(animated: bool = True) -> str:
    # Build clean SMIL-based SVG
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="410" height="490" viewBox="0 0 410 490" role="img" aria-label="Parametric Shell &amp; Finite Element Mesh">
  <title>Parametric Funicular Vault &amp; FEA Mesh Motif (Illustrative)</title>
  <defs>
    <linearGradient id="panelBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#090f17"/>
      <stop offset="100%" stop-color="#0d1726"/>
    </linearGradient>
    <linearGradient id="topbarGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#111f30"/>
      <stop offset="100%" stop-color="#16273d"/>
    </linearGradient>
    <linearGradient id="stressMap" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0b1b2d"/>
      <stop offset="25%" stop-color="#15557b"/>
      <stop offset="50%" stop-color="#0284c7"/>
      <stop offset="75%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#a5f3fc"/>
    </linearGradient>
    <pattern id="diagGrid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 24 M 0 0 L 24 24" fill="none" stroke="#16273d" stroke-width="0.6" opacity="0.4"/>
    </pattern>
    <filter id="meshGlow" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="1.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Panel Frame -->
  <rect width="410" height="490" rx="12" fill="url(#panelBg)" stroke="#1e293b" stroke-width="1.2"/>
  <rect width="410" height="490" rx="12" fill="url(#diagGrid)"/>

  <!-- Terminal Title Bar -->
  <path d="M 1 12 Q 1 1 12 1 L 398 1 Q 409 1 409 12 L 409 38 L 1 38 Z" fill="url(#topbarGrad)"/>
  <line x1="1" y1="38" x2="409" y2="38" stroke="#1e293b" stroke-width="1"/>
  <circle cx="20" cy="19" r="4.5" fill="#f87171"/>
  <circle cx="34" cy="19" r="4.5" fill="#fbbf24"/>
  <circle cx="48" cy="19" r="4.5" fill="#34d399"/>
  <text x="64" y="23" fill="#64748b" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5" letter-spacing="0.06em">GEOMETRY :: FUNICULAR HYPAR / ILLUSTRATIVE</text>

  <!-- 3D Isometric Computational Shell Mesh -->
  <g transform="translate(205, 235)" filter="url(#meshGlow)">
    <!-- Base Boundary Supports -->
    <path d="M -160,70 L 0,145 L 160,70 L 0,-10 Z" fill="none" stroke="#1e3a5f" stroke-dasharray="4,4" stroke-width="1.2"/>

    <!-- Arch Directrices (Compression Ribs) -->
    <path d="M -160,70 Q -80,-30 0,-95 Q 80,-30 160,70" fill="none" stroke="#0284c7" stroke-width="1.6" opacity="0.9">
      {"<animate attributeName='stroke-dashoffset' from='600' to='0' dur='1.6s' fill='freeze'/>" if animated else ""}
    </path>
    <path d="M -130,85 Q -65,0 0,-60 Q 65,0 130,85" fill="none" stroke="#0ea5e9" stroke-width="1.4" opacity="0.85"/>
    <path d="M -100,100 Q -50,30 0,-25 Q 50,30 100,100" fill="none" stroke="#38bdf8" stroke-width="1.4" opacity="0.85"/>
    <path d="M -70,115 Q -35,60 0,10 Q 35,60 70,115" fill="none" stroke="#7dd3fc" stroke-width="1.4" opacity="0.85"/>
    <path d="M -40,130 Q -20,90 0,45 Q 20,90 40,130" fill="none" stroke="#a5f3fc" stroke-width="1.3" opacity="0.8"/>

    <!-- Transverse Saddle Curvatures (Tension Generators) -->
    <path d="M -160,70 Q -70,100 0,145 Q 70,100 160,70" fill="none" stroke="#0369a1" stroke-width="1.5" opacity="0.9"/>
    <path d="M -125,35 Q -40,65 0,100 Q 40,65 125,35" fill="none" stroke="#0284c7" stroke-width="1.3" opacity="0.8"/>
    <path d="M -90,-5 Q -20,30 0,55 Q 20,30 90,-5" fill="none" stroke="#0ea5e9" stroke-width="1.3" opacity="0.8"/>
    <path d="M -55,-48 Q -10,-5 0,10 Q 10,-5 55,-48" fill="none" stroke="#38bdf8" stroke-width="1.3" opacity="0.8"/>
    <path d="M -25,-75 Q 0,-50 0,-35 Q 0,-50 25,-75" fill="none" stroke="#7dd3fc" stroke-width="1.2" opacity="0.8"/>

    <!-- Critical Analysis Nodes -->
    <circle cx="0" cy="-95" r="3.5" fill="#a5f3fc"/>
    <circle cx="0" cy="145" r="3.5" fill="#38bdf8"/>
    <circle cx="-160" cy="70" r="3.5" fill="#0284c7"/>
    <circle cx="160" cy="70" r="3.5" fill="#0284c7"/>
    <circle cx="0" cy="10" r="3" fill="#38bdf8"/>
    <circle cx="-70" cy="115" r="2.5" fill="#7dd3fc"/>
    <circle cx="70" cy="115" r="2.5" fill="#7dd3fc"/>
  </g>

  <!-- Spec & Dimension Callouts -->
  <g transform="translate(24, 385)">
    <text x="0" y="0" fill="#64748b" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5" letter-spacing="0.05em">ILLUSTRATIVE COLOUR SCALE</text>
    <rect x="0" y="8" width="362" height="6" rx="2" fill="url(#stressMap)"/>
    <text x="0" y="27" fill="#64748b" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9">Low</text>
    <text x="170" y="27" fill="#38bdf8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9">Mid</text>
    <text x="340" y="27" fill="#a5f3fc" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9">High</text>
  </g>

  <!-- Structural Metadata Matrix -->
  <g transform="translate(24, 438)">
    <line x1="0" y1="0" x2="362" y2="0" stroke="#1e293b" stroke-width="1"/>
    <text x="0" y="16" fill="#475569" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5">SOLVER</text>
    <text x="56" y="16" fill="#94a3b8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5">CalculiX + OpenSeesPy</text>

    <text x="210" y="16" fill="#475569" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5">MESH</text>
    <text x="250" y="16" fill="#38bdf8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5">Gmsh Quad-Shell (S8R)</text>

    <text x="0" y="32" fill="#475569" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5">SEISMIC</text>
    <text x="56" y="32" fill="#94a3b8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5">GB 50011 / EC8 (0.05-0.40g)</text>

    <text x="210" y="32" fill="#475569" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5">CARBON</text>
    <text x="262" y="32" fill="#38bdf8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="9.5">Low-carbon focus</text>
  </g>
</svg>"""
    return svg


def main() -> int:
    content = generate_shell_svg(animated=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[ok] Structural shell SVG rendered -> {OUTPUT}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
