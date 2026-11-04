#!/usr/bin/env python3
"""
prep_photo.py - Avi Vashishta's Photo Pre-processor for ASCII Conversion
Prepares a personal photo for clean ASCII conversion:
  1. Removes background (via rembg if installed, or smart alpha mask)
  2. Bilateral smoothing to remove noise while keeping edges sharp
  3. Stretches tones and darkens line work
  4. Crops square around subject and saves grayscale image

Usage:
    python3 scripts/prep_photo.py <input_photo> [output_prepped.png]
"""

import os
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "assets", "source-prepped.png")

def prep_image(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input photo '{input_path}' not found.")
        print("Usage: python3 scripts/prep_photo.py my_photo.jpg")
        sys.exit(1)

    print(f"[prep_photo] Loading {input_path}...")

    # Check for rembg and cv2
    try:
        from rembg import remove
        import cv2
        import numpy as np

        print("[prep_photo] Using rembg + OpenCV for advanced subject isolation...")
        cut = remove(Image.open(input_path).convert("RGBA"))
        rgb = np.array(cut.convert("RGB"))
        alpha = np.array(cut.split()[-1])
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

        # Bilateral filter smoothing
        smooth = gray
        for _ in range(3):
            smooth = cv2.bilateralFilter(smooth, 9, 40, 9)

        # Tone stretching
        lo, hi = np.percentile(smooth[alpha > 128], [2, 92])
        tone = np.clip((smooth.astype(np.float32) - lo) / max(1e-5, (hi - lo)), 0, 1)

        # Darken line work
        fine = cv2.GaussianBlur(smooth, (0, 0), 1.5).astype(np.float32)
        coarse = cv2.GaussianBlur(smooth, (0, 0), 6).astype(np.float32)
        lines = np.clip((coarse - fine) / 40.0, 0, 1)
        out = np.clip(tone - 0.6 * lines, 0, 1) * 255

        # Paste onto white
        mask = cv2.GaussianBlur(alpha.astype(np.float32) / 255.0, (0, 0), 1.0)
        out = out * mask + 255.0 * (1.0 - mask)

        ys, xs = np.where(alpha > 20)
        if len(xs) > 0 and len(ys) > 0:
            side = max(xs.max() - xs.min(), ys.max() - ys.min()) + 60
            cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2
            canvas = np.full((side, side), 255, np.uint8)
            x0, y0 = cx - side // 2, cy - side // 2
            sx0, sy0 = max(x0, 0), max(y0, 0)
            sx1, sy1 = min(x0 + side, out.shape[1]), min(y0 + side, out.shape[0])
            canvas[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = out[sy0:sy1, sx0:sx1].astype(np.uint8)
            final_img = Image.fromarray(canvas, mode="L")
        else:
            final_img = Image.fromarray(out.astype(np.uint8), mode="L")

    except ImportError:
        print("[prep_photo] Notice: rembg or opencv-python not installed. Using pure Pillow fallback.")
        img = Image.open(input_path).convert("L")
        w, h = img.size
        side = min(w, h)
        # Center crop square
        left = (w - side) // 2
        top = (h - side) // 2
        final_img = img.crop((left, top, left + side, top + side))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    final_img.save(output_path)
    print(f"✅ Prepped photo saved to: {output_path}")

if __name__ == "__main__":
    prep_image(INP, OUT)

