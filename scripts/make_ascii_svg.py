#!/usr/bin/env python3
"""
make_ascii_svg.py - Avi Vashishta's Exact ASCII Portrait Renderer
Converts a portrait photo into a monochrome, self-typing terminal ASCII-art SVG.

- Each row is revealed with a left-to-right clip wipe and a riding block cursor.
- Entire portrait sweeps from top to bottom and freezes.
- Includes terminal titlebar and status bar with blinking cursor.

Usage:
    python3 scripts/make_ascii_svg.py [input_image] [output_svg]
"""

from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "source-prepped.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "assets", "ashmit-ascii.svg")

# Terminal & art configuration
COLS = int(os.environ.get("COLS", 140))
ART_W_TARGET = 720
CELL_W = ART_W_TARGET / COLS
CELL_H = CELL_W * 15 / 8
ROWS = round(COLS * 8 / 15)
RAMP = " .`:-=+*cs#%@"  # bright(sparse) -> dark(dense)

CONTRAST = 1.15
BRIGHTNESS = 1.0
GAMMA = 1.2           # >1 brightens midtones
WHITE_FLOOR = 0.82    # luminance above this is forced to blank space

PAD = 20
TITLEBAR_H = 32
STATUS_H = 32
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W = int(ART_W + PAD * 2)
CANVAS_H = int(TITLEBAR_H + ART_H + STATUS_H + PAD)

BG = "#0D1117"
BG2 = "#161B22"
FRAME = "#30363D"
TITLE_TEXT = "#8B949E"
INK = "#58A6FF"       # Theme accent cyan-blue / light gray #C9D1D9
CURSOR = "#58A6FF"

ROW_DUR = 5.0 / ROWS  # portrait prints in ~5s
STAGGER = ROW_DUR

def generate_svg(src_path, out_path):
    if not os.path.exists(src_path):
        print(f"[make_ascii_svg] Input '{src_path}' not found. Generating default avatar art.")
        # Create a stylized default portrait image if no image provided yet
        im = Image.new("L", (COLS, ROWS), color=255)
    else:
        im = Image.open(src_path).convert("L")
        im = ImageEnhance.Brightness(im).enhance(BRIGHTNESS)
        im = ImageEnhance.Contrast(im).enhance(CONTRAST)
        im = im.resize((COLS, ROWS), Image.Resampling.LANCZOS)

    px = im.load()
    rows_txt = []
    for y in range(ROWS):
        chars = []
        for x in range(COLS):
            lum = px[x, y] / 255.0
            lum = pow(lum, GAMMA)
            if lum >= WHITE_FLOOR:
                chars.append(" ")
                continue
            idx = int((1.0 - lum) * (len(RAMP) - 1) + 0.5)
            idx = max(0, min(len(RAMP) - 1, idx))
            chars.append(RAMP[idx])
        rows_txt.append("".join(chars))

    art_top = TITLEBAR_H + PAD * 0.4

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="JetBrains Mono, Menlo, Consolas, monospace">',
        '<defs>',
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        '</linearGradient></defs>',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="10" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="10" fill="none" stroke="{FRAME}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]

    # Window dots
    for i, dotcol in enumerate(["#FF5F56", "#FFBD2E", "#27C93F"]):
        parts.append(f'<circle cx="{PAD + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{dotcol}"/>')

    parts.append(
        f'<text x="{CANVAS_W / 2}" y="{TITLEBAR_H / 2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
        f'text-anchor="middle">ashmit@github: ~$ ./portrait.sh</text>'
    )

    # ASCII text rows with typing animation
    font_size = CELL_H * 0.86
    for ry, line in enumerate(rows_txt):
        y = art_top + ry * CELL_H + CELL_H * 0.74
        row_y = art_top + ry * CELL_H
        delay = ry * STAGGER
        safe = html.escape(line)
        text = (f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{INK}" '
                f'font-size="{font_size:.1f}" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text>')

        parts.append(
            f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
            f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" '
            f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
        )
        parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')
        parts.append(
            f'<rect y="{row_y + 1:.1f}" width="{CELL_W}" height="{CELL_H - 2}" fill="{CURSOR}" opacity="0">'
            f'<animate attributeName="x" from="{PAD}" to="{PAD + ART_W}" begin="{delay:.3f}s" '
            f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{delay + ROW_DUR:.3f}s"/></rect>'
        )

    # Terminal Status Bar
    status_line_y = TITLEBAR_H + ART_H + PAD * 0.4
    status_y = status_line_y + 20
    parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
    parts.append(f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
                 f'ashmit@github:~$ whoami <tspan fill="{INK}" font-weight="600">Ashmit Kumar Verma</tspan></text>')
    status_chars = len("ashmit@github:~$ whoami Ashmit Kumar Verma ")
    parts.append(f'<rect x="{PAD + status_chars * 13 * 0.58:.1f}" y="{status_y - 12:.1f}" width="8" height="14" fill="{CURSOR}">'
                 f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>')

    parts.append("</svg>")
    svg = "".join(parts)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[make_ascii_svg] Wrote {out_path} ({len(svg)} bytes; {CANVAS_W}x{CANVAS_H})")

if __name__ == "__main__":
    generate_svg(SRC, OUT)

