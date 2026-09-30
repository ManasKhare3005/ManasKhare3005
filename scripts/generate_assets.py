"""Generates the Nocturne SVGs in ../assets. Run: python3 scripts/generate_assets.py"""
import math
import os

from nocturne import (BG, GOLD, SILVER, TEXT, SOFT, MUTED, SERIF, SANS,
                      esc, sparkle, svg, caps, header)

OUT = os.environ.get("ASSETS_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets"))


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


def constellation(points, edges, color=SILVER, star=GOLD, pid=None, labels=None, travel=None):
    """Stars joined by hairlines. labels: {index: (text, dx, dy, anchor)}; pid adds a light travelling the lines."""
    out = []
    for a, b in edges:
        (x1, y1), (x2, y2) = points[a], points[b]
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-opacity="0.45" stroke-width="1"/>')
    for i, (x, y) in enumerate(points):
        big = labels and i in labels
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{9 if big else 6}" fill="{star}" opacity="0.10" filter="url(#glow)"/>')
        out.append(sparkle(x, y, 7 if big else 4.5, star, 1.0 if big else 0.85, (round(3 + (i % 3) * 0.8, 1), round(i * 0.45, 2))))
        if big:
            text, dx, dy, anchor = labels[i]
            out.append(f'<text x="{x + dx:.0f}" y="{y + dy:.0f}" text-anchor="{anchor}" font-family="{SERIF}" font-style="italic" '
                       f'font-size="15" fill="{SOFT}">{esc(text)}</text>')
    if pid:
        d = "M" + " L".join(f"{points[a][0]:.1f},{points[a][1]:.1f} {points[b][0]:.1f},{points[b][1]:.1f}" for a, b in edges)
        out.append(f'<path id="{pid}" d="{d}" fill="none" stroke="none"/>'
                   f'<circle r="2.2" fill="{GOLD}" filter="url(#glow)"><animateMotion dur="{travel or 8}s" repeatCount="indefinite">'
                   f'<mpath href="#{pid}"/></animateMotion></circle>')
    return "".join(out)


def crescent(cx, cy, r, mid, phase_dx, color=GOLD, halo=True):
    """Moon; phase_dx is how far the shadow disc is shifted (small = thin crescent, >= 2r = full)."""
    out = [f'<mask id="{mid}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>'
           f'<circle cx="{cx + phase_dx}" cy="{cy - phase_dx * 0.15:.1f}" r="{r * 0.96:.1f}" fill="#000"/></mask>']
    if halo:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 1.9:.0f}" fill="{color}" opacity="0.07" filter="url(#softglow)"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-opacity="0.25"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" mask="url(#{mid})" filter="url(#glow)"/>')
    return "".join(out)


def shooting_star(x, y, dx, dy, dur, begin, length=110):
    ang = math.degrees(math.atan2(dy, dx))
    times = f"{begin}s"
    return (f'<g opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="0;0.03;0.1;1" dur="{dur}s" begin="{times}" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="{x} {y};{x + dx} {y + dy};{x + dx} {y + dy}" keyTimes="0;0.1;1" '
            f'dur="{dur}s" begin="{times}" repeatCount="indefinite"/>'
            f'<line x1="0" y1="0" x2="{-length}" y2="0" stroke="url(#trail)" stroke-width="1.6" stroke-linecap="round" transform="rotate({ang:.1f})"/>'
            f'<circle r="1.8" fill="#fff"/></g>')


TRAIL = ('<linearGradient id="trail" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.9"/>'
         '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')


def ornament(cx, y, half, color=GOLD):
    """Hairline, sparkle, hairline."""
    return (f'<line x1="{cx - half}" y1="{y}" x2="{cx - 14}" y2="{y}" stroke="{color}" stroke-opacity="0.35"/>'
            f'<line x1="{cx + 14}" y1="{y}" x2="{cx + half}" y2="{y}" stroke="{color}" stroke-opacity="0.35"/>' + sparkle(cx, y, 6, color, 0.9))


# ---------------- HERO ----------------
def hero():
    W, H = 1200, 470
    left = [(92, 112), (178, 158), (66, 246), (206, 262), (118, 366), (232, 346)]
    right = [(1108, 104), (1018, 166), (1136, 236), (994, 276), (1092, 362), (972, 380)]
    inner = [
        constellation(left, [(0, 1), (1, 3), (3, 2), (3, 5), (5, 4)], pid="cl",
                      labels={0: ("AI · LLMs", 0, -18, "middle"), 2: ("Agents", 0, 30, "middle"), 4: ("Full-Stack", 0, 30, "middle")}),
        constellation(right, [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5)], pid="cr", travel=9,
                      labels={0: ("Cloud", 0, -18, "middle"), 2: ("FinTech", 0, 30, "middle"), 4: ("HealthTech", 0, 30, "middle")}),
        crescent(880, 92, 24, "moon", 11),
        shooting_star(330, 40, 260, 90, 9, 2),
        shooting_star(760, 30, 220, 70, 13, 6.5, 90),
        '<g text-anchor="middle">',
        f'<g class="rise">{caps(600, 128, "I · Prelude", GOLD, 13, "middle", 6, 0.85)}</g>',
        f'<g class="rise" style="animation-delay:.25s"><text x="600" y="206" text-anchor="middle" font-family="{SERIF}" font-size="76" fill="{GOLD}" '
        f'letter-spacing="1" filter="url(#softglow)">Manas Khare</text></g>',
        f'<g class="rise" style="animation-delay:.5s"><text x="600" y="246" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="21" fill="{SILVER}">'
        f'Full-Stack Engineer · ML / AI</text></g>',
        f'<g class="rise" style="animation-delay:.7s">{ornament(600, 274, 120)}</g>',
        f'<g class="rise" style="animation-delay:.9s"><text x="600" y="310" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="16.5" fill="{SOFT}">'
        f'“I build software the way I watch the night sky: patiently, curiously, one small light at a time.”</text></g>',
        f'<g class="rise" style="animation-delay:1.1s"><text x="600" y="346" text-anchor="middle" font-family="{SANS}" font-size="14.5" fill="{MUTED}">'
        f'M.S. Computer Science · Arizona State University</text></g>',
        f'<g class="rise" style="animation-delay:1.3s">'
        f'<rect x="425" y="372" width="350" height="34" rx="17" fill="{GOLD}" fill-opacity="0.06" stroke="{GOLD}" stroke-opacity="0.35"/>'
        + sparkle(449, 389, 6, GOLD, 1, (2.2, 0)) +
        f'{caps(612, 393, "open to software engineering roles", GOLD, 11, "middle", 2)}</g>',
        '</g>',
    ]
    write("hero.svg", svg(W, H, "Manas Khare, Full-Stack Engineer and ML / AI", "".join(inner), seed=11, defs=TRAIL, stars=110, twinkle=16))


