"""Generates the animated SVGs in ../assets. Run: python3 scripts/generate_assets.py"""
import random, os
random.seed(7)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
BG, BG2 = "#070b16", "#0d1428"
CYAN, VIOLET, PINK, TEXT, MUTED = "#22d3ee", "#a78bfa", "#f472b6", "#e2e8f0", "#64748b"
SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

def stars(w, h, n, twinkle=10):
    s = []
    for i in range(n):
        x, y, r = random.uniform(0, w), random.uniform(0, h), random.choice([0.6, 0.8, 1, 1.2])
        op = random.uniform(0.2, 0.6)
        if i < twinkle:
            d = random.uniform(2, 5)
            s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity="{op:.2f}">'
                     f'<animate attributeName="opacity" values="{op:.2f};0.05;{op:.2f}" dur="{d:.1f}s" repeatCount="indefinite"/></circle>')
        else:
            s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity="{op:.2f}"/>')
    return "\n".join(s)

GLOW = '''<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="softglow" x="-20%" y="-50%" width="140%" height="200%">
  <feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'''

# ---------------- HERO ----------------
W, H = 1200, 440
L1 = {"AI · LLMs": (95, 95), "Agents": (60, 220), "Full-Stack": (95, 345)}
R1 = {"Cloud": (1105, 95), "FinTech": (1140, 220), "HealthTech": (1105, 345)}
L2 = [(205, 145), (205, 295)]
R2 = [(995, 145), (995, 295)]
HL, HR = (305, 220), (895, 220)

edges = []  # (id, d, color)
def line(a, b): return f"M{a[0]},{a[1]} L{b[0]},{b[1]}"
n = 0
for p in L1.values():
    for q in L2:
        edges.append((f"e{n}", line(p, q), CYAN)); n += 1
for q in L2:
    edges.append((f"e{n}", line(q, HL), CYAN)); n += 1
edges.append((f"e{n}", line(L1["Agents"], HL), CYAN)); n += 1
edges.append(("arcT", f"M{HL[0]},{HL[1]} Q600,-20 {HR[0]},{HR[1]}", "url(#arcg)"))
edges.append(("arcB", f"M{HL[0]},{HL[1]} Q600,460 {HR[0]},{HR[1]}", "url(#arcg)"))
for q in R2:
    edges.append((f"e{n}", line(HR, q), VIOLET)); n += 1
edges.append((f"e{n}", line(HR, R1["FinTech"]), VIOLET)); n += 1
for q in R2:
    for p in R1.values():
        edges.append((f"e{n}", line(q, p), VIOLET)); n += 1

edge_svg = []
for eid, d, c in edges:
    dash = ' stroke-dasharray="4 6"' if eid.startswith("arc") else ""
    edge_svg.append(f'<path id="{eid}" d="{d}" stroke="{c}" stroke-width="1.2" fill="none" opacity="0.35"{dash}/>')

pulses = []
for i, (eid, d, c) in enumerate(edges):
    col = PINK if eid.startswith("arc") else (CYAN if c == CYAN else VIOLET)
    dur = 4.5 if eid.startswith("arc") else random.uniform(1.8, 3.2)
    begin = random.uniform(0, 3)
    pulses.append(
        f'<circle r="3" fill="{col}" filter="url(#glow)" opacity="0">'
        f'<animateMotion dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"><mpath href="#{eid}"/></animateMotion>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
        f'</circle>')

