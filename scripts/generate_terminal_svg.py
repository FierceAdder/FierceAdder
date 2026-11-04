"""
generate_terminal_svg.py
Generates a neofetch-inspired terminal stats card SVG for GitHub profile README.

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
GH_TOKEN    = os.environ.get("GH_TOKEN") or os.environ.get("GH_TOKEN")

HEADERS = {"Authorization": f"Bearer {GH_TOKEN}"} if GH_TOKEN else {}

# ─── Color Themes ─────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg":          "#0D1117",
        "border":      "#30363D",
        "prompt":      "#58A6FF",   # blue  — user@host
        "key":         "#58A6FF",   # blue  — left column keys
        "value":       "#C9D1D9",   # white — right column values
        "highlight":   "#3FB950",   # green — OS / special lines
        "separator":   "#21262D",
        "cursor":      "#58A6FF",
        "text":        "#C9D1D9",
    },
    "light": {
        "bg":          "#FFFFFF",
        "border":      "#D0D7DE",
        "prompt":      "#0969DA",
        "key":         "#0969DA",
        "value":       "#1F2328",
        "highlight":   "#1A7F37",
        "separator":   "#D0D7DE",
        "cursor":      "#0969DA",
        "text":        "#1F2328",
    },
}

# ─── GitHub REST / GraphQL helpers ────────────────────────────────────────────

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
    user = gh_rest(f"/users/{GH_USERNAME}")

    # Commit count via GraphQL
    gql = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
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

    total_stars = sum(r["stargazerCount"] for r in repos_data.get("nodes", []))

    return {
        "name":       user.get("name") or GH_USERNAME,
        "followers":  user.get("followers", 0),
        "following":  user.get("following", 0),
        "public_repos": user.get("public_repos", 0),
        "commits":    cc.get("totalCommitContributions", 0),
        "prs":        cc.get("totalPullRequestContributions", 0),
        "issues":     cc.get("totalIssueContributions", 0),
        "stars":      total_stars,
        "created":    user.get("created_at", "")[:10],
        "updated":    datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }


# ─── SVG Builder ──────────────────────────────────────────────────────────────

FONT_MONO = "JetBrains Mono, Fira Code, Consolas, monospace"

def escape(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(stats: dict, mode: str) -> str:
    c = THEMES[mode]

    name     = escape(stats["name"])
    username = escape(GH_USERNAME)
    today    = stats["updated"]

    # Lines displayed in the info panel
    info_lines = [
        ("OS",         "GitHub Profile v3.0"),
        ("Host",       f"github.com/{username}"),
        ("Uptime",     f"since {stats['created']}"),
        ("",           ""),
        ("Repos",      str(stats["public_repos"])),
        ("Commits",    str(stats["commits"]) + "  (this year)"),
        ("PRs",        str(stats["prs"])),
        ("Issues",     str(stats["issues"])),
        ("",           ""),
        ("Stars",      "⭐ " + str(stats["stars"])),
        ("Followers",  str(stats["followers"])),
        ("Following",  str(stats["following"])),
        ("",           ""),
        ("Updated",    today),
    ]

    LINE_H  = 22
    PAD_X   = 24
    PAD_Y   = 24
    W       = 720
    CONTENT_Y_START = 90          # below the prompt line
    BOX_H   = CONTENT_Y_START + len(info_lines) * LINE_H + 70

    lines_svg = ""
    for i, (key, val) in enumerate(info_lines):
        y = CONTENT_Y_START + i * LINE_H
        # stagger animation delay
        delay = 0.05 + i * 0.06

        if key == "":
            continue

        # key column
        lines_svg += f"""
  <text x="{PAD_X + 16}" y="{y}"
        font-family="{FONT_MONO}" font-size="13" fill="{c['key']}"
        opacity="0"
        style="animation: fadeIn 0.4s ease {delay:.2f}s forwards;">
    {escape(key)}
  </text>"""

        # separator
        lines_svg += f"""
  <text x="{PAD_X + 110}" y="{y}"
        font-family="{FONT_MONO}" font-size="13" fill="{c['separator']}"
        opacity="0"
        style="animation: fadeIn 0.4s ease {delay:.2f}s forwards;">
    ~
  </text>"""

        # value column
        fill = c["highlight"] if key in ("OS", "Host") else c["value"]
        lines_svg += f"""
  <text x="{PAD_X + 130}" y="{y}"
        font-family="{FONT_MONO}" font-size="13" fill="{fill}"
        opacity="0"
        style="animation: fadeIn 0.4s ease {delay + 0.03:.2f}s forwards;">
    {escape(val)}
  </text>"""

    # Color palette squares at the bottom
    palette_colors = ["#FF7B72","#FFA657","#E3B341","#3FB950","#58A6FF","#A371F7","#F778BA","#C9D1D9"]
    palette_svg = ""
    for idx, col in enumerate(palette_colors):
        px = PAD_X + 16 + idx * 22
        py = BOX_H - 44
        palette_svg += f'<rect x="{px}" y="{py}" width="16" height="16" rx="3" fill="{col}" />'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="{W}" height="{BOX_H}"
     viewBox="0 0 {W} {BOX_H}">

  <defs>
    <style>
      @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateX(-6px); }}
        to   {{ opacity: 1; transform: translateX(0);   }}
      }}
      @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50%       {{ opacity: 0; }}
      }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="{W}" height="{BOX_H}" rx="10" fill="{c['bg']}" />

  <!-- Border -->
  <rect width="{W - 2}" height="{BOX_H - 2}" x="1" y="1"
        rx="10" fill="none" stroke="{c['border']}" stroke-width="1.5" />

  <!-- Window chrome dots -->
  <circle cx="20" cy="22" r="6" fill="#FF5F57" />
  <circle cx="38" cy="22" r="6" fill="#FEBC2E" />
  <circle cx="56" cy="22" r="6" fill="#28C840" />

  <!-- Title bar text -->
  <text x="{W // 2}" y="27"
        font-family="{FONT_MONO}" font-size="13" fill="{c['text']}" text-anchor="middle">
    bash — {username}@github — 80×24
  </text>

  <!-- Horizontal rule under title bar -->
  <line x1="1" y1="38" x2="{W - 1}" y2="38"
        stroke="{c['border']}" stroke-width="1" />

  <!-- Prompt line -->
  <text x="{PAD_X}" y="62"
        font-family="{FONT_MONO}" font-size="14" fill="{c['prompt']}">
    {username}@github
  </text>
  <text x="{PAD_X + len(username) * 8 + 72}" y="62"
        font-family="{FONT_MONO}" font-size="14" fill="{c['text']}">
    :~$
  </text>
  <text x="{PAD_X + len(username) * 8 + 110}" y="62"
        font-family="{FONT_MONO}" font-size="14" fill="{c['highlight']}">
    neofetch
  </text>

  <!-- ASCII art logo placeholder (left column) -->
  <text x="{W - 230}" y="100"
        font-family="{FONT_MONO}" font-size="11" fill="{c['highlight']}"
        opacity="0.7"
        style="animation: fadeIn 0.5s ease 0.3s forwards;">
    ╔═══════════╗
  </text>
  <text x="{W - 230}" y="115"
        font-family="{FONT_MONO}" font-size="11" fill="{c['highlight']}"
        opacity="0"
        style="animation: fadeIn 0.5s ease 0.4s forwards;">
    ║   ۩ AKV  ║
  </text>
  <text x="{W - 230}" y="130"
        font-family="{FONT_MONO}" font-size="11" fill="{c['highlight']}"
        opacity="0"
        style="animation: fadeIn 0.5s ease 0.5s forwards;">
    ╚═══════════╝
  </text>

  <!-- Info lines -->
  {lines_svg}

  <!-- Color palette -->
  {palette_svg}

  <!-- Blinking cursor -->
  <rect x="{PAD_X + 16}" y="{BOX_H - 24}" width="8" height="14" rx="1"
        fill="{c['cursor']}"
        style="animation: blink 1s step-end infinite;" />

</svg>"""
    return svg


# ─── Entry point ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["dark", "light"], default="dark")
    args = parser.parse_args()

    print(f"[terminal-svg] Fetching GitHub stats for @{GH_USERNAME} …")
    try:
        stats = fetch_stats()
    except Exception as e:
        print(f"[terminal-svg] Warning: could not fetch stats ({e}). Using placeholders.")
        stats = {
            "name": "Ashmit Kumar Verma",
            "followers": 0, "following": 0, "public_repos": 0,
            "commits": 0, "prs": 0, "issues": 0, "stars": 0,
            "created": "2024-01-01", "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        }

    svg = build_svg(stats, args.mode)
    out_path = f"assets/{args.mode}_mode.svg"
    os.makedirs("assets", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[terminal-svg] Written → {out_path}")


if __name__ == "__main__":
    main()

