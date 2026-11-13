#!/usr/bin/env python3
"""Render the profile artwork into profile/assets/.

Standard library only. Run from anywhere:

    python3 tools/render_assets.py

Everything is drawn from three colours and one square. The typefaces are
system stacks on purpose: the site's heading face is commercial and is not
embedded or redistributed here.
"""

from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "profile" / "assets"

PAPER = "#f7f4ec"
INK = "#161512"
GOLD = "#cfab0a"

THEMES = {
    "light": {"bg": PAPER, "fg": INK, "muted": "#8a8154", "gold": "#af9209"},
    "dark": {"bg": INK, "fg": PAPER, "muted": "#918c76", "gold": GOLD},
}

SANS = "'Styrene A','Inter','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono',ui-monospace,'SFMono-Regular',Menlo,Consolas,monospace"

# The mark, on a 100-unit square: a solid block, a hollow, a bit in each.
MARK = "M0 0H100V100H0Z M50 10H90V90H50Z M22 42H38V58H22Z M62 42H78V58H62Z"


def smooth(a: float, b: float, x: float) -> float:
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def mark(x: float, y: float, size: float, fill: str) -> str:
    s = size / 100
    return (
        f'<path transform="translate({x} {y}) scale({s})" fill="{fill}" '
        f'fill-rule="evenodd" d="{MARK}"/>'
    )


def field(theme: str, w: int, h: int) -> str:
    """A lit sphere, set in squares. Size carries tone; nothing else does."""
    t = THEMES[theme]
    cell = 12
    cx0, cy0, r = 1012.0, 210.0, 150.0
    lx, ly, lz = -0.52, -0.60, 0.61
    ln = math.sqrt(lx * lx + ly * ly + lz * lz)
    lx, ly, lz = lx / ln, ly / ln, lz / ln

    # One bit stands apart from the body it belongs to.
    ang, dist = math.radians(-38), 1.34
    gx = round((cx0 + math.cos(ang) * r * dist) / cell)
    gy = round((cy0 + math.sin(ang) * r * dist) / cell)

    rects = []
    for j in range(h // cell):
        for i in range(w // cell):
            x, y = i * cell + cell / 2, j * cell + cell / 2
            if (i, j) == (gx, gy):
                continue
            dx, dy = (x - cx0) / r, (y - cy0) / r
            d2 = dx * dx + dy * dy
            if d2 < 1.0:
                z = math.sqrt(1 - d2)
                lam = max(0.0, dx * lx + dy * ly + z * lz)
                tone = lam if theme == "dark" else 1 - lam
                v = 0.10 + 0.84 * tone**1.15
            else:
                # The ground: a faint grid that thins towards the words.
                halo = math.exp(-((math.sqrt(d2) - 1) ** 2) * 3.2)
                v = (0.07 + 0.09 * halo) * smooth(540, 900, x)
            side = round(cell * v, 2)
            if side < 0.35:
                continue
            o = round(x - side / 2, 2), round(y - side / 2, 2)
            rects.append(f'<rect x="{o[0]}" y="{o[1]}" width="{side}" height="{side}"/>')

    bit = cell - 2
    gold = (
        f'<rect x="{gx * cell + 1}" y="{gy * cell + 1}" width="{bit}" '
        f'height="{bit}" fill="{t["gold"]}"/>'
    )
    return f'<g fill="{t["fg"]}">{"".join(rects)}</g>{gold}'


def ticks(w: int, h: int, colour: str) -> str:
    """Registration marks, as on a printed sheet."""
    m, n = 28, 10
    d = "".join(
        f"M{x} {y}h{sx * n}M{x} {y}v{sy * n}"
        for x, y, sx, sy in (
            (m, m, 1, 1),
            (w - m, m, -1, 1),
            (m, h - m, 1, -1),
            (w - m, h - m, -1, -1),
        )
    )
    return f'<path d="{d}" stroke="{colour}" stroke-width="1" fill="none"/>'


def banner(theme: str) -> str:
    t = THEMES[theme]
    w, h = 1280, 420
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
<title id="t">The Bit Trading Company</title>
<desc id="d">The company's mark and name beside a sphere drawn in small squares, with a single gold square set apart from it.</desc>
<rect width="{w}" height="{h}" fill="{t['bg']}"/>
{field(theme, w, h)}
{ticks(w, h, t['muted'])}
{mark(72, 84, 44, t['fg'])}
<text x="72" y="222" font-family="{SANS}" font-size="46" font-weight="500" letter-spacing="-0.6" fill="{t['fg']}" textLength="548" lengthAdjust="spacingAndGlyphs">The Bit Trading Company</text>
<text x="73" y="262" font-family="{MONO}" font-size="12.5" letter-spacing="2.6" fill="{t['muted']}">COMPANIES, BUILT FROM THE INSIDE AND KEPT</text>
<path d="M72 322H420" stroke="{t['fg']}" stroke-width="1"/>
<rect x="72" y="338" width="7" height="7" fill="{t['gold']}"/>
<text x="90" y="345" font-family="{MONO}" font-size="10.5" letter-spacing="2.4" fill="{t['muted']}">REGISTER OF WORKS  /  FOLIO I  /  N&#176; &#8212;</text>
</svg>
"""


def rule(theme: str) -> str:
    """A section rule: a hairline that ends in one bit."""
    t = THEMES[theme]
    w, h = 1280, 16
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="presentation">
<path d="M0 8H1262" stroke="{t['muted']}" stroke-width="1" opacity="0.55"/>
<rect x="1272" y="4" width="8" height="8" fill="{t['gold']}"/>
</svg>
"""


def standalone_mark(theme: str) -> str:
    t = THEMES[theme]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="96" height="96" role="img" aria-label="The Bit Trading Company">
<path fill="{t['fg']}" fill-rule="evenodd" d="{MARK}"/>
</svg>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        (OUT / f"banner-{theme}.svg").write_text(banner(theme))
        (OUT / f"rule-{theme}.svg").write_text(rule(theme))
        (OUT / f"mark-{theme}.svg").write_text(standalone_mark(theme))
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.relative_to(OUT.parent.parent)}  {p.stat().st_size / 1024:.1f} kB")


if __name__ == "__main__":
    main()
