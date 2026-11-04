"""
generate_heatmap.py
Fetches your GitHub contribution data via GraphQL and renders a
terminal-style contribution heatmap SVG (dark + light variants).

Both SVGs use pure SVG + CSS @keyframes — no JS, works in GitHub READMEs.
"""

import os
import json
import math
import requests
from datetime import datetime, timezone, timedelta

GH_USERNAME = os.environ.get("GH_USERNAME", "ashmitv704")
GH_TOKEN    = os.environ.get("GH_TOKEN") or os.environ.get("GH_TOKEN")
HEADERS     = {"Authorization": f"Bearer {GH_TOKEN}"} if GH_TOKEN else {}

# ─── Color scales ────────────────────────────────────────────────────────────
DARK_SCALE  = ["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"]
LIGHT_SCALE = ["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"]

THEMES = {
    "dark": {
        "bg":     "#0D1117",
        "border": "#30363D",
        "text":   "#8B949E",
        "prompt": "#58A6FF",
        "scale":  DARK_SCALE,
    },
    "light": {
        "bg":     "#FFFFFF",
        "border": "#D0D7DE",
        "text":   "#57606A",
        "prompt": "#0969DA",
        "scale":  LIGHT_SCALE,
    },
}

MONTH_ABBR = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
DAY_ABBR   = ["Mon","","Wed","","Fri","",""]


# ─── Fetch contributions ─────────────────────────────────────────────────────

def fetch_contributions():
    """Returns list of (date_str, count) for the past 53 weeks."""
    # We fetch the last year
    end   = datetime.now(timezone.utc)
    start = end - timedelta(weeks=53)

    gql = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    variables = {
        "login": GH_USERNAME,
        "from":  start.isoformat(),
        "to":    end.isoformat(),
    }
    url = "https://api.github.com/graphql"
    r = requests.post(url, json={"query": gql, "variables": variables},
                      headers=HEADERS, timeout=15)
    r.raise_for_status()
    data = r.json()

    weeks = (data["data"]["user"]["contributionsCollection"]
             ["contributionCalendar"]["weeks"])

    days = []
    for week in weeks:
        for day in week["contributionDays"]:
            days.append((day["date"], day["contributionCount"]))
    return days


def fallback_contributions():
    """Random-ish fallback if API is unavailable."""
    import random
    random.seed(42)
    today = datetime.now(timezone.utc).date()
    days = []
    for i in range(371, -1, -1):
        d = today - timedelta(days=i)
        # Simulate heavier weekday activity
        weight = 1 if d.weekday() < 5 else 0.3
        count = random.choices([0,1,2,4,6,9], weights=[40,20,15,12,8,5])[0]
        count = int(count * weight)
        days.append((str(d), count))
    return days


def count_to_level(count, max_count):
    if count == 0:
        return 0
    if max_count == 0:
        return 0
    ratio = count / max_count
    if ratio < 0.15: return 1
    if ratio < 0.40: return 2
    if ratio < 0.70: return 3
    return 4


# ─── SVG builder ─────────────────────────────────────────────────────────────

FONT_MONO = "JetBrains Mono, Fira Code, Consolas, monospace"
CELL      = 13   # cell size
GAP       = 3    # gap between cells
PAD_LEFT  = 44   # for day labels
PAD_TOP   = 54   # for month labels + prompt
PAD_BOT   = 48   # bottom padding
PAD_RIGHT = 24


