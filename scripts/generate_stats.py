"""Renders GitHub stats + activity SVGs in the profile's neural theme.

Runs in the update-profile workflow with GITHUB_TOKEN, writing into dist/.
Local preview with fake data: python3 scripts/generate_stats.py --mock
"""
import datetime as dt
import json
import os
import random
import sys
import urllib.request

LOGIN = os.environ.get("GITHUB_USER", "ManasKhare3005")
OUT = os.environ.get("OUT_DIR", "dist")
BG, BG2 = "#070b16", "#0d1428"
CYAN, VIOLET, PINK, AMBER, GREEN, TEXT, MUTED = "#22d3ee", "#a78bfa", "#f472b6", "#fbbf24", "#34d399", "#e2e8f0", "#64748b"
SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if "errors" in body:
        sys.exit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]


def mock():
    random.seed(1)
    today = dt.date.today()
    days = [{"date": str(today - dt.timedelta(days=i)), "contributionCount": random.choice([0, 0, 1, 2, 3, 5, 8])} for i in range(364, -1, -1)]
    weeks = [{"contributionDays": days[i:i + 7]} for i in range(0, len(days), 7)]
    langs = [("TypeScript", "#3178c6", 900), ("JavaScript", "#f1e05a", 700), ("Python", "#3572A5", 600),
             ("Java", "#b07219", 300), ("CSS", "#663399", 150), ("HTML", "#e34c26", 100)]
    return {"followers": {"totalCount": 42},
            "repositories": {"totalCount": 18, "nodes": [{"stargazerCount": 3, "languages": {"edges": [
                {"size": s, "node": {"name": n, "color": c}} for n, c, s in langs]}}]},
            "contributionsCollection": {"totalCommitContributions": 310, "totalPullRequestContributions": 24,
                                        "restrictedContributionsCount": 0,
                                        "contributionCalendar": {"totalContributions": sum(d["contributionCount"] for d in days), "weeks": weeks}}}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


DEFS = f'''<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="bgg" cx="50%" cy="40%" r="75%"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></radialGradient>
<linearGradient id="rail" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<style>.rise {{ animation: rise .9s ease-out both }} @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px) }} to {{ opacity: 1; transform: none }} }}</style>'''


def frame(w, h, title, inner, defs=""):
    random.seed(5)
    stars = "".join(f'<circle cx="{random.uniform(0, w):.0f}" cy="{random.uniform(0, h):.0f}" r="{random.choice([0.6, 0.9, 1.2])}" fill="#fff" opacity="{random.uniform(0.15, 0.5):.2f}"/>' for _ in range(45))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title><defs>{DEFS}{defs}</defs><rect width="{w}" height="{h}" rx="18" fill="url(#bgg)"/>{stars}{inner}</svg>')


def header(label, sub, color):
    return (f'<text x="40" y="48" font-family="{MONO}" font-size="15" fill="{color}" letter-spacing="3">{esc(label)}</text>'
            f'<text x="1160" y="48" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTED}">{esc(sub)}</text>')


def stats_svg(u):
    cc = u["contributionsCollection"]
    repos = u["repositories"]["nodes"]
    metrics = [
        ("contributions", cc["contributionCalendar"]["totalContributions"], CYAN),
        ("commits", cc["totalCommitContributions"] + cc["restrictedContributionsCount"], CYAN),
        ("pull requests", cc["totalPullRequestContributions"], VIOLET),
        ("public repos", u["repositories"]["totalCount"], VIOLET),
        ("stars earned", sum(r["stargazerCount"] for r in repos), PINK),
        ("followers", u["followers"]["totalCount"], PINK),
    ]
    W, Y = 1200, 150
    xs = [120 + i * 192 for i in range(len(metrics))]
    parts = [header("ACTIVATIONS.stats", "last 12 months · auto-updated", CYAN),
             f'<path id="mr" d="M40,{Y} L1160,{Y}" stroke="url(#rail)" stroke-width="1.5" opacity="0.45"/>',
             f'<circle r="3.5" fill="{PINK}" filter="url(#glow)"><animateMotion dur="6s" repeatCount="indefinite"><mpath href="#mr"/></animateMotion></circle>']
    for i, ((label, val, c), x) in enumerate(zip(metrics, xs)):
        parts.append(f'<g class="rise" style="animation-delay:{i * 0.15:.2f}s">'
                     f'<circle cx="{x}" cy="{Y}" r="46" fill="{BG}" stroke="{c}" stroke-width="2" filter="url(#glow)">'
                     f'<animate attributeName="stroke-opacity" values="1;0.35;1" dur="3s" begin="{i * 0.4:.1f}s" repeatCount="indefinite"/></circle>'
                     f'<text x="{x}" y="{Y + 9}" text-anchor="middle" font-family="{SANS}" font-size="27" font-weight="800" fill="{TEXT}">{fmt(val)}</text>'
                     f'<text x="{x}" y="{Y + 76}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{c}" letter-spacing="1">{esc(label.upper())}</text></g>')

    sizes = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            sizes.setdefault(n, [0, e["node"]["color"] or MUTED])[0] += e["size"]
    top = sorted(sizes.items(), key=lambda kv: -kv[1][0])[:6]
    total = sum(v[0] for _, v in top) or 1
    BY = 290
    parts.append(f'<text x="40" y="{BY - 16}" font-family="{MONO}" font-size="13" fill="{VIOLET}" letter-spacing="3">TOP LANGUAGES</text>'
                 f'<clipPath id="bar"><rect x="40" y="{BY}" width="1120" height="14" rx="7"/></clipPath><g clip-path="url(#bar)">'
                 f'<rect x="40" y="{BY}" width="1120" height="14" fill="#fff" fill-opacity="0.06"/>')
    x = 40.0
    for i, (name, (size, color)) in enumerate(top):
        w = 1120 * size / total
        parts.append(f'<rect x="{x:.1f}" y="{BY}" width="0" height="14" fill="{color}">'
                     f'<animate attributeName="width" from="0" to="{w:.1f}" begin="{0.3 + i * 0.15:.2f}s" dur="0.8s" fill="freeze"/></rect>')
        x += w
    parts.append('</g>')
    for i, (name, (size, color)) in enumerate(top):
        lx, ly = 40 + (i % 6) * 190, BY + 48
        parts.append(f'<circle cx="{lx + 6}" cy="{ly - 5}" r="6" fill="{color}"/>'
                     f'<text x="{lx + 20}" y="{ly}" font-family="{SANS}" font-size="15" fill="{TEXT}">{esc(name)}'
                     f'<tspan dx="8" font-family="{MONO}" font-size="13" fill="{MUTED}">{100 * size / total:.1f}%</tspan></text>')
    return frame(W, 370, f"GitHub stats for {LOGIN}", "".join(parts))


