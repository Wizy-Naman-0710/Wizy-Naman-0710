"""Build assets/header-dark.svg and assets/header-light.svg.

One authored motion moment: the terminal session under the name types itself in.
JetBrains Mono (OFL) is subset and embedded so it renders the same on every OS.
"""
import base64, io, pathlib, sys
from fontTools import subset
from fontTools.ttLib import TTFont

FONTS = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

W, H = 960, 414
X0 = 40
CH = 0.6  # JetBrains Mono advance, em

THEMES = {
    # GitHub's own page colours, so the header sits on the page instead of in a box
    "dark": dict(bg="#0D1117", frame="#0D1117", bar="#161B22", line="#30363D",
                 text="#E6EDF3", dim="#8B949E", amber="#FFB000", soft="#FFCF66"),
    "light": dict(bg="#FFFFFF", frame="#FFFFFF", bar="#F6F8FA", line="#D0D7DE",
                  text="#1F2328", dim="#59636E", amber="#9C5700", soft="#B86A00"),
}

NAME = "naman murarka"
SUB = "b.e. computer science · bits pilani '29 · head of operations, sutt"

# (kind, text, t_start, extra)
SESSION = [
    ("cmd", "cat ~/.plan", 0.5),
    ("out", "write the backend. terraform the cloud. bribe the agents (for science).", 1.45),
    ("cmd", "uptime", 2.05),
    ("out", "up 2y, 655 commits this year, load average: bosm, rexops, sleep debt", 2.75),
    ("prompt", "", 3.35),
]


def font_b64(weight: str, text: str) -> str:
    f = TTFont(FONTS / f"jbm-{weight}.woff2")
    opts = subset.Options()
    opts.flavor = "woff"
    opts.layout_features = ["kern"]
    sub = subset.Subsetter(opts)
    sub.populate(text=text)
    sub.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff"
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


all_text = NAME + SUB + "".join(s[1] for s in SESSION) + "naman@pilani:~$ zsh80x24·_"
REG = font_b64("400", all_text)
BOLD = font_b64("800", NAME + "_")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(theme: str) -> str:
    c = THEMES[theme]
    fs = 16
    lh = 30
    y = 248
    rows = []
    prompt_w = len("naman@pilani:~$ ") * fs * CH
    for kind, text, t in SESSION:
        if kind == "cmd":
            n = len(text)
            dur = round(0.055 * n + 0.15, 2)
            tx = X0 + prompt_w
            tw = n * fs * CH + 2
            rows.append(
                f'<g class="r" style="animation-delay:{t - 0.25:.2f}s">'
                f'<text x="{X0}" y="{y}" class="t"><tspan class="a">naman@pilani</tspan>'
                f'<tspan class="d">:~$ </tspan><tspan class="x">{esc(text)}</tspan></text>'
                f'<rect class="cover" x="{tx:.1f}" y="{y - 18}" width="{tw:.1f}" height="26" '
                f'style="--w:{tw:.1f}px;animation-duration:{dur}s;animation-delay:{t:.2f}s;'
                f'animation-timing-function:steps({n},end)"/></g>'
            )
            y += lh
        elif kind == "out":
            rows.append(
                f'<text x="{X0 + 2 * fs * CH:.1f}" y="{y}" class="t o r" '
                f'style="animation-delay:{t:.2f}s">{esc(text)}</text>'
            )
            y += lh + 8
        else:
            cx = X0 + prompt_w
            rows.append(
                f'<g class="r" style="animation-delay:{t:.2f}s">'
                f'<text x="{X0}" y="{y}" class="t"><tspan class="a">naman@pilani</tspan>'
                f'<tspan class="d">:~$ </tspan></text>'
                f'<rect class="cur" x="{cx:.1f}" y="{y - 15}" width="9.6" height="19" '
                f'style="animation-delay:{t + 0.2:.2f}s"/></g>'
            )

    name_fs = 64
    name_w = len(NAME) * name_fs * CH
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ttl desc">
<title id="ttl">Naman Murarka</title>
<desc id="desc">Terminal: naman murarka, B.E. Computer Science at BITS Pilani, Head of Operations at SUTT. cat ~/.plan prints: write the backend, terraform the cloud, bribe the agents (for science).</desc>
<style>
@font-face{{font-family:"JBM";font-weight:400;src:url(data:font/woff;base64,{REG}) format("woff")}}
@font-face{{font-family:"JBM";font-weight:800;src:url(data:font/woff;base64,{BOLD}) format("woff")}}
text{{font-family:"JBM",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-variant-ligatures:none}}
.t{{font-size:16px;fill:{c["text"]}}}
.a{{fill:{c["amber"]}}}
.d{{fill:{c["dim"]}}}
.o{{fill:{c["dim"]}}}
.bar{{font-size:12.5px;fill:{c["dim"]};letter-spacing:.02em}}
.name{{font-size:{name_fs}px;font-weight:800;fill:{c["text"]};letter-spacing:-.02em}}
.sub{{font-size:15px;fill:{c["dim"]}}}
.cover{{fill:{c["frame"]};animation-name:wipe;animation-fill-mode:both}}
.r{{animation:rise .5s cubic-bezier(.16,1,.3,1) both}}
.cur{{fill:{c["amber"]};animation:blink 1.1s steps(1,end) infinite}}
@keyframes wipe{{from{{transform:translateX(0)}}to{{transform:translateX(var(--w))}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:none}}}}
@keyframes blink{{0%,55%{{opacity:1}}56%,100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.r,.cur{{animation:none}}.cover{{display:none}}}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="{c["frame"]}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="13.5" fill="none" stroke="{c["line"]}"/>
<path d="M1 44V14A13 13 0 0 1 14 1H{W - 14}A13 13 0 0 1 {W - 1} 14V44Z" fill="{c["bar"]}"/>
<line x1="1" y1="44.5" x2="{W - 1}" y2="44.5" stroke="{c["line"]}"/>
<text x="{X0}" y="27" class="bar">naman@pilani: ~</text>
<text x="{W - X0}" y="27" class="bar" text-anchor="end">zsh · 80x24</text>
<text x="{X0 - 3}" y="128" class="name">{NAME}<tspan fill="{c["amber"]}">_</tspan></text>
<text x="{X0}" y="164" class="sub">{esc(SUB)}</text>
<line x1="{X0}" y1="196.5" x2="{W - X0}" y2="196.5" stroke="{c["line"]}" stroke-dasharray="2 6"/>
{chr(10).join(rows)}
</svg>
'''


for t in THEMES:
    (OUT / f"header-{t}.svg").write_text(build(t))
    print(t, (OUT / f"header-{t}.svg").stat().st_size, "bytes")
