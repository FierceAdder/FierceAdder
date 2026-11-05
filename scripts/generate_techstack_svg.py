#!/usr/bin/env python3
"""Generate true-proportioned 10-9-7 mechanical keyboard tech stack SVG with enhanced 3D depth."""
import urllib.request, json, re, sys, os

ROWS = [
    # Row 1 (10 keys - Languages & Core AI/ML)
    [
        {"slug": "python", "label": "Python", "color": "#3776AB", "dark": "#183957", "darker": "#0f2538", "tc": "#ffffff"},
        {"slug": "openjdk", "label": "Java", "color": "#ED8B00", "dark": "#824c00", "darker": "#4f2e00", "tc": "#ffffff"},
        {"slug": "c", "label": "C", "color": "#5b6f8a", "dark": "#313c4c", "darker": "#1d242e", "tc": "#ffffff"},
        {"slug": "javascript", "label": "JavaScript", "color": "#F7DF1E", "dark": "#8a7b0c", "darker": "#524905", "tc": "#0D1117"},
        {"slug": "typescript", "label": "TypeScript", "color": "#3178C6", "dark": "#194270", "darker": "#0f2947", "tc": "#ffffff"},
        {"slug": "postgresql", "label": "SQL", "color": "#336791", "dark": "#19364f", "darker": "#0f2130", "tc": "#ffffff"},
        {"slug": "pytorch", "label": "PyTorch", "color": "#EE4C2C", "dark": "#872713", "darker": "#54170a", "tc": "#ffffff"},
        {"slug": "tensorflow", "label": "TensorFlow", "color": "#FF6F00", "dark": "#8a3c00", "darker": "#522300", "tc": "#ffffff"},
        {"slug": "scikitlearn", "label": "Scikit", "color": "#F7931E", "dark": "#8c510d", "darker": "#543006", "tc": "#0D1117"},
        {"slug": "fastapi", "label": "FastAPI", "color": "#009688", "dark": "#004d46", "darker": "#00302b", "tc": "#ffffff"},
    ],
    # Row 2 (9 keys - Data, AI, & Backend)
    [
        {"slug": "numpy", "label": "NumPy", "color": "#013243", "dark": "#00151d", "darker": "#000a0e", "tc": "#4DABCF", "border": "#4DABCF"},
        {"slug": "pandas", "label": "Pandas", "color": "#150458", "dark": "#080124", "darker": "#040012", "tc": "#ffffff", "border": "#564a8a"},
        {"slug": "langchain", "label": "LangChain", "color": "#1C1C1C", "dark": "#0b0b0b", "darker": "#040404", "tc": "#3FB950", "border": "#3FB950"},
        {"slug": "nodedotjs", "label": "Node.js", "color": "#339933", "dark": "#194f19", "darker": "#0e330e", "tc": "#ffffff"},
        {"slug": "express", "label": "Express", "color": "#202020", "dark": "#0e0e0e", "darker": "#050505", "tc": "#ffffff", "border": "#6f6f60"},
        {"slug": "postgresql", "label": "Postgres", "color": "#4169E1", "dark": "#1e357d", "darker": "#11204d", "tc": "#ffffff"},
        {"slug": "mongodb", "label": "MongoDB", "color": "#47A248", "dark": "#235424", "darker": "#143315", "tc": "#ffffff"},
        {"slug": "redis", "label": "Redis", "color": "#DC382D", "dark": "#751b14", "darker": "#47100b", "tc": "#ffffff"},
        {"slug": "neo4j", "label": "Neo4j", "color": "#6E5494", "dark": "#392a4f", "darker": "#211730", "tc": "#ffffff"},
    ],
    # Row 3 (7 keys - Infra, DevOps, Cloud & Tools)
    [
        {"slug": "docker", "label": "Docker", "color": "#2496ED", "dark": "#104f80", "darker": "#092f4d", "tc": "#ffffff"},
        {"slug": "react", "label": "React", "color": "#20232A", "dark": "#0e1012", "darker": "#050607", "tc": "#61DAFB", "border": "#61DAFB"},
        {"slug": "nginx", "label": "Nginx", "color": "#1F2428", "dark": "#0d1012", "darker": "#050607", "tc": "#3FB950", "border": "#3FB950"},
        {"slug": "aws", "label": "AWS", "color": "#232F3E", "dark": "#0f161f", "darker": "#080c12", "tc": "#FF9900", "border": "#FF9900"},
        {"slug": "git", "label": "Git", "color": "#F05032", "dark": "#7d2616", "darker": "#4a160b", "tc": "#ffffff"},
        {"slug": "linux", "label": "Linux", "color": "#FCC624", "dark": "#8a6b0c", "darker": "#4f3c05", "tc": "#0D1117"},
        {"slug": "postman", "label": "Postman", "color": "#FF6C37", "dark": "#8a3514", "darker": "#541f0a", "tc": "#ffffff"},
    ]
]