# ---------------- DIVIDER ----------------
def divider():
    W, H = 1200, 44
    dots = "".join(f'<circle cx="{600 + s * (60 + i * 55)}" cy="22" r="{1.6 - i * 0.14:.2f}" fill="{GOLD}" opacity="{0.7 - i * 0.07:.2f}"/>'
                   for i in range(9) for s in (-1, 1))
    inner = (f'<defs><linearGradient id="dl" x1="0" x2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/>'
             f'<stop offset="0.5" stop-color="{GOLD}" stop-opacity="0.5"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>'
             f'<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3" result="b"/>'
             f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
             f'<line x1="40" y1="22" x2="1160" y2="22" stroke="url(#dl)"/>{dots}'
             f'<circle cx="600" cy="22" r="12" fill="{GOLD}" opacity="0.08" filter="url(#glow)"/>'
             + sparkle(600, 22, 9, GOLD, 1, (3, 0)) + sparkle(574, 22, 3.5, GOLD, 0.7, (3, 1)) + sparkle(626, 22, 3.5, GOLD, 0.7, (3, 1.5)))
    write("divider.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="divider">{inner}</svg>')


# ---------------- PROJECT PLATES ----------------
def plate(fname, seed, numeral, domain, title, lines, tags, shape, edges, fig, link):
    W, H = 1200, 262
    cx, cy = 158, 118
    ticks = "".join(
        f'<line x1="{cx + 88 * math.cos(math.radians(a)):.1f}" y1="{cy + 88 * math.sin(math.radians(a)):.1f}" '
        f'x2="{cx + (96 if a % 30 == 0 else 92) * math.cos(math.radians(a)):.1f}" y2="{cy + (96 if a % 30 == 0 else 92) * math.sin(math.radians(a)):.1f}" '
        f'stroke="{GOLD}" stroke-opacity="0.35"/>' for a in range(0, 360, 10))
    pts = [(cx + x, cy + y) for x, y in shape]
    lens = (f'<circle cx="{cx}" cy="{cy}" r="84" fill="{BG}" fill-opacity="0.6" stroke="{GOLD}" stroke-opacity="0.3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="56" fill="none" stroke="{SILVER}" stroke-opacity="0.08" stroke-dasharray="2 5"/>'
            f'<line x1="{cx - 84}" y1="{cy}" x2="{cx + 84}" y2="{cy}" stroke="{SILVER}" stroke-opacity="0.06"/>'
            f'<line x1="{cx}" y1="{cy - 84}" x2="{cx}" y2="{cy + 84}" stroke="{SILVER}" stroke-opacity="0.06"/>'
            f'<g>{ticks}<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="90s" repeatCount="indefinite"/></g>'
            + constellation(pts, edges, pid=f"p{seed}", travel=6) +
            f'<text x="{cx}" y="{cy + 118}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="13" fill="{MUTED}">{esc(fig)}</text>')
    x = 310
    body = "".join(f'<text x="{x}" y="{142 + i * 27}" font-family="{SERIF}" font-style="italic" font-size="18.5" fill="{SOFT}">{esc(l)}</text>'
                   for i, l in enumerate(lines))
    text = (f'<text x="1130" y="222" text-anchor="end" font-family="{SERIF}" font-size="190" fill="{GOLD}" opacity="0.05">{numeral}</text>' +
            caps(x, 62, f"Plate {numeral} · {domain}", GOLD, 12, spacing=5) +
            f'<text x="{x}" y="106" font-family="{SERIF}" font-size="38" fill="{TEXT}">{esc(title)}</text>' + body +
            caps(x, 212, "  ✦  ".join(tags), SILVER, 11.5, spacing=3, op=0.9) +
            (f'<text x="1152" y="62" text-anchor="end" font-family="{SERIF}" font-style="italic" font-size="15" fill="{GOLD}">view repository ↗</text>' if link else ""))
    write(fname, svg(W, H, f"{title}: {' '.join(lines)}", lens + text, seed=seed, stars=45, twinkle=6, band=False, plate=True))


# ---------------- TONIGHT (status) ----------------
def tonight():
    W, H = 1200, 330
    items = [("Studying", "M.S. CS @ ASU", "distributed systems & AI", 12),
             ("Exploring", "Vision Transformers", "Whisper · RAG · LoRA", 22),
             ("Shipping", "Nocturne", "a portfolio under the real sky", 32),
             ("Off-duty", "Stargazing", "soundtracks & good stories", 60)]
    cw = 1112 / 4
    parts = [header("II", "Tonight", "observed from Arizona")]
    for i, (lbl, main, sub, phase) in enumerate(items):
        cx = round(44 + cw * i + cw / 2)
        if i:
            parts.append(f'<line x1="{44 + cw * i:.0f}" y1="100" x2="{44 + cw * i:.0f}" y2="258" stroke="{GOLD}" stroke-opacity="0.12"/>')
        parts.append(f'<g class="rise" style="animation-delay:{i * 0.25:.2f}s">'
                     + crescent(cx, 124, 20, f"ph{i}", phase, halo=(i == 3)) +
                     caps(cx, 178, lbl, GOLD, 11.5, "middle", 4) +
                     f'<text x="{cx}" y="214" text-anchor="middle" font-family="{SERIF}" font-size="23" fill="{TEXT}">{esc(main)}</text>'
                     f'<text x="{cx}" y="242" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="15" fill="{MUTED}">{esc(sub)}</text></g>')
    parts.append(ornament(600, 282, 200) +
                 f'<text x="600" y="310" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="15" fill="{SOFT}">'
                 f'Clear skies tonight · every instrument calibrated</text>')
    write("now.svg", svg(W, H, "Tonight: studying at ASU, exploring vision transformers, shipping Nocturne, stargazing", "".join(parts), seed=21, stars=60))


# ---------------- JOURNEY (timeline) ----------------
def journey():
    W, H = 1200, 648
    epochs = [
        ("Jun 2019 – Jun 2023", "B.Tech. Computer Science", "SRM Institute of Science & Tech.", "8.42 CGPA · software dev + ML"),
        ("Oct – Nov 2020", "Technical Content Writer", "Oyesters Training · Remote", "engineering articles & docs"),
        ("Jun 2023 – Feb 2024", "Software Developer Trainee", "EQG Glassmach · India", "built order-management software"),
        ("Mar – Sep 2024", "Associate Engineer", "Brillio · Bengaluru", "+30% app efficiency · microservices"),
        ("Sep 2024 – Jul 2025", "Software Developer", "EQG Glassmach · India", "architected a company-wide OMS"),
        ("Aug 2025 – present", "M.S. Computer Science", "Arizona State University", "distributed systems & AI"),
        ("Jun 2026 – present", "Software Development Intern", "Ramsey Products Corp. · Remote", "legacy ASP → React/Node, zero data loss"),
    ]

    def arc_y(x):
        return 318 - 60 * math.sin(math.pi * (x - 40) / 1120)

    xs = [120 + i * 160 for i in range(len(epochs))]
    arc = "M40,318 " + " ".join(f"L{x},{arc_y(x):.1f}" for x in range(60, 1161, 20))
    parts = [header("III", "The journey", "2019 → now"),
             f'<path id="ecl" d="{arc}" fill="none" stroke="{GOLD}" stroke-opacity="0.35" stroke-dasharray="1 6" stroke-linecap="round"/>',
             f'<circle r="2.4" fill="{GOLD}" filter="url(#glow)"><animateMotion dur="12s" repeatCount="indefinite"><mpath href="#ecl"/></animateMotion></circle>']
    for i, ((date, title, org, note), x) in enumerate(zip(epochs, xs)):
        y = arc_y(x)
        now = i == len(epochs) - 1
        above = i % 2 == 0
        anchor = "start" if i == 0 else "end" if now else "middle"
        tx = x - 76 if i == 0 else x + 76 if now else x
        top = y - 150 if above else y + 42
        stem = (y - 18, top + 104) if above else (y + 18, top - 2)
        size = 6 + i * 0.75
        parts.append(f'<g class="rise" style="animation-delay:{i * 0.3:.1f}s">'
                     f'<line x1="{x}" y1="{stem[0]:.0f}" x2="{x}" y2="{stem[1]:.0f}" stroke="{GOLD}" stroke-opacity="0.22"/>'
                     + caps(tx, round(top + 14), date, GOLD, 11, anchor, 3) +
                     f'<text x="{tx}" y="{top + 44:.0f}" text-anchor="{anchor}" font-family="{SERIF}" font-size="19.5" fill="{TEXT}">{esc(title)}</text>'
                     f'<text x="{tx}" y="{top + 68:.0f}" text-anchor="{anchor}" font-family="{SERIF}" font-style="italic" font-size="15" fill="{SOFT}">{esc(org)}</text>'
                     f'<text x="{tx}" y="{top + 92:.0f}" text-anchor="{anchor}" font-family="{SANS}" font-size="13" fill="{MUTED}">{esc(note)}</text></g>')
        parts.append(f'<circle cx="{x}" cy="{y:.1f}" r="{size + 6:.0f}" fill="{GOLD}" opacity="0.10" filter="url(#glow)"/>')
        if now:
            parts.append(f'<circle cx="{x}" cy="{y:.1f}" r="10" fill="none" stroke="{GOLD}">'
                         f'<animate attributeName="r" values="10;26" dur="2.4s" repeatCount="indefinite"/>'
                         f'<animate attributeName="opacity" values="0.8;0" dur="2.4s" repeatCount="indefinite"/></circle>')
        parts.append(sparkle(x, y, size + 3, GOLD, 1, (round(3 + i * 0.3, 1), round(i * 0.4, 1))))
    parts.append(f'<line x1="44" y1="506" x2="1156" y2="506" stroke="{GOLD}" stroke-opacity="0.12"/>' + caps(44, 536, "Honours", GOLD, 12, spacing=5))
    honours = [("First place", "Design Experiences × Fulton Ambassadors Hackathon, ASU"), ("First place", "Hack-A-Code, among 35 teams"),
               ("Top 5", "HackBMU 4.0"), ("Top 25", "Zeta Hacks, of 200+ teams")]
    for i, (rank, ev) in enumerate(honours):
        hx, hy = 44 + (i % 2) * 560, 572 + (i // 2) * 40
        parts.append(f'<g class="rise" style="animation-delay:{2 + i * 0.3:.1f}s">' + sparkle(hx + 8, hy - 6, 7, GOLD, 1, (3, i)) +
                     f'<text x="{hx + 26}" y="{hy}" font-family="{SERIF}" font-size="18" fill="{GOLD}">{esc(rank)}'
                     f'<tspan font-style="italic" fill="{SOFT}" font-size="16" dx="10">{esc(ev)}</tspan></text></g>')
    write("timeline.svg", svg(W, H, "The journey: B.Tech at SRM, Oyesters, EQG Glassmach, Brillio, M.S. CS at ASU, Ramsey Products; honours at the Fulton hackathon, Hack-A-Code, HackBMU 4.0, Zeta Hacks",
                              "".join(parts), seed=31, stars=80))


# ---------------- INSTRUMENTS (stack) ----------------
def instruments():
    layers = [
        ("AI & ML", ["LLM Apps", "Embeddings & RAG", "PyTorch", "TensorFlow", "Vision Transformers", "Whisper", "LoRA Fine-tuning"]),
        ("Frontend", ["React", "TypeScript", "Next.js", "Tailwind", "Three.js", "D3", "HTML / CSS"]),
        ("Backend", ["Node / Express", "Spring Boot", "FastAPI", "Socket.IO", "PostgreSQL", "MySQL", "MongoDB", "Prisma"]),
        ("Languages", ["Python", "Java", "JavaScript", "TypeScript", "C / C++", "SQL"]),
        ("Cloud & DevOps", ["Docker", "GitHub Actions", "Microservices", "Redis", "AWS", "Oracle Cloud", "Linux"]),
    ]
    X0, XMAX, CH, GAP, LINE = 290, 1150, 8.8, 34, 34
    parts, y = [], 118
    for li, (name, skills) in enumerate(layers):
        widths = [len(s) * CH for s in skills]
        n = 1
        while True:  # fewest balanced lines that fit
            per = -(-len(skills) // n)
            chunks = [list(zip(skills[i:i + per], widths[i:i + per])) for i in range(0, len(skills), per)]
            if all(X0 + sum(w for _, w in ch) + GAP * (len(ch) - 1) <= XMAX for ch in chunks):
                break
            n += 1
        block = LINE * (len(chunks) - 1)
        mid = y + block / 2
        parts.append(f'<g class="rise" style="animation-delay:{li * 0.2:.1f}s">'
                     f'<text x="44" y="{mid - 4:.0f}" font-family="{SERIF}" font-style="italic" font-size="21" fill="{GOLD}">{esc(name)}</text>'
                     + caps(44, round(mid + 16), f"{len(skills)} instruments", MUTED, 10, spacing=3))
        for k, ch in enumerate(chunks):
            sep = f'<tspan dx="14" fill="{GOLD}" fill-opacity="0.75" font-size="12">✦</tspan>'
            parts.append(f'<text x="{X0}" y="{y + k * LINE:.0f}" font-family="{SANS}" font-size="16" fill="{TEXT}">'
                         + sep.join(f'<tspan dx="{14 if j else 0}">{esc(sk)}</tspan>' for j, (sk, _) in enumerate(ch)) + '</text>')
        parts.append('</g>')
        y += block + 40
        if li < len(layers) - 1:
            parts.append(f'<line x1="44" y1="{y - 6:.0f}" x2="1156" y2="{y - 6:.0f}" stroke="{GOLD}" stroke-opacity="0.08"/>')
        y += 36
    total = sum(len(s) for _, s in layers)
    write("stack.svg", svg(1200, int(y), "Instruments: AI & ML, Frontend, Backend, Languages, Cloud & DevOps",
                           header("V", "Instruments", f"{total} tools · 5 families") + "".join(parts), seed=41, stars=60))


# ---------------- SECTION TITLE + CODA ----------------
def section_title(fname, numeral, title, sub):
    inner = (caps(600, 50, f"{numeral} · {title}", GOLD, 13, "middle", 6) + ornament(600, 70, 150) +
             f'<text x="600" y="100" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="17" fill="{SOFT}">{esc(sub)}</text>')
    write(fname, svg(1200, 124, f"{title}: {sub}", inner, seed=sum(map(ord, title)), stars=40, twinkle=6, band=False))


def coda():
    inner = (crescent(600, 70, 20, "codamoon", 9) + caps(600, 132, "VIII · Coda", GOLD, 13, "middle", 6) +
             f'<text x="600" y="172" text-anchor="middle" font-family="{SERIF}" font-size="26" fill="{TEXT}">Recruiting, collaborating, or just curious?</text>'
             f'<text x="600" y="204" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="17" fill="{SOFT}">'
             f'Write to me. The letterbox is always open, even after dark.</text>'
             + shooting_star(200, 40, 240, 80, 10, 3))
    write("coda.svg", svg(1200, 236, "Coda: write to me", inner, seed=81, defs=TRAIL, stars=70))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    hero()
    divider()
    plate("project-stockintel.svg", 51, "I", "FinTech", "Stock Intel",
          ["AI-powered financial intelligence: market insights,", "interactive visualizations and data-driven analytics."],
          ["Python", "React", "APIs", "Machine Learning"],
          [(-62, 42), (-34, 18), (-10, 30), (14, -2), (38, 8), (60, -44)], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
          "fig. I — the rising line", False)
    plate("project-resumify.svg", 52, "II", "Careers", "Resumify",
          ["An AI resume optimizer that lifts ATS compatibility", "and recruiter appeal: good resumes, made great."],
          ["React", "Node.js", "Express", "OpenAI"],
          [(-38, -52), (18, -52), (40, -30), (40, 52), (-38, 52), (18, -30), (-20, -10), (22, -10), (-20, 14), (22, 14), (-20, 36), (6, 36)],
          [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 5), (5, 2), (6, 7), (8, 9), (10, 11)], "fig. II — the page", True)
    plate("project-curaconnect.svg", 53, "III", "HealthTech", "CuraConnect",
          ["A full-stack healthcare platform that improves", "communication between patients and providers."],
          ["MongoDB", "Express", "React", "Node.js"],
          [(0, 48), (-46, 4), (-44, -28), (-22, -44), (0, -24), (22, -44), (44, -28), (46, 4)],
          [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)], "fig. III — the heart", True)
    tonight()
    journey()
    instruments()
    section_title("section-projects.svg", "IV", "Constellations", "things I have built, one small light at a time")
    coda()
    print("ok")
