"""Build assets/gitlog-dark.svg and assets/gitlog-light.svg: a fake `git log --graph` of the last two years.

Usage: uv run --with fonttools --with brotli python make_gitlog.py fonts ../assets
"""
import base64, hashlib, io, pathlib, sys
from fontTools import subset
from fontTools.ttLib import TTFont

FONTS = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])

W = 960
X0 = 40
BAR = 44
ROW = 30
FS = 15
CW = FS * 0.6  # JetBrains Mono advance

THEMES = {
    "dark": dict(bg="#0D1117", bar="#161B22", line="#30363D", text="#E6EDF3", dim="#8B949E",
                 amber="#FFB000", lanes=["#FFB000", "#58A6FF", "#3FB950", "#D2A8FF", "#FF7B72"]),
    "light": dict(bg="#FFFFFF", bar="#F6F8FA", line="#D0D7DE", text="#1F2328", dim="#59636E",
                  amber="#9C5700", lanes=["#9C5700", "#0969DA", "#1A7F37", "#8250DF", "#CF222E"]),
}

# branch -> (lane, colour index)
BR = {"main": (0, 0), "road": (1, 2), "bosm": (2, 1), "rexops": (1, 4), "bench": (3, 3)}

# oldest first: (branch, refs, message, when, is_merge)
LOG = [
    ("main", "", "init: hello, pilani", "2 years ago", False),
    ("main", "", "chore: join SUTT, coffee++", "23 months ago", False),
    ("road", "", "infra: 8 phases of terraform, 0 console clicks", "10 months ago", False),
    ("main", "", "docs: write the CLAUDE.md before the code", "9 months ago", False),
    ("road", "", "feat: RGB-D model finds its first pothole in prod", "8 months ago", False),
    ("bosm", "", "feat: BOSM engine '26 boots on the first try", "7 months ago", False),
    ("main", "tag: road-v1", "Merge branch 'road-inspection'", "6 months ago", True),
    ("rexops", "", "feat: hard trust wall between agency and client", "5 months ago", False),
    ("bosm", "", "perf: registration day, zero 502s, p99 41ms", "4 months ago", False),
    ("bench", "", "sim: woz valley bank opens, bribes on the desk", "3 months ago", False),
    ("rexops", "", "feat: frame.io-grade approvals, block 8 of 8", "10 weeks ago", False),
    ("main", "tag: bosm-26", "Merge branch 'bosm-26'", "8 weeks ago", True),
    ("bench", "", "bench: B50 per model, priced to the rupee", "3 weeks ago", False),
    ("main", "tag: rexops-v1", "Merge branch 'rexops'", "2 weeks ago", True),
    ("main", "HEAD -> main, origin/main", "Merge branch 'temptation-bench'", "2 days ago", True),
]
# branch -> (fork commit index, merge commit index)
SPANS = {"road": (1, 6), "bosm": (3, 11), "rexops": (6, 13), "bench": (6, 14)}

PROMPT = "naman@pilani:~/life$ "
CMD = "git log --graph --oneline --decorate"
FOOT = "15 commits · 4 branches merged · 0 force-pushes to main · 1 incident (we don't talk about it)"
TOP = BAR + 72
H = TOP + (len(LOG) - 1) * ROW + 92


def font_b64(weight: str, text: str) -> str:
    f = TTFont(FONTS / f"jbm-{weight}.woff2")
    opts = subset.Options()
    opts.flavor = "woff"
    sub = subset.Subsetter(opts)
    sub.populate(text=text)
    sub.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff"
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&#39;")


def y(t: int) -> float:
    return TOP + (len(LOG) - 1 - t) * ROW  # newest on top


def lx(lane: int) -> float:
    return X0 + 8 + lane * 24


def sha(i: int, msg: str) -> str:
    return hashlib.sha1(f"{i}{msg}naman".encode()).hexdigest()[:7]


chars = PROMPT + CMD + FOOT + "naman@pilani: ~/life · zsh" + "".join(
    sha(i, m) + r + m + w + "()" for i, (_, r, m, w, _) in enumerate(LOG))
REG = font_b64("400", chars)
BOLD = font_b64("700", "".join(r for _, r, _, _, _ in LOG) + "()")


