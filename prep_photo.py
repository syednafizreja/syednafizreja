#!/usr/bin/env python3
"""Prepare a portrait for the animated ASCII profile artwork.

Preferred path: rembg background removal -> OpenCV CLAHE -> pure-white composite.
If rembg is unavailable, a restrained blue-screen fallback is used for a photo
with a uniformly blue/cyan backdrop (such as the supplied portrait).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def remove_with_rembg(image: Image.Image) -> Image.Image:
    try:
        from rembg import remove  # type: ignore
    except ImportError as exc:
        raise RuntimeError("rembg is not installed") from exc
    result = remove(image.convert("RGBA"))
    if isinstance(result, Image.Image):
        return result.convert("RGBA")
    return Image.open(result).convert("RGBA")


def blue_backdrop_alpha(rgb: np.ndarray) -> np.ndarray:
    """Estimate foreground alpha for a uniformly cyan/blue photo background.

    Only the largest, strongly saturated cyan-blue connected component is keyed
    out. A high saturation/value threshold protects blue-black clothing, tie
    details, and cool shadows from being mistaken for the background.
    """
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hue, sat, val = cv2.split(hsv)
    # This photo's cyan backdrop is close to RGB (0, 159, 211). Use a
    # deliberately strict chroma/value gate so blue-tinted suit highlights
    # are not confused with the background.
    blue = ((hue >= 80) & (hue <= 110) & (sat >= 220) & (val >= 185)).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(blue, connectivity=8)
    if count <= 1:
        return np.ones(rgb.shape[:2], dtype=np.float32)
    largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    background = (labels == largest).astype(np.uint8)
    # Remove a one-pixel cyan fringe, but use a stricter chroma threshold so
    # cool shadows and highlights in the dark suit remain foreground.
    background = cv2.dilate(background, np.ones((3, 3), np.uint8), iterations=1)
    bg_soft = cv2.GaussianBlur(background.astype(np.float32), (0, 0), sigmaX=0.75)
    return np.clip(1.0 - bg_soft, 0.0, 1.0)


def prepare(input_path: Path, output_path: Path) -> None:
    source = Image.open(input_path).convert("RGB")
    try:
        rgba = remove_with_rembg(source)
        method = "rembg"
    except Exception as exc:
        print(
            "WARNING: rembg could not run (" + str(exc) + "); using the blue-backdrop fallback "
            "for this uniformly cyan-background portrait.",
            file=sys.stderr,
        )
        rgb = np.asarray(source)
        alpha = blue_backdrop_alpha(rgb)
        rgba_arr = np.dstack([rgb, np.round(alpha * 255).astype(np.uint8)])
        rgba = Image.fromarray(rgba_arr, mode="RGBA")
        method = "blue-backdrop fallback"

    rgba_np = np.asarray(rgba.convert("RGBA"))
    rgb_np = rgba_np[:, :, :3]
    alpha = rgba_np[:, :, 3].astype(np.float32) / 255.0

    # Apply CLAHE to luminance while retaining the original colour-neutral image.
    gray = cv2.cvtColor(rgb_np, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.1, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Composite onto pure white. White becomes the empty end of the ASCII ramp.
    alpha_3 = alpha[:, :, None]
    composite = enhanced.astype(np.float32) * alpha + 255.0 * (1.0 - alpha)
    composite = np.clip(composite, 0, 255).astype(np.uint8)

    # Keep the full face and shoulders, but trim the extra vertical canvas.
    # The output crop ratio matches the 100 x 53 monospace character grid.
    h, w = composite.shape
    target_ratio = (100 * 0.60) / (53 * 1.20)
    target_h = min(h, int(round(w / target_ratio)))
    if target_h < h:
        # Bias the crop slightly upward so the shoulders remain visible.
        top = max(0, min(h - target_h, int((h - target_h) * 0.78)))
        composite = composite[top : top + target_h, :]

    # Output is deliberately grayscale PNG on pure white.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(composite, mode="L").save(output_path, optimize=True)
    print(f"Prepared {input_path} -> {output_path} ({method}, CLAHE, white composite)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("photo", type=Path, help="Input portrait (JPG/PNG)")
    parser.add_argument("--output", type=Path, default=Path("source-prepped.png"))
    args = parser.parse_args()
    if not args.photo.is_file():
        parser.error(f"photo not found: {args.photo}")
    prepare(args.photo, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