def build_heatmap_svg(days, mode):
    c    = THEMES[mode]
    scale = c["scale"]

    # Group into weeks (columns)
    # Pad front so week starts on Monday
    if days:
        first_date  = datetime.strptime(days[0][0], "%Y-%m-%d")
        # days since last Monday
        offset = first_date.weekday()   # Mon=0
        padded = [(None, 0)] * offset + days
    else:
        padded = days

    # Split into 53 weekly columns
    weeks = []
    week  = []
    for item in padded:
        week.append(item)
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:
        weeks.append(week)

    max_count = max((d[1] for d in days if d[0] is not None), default=1)

    num_weeks = len(weeks)
    W = PAD_LEFT + num_weeks * (CELL + GAP) + PAD_RIGHT
    H = PAD_TOP  + 7 * (CELL + GAP)         + PAD_BOT

    cells_svg  = ""
    month_seen = set()
    month_svg  = ""

    total_contribs = sum(d[1] for d in days if d[0] is not None)

    for wi, week in enumerate(weeks):
        x = PAD_LEFT + wi * (CELL + GAP)
        for di, (date_str, count) in enumerate(week):
            y = PAD_TOP + di * (CELL + GAP)
            if date_str is None:
                continue

            level = count_to_level(count, max_count)
            color = scale[level]

            # stagger animation per column → diagonal reveal
            delay = wi * 0.03 + di * 0.005

            tooltip = f"{date_str}: {count} contribution{'s' if count != 1 else ''}"

            cells_svg += f"""
  <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2"
        fill="{color}" opacity="0"
        style="animation: popIn 0.25s ease {delay:.3f}s forwards;">
    <title>{tooltip}</title>
  </rect>"""

            # Month label — only once per month, on row 0
            if date_str and di == 0:
                month = int(date_str[5:7])
                if month not in month_seen:
                    month_seen.add(month)
                    month_svg += f"""
  <text x="{x}" y="{PAD_TOP - 8}"
        font-family="{FONT_MONO}" font-size="10" fill="{c['text']}"
        opacity="0"
        style="animation: fadeIn 0.3s ease {wi * 0.02:.2f}s forwards;">
    {MONTH_ABBR[month - 1]}
  </text>"""

    # Day labels (Mon Wed Fri)
    day_labels_svg = ""
    for di, label in enumerate(DAY_ABBR):
        if not label:
            continue
        y = PAD_TOP + di * (CELL + GAP) + CELL - 2
        day_labels_svg += f"""
  <text x="{PAD_LEFT - 6}" y="{y}" text-anchor="end"
        font-family="{FONT_MONO}" font-size="9" fill="{c['text']}">{label}</text>"""

    # Legend
    legend_x = PAD_LEFT
    legend_y = H - 28
    legend_svg = f"""
  <text x="{legend_x}" y="{legend_y + 11}"
        font-family="{FONT_MONO}" font-size="10" fill="{c['text']}">Less</text>"""
    for li, col in enumerate(scale):
        lx = legend_x + 36 + li * (CELL + 3)
        legend_svg += f'<rect x="{lx}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="2" fill="{col}" />'
    legend_svg += f"""
  <text x="{legend_x + 36 + len(scale) * (CELL + 3) + 4}" y="{legend_y + 11}"
        font-family="{FONT_MONO}" font-size="10" fill="{c['text']}">More</text>"""

    # Prompt line
    prompt_svg = f"""
  <text x="{PAD_LEFT}" y="22"
        font-family="{FONT_MONO}" font-size="13" fill="{c['prompt']}">
    {GH_USERNAME}@github
  </text>
  <text x="{PAD_LEFT + len(GH_USERNAME) * 8 + 72}" y="22"
        font-family="{FONT_MONO}" font-size="13" fill="{c['text']}">
    :~$ git log --all --oneline | wc -l
  </text>
  <text x="{PAD_LEFT}" y="40"
        font-family="{FONT_MONO}" font-size="13" fill="{c['text']}">
    {total_contribs} commits in the last year
  </text>"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="{W}" height="{H}"
     viewBox="0 0 {W} {H}">

  <defs>
    <style>
      @keyframes popIn {{
        from {{ opacity: 0; transform: scale(0.4); }}
        to   {{ opacity: 1; transform: scale(1);   }}
      }}
      @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to   {{ opacity: 1; }}
      }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="{W}" height="{H}" rx="10" fill="{c['bg']}" />
  <rect width="{W-2}" height="{H-2}" x="1" y="1" rx="10"
        fill="none" stroke="{c['border']}" stroke-width="1" />

  {prompt_svg}
  {month_svg}
  {day_labels_svg}
  {cells_svg}
  {legend_svg}

</svg>"""
    return svg


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"[heatmap] Fetching contributions for @{GH_USERNAME} …")
    try:
        days = fetch_contributions()
        print(f"[heatmap] Got {len(days)} contribution days.")
    except Exception as e:
        print(f"[heatmap] Warning: API error ({e}). Using fallback data.")
        days = fallback_contributions()

    os.makedirs("assets", exist_ok=True)
    for mode in ("dark", "light"):
        svg  = build_heatmap_svg(days, mode)
        path = f"assets/contrib-heatmap-{mode}.svg"
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[heatmap] Written → {path}")


if __name__ == "__main__":
    main()

