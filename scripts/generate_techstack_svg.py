#!/usr/bin/env python3
"""
generate_techstack_svg.py
Generates a 3D mechanical-keycap-style tech stack SVG for GitHub README.
Each technology is rendered as an extruded rounded-rectangle "key" with:
  - A bright top face
  - A darker side/extrusion for the 3D pop
  - The tech logo (via Simple Icons CDN embedded as <image>) + name label
Output: assets/techstack-3d-dark.svg
"""

import os
import math
import textwrap

# ── Canvas & key geometry ───────────────────────────────────────────────────
BG         = "#0D1117"       # GitHub dark background
TOTAL_W    = 860             # SVG width (matches README width)
KEY_W      = 76              # top-face width
KEY_H      = 52              # top-face height
CORNER_R   = 10              # corner radius of each key
EXTRUDE    = 7               # 3-D extrusion depth (px)
GAP_X      = 10              # horizontal gap between keys
GAP_Y      = 14              # vertical gap between rows
FONT       = "JetBrains Mono, Fira Code, Cascadia Code, monospace"
LABEL_SIZE = 9               # font-size for key label (px)
ICON_SIZE  = 24              # icon image size

# ── Tech definitions ─────────────────────────────────────────────────────────
# (label, top-face color, Simple Icons slug)
# slug → https://cdn.simpleicons.org/{slug}/white
TECH_ROWS = [
    # Row 0 – Languages
    [
        ("Python",     "#3776AB", "python"),
        ("Java",       "#ED8B00", "openjdk"),
        ("C",          "#A8B9CC", "c"),
        ("JavaScript", "#F7DF1E", "javascript"),
        ("TypeScript", "#3178C6", "typescript"),
        ("SQL",        "#336791", "postgresql"),
    ],
    # Row 1 – ML / AI / Data
    [
        ("PyTorch",    "#EE4C2C", "pytorch"),
        ("FastAPI",    "#009688", "fastapi"),
        ("NumPy",      "#013243", "numpy"),
        ("Pandas",     "#150458", "pandas"),
        ("Scikit",     "#F7931E", "scikitlearn"),
        ("OpenAI",     "#412991", "openai"),
    ],
    # Row 2 – Backend / Infra
    [
        ("Node.js",    "#339933", "nodedotjs"),
        ("Express",    "#404040", "express"),
        ("MongoDB",    "#47A248", "mongodb"),
        ("PostgreSQL", "#4169E1", "postgresql"),
        ("Redis",      "#DC382D", "redis"),
        ("Docker",     "#2496ED", "docker"),
    ],
    # Row 3 – Frontend / Tools
    [
        ("React",      "#61DAFB", "react"),
        ("Next.js",    "#FFFFFF", "nextdotjs"),
        ("Tailwind",   "#06B6D4", "tailwindcss"),
        ("Git",        "#F05032", "git"),
        ("GitHub",     "#6E5494", "github"),
        ("AWS",        "#FF9900", "amazonaws"),
    ],
]

# ── Helper: darken a hex color ───────────────────────────────────────────────
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
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02x}{g:02x}{b:02x}"

