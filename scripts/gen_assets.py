#!/usr/bin/env python3
"""Generate the animated dot-matrix banner (dark and light variants)."""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
W, H, GAP = 900, 240, 15
COLS, ROWS = W // GAP, H // GAP
PHRASES = ["Machine Learning · Data Science", "Software Engineering", "Building from Kigali, Rwanda"]
CYCLE = 3.2 * len(PHRASES)

THEMES = {
    "dark": {"dot": "#8b949e", "title": "#f0f6fc", "sub": "#8b949e"},
    "light": {"dot": "#57606a", "title": "#1f2328", "sub": "#57606a"},
}


def build(t):
    c = THEMES[t]
    dots = []
    for r in range(ROWS):
        for col in range(COLS):
            x = col * GAP + GAP / 2 + (W - COLS * GAP) / 2
            y = r * GAP + GAP / 2 + (H - ROWS * GAP) / 2
            delay = -((col * 0.07 + r * 0.05) % 4.2)
            dots.append(f'<circle class="d" cx="{x:.1f}" cy="{y:.1f}" r="1.6" style="animation-delay:{delay:.2f}s"/>')
    subs = []
    for i, p in enumerate(PHRASES):
        subs.append(
            f'<text class="s" x="{W/2}" y="{H/2+34}" text-anchor="middle" '
            f'style="animation-delay:{i*3.2:.1f}s">{p}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Eddy Irasetsa">
<defs>
<radialGradient id="g" cx="50%" cy="50%" r="55%">
<stop offset="0" stop-color="#000"/><stop offset="0.38" stop-color="#000"/><stop offset="0.75" stop-color="#fff"/>
</radialGradient>
<mask id="m"><rect width="{W}" height="{H}" fill="url(#g)"/></mask>
</defs>
<style>
.d{{fill:{c["dot"]};opacity:.15;animation:p 4.2s ease-in-out infinite}}
@keyframes p{{0%,100%{{opacity:.12;r:1.2px}}50%{{opacity:.95;r:2.6px}}}}
.t{{font:700 46px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:{c["title"]};letter-spacing:1px;opacity:0;animation:in 1.2s .2s forwards}}
@keyframes in{{from{{opacity:0}}to{{opacity:1}}}}
.s{{font:400 20px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:{c["sub"]};opacity:0;animation:r {CYCLE}s infinite}}
@keyframes r{{0%{{opacity:0}}4%{{opacity:1}}30%{{opacity:1}}34%,100%{{opacity:0}}}}
.c{{fill:{c["sub"]};animation:b 1s steps(1) infinite}}
@keyframes b{{50%{{opacity:0}}}}
</style>
<g mask="url(#m)">
{chr(10).join(dots)}
</g>
<text class="t" x="{W/2}" y="{H/2-6}" text-anchor="middle">Eddy Irasetsa</text>
{chr(10).join(subs)}
</svg>
'''


for name in THEMES:
    (OUT / f"banner-{name}.svg").write_text(build(name), encoding="utf-8")
print("generated")