def fetch_simple_icon(slug):
    url = f"https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/{slug}.svg"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            svg = r.read().decode()
        m = re.search(r'<path\s+d="([^"]+)"', svg)
        return m.group(1) if m else None
    except Exception as e:
        print(f"WARN: Failed {slug}: {e}", file=sys.stderr)
        return None

def fetch_aws_icon():
    url = "https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original.svg"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            svg = r.read().decode()
        paths = re.findall(r'<path[^>]*fill="([^"]+)"[^>]*d="([^"]+)"', svg)
        return paths
    except Exception as e:
        print(f"WARN: Failed aws: {e}", file=sys.stderr)
        return []

print("Fetching icons...", file=sys.stderr)
cached_icons = {}
for row in ROWS:
    for item in row:
        s = item["slug"]
        if s not in cached_icons:
            if s == "aws":
                cached_icons[s] = fetch_aws_icon()
            else:
                cached_icons[s] = fetch_simple_icon(s)
            print(f"  {'✓' if cached_icons[s] else '✗'} {s}", file=sys.stderr)

# Keyboard Layout Specs with deeper 3D mechanical relief
KW = 66           # Key width
KH = 60           # Key height
EXT_R = 11        # Deep 3D right side extrusion (was 7)
EXT_B = 9         # Deep 3D bottom side extrusion (was 6)
ICON_BOX = 20     # Icon display size
ROW_PITCH_Y = 85  # Y step per row
Y_START = 80      # Y offset for row 1
CANVAS_W = 860
CANVAS_H = 400

ROW_STARTS = [52, 90, 166]

def render_key(item, rx, ry, idx):
    slug = item["slug"]
    label = item["label"]
    color = item["color"]
    dark = item["dark"]
    darker = item["darker"]
    tc = item["tc"]
    border = item.get("border", None)

    x = rx
    y = ry
    stroke_col = border if border else color

    out = []
    out.append(f'  <!-- Key {label} -->')
    out.append(f'  <g class="k{idx}" filter="url(#ks)">')
    # Right face (isometric side depth)
    out.append(f'    <polygon points="{x+KW},{y} {x+KW+EXT_R},{y+EXT_R} {x+KW+EXT_R},{y+KH+EXT_R} {x+KW},{y+KH}" fill="{dark}"/>')
    # Right face inner shading line
    out.append(f'    <line x1="{x+KW}" y1="{y}" x2="{x+KW+EXT_R}" y2="{y+EXT_R}" stroke="rgba(255,255,255,0.08)" stroke-width="0.8"/>')
    # Bottom face (ground contact shadow bevel)
    out.append(f'    <polygon points="{x},{y+KH} {x+KW},{y+KH} {x+KW+EXT_R},{y+KH+EXT_R} {x+EXT_R},{y+KH+EXT_R}" fill="{darker}"/>')
    # Top face
    out.append(f'    <rect x="{x}" y="{y}" width="{KW}" height="{KH}" rx="8" fill="{color}" stroke="{stroke_col}" stroke-width="1.2"/>')
    # Top face subtle top-edge highlight (tactile keycap ridge)
    out.append(f'    <line x1="{x+6}" y1="{y+1.5}" x2="{x+KW-6}" y2="{y+1.5}" stroke="rgba(255,255,255,0.18)" stroke-width="1" stroke-linecap="round"/>')

    # Icon centering
    icon_cx = x + (KW / 2)
    icon_cy = y + 22

    icon_data = cached_icons.get(slug)
    if slug == "aws" and isinstance(icon_data, list) and len(icon_data) >= 2:
        scale = 22 / 128
        tx = icon_cx - (128 * scale / 2)
        ty = icon_cy - (128 * scale / 2)
        out.append(f'    <g transform="translate({tx:.2f},{ty:.2f}) scale({scale:.4f})">')
        out.append(f'      <path d="{icon_data[0][1]}" fill="#FFFFFF"/>')
        out.append(f'      <path d="{icon_data[1][1]}" fill="#FF9900"/>')
        out.append('    </g>')
    elif icon_data and isinstance(icon_data, str):
        scale = ICON_BOX / 24
        tx = icon_cx - 12 * scale
        ty = icon_cy - 12 * scale
        fill_col = tc if tc != color else "#FFFFFF"
        out.append(f'    <g transform="translate({tx:.2f},{ty:.2f}) scale({scale:.4f})">')
        out.append(f'      <path d="{icon_data}" fill="{fill_col}"/>')
        out.append('    </g>')
    else:
        initials = label[:2].upper()
        out.append(f'    <text x="{icon_cx}" y="{icon_cy+6}" class="lbl" font-size="14" font-weight="900" fill="{tc}" text-anchor="middle">{initials}</text>')

    lbl_y = y + KH - 9
    fs = "8" if len(label) > 7 else "8.5"
    out.append(f'    <text x="{icon_cx}" y="{lbl_y}" class="lbl" font-size="{fs}" font-weight="700" fill="{tc}" text-anchor="middle">{label}</text>')
    out.append('  </g>')
    return "\n".join(out)

