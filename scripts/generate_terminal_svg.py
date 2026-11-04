"""
generate_terminal_svg.py
Generates an expanded, high-density neofetch-inspired terminal system card SVG
for Ashmit's GitHub profile README.

Usage:
  python generate_terminal_svg.py --mode dark
  python generate_terminal_svg.py --mode light
"""

import os
import sys
import argparse
import json
import requests
from datetime import datetime, timezone

# ─── Configuration ────────────────────────────────────────────────────────────
GH_USERNAME = os.environ.get("GH_USERNAME", "FierceAdder")
GH_TOKEN    = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

HEADERS = {"User-Agent": "terminal-svg-generator/2.0"}
if GH_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GH_TOKEN}"

# ─── Color Themes ─────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg":          "#0D1117",
        "border":      "#30363D",
        "prompt":      "#58A6FF",   # cyan-blue
        "key":         "#58A6FF",   # blue labels
        "value":       "#C9D1D9",   # light gray values
        "highlight":   "#3FB950",   # green accent
        "gold":        "#F1E05A",   # yellow/gold accent
        "purple":      "#BC8CFF",   # purple accent
        "orange":      "#FFA657",   # orange accent
        "separator":   "#30363D",
        "cursor":      "#58A6FF",
        "text":        "#8B949E",
    },
    "light": {
        "bg":          "#FFFFFF",
        "border":      "#D0D7DE",
        "prompt":      "#0969DA",
        "key":         "#0969DA",
        "value":       "#1F2328",
        "highlight":   "#1A7F37",
        "gold":        "#9A6700",
        "purple":      "#8250DF",
        "orange":      "#BC4C00",
        "separator":   "#D0D7DE",
        "cursor":      "#0969DA",
        "text":        "#57606A",
    },
}

def gh_rest(path):
    url = f"https://api.github.com{path}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()