# ── Determine icon text colour (white vs dark) ───────────────────────────────
def icon_color(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    # perceived luminance
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#0D1117" if lum > 0.55 else "#FFFFFF"

# ── Build one key's SVG group ────────────────────────────────────────────────
def make_key(label: str, top_color: str, slug: str, x: float, y: float, idx: int) -> str:
    kw, kh = KEY_W, KEY_H
    r  = CORNER_R
    ex = EXTRUDE
    side_color = darken(top_color, 0.50)
    shine_color = lighten(top_color, 0.30)
    text_col = icon_color(top_color)

    # gradient id unique per key
    gid   = f"kg{idx}"
    sid   = f"ks{idx}"   # shine/gloss

    # ── Extrusion (bottom-right solid block) ─────────────────────────────────
    # We draw the side faces as a path that sits behind the top face
    # Right side face
    right_face = (
        f"M {x+kw-r},{y+r} "
        f"Q {x+kw},{y} {x+kw+ex},{y+r+ex} "
        f"L {x+kw+ex},{y+kh-r+ex} "
        f"Q {x+kw+ex},{y+kh+ex} {x+kw},{y+kh} "
        f"L {x+kw},{y+r} Z"
    )
    # Bottom face
    bottom_face = (
        f"M {x+r},{y+kh} "
        f"L {x+kw},{y+kh} "
        f"Q {x+kw+ex},{y+kh+ex} {x+kw-r+ex},{y+kh+ex} "
        f"L {x+r+ex},{y+kh+ex} "
        f"Q {x+ex},{y+kh+ex} {x},{y+kh} Z"
    )
    # Corner triangle connector
    corner_tri = (
        f"M {x+kw},{y+kh} "
        f"L {x+kw+ex},{y+kh+ex} "
        f"L {x+kw+ex},{y+kh-r+ex} "
        f"Q {x+kw+ex},{y+kh+ex} {x+kw-r+ex},{y+kh+ex} Z"
    )

    # ── Top face rounded rect ─────────────────────────────────────────────────
    top_rect = f'<rect x="{x}" y="{y}" width="{kw}" height="{kh}" rx="{r}" ry="{r}" fill="url(#{gid})" stroke="{shine_color}" stroke-width="0.8" />'

    # ── Gloss shine (top-left arc highlight) ─────────────────────────────────
    shine = (
        f'<ellipse cx="{x + kw*0.35:.1f}" cy="{y + kh*0.25:.1f}" '
        f'rx="{kw*0.28:.1f}" ry="{kh*0.14:.1f}" '
        f'fill="white" opacity="0.12" />'
    )

    # ── Icon image (Simple Icons CDN) ─────────────────────────────────────────
    icon_col_str = "white" if text_col == "#FFFFFF" else "111111"
    icon_url = f"https://cdn.simpleicons.org/{slug}/{icon_col_str}"
    icon_x = x + (kw - ICON_SIZE) / 2
    icon_y = y + 7
    icon_img = (
        f'<image href="{icon_url}" '
        f'x="{icon_x:.1f}" y="{icon_y:.1f}" '
        f'width="{ICON_SIZE}" height="{ICON_SIZE}" '
        f'clip-path="url(#cp{idx})" />'
    )

    # ── Clip path so icon stays in the key ───────────────────────────────────
    clip = (
        f'<clipPath id="cp{idx}">'
        f'<rect x="{x}" y="{y}" width="{kw}" height="{kh}" rx="{r}" ry="{r}" />'
        f'</clipPath>'
    )

    # ── Label text ────────────────────────────────────────────────────────────
    # Truncate long labels
    display = label if len(label) <= 10 else label[:9] + "…"
    label_x = x + kw / 2
    label_y = y + kh - 8
    label_svg = (
        f'<text x="{label_x:.1f}" y="{label_y:.1f}" '
        f'font-family="{FONT}" font-size="{LABEL_SIZE}" '
        f'font-weight="600" fill="{text_col}" opacity="0.90" '
        f'text-anchor="middle" dominant-baseline="auto">{display}</text>'
    )

    # ── Hover animation (CSS class based) ────────────────────────────────────
    # We animate via CSS transform on the group
    anim_delay = f"{(idx % 6) * 0.08:.2f}s"

    # ── Gradient definition ───────────────────────────────────────────────────
    grad_def = (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="0.6" y2="1">'
        f'<stop offset="0%" stop-color="{lighten(top_color, 0.18)}" />'
        f'<stop offset="100%" stop-color="{top_color}" />'
        f'</linearGradient>'
    )

    group = f"""
  <g class="key" style="animation-delay:{anim_delay}">
    {clip}
    <!-- Extrusion -->
    <path d="{right_face}"  fill="{side_color}" />
    <path d="{bottom_face}" fill="{darken(top_color, 0.60)}" />
    <!-- Top face -->
    {top_rect}
    {shine}
    {icon_img}
    {label_svg}
  </g>"""
    return group, grad_def


# ── Layout calculation ────────────────────────────────────────────────────────
def compute_layout(rows):
    """Return list of (label, color, slug, x, y) for every key."""
    n_rows   = len(rows)
    max_keys = max(len(r) for r in rows)

    # Total key block width for a full row
    block_w = max_keys * (KEY_W + GAP_X) - GAP_X + EXTRUDE
    start_x = (TOTAL_W - block_w) / 2

    # Total height
    total_h = n_rows * (KEY_H + EXTRUDE + GAP_Y) - GAP_Y + EXTRUDE + 60  # 60 = top padding

    positions = []
    for row_idx, row in enumerate(rows):
        # Centre each row independently (keyboard stagger look)
        row_w = len(row) * (KEY_W + GAP_X) - GAP_X + EXTRUDE
        row_x = (TOTAL_W - row_w) / 2
        # Optional: stagger every other row slightly (like a keyboard)
        if row_idx % 2 == 1:
            row_x += (KEY_W + GAP_X) * 0.25

        y = 30 + row_idx * (KEY_H + EXTRUDE + GAP_Y)
        for col_idx, (label, color, slug) in enumerate(row):
            x = row_x + col_idx * (KEY_W + GAP_X)
            positions.append((label, color, slug, x, y))

    return positions, total_h


# ── Assemble SVG ─────────────────────────────────────────────────────────────
def build_svg() -> str:
    positions, total_h = compute_layout(TECH_ROWS)

    groups   = []
    grad_defs = []

    for idx, (label, color, slug, x, y) in enumerate(positions):
        grp, gdef = make_key(label, color, slug, x, y, idx)
        groups.append(grp)
        grad_defs.append(gdef)

    css = f"""
    <style>
      .key {{
        animation: key-pop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
      }}
      @keyframes key-pop {{
        from {{ transform: scale(0.6); opacity: 0; }}
        to   {{ transform: scale(1);   opacity: 1; }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .key {{ animation: none; }}
      }}
    </style>"""

    section_labels = ["Languages", "ML / AI", "Backend / Infra", "Frontend / Tools"]
    # Compute y positions for section labels (above each row)
    label_svgs = []
    for row_idx, row_label in enumerate(section_labels):
        y_pos = 24 + row_idx * (KEY_H + EXTRUDE + GAP_Y)
        label_svgs.append(
            f'<text x="{TOTAL_W//2}" y="{y_pos:.0f}" '
            f'font-family="{FONT}" font-size="10" font-weight="700" '
            f'fill="#58A6FF" opacity="0.70" text-anchor="middle" '
            f'letter-spacing="2">{row_label.upper()}</text>'
        )

    all_defs = "\n    ".join(grad_defs)
    all_groups = "\n".join(groups)
    all_labels = "\n  ".join(label_svgs)

    # Recompute total height with section label padding
    n_rows   = len(TECH_ROWS)
    total_h  = n_rows * (KEY_H + EXTRUDE + GAP_Y) + 30 + 20

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{TOTAL_W}" height="{total_h}"
     viewBox="0 0 {TOTAL_W} {total_h}">
  {css}
  <defs>
    {all_defs}
  </defs>

  <!-- Background -->
  <rect width="{TOTAL_W}" height="{total_h}" fill="{BG}" rx="12"/>

  <!-- Section labels -->
  {all_labels}

  <!-- Keys -->
  {all_groups}

</svg>"""
    return svg


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    out_path = os.path.join(
        os.path.dirname(__file__), "..", "assets", "techstack-3d-dark.svg"
    )
    out_path = os.path.normpath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    svg = build_svg()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✅ Written: {out_path}")
    print(f"   Keys   : {sum(len(r) for r in TECH_ROWS)}")
    print(f"   Rows   : {len(TECH_ROWS)}")