def node(p, color, r=6, label=None, above=False, delay=0):
    s = (f'<circle cx="{p[0]}" cy="{p[1]}" r="{r+8}" fill="{color}" opacity="0.08">'
         f'<animate attributeName="r" values="{r+4};{r+12};{r+4}" dur="3s" begin="{delay:.1f}s" repeatCount="indefinite"/></circle>'
         f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{BG}" stroke="{color}" stroke-width="2" filter="url(#glow)"/>'
         f'<circle cx="{p[0]}" cy="{p[1]}" r="{r/2.5:.1f}" fill="{color}"/>')
    if label:
        y = p[1] - 18 if above else p[1] + 28
        s += (f'<text x="{p[0]}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="13" '
              f'fill="{TEXT}" opacity="0.85">{label}</text>')
    return s

nodes = []
for i, (lbl, p) in enumerate(L1.items()):
    nodes.append(node(p, CYAN, label=lbl, above=(i == 0), delay=i * 0.4))
for i, (lbl, p) in enumerate(R1.items()):
    nodes.append(node(p, VIOLET, label=lbl, above=(i == 0), delay=i * 0.4 + 0.2))
for p in L2: nodes.append(node(p, CYAN, r=5, delay=1))
for p in R2: nodes.append(node(p, VIOLET, r=5, delay=1.5))
nodes.append(node(HL, CYAN, r=9, delay=0.5))
nodes.append(node(HR, VIOLET, r=9, delay=0.9))

hero = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Manas Khare: AI Engineer and Full-Stack Developer">
<title>Manas Khare: AI Engineer · Full-Stack Developer</title>
<defs>
<radialGradient id="bgg" cx="50%" cy="50%" r="65%"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></radialGradient>
<linearGradient id="arcg" gradientUnits="userSpaceOnUse" x1="{HL[0]}" y1="0" x2="{HR[0]}" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{PINK}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<linearGradient id="nameg" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{PINK}"/><stop offset="1" stop-color="{VIOLET}"/>
</linearGradient>
{GLOW}
</defs>
<style>
  .fade {{ animation: fade 1.2s ease-out both; }}
  .d1 {{ animation-delay: .3s }} .d2 {{ animation-delay: .6s }} .d3 {{ animation-delay: .9s }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateY(8px) }} to {{ opacity: 1; transform: none }} }}
  .blink {{ animation: blink 1.6s ease-in-out infinite; }}
  @keyframes blink {{ 50% {{ opacity: .25 }} }}
</style>
<rect width="{W}" height="{H}" rx="18" fill="url(#bgg)"/>
{stars(W, H, 90)}
{chr(10).join(edge_svg)}
{chr(10).join(pulses)}
{chr(10).join(nodes)}
<g text-anchor="middle">
  <text class="fade" x="600" y="152" font-family="{MONO}" font-size="15" fill="{MUTED}" letter-spacing="2">&gt; initializing neural profile ...</text>
  <text class="fade d1" x="600" y="218" font-family="{SANS}" font-size="58" font-weight="800" letter-spacing="5" fill="url(#nameg)" filter="url(#softglow)">MANAS KHARE</text>
  <text class="fade d2" x="600" y="262" font-family="{MONO}" font-size="17" fill="{CYAN}" letter-spacing="3">AI ENGINEER  ·  FULL-STACK DEVELOPER</text>
  <text class="fade d2" x="600" y="292" font-family="{SANS}" font-size="15" fill="{TEXT}" opacity="0.75">M.S. Computer Science @ Arizona State University</text>
  <g class="fade d3">
    <rect x="455" y="318" width="290" height="32" rx="16" fill="#0f2a1e" stroke="#34d399" stroke-opacity="0.5"/>
    <circle class="blink" cx="478" cy="334" r="5" fill="#34d399"/>
    <text x="610" y="339" font-family="{MONO}" font-size="13" fill="#6ee7b7">status: open to SWE roles</text>
  </g>
</g>
</svg>'''
open(f"{OUT}/hero.svg", "w").write(hero)

# ---------------- DIVIDER ----------------
DW, DH = 1200, 40
pts = [60 + i * 120 for i in range(10)]
dnodes = "".join(
    f'<circle cx="{x}" cy="20" r="4" fill="{BG}" stroke="{CYAN if i < 5 else VIOLET}" stroke-width="1.5">'
    f'<animate attributeName="r" values="3;5;3" dur="2s" begin="{i*0.2:.1f}s" repeatCount="indefinite"/></circle>'
    for i, x in enumerate(pts))
divider = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {DW} {DH}" width="{DW}" height="{DH}" role="img" aria-label="divider">
<defs><linearGradient id="dg" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="0.2" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{PINK}"/><stop offset="0.8" stop-color="{VIOLET}"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>{GLOW}</defs>
<path id="dl" d="M0,20 L{DW},20" stroke="url(#dg)" stroke-width="1.2" opacity="0.6"/>
{dnodes}
<circle r="3.5" fill="{PINK}" filter="url(#glow)"><animateMotion dur="5s" repeatCount="indefinite"><mpath href="#dl"/></animateMotion></circle>
<circle r="2.5" fill="{CYAN}" filter="url(#glow)"><animateMotion dur="5s" begin="2.5s" repeatCount="indefinite"><mpath href="#dl"/></animateMotion></circle>
</svg>'''
open(f"{OUT}/divider.svg", "w").write(divider)

