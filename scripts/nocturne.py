"""Shared palette and drawing helpers for the Nocturne profile SVGs."""
import random

BG, BG2 = "#03040b", "#0e1330"
GOLD, SILVER, ROSE, SEA = "#f5d58a", "#9fb4ff", "#e8a0bf", "#8fd3c1"
TEXT, SOFT, MUTED, FAINT = "#efe9dc", "#b9bdd0", "#7d839e", "#262c48"
STARLIGHT = "#e8e6ff"
SERIF = "Georgia, 'Times New Roman', 'DejaVu Serif', serif"
SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def glow(fid="glow", s=3):
    return (f'<filter id="{fid}" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="{s}" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def sparkle(x, y, s, color=STARLIGHT, op=1.0, twinkle=None):
    """Four-pointed star centred on (x, y); twinkle=(dur, begin) animates it."""
    d = (f"M{x:.1f},{y - s:.1f} Q{x:.1f},{y:.1f} {x + s:.1f},{y:.1f} Q{x:.1f},{y:.1f} {x:.1f},{y + s:.1f} "
         f"Q{x:.1f},{y:.1f} {x - s:.1f},{y:.1f} Q{x:.1f},{y:.1f} {x:.1f},{y - s:.1f} Z")
    anim = ""
    if twinkle:
        dur, begin = twinkle
        anim = (f'<animate attributeName="opacity" values="{op};{op * 0.25:.2f};{op}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>')
    return f'<path d="{d}" fill="{color}" opacity="{op}">{anim}</path>'


def sky(w, h, seed, n=70, twinkle=10, band=True):
    """Night-sky background: gradient, faint milky-way band and scattered stars."""
    rnd = random.Random(seed)
    out = [f'<rect width="{w}" height="{h}" rx="18" fill="url(#skyg)"/>']
    if band:
        out.append(f'<ellipse cx="{w * 0.55:.0f}" cy="{h * 0.45:.0f}" rx="{w * 0.6:.0f}" ry="{h * 0.16:.0f}" fill="{SILVER}" '
                   f'opacity="0.05" transform="rotate(-12 {w * 0.55:.0f} {h * 0.45:.0f})" filter="url(#haze)"/>')
    for i in range(n):
        x, y = rnd.uniform(8, w - 8), rnd.uniform(8, h - 8)
        r = rnd.choice([0.5, 0.7, 0.9, 1.1, 1.4])
        op = rnd.uniform(0.25, 0.8)
        col = GOLD if rnd.random() < 0.15 else STARLIGHT
        if i < twinkle:
            out.append(sparkle(x, y, r * 3.2, col, round(op, 2), (round(rnd.uniform(2.5, 6), 1), round(rnd.uniform(0, 4), 1))))
        else:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}" opacity="{op:.2f}"/>')
    return "\n".join(out)


def plate_border(w, h):
    """Double hairline frame with sparkles at the corners, like an old star-atlas plate."""
    out = [f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" rx="12" fill="none" stroke="{GOLD}" stroke-opacity="0.35"/>',
           f'<rect x="17" y="17" width="{w - 34}" height="{h - 34}" rx="8" fill="none" stroke="{GOLD}" stroke-opacity="0.12"/>']
    for cx, cy in ((17, 17), (w - 17, 17), (17, h - 17), (w - 17, h - 17)):
        out.append(sparkle(cx, cy, 6, GOLD, 0.8))
    return "".join(out)


def svg(w, h, title, inner, seed=1, defs="", stars=70, twinkle=10, band=True, plate=False):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title><defs>'
            f'<radialGradient id="skyg" cx="50%" cy="0%" r="110%"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></radialGradient>'
            f'<filter id="haze" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>'
            f'{glow()}{glow("softglow", 5)}'
            '<style>.rise{animation:rise 1.1s ease-out both}@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}</style>'
            f'{defs}</defs>{sky(w, h, seed, stars, twinkle, band)}{plate_border(w, h) if plate else ""}{inner}</svg>')


def caps(x, y, text, color=GOLD, size=12, anchor="start", spacing=4, op=1.0):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{SANS}" font-size="{size}" fill="{color}" '
            f'letter-spacing="{spacing}" opacity="{op}">{esc(text.upper())}</text>')


def header(numeral, title, right=""):
    return (caps(44, 54, f"{numeral} · {title}", GOLD, 13, spacing=5) +
            (caps(1156, 54, right, MUTED, 11, "end", 3) if right else "") +
            f'<line x1="44" y1="70" x2="1156" y2="70" stroke="{GOLD}" stroke-opacity="0.12"/>')