def smooth(pts, floor):
    """Catmull-Rom spline through pts as an SVG cubic path, never dipping below floor."""
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0, p1, p2 = pts[max(i - 1, 0)], pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, min(p1[1] + (p2[1] - p0[1]) / 6, floor))
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, min(p2[1] - (p3[1] - p1[1]) / 6, floor))
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def activity_svg(u):
    weeks = u["contributionsCollection"]["contributionCalendar"]["weeks"][-26:]
    counts = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks]
    starts = [w["contributionDays"][0]["date"] for w in weeks]
    W, H, L, R, T, B = 1200, 330, 70, 1150, 100, 262
    peak = max(counts, default=0) or 1
    step = (R - L) / max(len(counts) - 1, 1)
    pts = [(L + i * step, B - (B - T) * c / peak) for i, c in enumerate(counts)] or [(L, B), (R, B)]
    line = smooth(pts, B)
    area = f"{line} L{pts[-1][0]:.1f},{B} L{L},{B} Z"
    grid = "".join(f'<line x1="{L}" y1="{y:.0f}" x2="{R}" y2="{y:.0f}" stroke="#fff" stroke-opacity="0.06"/>'
                   f'<text x="{L - 14}" y="{y + 4:.0f}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">{v}</text>'
                   for v, y in ((round(peak * f), B - (B - T) * f) for f in (0, 0.5, 1)))
    months, seen = [], set()
    for i, s in enumerate(starts):
        m = s[:7]
        if m not in seen:
            seen.add(m)
            if i:  # skip the partial first month label
                months.append(f'<text x="{L + i * step:.0f}" y="{B + 28}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">{dt.date.fromisoformat(s).strftime("%b").upper()}</text>')
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{BG}" stroke="{VIOLET}" stroke-width="1.5"/>' for x, y in pts)
    peak_mark = ""
    if counts and max(counts):
        pi = max(range(len(counts)), key=counts.__getitem__)
        px, py = pts[pi]
        anchor = "start" if pi < 3 else "end" if pi > len(pts) - 4 else "middle"
        peak_mark = (f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{PINK}" filter="url(#glow)">'
                     f'<animate attributeName="r" values="4;8;4" dur="2s" repeatCount="indefinite"/></circle>'
                     f'<text x="{px:.0f}" y="{py - 16:.0f}" text-anchor="{anchor}" font-family="{MONO}" font-size="12" fill="{PINK}">peak week · {max(counts)}</text>')
    defs = (f'<linearGradient id="af" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0.45"/>'
            f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>')
    inner = (header("ACTIVITY.stream", f"{sum(counts)} contributions · last 26 weeks", VIOLET) + grid + "".join(months) +
             f'<path d="{area}" fill="url(#af)"><animate attributeName="opacity" from="0" to="1" dur="1.5s" fill="freeze"/></path>'
             f'<path id="al" d="{line}" fill="none" stroke="url(#rail)" stroke-width="2.5" pathLength="100" stroke-dasharray="100" filter="url(#glow)">'
             f'<animate attributeName="stroke-dashoffset" from="100" to="0" dur="2.5s" fill="freeze"/></path>'
             + dots +
             f'<circle r="3.5" fill="{CYAN}" filter="url(#glow)"><animateMotion dur="9s" repeatCount="indefinite"><mpath href="#al"/></animateMotion></circle>'
             + peak_mark)
    return frame(W, H, f"GitHub contribution activity for {LOGIN}", inner, defs)


if __name__ == "__main__":
    data = mock() if "--mock" in sys.argv else fetch()
    os.makedirs(OUT, exist_ok=True)
    for name, svg in (("stats.svg", stats_svg(data)), ("activity.svg", activity_svg(data))):
        with open(os.path.join(OUT, name), "w") as f:
            f.write(svg)
    print("wrote", OUT)
