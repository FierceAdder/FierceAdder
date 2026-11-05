#!/usr/bin/env python3
"""Generate a LeetCode contest rating graph SVG — rating line chart only."""
import urllib.request, json, os, sys, math

USERNAME = "Trying_out"

# ── Fetch contest history ────────────────────────────────────────────────────
QUERY = """
query userContestRankingInfo($username: String!) {
  userContestRanking(username: $username) {
    rating
    badge { name }
    attendedContestsCount
    globalRanking
    topPercentage
  }
  userContestRankingHistory(username: $username) {
    attended
    rating
    contest { title startTime }
  }
}
"""

def fetch():
    payload = json.dumps({"query": QUERY, "variables": {"username": USERNAME}}).encode()
    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://leetcode.com",
        },
    )
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read())["data"]

print("Fetching LeetCode contest data...", file=sys.stderr)
data = fetch()
info    = data["userContestRanking"]
history = [h for h in data["userContestRankingHistory"] if h["attended"]]
history.sort(key=lambda h: h["contest"]["startTime"])

rating  = round(info["rating"])
badge   = info["badge"]["name"] if info["badge"] else "Unrated"
count   = info["attendedContestsCount"]
top_pct = round(info["topPercentage"], 1)
ratings = [h["rating"] for h in history]

print(f"  Rating: {rating}  Badge: {badge}  Contests: {count}", file=sys.stderr)

# ── SVG layout constants ─────────────────────────────────────────────────────
W, H       = 500, 320
PAD_L      = 54
PAD_R      = 24
PAD_T      = 66
PAD_B      = 44
GW         = W - PAD_L - PAD_R   # graph width
GH         = H - PAD_T - PAD_B   # graph height

# Y axis: round to nearest 100
y_min = max(0,  (math.floor(min(ratings) / 100) - 1) * 100)
y_max =         (math.ceil(max(ratings)  / 100) + 1) * 100

def gx(i):   # x pixel for index i
    n = max(len(ratings) - 1, 1)
    return PAD_L + (i / n) * GW

def gy(r):   # y pixel for rating r
    return PAD_T + GH - ((r - y_min) / (y_max - y_min)) * GH

# ── Build SVG ────────────────────────────────────────────────────────────────
lines = []
def L(s): lines.append(s)

L(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
L('''  <defs>
    <style>
      .mono { font-family: "JetBrains Mono", "Fira Code", Consolas, monospace; }
    </style>
    <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#FFA116" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#FFA116" stop-opacity="0.02"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>''')

# Background
L(f'  <rect width="{W}" height="{H}" rx="10" fill="#0D1117" stroke="#30363D" stroke-width="1.2"/>')

# ── Header ───────────────────────────────────────────────────────────────────
L(f'  <text x="20" y="26" class="mono" font-size="12" font-weight="700" fill="#FFA116">⚔ Contest Rating</text>')
L(f'  <text x="{W-20}" y="26" class="mono" font-size="11" fill="#8B949E" text-anchor="end">{USERNAME} · {count} contests</text>')

# Badge pill
badge_color = {"Knight": "#FFA116", "Guardian": "#FF6B6B"}.get(badge, "#8B949E")
L(f'  <rect x="20" y="36" width="76" height="18" rx="9" fill="{badge_color}" opacity="0.18"/>')
L(f'  <text x="58" y="49" class="mono" font-size="9.5" font-weight="700" fill="{badge_color}" text-anchor="middle">{badge}</text>')

# Rating big number (top right)
L(f'  <text x="{W-20}" y="48" class="mono" font-size="11" fill="#8B949E" text-anchor="end">Top {top_pct}%</text>')

# ── Y-axis grid lines ────────────────────────────────────────────────────────
tick_step = 200
y_tick = y_min
while y_tick <= y_max:
    py = gy(y_tick)
    if PAD_T <= py <= PAD_T + GH:
        L(f'  <line x1="{PAD_L}" y1="{py:.1f}" x2="{PAD_L+GW}" y2="{py:.1f}" stroke="#21262D" stroke-width="1"/>')
        L(f'  <text x="{PAD_L-8}" y="{py+4:.1f}" class="mono" font-size="8.5" fill="#484F58" text-anchor="end">{y_tick}</text>')
    y_tick += tick_step

# ── Area fill ────────────────────────────────────────────────────────────────
area_pts = " ".join(f"{gx(i):.1f},{gy(r):.1f}" for i, r in enumerate(ratings))
area_pts += f" {gx(len(ratings)-1):.1f},{PAD_T+GH:.1f} {gx(0):.1f},{PAD_T+GH:.1f}"
L(f'  <polygon points="{area_pts}" fill="url(#areaGrad)"/>')

# ── Rating line ───────────────────────────────────────────────────────────────
path_d = " ".join(
    ("M" if i == 0 else "L") + f"{gx(i):.1f},{gy(r):.1f}"
    for i, r in enumerate(ratings)
)
L(f'  <path d="{path_d}" fill="none" stroke="#FFA116" stroke-width="2" stroke-linejoin="round" filter="url(#glow)"/>')

# ── Dots at each contest ──────────────────────────────────────────────────────
for i, r in enumerate(ratings):
    cx, cy = gx(i), gy(r)
    L(f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.5" fill="#FFA116"/>')

# ── Current rating dot + label (last point) ──────────────────────────────────
cx_last = gx(len(ratings) - 1)
cy_last = gy(ratings[-1])
L(f'  <circle cx="{cx_last:.1f}" cy="{cy_last:.1f}" r="5" fill="#0D1117" stroke="#FFA116" stroke-width="2"/>')
L(f'  <circle cx="{cx_last:.1f}" cy="{cy_last:.1f}" r="2.5" fill="#FFA116"/>')

# Rating callout
label_x = cx_last - 8 if cx_last > W * 0.7 else cx_last + 8
anchor   = "end" if cx_last > W * 0.7 else "start"
L(f'  <text x="{label_x:.1f}" y="{cy_last - 8:.1f}" class="mono" font-size="11" font-weight="700" fill="#FFA116" text-anchor="{anchor}">{rating}</text>')

# ── X-axis baseline ───────────────────────────────────────────────────────────
L(f'  <line x1="{PAD_L}" y1="{PAD_T+GH}" x2="{PAD_L+GW}" y2="{PAD_T+GH}" stroke="#30363D" stroke-width="1"/>')
L(f'  <line x1="{PAD_L}" y1="{PAD_T}" x2="{PAD_L}" y2="{PAD_T+GH}" stroke="#30363D" stroke-width="1"/>')

# X-axis label
L(f'  <text x="{PAD_L + GW/2:.1f}" y="{H-12}" class="mono" font-size="8.5" fill="#484F58" text-anchor="middle">contest history</text>')

L('</svg>')

# ── Write output ──────────────────────────────────────────────────────────────
content = "\n".join(lines) + "\n"
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_path  = os.path.join(repo_root, "assets", "lc-rating.svg")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"✅ Saved lc-rating.svg → {out_path}", file=sys.stderr)