# ---------------- PROJECT CARDS ----------------
def draw(d, color, dur=3):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round" '
            f'pathLength="100" stroke-dasharray="100" filter="url(#glow)">'
            f'<animate attributeName="stroke-dashoffset" values="100;0;0;100" keyTimes="0;0.5;0.85;1" dur="{dur*2}s" repeatCount="indefinite"/></path>')
grid = "".join(f'<line x1="820" y1="{y}" x2="1160" y2="{y}" stroke="#fff" stroke-opacity="0.05"/>' for y in (100, 140, 180))
candles = ""
import random as _r; _r.seed(3)
for i, x in enumerate(range(835, 1160, 30)):
    o = 175 - i * 6 + _r.uniform(-12, 12); c = o - _r.uniform(-8, 22)
    up = c < o; col = "#34d399" if up else "#f87171"
    candles += (f'<line x1="{x}" y1="{min(o,c)-8:.0f}" x2="{x}" y2="{max(o,c)+8:.0f}" stroke="{col}" stroke-opacity="0.5"/>'
                f'<rect x="{x-5}" y="{min(o,c):.0f}" width="10" height="{max(abs(o-c),2):.0f}" fill="{col}" fill-opacity="0.35"/>')
VIZ_STOCK = grid + candles + draw("M820,185 L860,170 L895,176 L930,150 L965,158 L1000,130 L1035,138 L1070,110 L1110,118 L1155,92", CYAN)
VIZ_RESUME = (f'<circle cx="1060" cy="140" r="48" fill="none" stroke="#fff" stroke-opacity="0.08" stroke-width="10"/>'
    f'<circle cx="1060" cy="140" r="48" fill="none" stroke="{PINK}" stroke-width="10" stroke-linecap="round" pathLength="100" '
    f'stroke-dasharray="100" transform="rotate(-90 1060 140)" filter="url(#glow)">'
    f'<animate attributeName="stroke-dashoffset" values="100;6;6;100" keyTimes="0;0.45;0.9;1" dur="5s" repeatCount="indefinite"/></circle>'
    f'<text x="1060" y="136" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{TEXT}" opacity="0.7">ATS</text>'
    f'<text x="1060" y="158" text-anchor="middle" font-family="{MONO}" font-size="18" font-weight="700" fill="{PINK}">READY</text>'
    + "".join(f'<rect x="850" y="{105+i*18}" width="{w}" height="7" rx="3.5" fill="#fff" fill-opacity="0.10"/>' for i, w in enumerate((120, 90, 130, 70, 110))))
VIZ_HEART = draw("M820,150 L900,150 L915,150 L928,110 L942,190 L956,130 L966,150 L1010,150 L1022,142 L1034,150 L1160,150", VIOLET, 2)

def card(fname, idx, title, lines, tags, color, glyph, cta, viz=""):
    CW, CH = 1200, 230
    tag_svg, x = [], 250
    for t in tags:
        w = 16 + len(t) * 9.2
        tag_svg.append(f'<rect x="{x}" y="168" width="{w:.0f}" height="30" rx="15" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.5"/>'
                       f'<text x="{x + w/2:.0f}" y="188" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{color}">{t}</text>')
        x += w + 10
    body = "".join(f'<text x="250" y="{112 + i*26}" font-family="{SANS}" font-size="19" fill="{TEXT}" opacity="0.8">{l}</text>'
                   for i, l in enumerate(lines))
    cta_svg = (f'<text x="1160" y="60" text-anchor="end" font-family="{MONO}" font-size="15" fill="{color}">{cta}</text>' if cta else "")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW}" height="{CH}" role="img" aria-label="{title}">
<title>{title}</title>
<defs>{GLOW}
<linearGradient id="cb" x1="0" x2="1"><stop offset="0" stop-color="{color}" stop-opacity="0.9"/><stop offset="1" stop-color="{color}" stop-opacity="0.1"/></linearGradient>
<radialGradient id="cbg" cx="10%" cy="50%" r="80%"><stop offset="0" stop-color="{color}" stop-opacity="0.10"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient></defs>
<rect x="1" y="1" width="{CW-2}" height="{CH-2}" rx="18" fill="{BG}"/>
<rect x="1" y="1" width="{CW-2}" height="{CH-2}" rx="18" fill="url(#cbg)" stroke="url(#cb)" stroke-width="1.5"/>
{stars(CW, CH, 30, 6)}
<circle cx="130" cy="115" r="62" fill="none" stroke="{color}" stroke-opacity="0.25" stroke-dasharray="3 7">
  <animateTransform attributeName="transform" type="rotate" from="0 130 115" to="360 130 115" dur="24s" repeatCount="indefinite"/></circle>
