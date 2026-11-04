#!/usr/bin/env python3
"""
generate_techstack_svg.py
Generates a 3D mechanical-keycap-style tech stack SVG for GitHub README.
Uses 100% INLINE SVG vector paths (no external images/CDNs) so that GitHub's
Camo image proxy and browser sandboxing render all icons perfectly!
"""

import os
import json

# ── Canvas & key geometry ───────────────────────────────────────────────────
BG         = "#0D1117"       # GitHub dark background
TOTAL_W    = 860             # SVG width
KEY_W      = 78              # top-face width
KEY_H      = 54              # top-face height
CORNER_R   = 10              # corner radius of each key
EXTRUDE    = 7               # 3-D extrusion depth (px)
GAP_X      = 10              # horizontal gap between keys
GAP_Y      = 16              # vertical gap between rows
FONT       = "JetBrains Mono, -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace"
LABEL_SIZE = 9.5             # font-size for key label (px)
ICON_SIZE  = 20              # icon size (px)

# ── Tech definitions (4 rows of 6 keys = 24 keys) ───────────────────────────
TECH_ROWS = [
    # Row 0 – Languages
    [
        ("Python",     "#3776AB", "python"),
        ("Java",       "#ED8B00", "openjdk"),
        ("C",          "#627894", "c"),
        ("JavaScript", "#F7DF1E", "javascript"),
        ("TypeScript", "#3178C6", "typescript"),
        ("SQL",        "#336791", "postgresql"),
    ],
    # Row 1 – ML / AI / Data
    [
        ("PyTorch",    "#EE4C2C", "pytorch"),
        ("TensorFlow", "#FF6F00", "tensorflow"),
        ("FastAPI",    "#009688", "fastapi"),
        ("NumPy",      "#013243", "numpy"),
        ("Pandas",     "#150458", "pandas"),
        ("Scikit",     "#F7931E", "scikitlearn"),
    ],
    # Row 2 – Backend / Infra
    [
        ("Node.js",    "#339933", "nodedotjs"),
        ("Express",    "#383838", "express"),
        ("MongoDB",    "#47A248", "mongodb"),
        ("PostgreSQL", "#4169E1", "postgresql"),
        ("Redis",      "#DC382D", "redis"),
        ("Docker",     "#2496ED", "docker"),
    ],
    # Row 3 – Frontend / Tools
    [
        ("React",      "#61DAFB", "react"),
        ("Next.js",    "#1F2428", "nextdotjs"),
        ("Tailwind",   "#06B6D4", "tailwindcss"),
        ("Linux",      "#EBB317", "linux"),
        ("Git",        "#F05032", "git"),
        ("GitHub",     "#6E5494", "github"),
    ],
]

# ── Color utilities ─────────────────────────────────────────────────────────
def darken(hex_color: str, factor: float = 0.45) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = max(0, int(r * (1 - factor)))
    g = max(0, int(g * (1 - factor)))
    b = max(0, int(b * (1 - factor)))
    return f"#{r:02x}{g:02x}{b:02x}"

def lighten(hex_color: str, factor: float = 0.25) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - g) * factor))
    return f"#{r:02x}{g:02x}{b:02x}"

