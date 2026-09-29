"""Renders GitHub stats + activity SVGs in the profile's Nocturne style.

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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nocturne import GOLD, SILVER, ROSE, SEA, TEXT, SOFT, MUTED, SERIF, esc, sparkle, svg, caps, header  # noqa: E402

SPECTRUM = [GOLD, SILVER, ROSE, SEA, "#c9b8ff", "#f0b58a"]

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


def fmt(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def stats_svg(u):
    cc = u["contributionsCollection"]
    repos = u["repositories"]["nodes"]
    metrics = [
        ("contributions", cc["contributionCalendar"]["totalContributions"]),
        ("commits", cc["totalCommitContributions"] + cc["restrictedContributionsCount"]),
        ("pull requests", cc["totalPullRequestContributions"]),
        ("public repos", u["repositories"]["totalCount"]),
        ("stars earned", sum(r["stargazerCount"] for r in repos)),
        ("followers", u["followers"]["totalCount"]),
    ]
    cw = 1112 / len(metrics)
    parts = [header("VI", "Observations", "last 12 months · refreshed twice a day")]
    for i, (label, val) in enumerate(metrics):
        cx = round(44 + cw * i + cw / 2)
        if i:
            parts.append(f'<line x1="{44 + cw * i:.0f}" y1="104" x2="{44 + cw * i:.0f}" y2="196" stroke="{GOLD}" stroke-opacity="0.12"/>')
        parts.append(f'<g class="rise" style="animation-delay:{i * 0.15:.2f}s">'
                     + sparkle(cx, 108, 4, GOLD, 0.8, (3, round(i * 0.5, 1))) +
                     f'<text x="{cx}" y="160" text-anchor="middle" font-family="{SERIF}" font-size="48" fill="{GOLD}">{fmt(val)}</text>'
                     + caps(cx, 190, label, MUTED, 10.5, "middle", 3) + '</g>')

    sizes = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            sizes[e["node"]["name"]] = sizes.get(e["node"]["name"], 0) + e["size"]
    top = sorted(sizes.items(), key=lambda kv: -kv[1])[:6]
    total = sum(v for _, v in top) or 1
    BY = 262
    parts.append(caps(44, BY - 20, "Spectral lines · top languages", GOLD, 11.5, spacing=4) +
                 f'<clipPath id="bar"><rect x="44" y="{BY}" width="1112" height="6" rx="3"/></clipPath>'
                 f'<rect x="44" y="{BY}" width="1112" height="6" rx="3" fill="{GOLD}" fill-opacity="0.08"/><g clip-path="url(#bar)">')
    x = 44.0
    for i, (name, size) in enumerate(top):
        w = 1112 * size / total
        parts.append(f'<rect x="{x:.1f}" y="{BY}" width="0" height="6" fill="{SPECTRUM[i]}">'
                     f'<animate attributeName="width" from="0" to="{max(w - 3, 0):.1f}" begin="{0.4 + i * 0.15:.2f}s" dur="0.9s" fill="freeze"/></rect>')
        x += w
    parts.append('</g>')
    lw = 1112 / 6
    for i, (name, size) in enumerate(top):
        lx = 44 + lw * i
        parts.append(sparkle(lx + 5, 300, 5, SPECTRUM[i], 1) +
                     f'<text x="{lx + 18:.0f}" y="305" font-family="{SERIF}" font-size="16" fill="{TEXT}">{esc(name)}'
                     f'<tspan dx="8" font-style="italic" font-size="14" fill="{MUTED}">{100 * size / total:.0f}%</tspan></text>')
    return svg(1200, 340, f"GitHub stats for {LOGIN}", "".join(parts), seed=61, stars=55)


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
    L, R, T, B = 80, 1140, 118, 262
    peak = max(counts, default=0) or 1
    step = (R - L) / max(len(counts) - 1, 1)
    pts = [(L + i * step, B - (B - T) * c / peak) for i, c in enumerate(counts)] or [(L, B), (R, B)]
    line = smooth(pts, B)
    area = f"{line} L{pts[-1][0]:.1f},{B} L{L},{B} Z"
    grid = "".join(f'<line x1="{L}" y1="{y:.0f}" x2="{R}" y2="{y:.0f}" stroke="{GOLD}" stroke-opacity="0.07" stroke-dasharray="1 5"/>'
                   f'<text x="{L - 16}" y="{y + 4:.0f}" text-anchor="end" font-family="{SERIF}" font-style="italic" font-size="12" fill="{MUTED}">{v}</text>'
                   for v, y in ((round(peak * f), B - (B - T) * f) for f in (0, 0.5, 1)))
    months, seen = [], set()
    for i, st in enumerate(starts):
        if st[:7] not in seen:
            seen.add(st[:7])
            if i:  # skip the partial first month
                months.append(caps(round(L + i * step), B + 30, dt.date.fromisoformat(st).strftime("%b"), MUTED, 10.5, "middle", 3))
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.8" fill="{GOLD}" opacity="0.8"/>' for x, y in pts)
    peak_mark = ""
    if counts and max(counts):
        pi = max(range(len(counts)), key=counts.__getitem__)
        px, py = pts[pi]
        anchor = "start" if pi < 3 else "end" if pi > len(pts) - 4 else "middle"
        peak_mark = (f'<circle cx="{px:.1f}" cy="{py:.1f}" r="12" fill="{GOLD}" opacity="0.12" filter="url(#glow)"/>'
                     + sparkle(px, py, 8, GOLD, 1, (2.5, 0)) +
                     f'<text x="{px:.0f}" y="{py - 18:.0f}" text-anchor="{anchor}" font-family="{SERIF}" font-style="italic" font-size="14" '
                     f'fill="{SOFT}">brightest week · {max(counts)}</text>')
    defs = (f'<linearGradient id="af" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.22"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>')
    inner = (header("VII", "Night log", f"{sum(counts)} contributions · last 26 weeks") + grid + "".join(months) +
             f'<path d="{area}" fill="url(#af)"><animate attributeName="opacity" from="0" to="1" dur="1.5s" fill="freeze"/></path>'
             f'<path id="al" d="{line}" fill="none" stroke="{GOLD}" stroke-width="1.8" pathLength="100" stroke-dasharray="100">'
             f'<animate attributeName="stroke-dashoffset" from="100" to="0" dur="2.5s" fill="freeze"/></path>'
             + dots +
             f'<circle r="2.6" fill="#fff" filter="url(#glow)"><animateMotion dur="10s" repeatCount="indefinite"><mpath href="#al"/></animateMotion></circle>'
             + peak_mark)
    return svg(1200, 320, f"GitHub contribution activity for {LOGIN}", inner, seed=71, stars=55, defs=defs)


if __name__ == "__main__":
    data = mock() if "--mock" in sys.argv else fetch()
    os.makedirs(OUT, exist_ok=True)
    for name, svg in (("stats.svg", stats_svg(data)), ("activity.svg", activity_svg(data))):
        with open(os.path.join(OUT, name), "w") as f:
            f.write(svg)
    print("wrote", OUT)