<circle cx="130" cy="115" r="44" fill="{BG}" stroke="{color}" stroke-width="2" filter="url(#glow)">
  <animate attributeName="stroke-opacity" values="1;0.4;1" dur="3s" repeatCount="indefinite"/></circle>
<text x="130" y="129" text-anchor="middle" font-size="38">{glyph}</text>
<path d="M174,115 L230,115" stroke="{color}" stroke-width="1.5" opacity="0.6" id="syn"/>
<circle r="3" fill="{color}" filter="url(#glow)"><animateMotion dur="1.6s" repeatCount="indefinite"><mpath href="#syn"/></animateMotion></circle>
<text x="250" y="48" font-family="{MONO}" font-size="14" fill="{color}" letter-spacing="3">NEURON_{idx:02d}</text>
{cta_svg}
<text x="250" y="82" font-family="{SANS}" font-size="32" font-weight="700" fill="{TEXT}">{title}</text>
{body}
{"".join(tag_svg)}
{viz}
</svg>'''
    open(f"{OUT}/{fname}", "w").write(svg)

card("project-stockintel.svg", 1, "Stock Intel",
     ["AI-powered financial intelligence platform: market insights,",
      "interactive visualizations and data-driven analytics."],
     ["Python", "React", "APIs", "Machine Learning"], CYAN, "📈", None, VIZ_STOCK)
card("project-resumify.svg", 2, "Resumify",
     ["AI-driven resume optimizer that boosts ATS compatibility",
      "and recruiter appeal, turning good resumes into great ones."],
     ["React", "Node.js", "Express", "OpenAI"], PINK, "📄", "view repo →", VIZ_RESUME)
card("project-curaconnect.svg", 3, "CuraConnect",
     ["Full-stack healthcare platform that improves communication",
      "and accessibility between patients and providers."],
     ["MongoDB", "Express", "React", "Node.js"], VIOLET, "🏥", "view repo →", VIZ_HEART)

AMBER, GREEN = "#fbbf24", "#34d399"

def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def frame(w, h, title, inner, extra_defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<defs>{GLOW}
<radialGradient id="bgg" cx="50%" cy="40%" r="75%"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></radialGradient>
<linearGradient id="rail" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
{extra_defs}</defs>
<rect width="{w}" height="{h}" rx="18" fill="url(#bgg)"/>
{stars(w, h, 50, 8)}
{inner}
</svg>'''

def header(label, sub, color=CYAN):
    return (f'<text x="40" y="48" font-family="{MONO}" font-size="15" fill="{color}" letter-spacing="3">{esc(label)}</text>'
            f'<text x="1160" y="48" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTED}">{esc(sub)}</text>')

# ---------------- TIMELINE ----------------
TW, TH = 1200, 560
RAIL_Y = 262
epochs = [
    ("study", "Jun 2019 – Jun 2023", "B.Tech. Computer Science", "SRM Institute of Science & Tech.", "8.42 CGPA · software dev + ML"),
    ("work",  "Oct – Nov 2020",      "Technical Content Writer", "Oyesters Training · Remote", "Tech articles & documentation"),
    ("work",  "Jun 2023 – Feb 2024", "Software Developer Trainee", "EQG Glassmach · India", "Built order-management software"),
    ("work",  "Mar – Sep 2024",      "Associate Engineer", "Brillio · Bengaluru", "+30% efficiency · microservices"),
    ("work",  "Sep 2024 – Jul 2025", "Software Developer", "EQG Glassmach · India", "Architected a company-wide OMS"),
    ("now",   "Aug 2025 – present",  "M.S. Computer Science", "Arizona State University", "Distributed systems & AI"),
]
CARD_W, CARD_H = 300, 118
tl = [header("TRAINING_HISTORY.log", "epochs: 2019 → now"),
      f'<path id="rail" d="M40,{RAIL_Y} L1160,{RAIL_Y}" stroke="url(#rail)" stroke-width="2" opacity="0.7"/>']