def icon_color(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#0D1117" if lum > 0.58 else "#FFFFFF"

# ── Load icon vector paths ──────────────────────────────────────────────────
def load_icon_paths():
    json_path = os.path.join(os.path.dirname(__file__), "tech_icons.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# ── Build one key ───────────────────────────────────────────────────────────
def make_key(label: str, top_color: str, slug: str, x: float, y: float, idx: int, icon_dict: dict) -> tuple:
    kw, kh = KEY_W, KEY_H
    r  = CORNER_R
    ex = EXTRUDE
    side_color = darken(top_color, 0.48)
    bottom_side = darken(top_color, 0.62)
    shine_color = lighten(top_color, 0.28)
    text_col = icon_color(top_color)

    gid = f"kg{idx}"

    # 3D Extrusion shapes
    right_face = (
        f"M {x+kw-r},{y+r} "
        f"Q {x+kw},{y} {x+kw+ex},{y+r+ex} "
        f"L {x+kw+ex},{y+kh-r+ex} "
        f"Q {x+kw+ex},{y+kh+ex} {x+kw},{y+kh} "
        f"L {x+kw},{y+r} Z"
    )
    bottom_face = (
        f"M {x+r},{y+kh} "
        f"L {x+kw},{y+kh} "
        f"Q {x+kw+ex},{y+kh+ex} {x+kw-r+ex},{y+kh+ex} "
        f"L {x+r+ex},{y+kh+ex} "
        f"Q {x+ex},{y+kh+ex} {x},{y+kh} Z"
    )

    # Top rounded rectangle
    top_rect = (
        f'<rect x="{x}" y="{y}" width="{kw}" height="{kh}" rx="{r}" ry="{r}" '
        f'fill="url(#{gid})" stroke="{shine_color}" stroke-width="0.8" />'
    )

    # Top-face highlight gloss
    shine = (
        f'<ellipse cx="{x + kw*0.35:.1f}" cy="{y + kh*0.25:.1f}" '
        f'rx="{kw*0.28:.1f}" ry="{kh*0.14:.1f}" '
        f'fill="white" opacity="0.12" />'
    )

    # Inline vector icon
    path_d = icon_dict.get(slug, "")
    if path_d:
        scale = ICON_SIZE / 24.0
        icon_x = x + (kw - ICON_SIZE) / 2
        icon_y = y + 7.5
        icon_svg = (
            f'<g transform="translate({icon_x:.2f}, {icon_y:.2f}) scale({scale:.4f})">'
            f'<path fill="{text_col}" d="{path_d}"/>'
            f'</g>'
        )
    else:
        # Fallback text initial
        icon_svg = (
            f'<text x="{x + kw/2:.1f}" y="{y + 24:.1f}" '
            f'font-family="{FONT}" font-size="14" font-weight="bold" '
            f'fill="{text_col}" text-anchor="middle">{label[0]}</text>'
        )

    # Label text below icon
    display = label if len(label) <= 10 else label[:9] + "…"
    label_y = y + kh - 8.5
    label_svg = (
        f'<text x="{x + kw/2:.1f}" y="{label_y:.1f}" '
        f'font-family="{FONT}" font-size="{LABEL_SIZE}" '
        f'font-weight="700" fill="{text_col}" opacity="0.95" '
        f'text-anchor="middle">{display}</text>'
    )

    grad_def = (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="0.5" y2="1">'
        f'<stop offset="0%" stop-color="{lighten(top_color, 0.15)}" />'
        f'<stop offset="100%" stop-color="{top_color}" />'
        f'</linearGradient>'
    )

    group = f"""
  <g class="key">
    <!-- 3D Extrusion -->
    <path d="{right_face}"  fill="{side_color}" />
    <path d="{bottom_face}" fill="{bottom_side}" />
    <!-- Top Face & Content -->
    {top_rect}
    {shine}
    {icon_svg}
    {label_svg}
  </g>"""
    return group, grad_def

# ── Build full SVG ──────────────────────────────────────────────────────────
def build_svg() -> str:
    icon_dict = load_icon_paths()
    section_labels = [
        "L A N G U A G E S",
        "M L   /   A I",
        "B A C K E N D   /   I N F R A",
        "F R O N T E N D   /   T O O L S"
    ]

    groups = []
    grad_defs = []
    label_svgs = []

    y_offset = 20
    for row_idx, row in enumerate(TECH_ROWS):
        # Section title above row
        label_svgs.append(
            f'<text x="{TOTAL_W//2}" y="{y_offset + 14}" '
            f'font-family="{FONT}" font-size="9" font-weight="800" '
            f'fill="#58A6FF" opacity="0.75" text-anchor="middle" '
            f'letter-spacing="2.5">{section_labels[row_idx]}</text>'
        )
        y_offset += 24

        row_w = len(row) * (KEY_W + GAP_X) - GAP_X + EXTRUDE
        row_x = (TOTAL_W - row_w) / 2
        # Slight keyboard stagger for row 1 and 3
        if row_idx % 2 == 1:
            row_x += (KEY_W + GAP_X) * 0.20

        for col_idx, (label, color, slug) in enumerate(row):
            x = row_x + col_idx * (KEY_W + GAP_X)
            y = y_offset
            idx = row_idx * 10 + col_idx
            grp, gdef = make_key(label, color, slug, x, y, idx, icon_dict)
            groups.append(grp)
            grad_defs.append(gdef)

        y_offset += KEY_H + EXTRUDE + GAP_Y

    total_h = y_offset + 10

    all_defs = "\n    ".join(grad_defs)
    all_labels = "\n  ".join(label_svgs)
    all_groups = "\n".join(groups)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="{TOTAL_W}" height="{total_h}"
     viewBox="0 0 {TOTAL_W} {total_h}">
  <style>
    .key {{
      transition: transform 0.2s ease;
    }}
  </style>
  <defs>
    {all_defs}
  </defs>

  <!-- Background Canvas -->
  <rect width="{TOTAL_W}" height="{total_h}" fill="{BG}" rx="14"/>

  <!-- Section Categories -->
  {all_labels}

  <!-- 3D Keys -->
  {all_groups}

</svg>"""
    return svg

# ── Entry point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    out_path = os.path.join(
        os.path.dirname(__file__), "..", "assets", "techstack-3d-dark.svg"
    )
    out_path = os.path.normpath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    svg = build_svg()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✅ Generated 100% inline vector 3D Tech Stack: {out_path}")
