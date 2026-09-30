"""Anime-style Nocturne avatar. Run: python3 scripts/generate_avatar.py  ->  assets/avatar.svg

Tweak the look with the constants below (skin, eyes, hair), then export a PNG for GitHub:
  render assets/avatar.svg at 1024x1024 in any browser, or see README notes.
"""
import os
import random

from nocturne import GOLD, SILVER, sparkle

OUT = os.environ.get("ASSETS_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets"))

SKIN, SKIN_SHADE, SKIN_LIGHT = "#c98d62", "#a36a45", "#e2aa7e"
EYES, EYES_LIGHT = "#2b1a12", "#8a5a2b"
HAIR, HAIR_SHINE = "#15131d", "#3a3f73"
BEARD = "#2a1d18"
HOODIE, HOODIE_DARK, HOODIE_LINE = "#1d2445", "#131933", "#2d3668"
PHONES, PHONES_DARK = "#262d54", "#171c38"
INK = "#140f14"


def eye(x, y, s):
    """Anime eye; s=+1 puts the outer corner on the viewer's right, s=-1 on the left."""
    inner, outer = x - 40 * s, x + 44 * s
    return (
        f'<path d="M{inner},{y + 2} C{x - 28 * s},{y - 26} {x + 26 * s},{y - 30} {outer},{y - 8} '
        f'C{x + 34 * s},{y + 22} {x - 22 * s},{y + 26} {inner},{y + 2} Z" fill="#f6f1e9"/>'
        f'<ellipse cx="{x}" cy="{y + 2}" rx="23" ry="27" fill="url(#iris)"/>'
        f'<ellipse cx="{x}" cy="{y + 2}" rx="23" ry="27" fill="none" stroke="#120a06" stroke-width="2.5"/>'
        f'<path d="M{x - 23},{y - 4} Q{x},{y - 30} {x + 23},{y - 4} Q{x},{y - 16} {x - 23},{y - 4} Z" fill="#120a06" opacity="0.55"/>'
        f'<ellipse cx="{x}" cy="{y + 5}" rx="10" ry="13" fill="#0e0907"/>'
        f'<ellipse cx="{x + 8 * s}" cy="{y - 8}" rx="7.5" ry="8.5" fill="#fff"/>'
        f'<circle cx="{x - 8 * s}" cy="{y + 14}" r="3.2" fill="#fff" opacity="0.9"/>'
        f'<path d="M{inner - 4 * s},{y + 1} C{x - 28 * s},{y - 33} {x + 28 * s},{y - 37} {outer + 4 * s},{y - 10}" '
        f'fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round"/>'
        f'<path d="M{outer + 2 * s},{y - 10} L{outer + 15 * s},{y - 21}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
        f'<path d="M{x + 12 * s},{y + 23} Q{x + 30 * s},{y + 19} {outer},{y + 3}" fill="none" stroke="{INK}" stroke-width="3" opacity="0.6"/>'
    )


def build():
    rnd = random.Random(9)
    stars = "".join(
        sparkle(rnd.uniform(40, 984), rnd.uniform(40, 560), rnd.choice([3, 4, 5, 7]), GOLD if rnd.random() < 0.3 else "#e8e6ff",
                round(rnd.uniform(0.4, 0.95), 2), (round(rnd.uniform(2.5, 5), 1), round(rnd.uniform(0, 3), 1)))
        for _ in range(26))
    dots = "".join(f'<circle cx="{rnd.uniform(0, 1024):.0f}" cy="{rnd.uniform(0, 700):.0f}" r="{rnd.choice([0.8, 1.2, 1.6])}" '
                   f'fill="#fff" opacity="{rnd.uniform(0.2, 0.7):.2f}"/>' for _ in range(120))

    hair = ("M350,502 C330,432 330,362 360,300 C390,236 450,196 520,192 C600,190 668,228 690,300 C708,360 700,420 684,482 "
            "L660,442 C656,422 650,406 640,396 C640,420 632,440 618,454 C612,422 600,400 584,388 C584,412 574,434 556,446 "
            "C552,416 540,394 522,384 C516,410 500,430 480,438 C484,412 480,394 470,382 C458,406 440,426 418,436 "
            "C426,412 424,396 418,386 C404,412 390,442 372,472 C372,488 360,498 350,502 Z")
    spikes = ("M468,204 C498,172 540,160 584,166 C556,178 538,192 528,206 Z "
              "M640,224 C682,206 718,214 746,242 C716,242 700,254 692,272 Z "
              "M372,298 C352,284 330,284 310,294 C332,300 344,312 352,326 Z "
              "M560,194 C590,178 626,176 656,190 C630,194 616,204 606,216 Z")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024" role="img" aria-label="Anime-style avatar of Manas under a night sky">