# Build Complete SVG
lines = []
lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}">
  <defs>
    <style>
      @keyframes popIn {{
        from {{ opacity: 0; transform: translateY(-10px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
      }}
      {" ".join(f".k{i} {{ animation: popIn 0.35s ease both {0.035*i:.2f}s; }}" for i in range(26))}
      .lbl {{ font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace; }}

      /* Hover: mechanical key-press depress effect */
      [class^="k"] {{
        cursor: pointer;
        transition: transform 0.10s cubic-bezier(0.25, 0.46, 0.45, 0.94),
                    filter 0.10s ease;
      }}
      [class^="k"]:hover {{
        transform: translate(5px, 5px);
        filter: url(#ks-pressed) brightness(1.3);
      }}
    </style>
    <!-- Normal drop shadow for keycaps -->
    <filter id="ks" x="-25%" y="-20%" width="160%" height="170%">
      <feDropShadow dx="3" dy="9" stdDeviation="4.5" flood-color="#000000" flood-opacity="0.75"/>
    </filter>
    <!-- Pressed shadow (smaller, tighter - key is down) -->
    <filter id="ks-pressed" x="-25%" y="-20%" width="160%" height="170%">
      <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
    <linearGradient id="boardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#161B22"/>
      <stop offset="100%" stop-color="#0E1217"/>
    </linearGradient>
  </defs>

  <!-- Terminal Window Chrome -->
  <rect width="{CANVAS_W}" height="{CANVAS_H}" rx="10" fill="#0D1117"/>
  <rect width="{CANVAS_W-2}" height="{CANVAS_H-2}" x="1" y="1" rx="10" fill="none" stroke="#30363D" stroke-width="1.2"/>
  <circle cx="22" cy="20" r="5.5" fill="#FF5F56"/>
  <circle cx="39" cy="20" r="5.5" fill="#FEBC2E"/>
  <circle cx="56" cy="20" r="5.5" fill="#28C840"/>
  <text x="430" y="24" class="lbl" font-size="12" fill="#8B949E" text-anchor="middle">FierceAdder@github — ~/tech-stack</text>
  <line x1="1" y1="35" x2="{CANVAS_W-1}" y2="35" stroke="#30363D" stroke-width="1"/>

  <!-- Mechanical Keyboard Chassis / Plate -->
  <rect x="34" y="52" width="792" height="298" rx="12" fill="url(#boardGrad)" stroke="#30363D" stroke-width="1.5"/>
  <polygon points="826,52 835,61 835,357 826,350" fill="#080B0F"/>
  <polygon points="34,350 826,350 835,357 43,357" fill="#05070A"/>
  <rect x="42" y="60" width="776" height="282" rx="8" fill="none" stroke="#21262D" stroke-width="1"/>
''')

# Render all rows
key_idx = 0
for r_i, row in enumerate(ROWS):
    x_start = ROW_STARTS[r_i]
    y_pos = Y_START + r_i * ROW_PITCH_Y
    for c_i, item in enumerate(row):
        x_pos = x_start + c_i * 76
        lines.append(render_key(item, x_pos, y_pos, key_idx))
        key_idx += 1

# Footer info line
lines.append(f'''
  <!-- Footer prompt -->
  <text x="46" y="378" class="lbl" font-size="9.5" fill="#58A6FF" font-weight="600">FierceAdder@github</text>
  <text x="186" y="378" class="lbl" font-size="9.5" fill="#8B949E">:~$</text>
  <text x="210" y="378" class="lbl" font-size="9.5" fill="#3FB950">cat stack.conf</text>
  <text x="315" y="378" class="lbl" font-size="9.5" fill="#8B949E"># daily driver stack</text>
  <rect x="475" y="368" width="7" height="12" rx="1" fill="#3FB950" opacity="0.75">
    <animate attributeName="opacity" values="0.75;0;0.75" dur="1.1s" repeatCount="indefinite"/>
  </rect>
</svg>''')

content = "\n".join(lines)
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_path = os.path.join(repo_root, "assets", "techstack-3d-dark.svg")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Saved techstack-3d-dark.svg successfully to {out_path}!", file=sys.stderr)
