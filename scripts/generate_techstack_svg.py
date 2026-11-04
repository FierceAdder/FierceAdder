#!/usr/bin/env python3
"""Generate isometric 3D tech stack SVG with real Simple Icons paths."""
import urllib.request, json, re, sys

ICONS = {
    "python": {"label": "Python", "color": "#3776AB", "dark": "#1e3d58", "darker": "#152b40", "tc": "#fff"},
    "openjdk": {"label": "Java", "color": "#ED8B00", "dark": "#7b4800", "darker": "#5a3400", "tc": "#fff"},
    "c": {"label": "C", "color": "#A8B9CC", "dark": "#4a5260", "darker": "#363c47", "tc": "#0D1117"},
    "javascript": {"label": "JavaScript", "color": "#F7DF1E", "dark": "#80730f", "darker": "#5d540b", "tc": "#0D1117"},
    "typescript": {"label": "TypeScript", "color": "#3178C6", "dark": "#193e66", "darker": "#122d4b", "tc": "#fff"},
    "postgresql": {"label": "SQL", "color": "#336791", "dark": "#1a3548", "darker": "#122537", "tc": "#fff"},
    "pytorch": {"label": "PyTorch", "color": "#EE4C2C", "dark": "#7b2716", "darker": "#5a1c10", "tc": "#fff"},
    "tensorflow": {"label": "TensorFlow", "color": "#FF6F00", "dark": "#843900", "darker": "#602a00", "tc": "#fff"},
    "fastapi": {"label": "FastAPI", "color": "#009688", "dark": "#004e46", "darker": "#003933", "tc": "#fff"},
    "numpy": {"label": "NumPy", "color": "#013243", "dark": "#001a22", "darker": "#001319", "tc": "#fff", "border": "#4DABCF"},
    "pandas": {"label": "Pandas", "color": "#150458", "dark": "#0a022d", "darker": "#070121", "tc": "#fff", "border": "#564a8a"},
    "scikitlearn": {"label": "Scikit-learn", "color": "#F7931E", "dark": "#804c0f", "darker": "#5d370b", "tc": "#0D1117"},
    "nodedotjs": {"label": "Node.js", "color": "#339933", "dark": "#1a4f1a", "darker": "#133a13", "tc": "#fff"},
    "express": {"label": "Express", "color": "#000000", "dark": "#1d1d1d", "darker": "#151515", "tc": "#fff", "border": "#6f6f60"},
    "mongodb": {"label": "MongoDB", "color": "#47A248", "dark": "#245425", "darker": "#1a3d1b", "tc": "#fff"},
    "postgresql": {"label": "PostgreSQL", "color": "#4169E1", "dark": "#213675", "darker": "#182755", "tc": "#fff"},
    "redis": {"label": "Redis", "color": "#DC382D", "dark": "#721d17", "darker": "#531511", "tc": "#fff"},
    "docker": {"label": "Docker", "color": "#2496ED", "dark": "#124e7b", "darker": "#0d3858", "tc": "#fff"},
    "react": {"label": "React", "color": "#20232A", "dark": "#1a4f5a", "darker": "#133a43", "tc": "#61DAFB", "border": "#61DAFB"},
    "nginx": {"label": "Nginx", "color": "#1F2428", "dark": "#131a1e", "darker": "#0d1317", "tc": "#3FB950", "border": "#3FB950"},
    "git": {"label": "Git", "color": "#F05032", "dark": "#7a2819", "darker": "#581e12", "tc": "#fff"},
    "neo4j": {"label": "Neo4j", "color": "#6E5494", "dark": "#382978", "darker": "#281e55", "tc": "#fff"},
    "amazonaws": {"label": "AWS", "color": "#232F3E", "dark": "#804d00", "darker": "#5d3800", "tc": "#FF9900", "border": "#FF9900"},
    "langchain": {"label": "LangChain", "color": "#1C1C1C", "dark": "#1a4f1a", "darker": "#133a13", "tc": "#3FB950", "border": "#3FB950"},
}

