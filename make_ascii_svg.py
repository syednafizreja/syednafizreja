#!/usr/bin/env python3
"""Create a self-typing monochrome ASCII portrait SVG (100 x 53 characters)."""
from __future__ import annotations

import argparse
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # bright -> dark


def image_to_rows(path: Path, columns: int = 100, rows: int = 53) -> list[str]:
    image = Image.open(path).convert("L")
    # Cell aspect ratio compensates for the narrow advance of monospace glyphs.
    image = image.resize((columns, rows), Image.Resampling.LANCZOS)
    values = np.asarray(image, dtype=np.uint8)
    indices = np.clip(((255 - values.astype(np.float32)) / 255.0 * (len(RAMP) - 1)).round(), 0, len(RAMP) - 1).astype(int)
    return ["".join(RAMP[i] for i in row) for row in indices]


def build_svg(rows: list[str], output: Path, animated: bool = True) -> None:
    columns = 100
    row_count = len(rows)
    cell_w, cell_h = 6.0, 12.0
    width, height = columns * cell_w, row_count * cell_h
    text_color = "#b8c5d1"
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" height="{height:g}" viewBox="0 0 {width:g} {height:g}" role="img" aria-label="Animated monochrome ASCII portrait of Syed Nafiz Reja Hasib">',
        '<title>Syed Nafiz Reja Hasib — ASCII portrait</title>',
        '<defs><linearGradient id="plate" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0c1b29"/><stop offset="1" stop-color="#101d2c"/></linearGradient></defs>',
        '<rect x="1.5" y="1.5" width="597" height="633" rx="18" fill="url(#plate)" stroke="#31536a" stroke-width="3"/>',
        '<defs>',
    ]
    for i in range(row_count):
        parts.append(
            f'<clipPath id="row-clip-{i}"><rect x="0" y="{i * cell_h:g}" width="{width if not animated else 0:g}" height="{cell_h:g}">'
            + (f'<animate attributeName="width" from="0" to="{width:g}" begin="{i * 0.047:.3f}s" dur="0.72s" fill="freeze"/>' if animated else "")
            + '</rect></clipPath>'
        )
    parts.extend(['</defs>'])

    for i, row in enumerate(rows):
        y = (i + 1) * cell_h - 1.4
        parts.append(f'<g clip-path="url(#row-clip-{i})">')
        parts.append(
            f'<text x="0" y="{y:.1f}" fill="{text_color}" font-family="DejaVu Sans Mono, Menlo, Consolas, monospace" font-size="10" xml:space="preserve">{escape(row)}</text>'
        )
        if animated:
            delay = i * 0.047
            parts.append(
                f'<rect x="0" y="{i * cell_h + 1.4:g}" width="6" height="9.2" fill="#b8c5d1" opacity="0.9">'
                f'<animate attributeName="x" from="0" to="{width - 6:g}" begin="{delay:.3f}s" dur="0.72s" fill="freeze"/>'
                f'<animate attributeName="opacity" values="0.95;0.95;0" keyTimes="0;0.97;1" begin="{delay:.3f}s" dur="0.72s" fill="freeze"/>'
                '</rect>'
            )
        parts.append('</g>')

    parts.append('</svg>')
    output.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {output} ({columns} x {row_count} characters; {'one-shot animated' if animated else 'static'})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("source-prepped.png"))
    parser.add_argument("--output", type=Path, default=Path("ascii.svg"))
    parser.add_argument("--static", action="store_true", help="Render without animation")
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"prepared image not found: {args.input}; run prep_photo.py first")
    rows = image_to_rows(args.input)
    build_svg(rows, args.output, animated=not args.static)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
