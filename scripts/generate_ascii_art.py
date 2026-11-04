#!/usr/bin/env python3
"""
generate_ascii_art.py
Converts a personal photo / portrait into high-contrast monospace ASCII art
and saves it to assets/ascii_art.txt for the neofetch terminal card.

Inspired by Avi Vashishta's animated ASCII profile portrait.

Usage:
    python3 scripts/generate_ascii_art.py path/to/your_photo.jpg
    python3 scripts/generate_ascii_art.py path/to/your_photo.jpg --width 24 --invert
"""

import sys
import os
import argparse

try:
    from PIL import Image, ImageOps, ImageEnhance
except ImportError:
    print("Error: Pillow is required. Run: pip install pillow")
    sys.exit(1)

# Character ramps ordered from darkest (sparse) to brightest (dense)
RAMPS = {
    "standard": " .':;+*#%@",
    "detailed": " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
    "blocks":   " ░▒▓█",
    "minimal":  " .:+*#@",
}

def convert_image_to_ascii(image_path, target_width=24, ramp_name="minimal", invert=False, contrast=1.4):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")

    img = Image.open(image_path)

    # Convert to grayscale
    img = img.convert("L")

    # Enhance contrast to make facial features crisp
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)

    # Monospace fonts are ~2x taller than wide, scale height by 0.55
    orig_w, orig_h = img.size
    aspect_ratio = orig_h / orig_w
    target_height = int(target_width * aspect_ratio * 0.55)

    # Cap maximum lines to fit inside neofetch card nicely (12-16 lines)
    if target_height > 16:
        target_height = 16
        target_width = int(target_height / (aspect_ratio * 0.55))

    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

    chars = RAMPS.get(ramp_name, RAMPS["minimal"])
    if invert:
        chars = chars[::-1]

    num_chars = len(chars)

    pixels = list(img.getdata())
    ascii_lines = []
    for row in range(target_height):
        start = row * target_width
        end = start + target_width
        row_pixels = pixels[start:end]
        row_chars = [chars[min(num_chars - 1, int(p / 256 * num_chars))] for p in row_pixels]
        ascii_lines.append("".join(row_chars))

    return ascii_lines

def main():
    parser = argparse.ArgumentParser(description="Convert photo to ASCII portrait for neofetch card")
    parser.add_argument("image_path", help="Path to your photo (jpg, png, webp)")
    parser.add_argument("--width", type=int, default=24, help="Target width in characters (default: 24)")
    parser.add_argument("--ramp", choices=list(RAMPS.keys()), default="minimal", help="Character ramp style")
    parser.add_argument("--invert", action="store_true", help="Invert character density")
    parser.add_argument("--contrast", type=float, default=1.5, help="Contrast boost (default: 1.5)")
    parser.add_argument("--output", default="assets/ascii_art.txt", help="Output text file path")

    args = parser.parse_args()

    print(f"[ascii-art] Processing: {args.image_path}")
    lines = convert_image_to_ascii(
        args.image_path,
        target_width=args.width,
        ramp_name=args.ramp,
        invert=args.invert,
        contrast=args.contrast
    )

    print("\n--- Preview ---")
    for line in lines:
        print(line)
    print("---------------\n")

    out_path = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"✅ ASCII art saved to: {out_path}")
    print("Now run `python3 scripts/generate_terminal_svg.py` to embed it into your neofetch card!")

if __name__ == "__main__":
    main()