<defs>
  <radialGradient id="sky" cx="62%" cy="18%" r="95%"><stop offset="0" stop-color="#1b2352"/><stop offset="0.55" stop-color="#0b1030"/><stop offset="1" stop-color="#03040b"/></radialGradient>
  <radialGradient id="moonglow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.22"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
  <radialGradient id="iris" cx="45%" cy="35%" r="75%"><stop offset="0" stop-color="{EYES_LIGHT}"/><stop offset="0.7" stop-color="{EYES}"/></radialGradient>
  <linearGradient id="face" x1="0" y1="0" x2="1" y2="0.3"><stop offset="0" stop-color="{SKIN_SHADE}"/><stop offset="0.35" stop-color="{SKIN}"/><stop offset="1" stop-color="{SKIN_LIGHT}"/></linearGradient>
  <linearGradient id="hood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{HOODIE_DARK}"/><stop offset="0.6" stop-color="{HOODIE}"/><stop offset="1" stop-color="{HOODIE_LINE}"/></linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <linearGradient id="stubble" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BEARD}" stop-opacity="0.25"/><stop offset="0.5" stop-color="{BEARD}" stop-opacity="0.6"/><stop offset="1" stop-color="{BEARD}" stop-opacity="0.75"/></linearGradient>
  <filter id="haze"><feGaussianBlur stdDeviation="40"/></filter>
  <mask id="moonmask"><circle cx="790" cy="215" r="74" fill="#fff"/><circle cx="822" cy="196" r="70" fill="#000"/></mask>
</defs>

<rect width="1024" height="1024" fill="url(#sky)"/>
<ellipse cx="560" cy="330" rx="620" ry="120" fill="{SILVER}" opacity="0.07" transform="rotate(-18 560 330)" filter="url(#haze)"/>
{dots}{stars}
<circle cx="776" cy="226" r="190" fill="url(#moonglow)"/>
<circle cx="790" cy="215" r="74" fill="{GOLD}" mask="url(#moonmask)" filter="url(#glow)"/>
<path d="M170,160 L260,190 L300,120 L380,150" fill="none" stroke="{SILVER}" stroke-opacity="0.35"/>
{sparkle(170, 160, 6, GOLD, 0.9)}{sparkle(260, 190, 5, GOLD, 0.9)}{sparkle(300, 120, 7, GOLD, 1)}{sparkle(380, 150, 5, GOLD, 0.9)}
<ellipse cx="512" cy="1010" rx="520" ry="150" fill="{GOLD}" opacity="0.08" filter="url(#haze)"/>

<!-- hood behind the neck, headphone band behind the neck -->
<path d="M318,812 C330,716 414,682 512,682 C610,682 694,716 706,812 Z" fill="{HOODIE_DARK}"/>
<path d="M404,778 Q512,690 620,778" fill="none" stroke="{PHONES}" stroke-width="22" stroke-linecap="round"/>
<!-- neck -->
<path d="M452,630 L452,770 Q512,800 572,770 L572,630 Z" fill="{SKIN_SHADE}"/>
<path d="M452,664 Q512,730 572,664 L572,700 Q512,752 452,700 Z" fill="#8a5738" opacity="0.6"/>
<!-- hoodie body -->
<path d="M120,1024 C140,860 290,786 430,770 Q512,812 594,770 C734,786 884,860 904,1024 Z" fill="url(#hood)"/>
<path d="M594,770 C734,786 884,860 904,1024" fill="none" stroke="{GOLD}" stroke-opacity="0.55" stroke-width="4" filter="url(#glow)"/>
<!-- hoodie collar + headphone cups resting on it -->
<path d="M376,806 C386,748 448,726 512,726 C576,726 638,748 648,806 C604,786 562,778 512,778 C462,778 420,786 376,806 Z" fill="{HOODIE_DARK}"/>
<g transform="rotate(-38 404 784)"><ellipse cx="404" cy="784" rx="44" ry="56" fill="{PHONES_DARK}"/><ellipse cx="404" cy="784" rx="31" ry="41" fill="{PHONES}"/>
  <ellipse cx="404" cy="784" rx="31" ry="41" fill="none" stroke="{GOLD}" stroke-width="3" opacity="0.75"/><path d="M372,760 Q380,740 400,734" stroke="#fff" stroke-opacity="0.25" stroke-width="4" fill="none" stroke-linecap="round"/></g>
<g transform="rotate(38 620 784)"><ellipse cx="620" cy="784" rx="44" ry="56" fill="{PHONES_DARK}"/><ellipse cx="620" cy="784" rx="31" ry="41" fill="{PHONES}"/>
  <ellipse cx="620" cy="784" rx="31" ry="41" fill="none" stroke="{GOLD}" stroke-width="3" opacity="0.85" filter="url(#glow)"/></g>
<path d="M474,812 C470,850 466,880 462,912 M550,812 C554,850 558,880 562,912" stroke="#c9cbe0" stroke-width="5" stroke-linecap="round" fill="none"/>
<rect x="455" y="908" width="14" height="26" rx="4" fill="{GOLD}"/><rect x="555" y="908" width="14" height="26" rx="4" fill="{GOLD}"/>
<path d="M260,900 C300,880 330,900 360,960 M764,900 C724,880 694,900 664,960" stroke="{HOODIE_LINE}" stroke-width="4" fill="none" opacity="0.8"/>
{sparkle(628, 918, 14, GOLD, 0.95)}