ROWS = [
    ["python","openjdk","c","javascript","typescript","postgresql"],  # Using postgresql slug for SQL row
    ["pytorch","tensorflow","fastapi","numpy","pandas","scikitlearn"],
    ["nodedotjs","express","mongodb","postgresql","redis","docker"],
    ["react","nginx","git","neo4j","amazonaws","langchain"],
]
ROW_LABELS = ["# LANGUAGES","# ML / AI","# BACKEND","# FRONTEND / TOOLS"]
# Fix: row 0 SQL should use postgresql icon but display "SQL"
ROW0_LABELS = {"postgresql": "SQL"}

def fetch_icon_path(slug):
    url = f"https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/{slug}.svg"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            svg = r.read().decode()
        m = re.search(r'<path\s+d="([^"]+)"', svg)
        return m.group(1) if m else None
    except Exception as e:
        print(f"  WARN: could not fetch {slug}: {e}", file=sys.stderr)
        return None

print("Fetching Simple Icons paths...", file=sys.stderr)
icon_paths = {}
seen = set()
for row in ROWS:
    for slug in row:
        if slug not in seen:
            seen.add(slug)
            path = fetch_icon_path(slug)
            icon_paths[slug] = path
            status = "✓" if path else "✗"
            print(f"  {status} {slug}", file=sys.stderr)

# Key layout constants
KW, KH = 110, 60       # key width, height
KGX, KGY = 126, 90    # key x gap, y gap  
START_X, START_Y = 68, 118
EXT_R = 10             # right extrusion width
EXT_B = 7              # bottom extrusion height
ICON_SIZE = 20         # icon render size in key

def key_svg(slug, row, col, label_override=None):
    info = ICONS.get(slug, {})
    label = label_override or info.get("label", slug)
    color = info.get("color", "#444")
    dark  = info.get("dark",  "#222")
    darker= info.get("darker","#111")
    tc    = info.get("tc",    "#fff")
    border= info.get("border", None)
    anim_cls = f"k{row*6+col}"

    bx = START_X + col * KGX
    by = START_Y + row * KGY

    # Determine if icon path exists
    path_d = icon_paths.get(slug)
    # Icon transform: simple-icons paths use 24x24 viewBox, we want ~20px
    icon_scale = ICON_SIZE / 24
    # Center the icon in top 2/3 of key
    icon_cx = bx + KW/2
    icon_cy = by + KH * 0.4
    # Translate so the 24x24 icon is centered at icon_cx, icon_cy
    tx = icon_cx - 12 * icon_scale
    ty = icon_cy - 12 * icon_scale

    border_color = border or color
    # lighter border
    import colorsys
    def lighten(hex_color, amount=0.3):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            return "#888"
        r,g,b = int(hex_color[:2],16), int(hex_color[2:4],16), int(hex_color[4:],16)
        h,l,s = colorsys.rgb_to_hls(r/255,g/255,b/255)
        l = min(1.0, l + amount)
        r2,g2,b2 = colorsys.hls_to_rgb(h,l,s)
        return f"#{int(r2*255):02x}{int(g2*255):02x}{int(b2*255):02x}"

    stroke = lighten(color, 0.25)
    if border:
        stroke = border

    parts = []
    parts.append(f'<g class="{anim_cls}" filter="url(#ks)">')
    # Right face
    parts.append(f'  <polygon points="{bx+KW},{by} {bx+KW+EXT_R},{by+EXT_R} {bx+KW+EXT_R},{by+KH+EXT_R} {bx+KW},{by+KH}" fill="{dark}"/>')
    # Bottom face
    parts.append(f'  <polygon points="{bx},{by+KH} {bx+KW},{by+KH} {bx+KW+EXT_R},{by+KH+EXT_R} {bx+EXT_R},{by+KH+EXT_R}" fill="{darker}"/>')
    # Top face
    parts.append(f'  <rect x="{bx}" y="{by}" width="{KW}" height="{KH}" rx="9" fill="{color}" stroke="{stroke}" stroke-width="0.9"/>')

    # Icon
    if path_d:
        icon_color = tc if tc != color else "#fff"
        parts.append(f'  <g transform="translate({tx:.1f},{ty:.1f}) scale({icon_scale:.4f})">')
        parts.append(f'    <path d="{path_d}" fill="{icon_color}"/>')
        parts.append(f'  </g>')
    else:
        # Fallback: big initials
        initials = label[:2].upper()
        parts.append(f'  <text x="{bx+KW/2}" y="{icon_cy+6}" class="lbl" font-size="16" font-weight="900" fill="{tc}" text-anchor="middle" opacity="0.9">{initials}</text>')

    # Label at bottom of key
    label_y = by + KH - 8
    fs = "8" if len(label) > 8 else "9"
    parts.append(f'  <text x="{bx+KW/2}" y="{label_y}" class="lbl" font-size="{fs}" font-weight="700" fill="{tc}" text-anchor="middle" opacity="0.95">{label}</text>')
    parts.append('</g>')
    return "\n".join(parts)