for k, (b, d) in enumerate(((0, 7), (3.5, 7))):
    tl.append(f'<circle r="{4 - k}" fill="{PINK if k == 0 else CYAN}" filter="url(#glow)">'
              f'<animateMotion dur="{d}s" begin="{b}s" repeatCount="indefinite"><mpath href="#rail"/></animateMotion></circle>')
for i, (kind, date, title, org, note) in enumerate(epochs):
    x = 110 + i * 196
    color = {"study": CYAN, "work": VIOLET, "now": PINK}[kind]
    above = i % 2 == 0
    cx = min(max(x - CARD_W / 2, 30), 1170 - CARD_W)
    cy = RAIL_Y - 44 - CARD_H if above else RAIL_Y + 44
    stem_y = cy + CARD_H if above else cy
    delay = i * 0.35
    tl.append(f'<g class="rise" style="animation-delay:{delay:.2f}s">')
    tl.append(f'<line x1="{x}" y1="{RAIL_Y}" x2="{x}" y2="{stem_y}" stroke="{color}" stroke-opacity="0.5" stroke-dasharray="3 4"/>')
    tl.append(f'<rect x="{cx:.0f}" y="{cy}" width="{CARD_W}" height="{CARD_H}" rx="12" fill="{BG}" fill-opacity="0.85" stroke="{color}" stroke-opacity="0.55"/>')
    tl.append(f'<rect x="{cx:.0f}" y="{cy}" width="4" height="{CARD_H}" rx="2" fill="{color}"/>')
    tx = cx + 20
    tl.append(f'<text x="{tx:.0f}" y="{cy + 26}" font-family="{MONO}" font-size="12.5" fill="{color}" letter-spacing="1">{esc(date.upper())}</text>')
    tl.append(f'<text x="{tx:.0f}" y="{cy + 52}" font-family="{SANS}" font-size="19" font-weight="700" fill="{TEXT}">{esc(title)}</text>')
    tl.append(f'<text x="{tx:.0f}" y="{cy + 75}" font-family="{SANS}" font-size="14.5" fill="{TEXT}" opacity="0.65">{esc(org)}</text>')
    tl.append(f'<text x="{tx:.0f}" y="{cy + 100}" font-family="{MONO}" font-size="12.5" fill="{TEXT}" opacity="0.85">› {esc(note)}</text>')
    tl.append('</g>')
    if kind == "now":
        tl.append(f'<circle cx="{x}" cy="{RAIL_Y}" r="10" fill="none" stroke="{color}" stroke-width="2">'
                  f'<animate attributeName="r" values="8;22" dur="1.8s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values="0.9;0" dur="1.8s" repeatCount="indefinite"/></circle>')
    tl.append(node((x, RAIL_Y), color, r=7, delay=delay))
# legend + awards
leg_y = 488
tl.append(f'<line x1="40" y1="{leg_y - 34}" x2="1160" y2="{leg_y - 34}" stroke="#fff" stroke-opacity="0.07"/>')
tl.append(f'<text x="40" y="{leg_y - 8}" font-family="{MONO}" font-size="13" fill="{AMBER}" letter-spacing="3">BENCHMARKS</text>')
awards = [("🏆", "1st place", "Hack-A-Code · 35 teams"), ("🥇", "Top 5", "HackBMU 4.0"), ("⭐", "Top 25", "Zeta Hacks · 200+ teams")]
ax = 40
for i, (ic, rank, ev) in enumerate(awards):
    w = 350
    tl.append(f'<g class="rise" style="animation-delay:{2.2 + i*0.3:.1f}s">'
              f'<rect x="{ax}" y="{leg_y + 6}" width="{w}" height="44" rx="22" fill="{AMBER}" fill-opacity="0.08" stroke="{AMBER}" stroke-opacity="0.45"/>'
              f'<text x="{ax + 22}" y="{leg_y + 35}" font-size="19">{ic}</text>'
              f'<text x="{ax + 54}" y="{leg_y + 34}" font-family="{SANS}" font-size="16" font-weight="700" fill="{AMBER}">{esc(rank)}</text>'
              f'<text x="{ax + 54 + len(rank) * 9 + 8:.0f}" y="{leg_y + 34}" font-family="{SANS}" font-size="15" fill="{TEXT}" opacity="0.8">{esc(ev)}</text></g>')
    ax += w + 25