<!-- ears -->
<ellipse cx="370" cy="478" rx="24" ry="40" fill="{SKIN_SHADE}"/><ellipse cx="374" cy="480" rx="11" ry="22" fill="#8a5738" opacity="0.6"/>
<ellipse cx="654" cy="478" rx="24" ry="40" fill="{SKIN}"/><ellipse cx="650" cy="480" rx="11" ry="22" fill="{SKIN_SHADE}" opacity="0.6"/>
<!-- face -->
<path d="M372,420 C372,560 424,648 512,690 C600,648 652,560 652,420 C652,300 590,252 512,252 C434,252 372,300 372,420 Z" fill="url(#face)"/>
<path d="M372,420 C372,560 424,648 512,690 C462,640 420,560 412,462 Z" fill="{SKIN_SHADE}" opacity="0.45"/>
<path d="M652,420 C652,560 600,648 512,690" fill="none" stroke="{GOLD}" stroke-width="4" stroke-opacity="0.8" filter="url(#glow)"/>
<!-- stubble / beard -->
<path d="M390,528 C398,610 452,672 512,692 C572,672 626,610 634,528 C616,596 572,634 512,640 C452,634 408,596 390,528 Z" fill="url(#stubble)"/>
<path d="M482,606 Q512,598 542,606 L538,612 Q512,606 486,612 Z" fill="{BEARD}" opacity="0.45"/>
<path d="M488,622 Q514,640 542,618" fill="none" stroke="#5e3526" stroke-width="4.5" stroke-linecap="round"/>
<path d="M542,618 l6,-4" stroke="#5e3526" stroke-width="3.5" stroke-linecap="round"/>
<!-- nose -->
<path d="M518,532 L508,576 Q514,584 526,578" fill="none" stroke="{SKIN_SHADE}" stroke-width="4" stroke-linecap="round"/>
<ellipse cx="434" cy="580" rx="26" ry="10" fill="#e8859a" opacity="0.14"/><ellipse cx="592" cy="580" rx="26" ry="10" fill="#e8859a" opacity="0.14"/>
<!-- eyes + brows -->
{eye(452, 506, -1)}{eye(572, 506, 1)}
<path d="M404,456 Q446,436 492,452" fill="none" stroke="{HAIR}" stroke-width="10" stroke-linecap="round"/>
<path d="M532,452 Q578,436 620,456" fill="none" stroke="{HAIR}" stroke-width="10" stroke-linecap="round"/>
<!-- glasses -->
<rect x="398" y="466" width="110" height="80" rx="24" fill="#cfe0ff" fill-opacity="0.07" stroke="#1b1a24" stroke-width="5.5"/>
<rect x="516" y="466" width="110" height="80" rx="24" fill="#cfe0ff" fill-opacity="0.07" stroke="#1b1a24" stroke-width="5.5"/>
<path d="M508,494 Q512,486 516,494" fill="none" stroke="#1b1a24" stroke-width="5"/>
<path d="M398,494 L372,484 M626,494 L652,484" stroke="#1b1a24" stroke-width="5" stroke-linecap="round"/>
<path d="M590,474 L608,474 L578,538 L560,538 Z" fill="#fff" opacity="0.18"/><path d="M612,478 L620,478 L596,530 L588,530 Z" fill="#fff" opacity="0.12"/>
<path d="M472,474 L486,474 L462,528 L448,528 Z" fill="#fff" opacity="0.10"/>
<rect x="516" y="466" width="110" height="80" rx="24" fill="none" stroke="{GOLD}" stroke-opacity="0.45" stroke-width="1.5"/>
{sparkle(606, 480, 9, "#fff", 0.9, (3.5, 0))}

<!-- hair -->
<path d="{hair}" fill="{HAIR}"/>
<path d="{spikes}" fill="{HAIR}"/>
<path d="M408,304 Q510,248 618,298" fill="none" stroke="{HAIR_SHINE}" stroke-width="10" stroke-linecap="round" opacity="0.5"/>
<path d="M438,292 Q452,270 470,262 M492,280 Q506,256 526,250 M548,278 Q566,258 586,254 M600,290 Q618,276 636,276" fill="none" stroke="#5a60a0" stroke-width="3.5" stroke-linecap="round" opacity="0.8"/>
<path d="M520,192 C600,190 668,228 690,300 C708,360 700,420 684,482" fill="none" stroke="{GOLD}" stroke-width="3.5" stroke-opacity="0.85" filter="url(#glow)"/>
<path d="M640,224 C682,206 718,214 746,242 M584,166 C556,178 538,192 528,206" fill="none" stroke="{GOLD}" stroke-width="2.5" stroke-opacity="0.75"/>
<circle cx="512" cy="512" r="500" fill="none" stroke="{GOLD}" stroke-opacity="0.35" stroke-width="3"/>
</svg>'''


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "avatar.svg"), "w") as f:
        f.write(build())
    print("ok")