def build(theme: str) -> str:
    c = THEMES[theme]
    col = lambda b: c["lanes"][BR[b][1]]
    edges, nodes, texts = [], [], []

    # main trunk
    edges.append(f'<line x1="{lx(0)}" y1="{y(0)}" x2="{lx(0)}" y2="{y(len(LOG) - 1)}" stroke="{col("main")}" />')
    # branches: fork curve, lane, merge curve
    for b, (tf, tm) in SPANS.items():
        x, x_0 = lx(BR[b][0]), lx(0)
        ya, yb = y(tf), y(tm)
        h = ROW
        d = (f"M{x_0} {ya} C{x_0} {ya - h * .55} {x} {ya - h * .45} {x} {ya - h} "
             f"L{x} {yb + h} C{x} {yb + h * .45} {x_0} {yb + h * .55} {x_0} {yb}")
        edges.append(f'<path d="{d}" stroke="{col(b)}" />')

    tx = X0 + 8 + 4 * 24 + 14
    for i, (b, refs, msg, when, merge) in enumerate(LOG):
        cx, cy = lx(BR[b][0]), y(i)
        head = refs.startswith("HEAD")
        if head:
            nodes.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{c["bg"]}" stroke="{c["amber"]}" stroke-width="2.5"/>'
                         f'<circle cx="{cx}" cy="{cy}" r="3" fill="{c["amber"]}"/>')
        elif merge:
            nodes.append(f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{c["bg"]}" stroke="{col(b)}" stroke-width="2.5"/>')
        else:
            nodes.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{col(b)}"/>')

        line = f'<tspan class="h">{sha(i, msg)}</tspan> '
        if refs:
            line += f'<tspan class="r">({esc(refs)})</tspan> '
        kind, _, rest = msg.partition(": ")
        if rest:
            line += f'<tspan fill="{col(b)}">{esc(kind)}:</tspan> {esc(rest)}'
        else:
            line += f'<tspan class="m">{esc(msg)}</tspan>'
        texts.append(f'<text x="{tx}" y="{cy + 5}" class="t">{line}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ttl desc">
<title id="ttl">git log --graph</title>
<desc id="desc">A playful git history of the last two years: road-inspection, bosm-26, rexops and temptation-bench branches, all merged into main.</desc>
<style>
@font-face{{font-family:"JBM";font-weight:400;src:url(data:font/woff;base64,{REG}) format("woff")}}
@font-face{{font-family:"JBM";font-weight:700;src:url(data:font/woff;base64,{BOLD}) format("woff")}}
text{{font-family:"JBM",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-variant-ligatures:none}}
.t{{font-size:{FS}px;fill:{c["text"]}}}
.d,.h,.bar{{fill:{c["dim"]}}}
.m{{fill:{c["dim"]}}}
.r{{fill:{c["amber"]};font-weight:700}}
.a{{fill:{c["amber"]}}}
.bar{{font-size:12.5px;letter-spacing:.02em}}
.edges path,.edges line{{fill:none;stroke-width:2.5;stroke-linecap:round}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="{c["bg"]}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="13.5" fill="none" stroke="{c["line"]}"/>
<path d="M1 {BAR}V14A13 13 0 0 1 14 1H{W - 14}A13 13 0 0 1 {W - 1} 14V{BAR}Z" fill="{c["bar"]}"/>
<line x1="1" y1="{BAR + .5}" x2="{W - 1}" y2="{BAR + .5}" stroke="{c["line"]}"/>
<text x="{X0}" y="27" class="bar">naman@pilani: ~/life</text>
<text x="{W - X0}" y="27" class="bar" text-anchor="end">zsh</text>
<text x="{X0}" y="{BAR + 36}" class="t"><tspan class="a">naman@pilani</tspan><tspan class="d">:~/life$ </tspan>{CMD}</text>
<g class="edges">{"".join(edges)}</g>
{"".join(nodes)}
{chr(10).join(texts)}
<line x1="{X0}" y1="{H - 50.5}" x2="{W - X0}" y2="{H - 50.5}" stroke="{c["line"]}" stroke-dasharray="2 6"/>
<text x="{X0}" y="{H - 22}" class="t d">{esc(FOOT)}</text>
</svg>
'''


for t in THEMES:
    (OUT / f"gitlog-{t}.svg").write_text(build(t))
    print(t, (OUT / f"gitlog-{t}.svg").stat().st_size, "bytes")