for j, (lbl, c) in enumerate((("study", CYAN), ("work", VIOLET), ("now", PINK))):
    lx = 900 + j * 90
    tl.append(f'<circle cx="{lx}" cy="{leg_y - 13}" r="5" fill="{c}"/><text x="{lx + 12}" y="{leg_y - 8}" font-family="{MONO}" font-size="12.5" fill="{MUTED}">{lbl}</text>')
RISE = '''<style>.rise { animation: rise .9s ease-out both } @keyframes rise { from { opacity: 0; transform: translateY(10px) } to { opacity: 1; transform: none } }</style>'''
open(f"{OUT}/timeline.svg", "w").write(frame(TW, TH, "Manas Khare: career and education timeline", RISE + "\n".join(tl)))

# ---------------- NOW / STATUS ----------------
NW, NH = 1200, 330
panels = [
    ("TRAINING", CYAN, "🎓", "M.S. CS @ ASU", "distributed systems + AI"),
    ("EXPLORING", PINK, "🧠", "Vision Transformers", "Whisper · RAG · LoRA"),
    ("SHIPPING", VIOLET, "🚀", "Nocturne", "portfolio under a real night sky"),
    ("OFF-DUTY", AMBER, "🔭", "Stargazing", "soundtracks & good stories"),
]
nw = [f'<rect x="20" y="20" width="1160" height="46" rx="12" fill="#fff" fill-opacity="0.03"/>',
      "".join(f'<circle cx="{46 + k*22}" cy="43" r="6" fill="{c}" opacity="0.85"/>' for k, c in enumerate(("#f87171", AMBER, GREEN))),
      f'<text x="130" y="48" font-family="{MONO}" font-size="15" fill="{TEXT}" opacity="0.8">manas@asu:~$ <tspan fill="{CYAN}">watch</tspan> status --live</text>',
      f'<circle cx="1062" cy="43" r="5" fill="{GREEN}"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/></circle>',
      f'<text x="1160" y="48" text-anchor="end" font-family="{MONO}" font-size="13" fill="{GREEN}">LIVE</text>']
PW = 267
for i, (lbl, c, ic, main, sub) in enumerate(panels):
    px = 30 + i * (PW + 13)
    py = 86
    nw.append(f'<g class="rise" style="animation-delay:{i*0.25:.2f}s">'
              f'<rect x="{px}" y="{py}" width="{PW}" height="168" rx="14" fill="{c}" fill-opacity="0.05" stroke="{c}" stroke-opacity="0.4"/>'
              f'<text x="{px + 20}" y="{py + 30}" font-family="{MONO}" font-size="12.5" fill="{c}" letter-spacing="3">{lbl}</text>'
              f'<text x="{px + PW - 20}" y="{py + 34}" text-anchor="end" font-size="24">{ic}</text>'
              f'<text x="{px + 20}" y="{py + 78}" font-family="{SANS}" font-size="22" font-weight="700" fill="{TEXT}">{esc(main)}</text>'
              f'<text x="{px + 20}" y="{py + 104}" font-family="{SANS}" font-size="14.5" fill="{TEXT}" opacity="0.65">{esc(sub)}</text>'
              f'<rect x="{px + 20}" y="{py + 132}" width="{PW - 40}" height="6" rx="3" fill="#fff" fill-opacity="0.08"/>'
              f'<rect x="{px + 20}" y="{py + 132}" width="0" height="6" rx="3" fill="{c}" filter="url(#glow)">'
              f'<animate attributeName="width" values="0;{PW - 40};{PW - 40};0" keyTimes="0;0.6;0.9;1" dur="{4 + i*0.7:.1f}s" repeatCount="indefinite"/></rect>'
              f'</g>')
ticker = "  ✦  ".join(["loss ↓  curiosity ↑", "shipping full-stack + ML", "open to SWE roles", "coffee: brewing ☕",
                       "last seen: under a dark sky", "backprop through bugs", "forward_pass(idea) → product"])