# Build full SVG
SVG_H = 500
lines = []
lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{SVG_H}" viewBox="0 0 860 {SVG_H}">
  <defs>
    <style>
      @keyframes keyPop {{
        from {{ opacity: 0; transform: translateY(-10px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
      }}
      {" ".join(f".k{i} {{ animation: keyPop 0.4s ease both; animation-delay: {0.05+i*0.055:.2f}s; }}" for i in range(24))}
      .lbl {{ font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace; }}
    </style>
    <filter id="ks" x="-30%" y="-20%" width="170%" height="180%">
      <feDropShadow dx="3" dy="7" stdDeviation="5" flood-color="#000" flood-opacity="0.6"/>
    </filter>
    <linearGradient id="boardTop" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1C2128"/>
      <stop offset="100%" stop-color="#161B22"/>
    </linearGradient>
    <radialGradient id="boardAO" cx="50%" cy="50%" r="55%">
      <stop offset="60%" stop-color="transparent"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.3"/>
    </radialGradient>
  </defs>

  <!-- Terminal chrome -->
  <rect width="860" height="{SVG_H}" rx="10" fill="#0D1117"/>
  <rect width="858" height="{SVG_H-2}" x="1" y="1" rx="10" fill="none" stroke="#30363D" stroke-width="1.2"/>
  <circle cx="22" cy="20" r="5.5" fill="#FF5F56"/>
  <circle cx="39" cy="20" r="5.5" fill="#FEBC2E"/>
  <circle cx="56" cy="20" r="5.5" fill="#28C840"/>
  <text x="430" y="24" class="lbl" font-size="12" fill="#8B949E" text-anchor="middle">keyboard.layout — tech-stack</text>
  <line x1="1" y1="35" x2="859" y2="35" stroke="#30363D" stroke-width="1"/>

  <!-- Board chassis -->
  <rect x="38" y="50" width="784" height="400" rx="12" fill="url(#boardTop)" stroke="#30363D" stroke-width="1.5"/>
  <polygon points="822,50 834,61 834,450 822,450" fill="#0D1117" opacity="0.85"/>
  <polygon points="38,450 822,450 834,461 50,461" fill="#0D1117" opacity="0.7"/>
  <rect x="38" y="50" width="784" height="400" rx="12" fill="url(#boardAO)"/>
  <rect x="46" y="58" width="768" height="385" rx="10" fill="none" stroke="#21262D" stroke-width="1"/>
''')

# Row labels
label_ys = [112, 202, 292, 382]
for i, (lbl, ly) in enumerate(zip(ROW_LABELS, label_ys)):
    lines.append(f'  <text x="56" y="{ly}" class="lbl" font-size="8.5" font-weight="700" fill="#3FB950" opacity="0.85" letter-spacing="1.5">{lbl}</text>')

# Keys
for ri, row in enumerate(ROWS):
    for ci, slug in enumerate(row):
        label_ov = None
        if ri == 0 and slug == "postgresql":
            label_ov = "SQL"
        lines.append(key_svg(slug, ri, ci, label_ov))

# Footer
lines.append(f'''
  <text x="56" y="478" class="lbl" font-size="10" fill="#3FB950" opacity="0.7">FierceAdder@github:~$</text>
  <text x="196" y="478" class="lbl" font-size="10" fill="#8B949E" opacity="0.6"> 24 tools loaded ·</text>
  <text x="306" y="478" class="lbl" font-size="10" fill="#58A6FF" opacity="0.6"> python · ml · backend · frontend</text>
  <rect x="490" y="468" width="8" height="12" rx="1" fill="#3FB950" opacity="0.7">
    <animate attributeName="opacity" values="0.7;0;0.7" dur="1.2s" repeatCount="indefinite"/>
  </rect>
</svg>''')

print("\n".join(lines))