def gh_graphql(query, variables=None):
    url = "https://api.github.com/graphql"
    payload = {"query": query, "variables": variables or {}}
    r = requests.post(url, json=payload, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

def fetch_stats():
    user = {}
    try:
        user = gh_rest(f"/users/{GH_USERNAME}")
    except Exception as e:
        print(f"[terminal-svg] Notice: User REST call failed ({e}). Using defaults.")

    commits = 0
    total_contribs = 0
    prs = 0
    issues = 0
    total_stars = 0

    if GH_TOKEN:
        try:
            gql = """
            query($login: String!) {
              user(login: $login) {
                contributionsCollection {
                  contributionCalendar {
                    totalContributions
                  }
                  totalCommitContributions
                  totalPullRequestContributions
                  totalIssueContributions
                }
                repositories(first: 100, ownerAffiliations: OWNER) {
                  totalCount
                  nodes { stargazerCount }
                }
              }
            }
            """
            gql_data = gh_graphql(gql, {"login": GH_USERNAME})
            gql_user = gql_data.get("data", {}).get("user", {})
            cc = gql_user.get("contributionsCollection", {})
            repos_data = gql_user.get("repositories", {})

            calendar = cc.get("contributionCalendar", {})
            total_contribs = calendar.get("totalContributions", 0)
            commits = cc.get("totalCommitContributions", 0)
            prs = cc.get("totalPullRequestContributions", 0)
            issues = cc.get("totalIssueContributions", 0)
            total_stars = sum(r.get("stargazerCount", 0) for r in repos_data.get("nodes", []))
        except Exception as e:
            print(f"[terminal-svg] Notice: GraphQL query failed ({e}), falling back to REST.")

    if total_stars == 0:
        try:
            repos = gh_rest(f"/users/{GH_USERNAME}/repos?per_page=100")
            total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        except Exception:
            pass

    return {
        "name":         user.get("name") or "Ashmit Kumar Verma",
        "role":         "AI / ML Systems Engineer",
        "education":    "B.E. CSE (AI/ML) · MSRIT Bengaluru",
        "cgpa":         "9.46 / 10.0",
        "internship":   "Ex-AI Engineer Intern @ Rtifact",
        "research":     "MESA Transformer (2nd @ Scaler Rethesis)",
        "leetcode":     "Knight 🏅 (Rating 2073 · Top 1% Worldwide)",
        "codeforces":   "Pupil (Rating 1385)",
        "stack":        "PyTorch · FastAPI · React · Neo4j · Docker",
        "focus":        "Agentic AI · Knowledge Graphs · Code Intelligence",
        "followers":    user.get("followers", 7),
        "following":    user.get("following", 7),
        "public_repos": user.get("public_repos", 22),
        "commits":      total_contribs if total_contribs > 0 else (commits if commits > 0 else 340),
        "prs":          prs,
        "issues":       issues,
        "stars":        total_stars if total_stars > 0 else 4,
        "uptime":       f"since {user.get('created_at', '2024-01-19')[:10]}",
        "updated":      datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }

FONT_MONO = "JetBrains Mono, Fira Code, Consolas, monospace"

def escape(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build_svg(stats: dict, mode: str) -> str:
    c = THEMES[mode]
    username = escape(GH_USERNAME)

    # Rich Neofetch item structure (Key, Value, Color category)
    items = [
        ("User",       f"Ashmit Kumar Verma (@{username})",      "highlight"),
        ("Role",       stats["role"],                           "value"),
        ("Education",  f"{stats['education']} "),
        ("Experience", stats["internship"],                     "value"),
        ("Research",   stats["research"],                       "purple"),
        ("Interests",  stats["focus"],                          "highlight"),
        ("---",        "",                                      "sep"),
        ("Repos",      f"{stats['public_repos']} public repos",  "value"),
        ("Commits",    f"{stats['commits']} total contributions","value"),
        ("Stars",      f"⭐ {stats['stars']} stars",      "gold"),
        ("System",     f"GitHub Profile v3.0 · Uptime: {stats['uptime']}", "text"),
    ]

    LINE_H = 22
    PAD_X = 26
    W = 860
    CONTENT_Y_START = 82
    
    # Calculate box height
    valid_lines_count = sum(1 for k, v, t in items if k != "---") + sum(1 for k, v, t in items if k == "---") * 0.5
    BOX_H = int(CONTENT_Y_START + len(items) * LINE_H + 46)

    lines_svg = ""
    curr_y = CONTENT_Y_START

    for i, (key, val, col_type) in enumerate(items):
        delay = 0.04 + i * 0.04

        if key == "---":
            curr_y += 10
            lines_svg += f"""
  <line x1="{PAD_X + 10}" y1="{curr_y}" x2="{W - PAD_X - 10}" y2="{curr_y}" stroke="{c['separator']}" stroke-dasharray="3 3" opacity="0.6" />"""
            curr_y += 12
            continue

        fill_color = c.get(col_type, c["value"])
        weight = "600" if col_type in ("highlight", "gold", "purple", "prompt") else "400"

        # Key column
        lines_svg += f"""
  <text x="{PAD_X + 16}" y="{curr_y}" font-family="{FONT_MONO}" font-size="12.5" font-weight="600" fill="{c['key']}" opacity="0" style="animation: fadeIn 0.35s ease {delay:.2f}s forwards;">
    {escape(key)}
  </text>
  <text x="{PAD_X + 125}" y="{curr_y}" font-family="{FONT_MONO}" font-size="12.5" fill="{c['separator']}" opacity="0" style="animation: fadeIn 0.35s ease {delay:.2f}s forwards;">
    ~
  </text>
  <text x="{PAD_X + 145}" y="{curr_y}" font-family="{FONT_MONO}" font-size="12.5" font-weight="{weight}" fill="{fill_color}" opacity="0" style="animation: fadeIn 0.35s ease {delay + 0.02:.2f}s forwards;">
    {escape(val)}
  </text>"""
        curr_y += LINE_H

    # Bottom terminal color palette badges
    palette_colors = ["#FF7B72", "#FFA657", "#F1E05A", "#3FB950", "#58A6FF", "#BC8CFF", "#F778BA", "#C9D1D9"]
    palette_svg = ""
    for idx, col in enumerate(palette_colors):
        px = PAD_X + 16 + idx * 22
        py = BOX_H - 30
        palette_svg += f'<rect x="{px}" y="{py}" width="16" height="13" rx="3" fill="{col}" />'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{BOX_H}" viewBox="0 0 {W} {BOX_H}">
  <defs>
    <style>
      @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(-3px); }}
        to   {{ opacity: 1; transform: translateY(0);    }}
      }}
      @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50%       {{ opacity: 0; }}
      }}
    </style>
  </defs>

  <!-- Terminal Window Background -->
  <rect width="{W}" height="{BOX_H}" rx="10" fill="{c['bg']}" />
  <rect width="{W - 2}" height="{BOX_H - 2}" x="1" y="1" rx="10" fill="none" stroke="{c['border']}" stroke-width="1.2" />

  <!-- Terminal Window Chrome -->
  <circle cx="22" cy="20" r="5.5" fill="#FF5F56" />
  <circle cx="39" cy="20" r="5.5" fill="#FEBC2E" />
  <circle cx="56" cy="20" r="5.5" fill="#28C840" />

  <!-- Title bar -->
  <text x="{W // 2}" y="24" font-family="{FONT_MONO}" font-size="12" fill="{c['text']}" text-anchor="middle">
    ashmit@portfolio — bash (neofetch) — 110×28
  </text>
  <line x1="1" y1="35" x2="{W - 1}" y2="35" stroke="{c['border']}" stroke-width="1" />

  <!-- Prompt command -->
  <text x="{PAD_X + 16}" y="58" font-family="{FONT_MONO}" font-size="13" font-weight="600" fill="{c['prompt']}">
    {username}@github
  </text>
  <text x="{PAD_X + 16 + len(username) * 8 + 62}" y="58" font-family="{FONT_MONO}" font-size="13" fill="{c['text']}">
    :~$
  </text>
  <text x="{PAD_X + 16 + len(username) * 8 + 98}" y="58" font-family="{FONT_MONO}" font-size="13" font-weight="600" fill="{c['highlight']}">
    neofetch --full
  </text>

  <!-- Output Lines -->
  {lines_svg}

  <!-- Palette -->
  {palette_svg}

  <!-- Blinking Cursor -->
  <rect x="{PAD_X + 16 + len(palette_colors) * 22 + 8}" y="{BOX_H - 30}" width="8" height="13" rx="1" fill="{c['cursor']}" style="animation: blink 1s step-end infinite;" />
</svg>"""
    return svg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["dark", "light"], default="dark")
    args = parser.parse_args()

    print(f"[terminal-svg] Fetching GitHub stats for @{GH_USERNAME}...")
    stats = fetch_stats()
    print(f"[terminal-svg] Stats loaded successfully.")

    svg = build_svg(stats, args.mode)
    out_path = f"assets/{args.mode}_mode.svg"
    os.makedirs("assets", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[terminal-svg] Written → {out_path}")

if __name__ == "__main__":
    main()
