"""
generate_heatmap.py
Renders a terminal-style ASCII glyph contribution graph SVG (dark + light variants)
inspired by Avi Vashishta's terminal portfolio design.

Features:
- Prompt: user@github ~ $ ./contributions.sh
- ASCII glyph grid based on GitHub's native contributionLevel:
    Level 0 (NONE):            '.'
    Level 1 (FIRST_QUARTILE):  ':'
    Level 2 (SECOND_QUARTILE): '+'
    Level 3 (THIRD_QUARTILE):  '#'
    Level 4 (FOURTH_QUARTILE): '@'
- Summary bar: {total} contributions · {streak} day streak · best day {best}
- Staggered terminal typing / reveal animation using pure CSS keyframes
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

GH_USERNAME = os.environ.get("GH_USERNAME", "FierceAdder")
GH_TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {GH_TOKEN}"} if GH_TOKEN else {}

GLYPHS = {
    0: ".",
    1: ":",
    2: "+",
    3: "#",
    4: "@",
}

LEVEL_MAP = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}

# Terminal themes matching GitHub and Avi Vashishta's portfolio
THEMES = {
    "dark": {
        "bg": "#0D1117",
        "border": "#30363D",
        "prompt_user": "#58A6FF",
        "prompt_host": "#8B949E",
        "prompt_cmd": "#39D353",
        "stats_text": "#39D353",
        "colors": {
            0: "#30363D",  # dim dot
            1: "#0E4429",
            2: "#006D32",
            3: "#26A641",
            4: "#39D353",  # brightest neon green
        },
    },
    "light": {
        "bg": "#FFFFFF",
        "border": "#E1E4E8",
        "prompt_user": "#24292F",
        "prompt_host": "#57606A",
        "prompt_cmd": "#216E39",
        "stats_text": "#216E39",
        "colors": {
            0: "#D0D7DE",  # dim dot
            1: "#9BE9A8",
            2: "#40C463",
            3: "#30A14E",
            4: "#216E39",  # deep forest green
        },
    },
}

FONT_FAMILY = "JetBrains Mono, Fira Code, 'Courier New', Menlo, Monaco, monospace"


def fetch_contributions_graphql():
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=365)

    gql = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
                contributionLevel
              }
            }
          }
        }
      }
    }
    """
    variables = {
        "login": GH_USERNAME,
        "from": start.isoformat(),
        "to": end.isoformat(),
    }
    url = "https://api.github.com/graphql"
    payload = json.dumps({"query": gql, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={**HEADERS, "Content-Type": "application/json", "User-Agent": "terminal-heatmap/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode())

    if "errors" in data:
        raise RuntimeError(str(data["errors"]))

    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    total = cal["totalContributions"]
    weeks = cal["weeks"]

    days = []
    for w in weeks:
        for d in w["contributionDays"]:
            lvl = LEVEL_MAP.get(d["contributionLevel"], 0)
            cnt = d["contributionCount"]
            days.append((d["date"], cnt, lvl))

    return total, days


def fallback_contributions():
    import random
    random.seed(1337)
    today = datetime.now(timezone.utc).date()
    days = []
    total = 0
    for i in range(370, -1, -1):
        d = today - timedelta(days=i)
        is_weekday = d.weekday() < 5
        if is_weekday and random.random() > 0.25:
            cnt = random.choice([1, 2, 3, 5, 8, 12])
            lvl = min(4, max(1, cnt // 2))
        elif not is_weekday and random.random() > 0.6:
            cnt = random.choice([1, 2, 4])
            lvl = 1
        else:
            cnt = 0
            lvl = 0
        total += cnt
        days.append((str(d), cnt, lvl))
    return total, days


def compute_metrics(days):
    """Calculates total, longest/current streak, and best single day."""
    total = sum(d[1] for d in days)
    best_day = max((d[1] for d in days), default=0)

    # Calculate streaks
    longest_streak = 0
    current_streak = 0
    temp_streak = 0
    for date_str, cnt, _ in days:
        if cnt > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    # Current streak (from most recent day backwards)
    for date_str, cnt, _ in reversed(days):
        if cnt > 0:
            current_streak += 1
        else:
            break

    streak_to_report = current_streak if current_streak > 0 else longest_streak
    return total, streak_to_report, best_day


def build_terminal_svg(total, days, streak, best_day, mode="dark"):
    t = THEMES[mode]

    # Organize days into 53 columns (weeks), each 7 days
    if days:
        first_date = datetime.strptime(days[0][0], "%Y-%m-%d")
        pad_front = first_date.weekday()  # Monday = 0
        padded = [(None, 0, 0)] * pad_front + days
    else:
        padded = days

    weeks = []
    curr_week = []
    for item in padded:
        curr_week.append(item)
        if len(curr_week) == 7:
            weeks.append(curr_week)
            curr_week = []
    if curr_week:
        weeks.append(curr_week + [(None, 0, 0)] * (7 - len(curr_week)))

    # Terminal dimensions
    COL_SPACING = 15.5
    ROW_SPACING = 17
    START_X = 35
    START_Y = 85

    W = 890
    H = 265

    # Build glyphs
    glyph_nodes = []
    for c_idx, week in enumerate(weeks):
        x = START_X + c_idx * COL_SPACING
        for r_idx, (d_str, cnt, lvl) in enumerate(week):
            if d_str is None:
                continue
            y = START_Y + r_idx * ROW_SPACING
            char = GLYPHS.get(lvl, ".")
            color = t["colors"].get(lvl, t["colors"][0])
            delay = round(c_idx * 0.02 + r_idx * 0.005, 3)
            title = f"{d_str}: {cnt} contribution{'s' if cnt != 1 else ''}"
            weight = "700" if lvl >= 3 else "600" if lvl >= 2 else "400"
            font_size = "13" if char in ("#", "@") else "14"

            glyph_nodes.append(
                f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" '
                f'font-family="{FONT_FAMILY}" font-size="{font_size}" font-weight="{weight}" '
                f'text-anchor="middle" opacity="0" '
                f'style="animation: termReveal 0.2s ease {delay}s forwards;">'
                f'<title>{title}</title>{char}</text>'
            )

    glyphs_markup = "\n    ".join(glyph_nodes)

    user_str = GH_USERNAME
    formatted_total = f"{total:,}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <style>
      @keyframes termReveal {{
        0% {{ opacity: 0; transform: translateY(-2px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes blinkCursor {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
      }}
    </style>
  </defs>

  <!-- Terminal Window Background -->
  <rect width="{W}" height="{H}" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="1.2" />

  <!-- Prompt Command -->
  <g font-family="{FONT_FAMILY}" font-size="13">
    <text x="35" y="42" fill="{t['prompt_user']}" font-weight="600">{user_str}@github</text>
    <text x="{35 + len(user_str) * 8 + 65}" y="42" fill="{t['prompt_host']}">~ $</text>
    <text x="{35 + len(user_str) * 8 + 98}" y="42" fill="{t['prompt_cmd']}" font-weight="600">./contributions.sh</text>
    <rect x="{35 + len(user_str) * 8 + 250}" y="31" width="7" height="14" fill="{t['prompt_cmd']}" style="animation: blinkCursor 1s step-end infinite;" />
  </g>

  <!-- ASCII Glyphs Grid (. : + # @) -->
  <g>
    {glyphs_markup}
  </g>

  <!-- Terminal Bottom Status Bar -->
  <g font-family="{FONT_FAMILY}" font-size="12" fill="{t['stats_text']}" font-weight="500">
    <text x="35" y="{H - 30}">
      {formatted_total} contributions   ·   {streak} day streak   ·   best day {best_day}
    </text>
  </g>
</svg>"""
    return svg


def main():
    print(f"[terminal-heatmap] Fetching contributions for @{GH_USERNAME}...")
    try:
        total, days = fetch_contributions_graphql()
        print(f"[terminal-heatmap] Successfully fetched {len(days)} days from GitHub GraphQL API.")
    except Exception as e:
        print(f"[terminal-heatmap] GraphQL notice ({e}). Generating fallback data.")
        total, days = fallback_contributions()

    total, streak, best_day = compute_metrics(days)
    print(f"[terminal-heatmap] Metrics: {total} total, {streak} streak, best day {best_day}")

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(repo_root, "assets")
    os.makedirs(out_dir, exist_ok=True)
    for mode in ("dark", "light"):
        svg = build_terminal_svg(total, days, streak, best_day, mode=mode)
        out_path = os.path.join(out_dir, f"contrib-heatmap-{mode}.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[terminal-heatmap] Written → {out_path}")


if __name__ == "__main__":
    main()