nw.append(f'<clipPath id="tk"><rect x="20" y="272" width="1160" height="40"/></clipPath>'
          f'<rect x="20" y="272" width="1160" height="40" rx="10" fill="#fff" fill-opacity="0.03"/>'
          f'<g clip-path="url(#tk)"><text y="298" font-family="{MONO}" font-size="14" fill="{MUTED}">'
          f'<tspan x="40">{esc(ticker)}  ✦  {esc(ticker)}</tspan>'
          f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-{len(ticker) * 8.4 + 43:.0f} 0" dur="28s" repeatCount="indefinite"/></text></g>')
open(f"{OUT}/now.svg", "w").write(frame(NW, NH, "What Manas is up to right now", RISE + "\n".join(nw)))

# ---------------- STACK / WEIGHTS MATRIX ----------------
layers = [
    ("AI / ML", CYAN, ["LLM Apps", "Embeddings & RAG", "PyTorch", "TensorFlow", "Vision Transformers", "Whisper", "LoRA Fine-tuning"]),
    ("Frontend", PINK, ["React", "TypeScript", "Next.js", "Tailwind", "Three.js", "D3", "HTML / CSS"]),
    ("Backend", VIOLET, ["Node / Express", "Spring Boot", "FastAPI", "Socket.IO", "PostgreSQL", "MySQL", "MongoDB", "Prisma"]),
    ("Languages", AMBER, ["Python", "Java", "JavaScript", "TypeScript", "C / C++", "SQL"]),
    ("Cloud & DevOps", GREEN, ["Docker", "GitHub Actions", "Microservices", "Redis", "AWS", "Oracle Cloud", "Linux"]),
]
SW = 1200
ROW_H, X0, XMAX, CH_W = 64, 250, 1165, 8.3
rows, y = [], 100
for li, (name, c, skills) in enumerate(layers):
    # wrap pills into lines
    widths = [len(s) * CH_W + 40 for s in skills]
    n_lines = 1
    while True:  # balance pills evenly across the fewest lines that fit
        per = -(-len(skills) // n_lines)
        chunks = [list(zip(skills[i:i + per], widths[i:i + per])) for i in range(0, len(skills), per)]
        if all(X0 + sum(w for _, w in ch) + 12 * (len(ch) - 1) <= XMAX for ch in chunks): break
        n_lines += 1
    lines = []
    for chunk in chunks:
        x, line = X0, []
        for s, w in chunk:
            line.append((s, x, w)); x += w + 12
        lines.append(line)
    block_h = ROW_H * len(lines)
    mid = y + block_h / 2 - ROW_H / 2 + 20
    rows.append(f'<g class="rise" style="animation-delay:{li*0.2:.1f}s">')
    rows.append(f'<rect x="30" y="{mid - 20:.0f}" width="190" height="40" rx="20" fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-opacity="0.6"/>'
                f'<text x="48" y="{mid + 5:.0f}" font-family="{MONO}" font-size="12" fill="{c}" opacity="0.7">L{li+1}</text>'
                f'<text x="76" y="{mid + 5:.0f}" font-family="{SANS}" font-size="15.5" font-weight="700" fill="{TEXT}">{esc(name)}</text>')
    for k, line in enumerate(lines):
        ly = y + k * ROW_H + 20
        end = line[-1][1] + line[-1][2]
        pid = f"r{li}_{k}"
        rows.append(f'<path id="{pid}" d="M220,{mid:.0f} C235,{mid:.0f} 230,{ly} {X0},{ly} L{end:.0f},{ly}" stroke="{c}" stroke-opacity="0.3" fill="none"/>')
        rows.append(f'<circle r="3" fill="{c}" filter="url(#glow)"><animateMotion dur="{3.5 + li*0.4 + k*0.3:.1f}s" begin="{li*0.3:.1f}s" repeatCount="indefinite"><mpath href="#{pid}"/></animateMotion></circle>')
        for s, sx, w in line:
            rows.append(f'<rect x="{sx:.0f}" y="{ly - 17}" width="{w:.0f}" height="34" rx="17" fill="{BG}" stroke="{c}" stroke-opacity="0.45"/>'
                        f'<circle cx="{sx + 17:.0f}" cy="{ly}" r="4" fill="{c}"/>'
                        f'<text x="{sx + 29:.0f}" y="{ly + 5}" font-family="{MONO}" font-size="14" fill="{TEXT}">{esc(s)}</text>')
    rows.append('</g>')
    y += block_h + 14
SH = int(y + 20)
open(f"{OUT}/stack.svg", "w").write(frame(SW, SH, "Manas Khare's tech stack",
     RISE + header("WEIGHTS.matrix", f"{sum(len(l[2]) for l in layers)} parameters · {len(layers)} layers", VIOLET) + "\n".join(rows)))
print("ok")
