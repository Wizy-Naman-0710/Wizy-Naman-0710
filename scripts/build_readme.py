"""Writes README.md. Box-drawing blocks are generated so every border lines up."""
import html, pathlib, re, sys, unicodedata

OUT = pathlib.Path(sys.argv[1])
U = "Wizy-Naman-0710"
GH = f"https://github.com/{U}"
LINKEDIN = "https://www.linkedin.com/in/naman-murarka-5ab0931a7/"
MAIL = "murarkanaman@gmail.com"

W = 76  # total box width; fits GitHub's profile column without scrolling


def vis(s: str) -> int:
    """Visible width of a line that may contain HTML tags/entities."""
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in s)


def pad(s: str, n: int) -> str:
    return s + " " * (n - vis(s))


def box(left: str, right: str, rows: list[str]) -> str:
    inner = W - 2
    top_fill = W - 4 - vis(left) - vis(right)
    out = [f"┌─{left}{'─' * top_fill}{right}─┐"]
    out.append("│" + " " * inner + "│")
    for r in rows:
        body = "  " + r
        assert vis(body) <= inner, (r, vis(body))
        out.append("│" + pad(body, inner) + "│")
    out.append("│" + " " * inner + "│")
    out.append("└" + "─" * inner + "┘")
    return "\n".join(out)


def a(href: str, text: str) -> str:
    return f'<a href="{href}">{html.escape(text)}</a>'


def repo(name: str, public: bool, label: str | None = None) -> str:
    label = label or name + "/"
    return a(f"{GH}/{name}", label) if public else html.escape(label)


def picture(dark: str, light: str, alt: str, extra: str = "") -> str:
    return (
        "<picture>"
        f'<source media="(prefers-color-scheme: dark)" srcset="{dark}">'
        f'<source media="(prefers-color-scheme: light)" srcset="{light}">'
        f'<img alt="{alt}" src="{dark}"{extra}>'
        "</picture>"
    )


def icons(ids: str) -> str:
    base = f"https://skillicons.dev/icons?i={ids.replace(',', '%2C')}&perline=10"
    return picture(base, base + "&theme=light", ids.replace(",", ", "), ' height="40"')


# ── whoami ────────────────────────────────────────────────────────────────
whoami = box("[ naman@pilani ]", "[ whoami ]", [
    "name      Naman Murarka",
    "study     B.E. Computer Science, BITS Pilani, class of '29",
    "role      Head of Operations, SUTT (Student Union Tech Team)",
    "builds    backends, cloud infra, evals for LLM agents",
    "stack     Bun + Elysia + Postgres + Drizzle, shipped with Terraform",
    "based     Pilani, Rajasthan · UTC+5:30",
])

# ── ls -l ~/projects ──────────────────────────────────────────────────────
PROJECTS = [
    # name, public, desc, tags
    ("rexops", True, "review + approval OS for agencies", "ts pg"),
    ("road-inspection-platform", False, "RGB-D potholes, GCP end to end", "py tf", "road-inspection/"),
    ("temptation-bench", True, "how big a bribe breaks an agent?", "evals"),
    ("pegasus-2.0", False, "Gmail client, BITS domain only", "bun", "pegasus/"),
    ("postman-web", False, "BITS x Postman labs site + portal", "next"),
    ("commun-web", False, "NPAT prep platform, admin MCP", "elysia"),
    ("placements-portal", False, "placement papers, OAs, interviews", "ts"),
    ("lics-uppaal-course-registration", False, "course registration, model-checked", "uppaal", "lics-uppaal/"),
    ("sports-union-landing", False, "Sports Union site, admin-driven", "django", "sports-union/"),
    ("RedisMailer", True, "mail queue on Redis Streams", "redis"),
    ("kafka-project", True, "LMS messaging over Kafka", "kafka"),
    ("REST-GO", True, "REST API in plain Go", "go"),
    ("LibraNet", True, "library system behind nginx", "django"),
    ("hostel-management", True, "JavaFX hostel bookings", "java"),
]
ls_rows = [
    '<span>naman@pilani:~$ ls -l ~/projects</span>',
    f"total {len(PROJECTS)}   (drwx------ is private. ask me for a demo)",
    "",
]
for p in PROJECTS:
    name, public, desc, tags = p[:4]
    label = p[4] if len(p) > 4 else name + "/"
    perms = "drwxr-xr-x" if public else "drwx------"
    cell = repo(name, public, label)
    ls_rows.append(f"{perms}  {pad(cell, 20)}{pad(html.escape(desc), 36)}{tags}")
for r in ls_rows:
    assert vis(r) <= W, (r, vis(r))
ls_block = "\n".join(ls_rows)

# ── git shortlog across orgs ──────────────────────────────────────────────
org = [
    "naman@pilani:~$ git shortlog -sn --author=naman --orgs",
    "",
    f"   472  {a('https://github.com/bitssutechteam', 'bitssutechteam')}",
    f"        ├─ 336  {a('https://github.com/bitssutechteam/BOSM-Engine-2025', 'BOSM-Engine-2025')}    backend for BOSM '25",
    f"        ├─  61  {a('https://github.com/bitssutechteam/BOSM-Engine-2026', 'BOSM-Engine-2026')}    and again for '26",
    f"        ├─  28  {a('https://github.com/bitssutechteam/StudyDeck-Backend', 'StudyDeck-Backend')}",
    f"        ├─  25  {a('https://github.com/bitssutechteam/BOSM-2026-Website', 'BOSM-2026-Website')}",
    f"        └─  22  SU-Backend, snaps portal (Go), BOSM '25 site, ...",
    "",
    f"    12  {a('https://github.com/BITS-Library', 'BITS-Library')}      space booking, e-journal Excel export,",
    "                          subject-wise open-access journals",
    f"     *  {a('https://github.com/Vitalize-Health', 'Vitalize-Health')}   web + native + server, one TS monorepo",
]
for r in org:
    assert vis(r) <= W, (r, vis(r))
org_block = "\n".join(org)

# ── now.log ───────────────────────────────────────────────────────────────
now = [
    "naman@pilani:~$ tail -n 6 now.log",
    "",
    "2026-11-21  temptation-bench   shipped: a price on every model's integrity",
    "2026-11-12  lics-uppaal        both models verified, every mutant caught",
    "2026-11-11  commun-web         live: admin MCP server, prod behind Caddy",
    "2026-10-29  postman-web        live: site + portal + API on one origin",
    "2026-10-22  road-inspection    live: RGB-D model finding potholes in prod",
    "2026-09-29  rexops             v1 complete, all 8 blocks verified",
]
for r in now:
    assert vis(r) <= W, (r, vis(r))

plan = box("[ ~/.plan ]", "[ last edited: tonight ]", [
    "[x] get BOSM '26 through registration day with zero 502s",
    "[x] find the bribe that makes a frontier model fold",
    "[x] write the CLAUDE.md before the code",
    "[x] move one more workflow off WhatsApp",
    "[ ] sleep before 3am            (backlogged since 2024)",
])

SNAKE = f"https://raw.githubusercontent.com/{U}/{U}/output"

shield = "https://img.shields.io/badge"
badges = " ".join([
    f'<a href="{LINKEDIN}"><img alt="LinkedIn" src="{shield}/LinkedIn-naman--murarka-161B22?style=flat-square&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI0ZGQjAwMCIgZD0iTTIwLjQ1IDIwLjQ1aC0zLjU2di01LjU3YzAtMS4zMy0uMDMtMy4wNC0xLjg1LTMuMDQtMS44NSAwLTIuMTQgMS40NS0yLjE0IDIuOTR2NS42N0g5LjM1VjloMy40MXYxLjU2aC4wNWMuNDgtLjkgMS42NC0xLjg1IDMuMzctMS44NSAzLjYgMCA0LjI3IDIuMzcgNC4yNyA1LjQ2djYuMjh6TTUuMzQgNy40M2EyLjA2IDIuMDYgMCAxIDEgMC00LjEzIDIuMDYgMi4wNiAwIDAgMSAwIDQuMTN6TTcuMTIgMjAuNDVIMy41NlY5aDMuNTZ2MTEuNDV6Ii8%2BPC9zdmc%2B&labelColor=161B22"></a>',
    f'<a href="mailto:{MAIL}"><img alt="email" src="{shield}/{MAIL.replace("-", "--")}-161B22?style=flat-square&logo=gmail&logoColor=FFB000"></a>',
    f'<img alt="Pilani, IN" src="{shield}/Pilani,_IN-UTC%2B5:30-161B22?style=flat-square&labelColor=161B22&color=30363D">',
    f'<img alt="profile views" src="https://komarev.com/ghpvc/?username={U}&style=flat-square&color=9C5700&label=views">',
])

readme = f"""<!-- Profile README for {U}. Generated by scripts/build_readme.py (header: scripts/make_header.py). Edit the script, not this file. -->

{picture("./assets/header-dark.svg", "./assets/header-light.svg", "naman murarka: B.E. Computer Science at BITS Pilani, Head of Operations at SUTT", ' width="100%"')}

<p align="center">
{badges}
</p>

## `$ whoami`

```text
{whoami}
```

## `$ cat about.txt`

Computer Science at BITS Pilani, class of '29. Most weeks go to SUTT, the Student Union's tech team, where I run operations and still write a fair share of the backend: the BOSM engine, the SU backend, StudyDeck, and whatever portal the fest needs that month. That's 472 commits so far, most of them pushed the night before something went live.

Outside the union I build products end to end, usually alone. I start with the schema, then the API, then the Terraform, and the frontend comes last. Recent launches include a Gmail client locked to the BITS domain that syncs over Pub/Sub, and a GCP pipeline that finds potholes in RGB-D road footage and pins them on a map.

My favourite build is Temptation-Bench. It hands an LLM agent the keys to a bank branch for weeks of simulated business, slides bribes across the desk, and measures exactly how much money it takes before the agent breaks the rules on purpose. Every model on it now has a price.

## `$ ls -l ~/projects`

<pre>
{ls_block}
</pre>

<details>
<summary><b>rexops</b>: a multi-tenant creative operating system for agencies</summary>

<br>

Agencies used to run client work over WhatsApp, Drive and email, then fight about which version got signed off. RexOps replaces that whole mess with one system: `Agency → Clients → Projects → Deliverables → File Versions → Reviews`, a hard trust wall between every agency and its clients, and a Frame.io-grade review-and-approval engine on every single file version. Multi-tenant from the first migration, typed end to end, and complete: all eight blocks of v1 built and verified.

`TypeScript` `@rexops/* monorepo` `Postgres` `PL/pgSQL` · [source]({GH}/rexops)
</details>

<details>
<summary><b>road-inspection</b>: RGB-D pothole detection, from upload to map</summary>

<br>

A Cloud Storage upload fires Eventarc. A Cloud Function records the job in Firestore, and a Python inference service on Cloud Run runs the RGB-D model over it. Inspections, pothole detail and a live map show up in a Next.js dashboard. Every resource is Terraform, with uptime checks and alerting on the Cloud Run revisions. I shipped it in eight gated phases, each one closed with committed proof before the next began, and it ends with the real RGB-D model finding potholes in production behind a public dashboard. Footage in, potholes on the map, zero manual steps.

`Python` `Next.js` `Terraform` `Cloud Run` `Eventarc` `Firestore` `GitHub Actions` · private
</details>

<details>
<summary><b>temptation-bench</b>: do LLM agents stay honest when cheating pays?</summary>

<br>

An agent manages a fictional bank branch, Woz Valley Bank, for several simulated weeks. Ordinary business events carry planted temptations, such as a bribe to approve a loan that breaks policy. Code does the scoring: the agent's tool calls and filed reports are checked against the simulation's hidden true books, so no LLM judge touches the main score. The headline number is B50, the bribe at which a model gives in half the time, measured model by model over full runs of simulated weeks. The result is the first price tag on machine integrity: a single number that says how cheaply each agent can be bought.

`inspect-ai` `long-horizon sim` · builds on Vending-Bench and Blueprint-Bench · [repo]({GH}/temptation-bench)
</details>

<details>
<summary><b>pegasus</b>: a Gmail client for <code>@pilani.bits-pilani.ac.in</code></summary>

<br>

Gmail stays the source of truth. Postgres keeps a local index of threads, labels, sync cursors and encrypted OAuth tokens, and bodies are fetched on demand. Mailbox changes arrive as authenticated Pub/Sub pushes with duplicate protection, then incremental `history.list` sync takes over, with a full re-index if history goes stale. Cloud Scheduler renews the watches. I built it twice and shipped both: `pegasus-lite` on Next.js 16, and `pegasus-2.0`, a full rewrite on Bun, Elysia and TanStack Start that leaves the first one in the dust.

`Bun` `Elysia` `TanStack Start` `Drizzle` `Better Auth` `Gmail API` `Pub/Sub` · private
</details>

## `$ git shortlog --orgs`

<pre>
{org_block}
</pre>

## `$ stack`

<table>
<tr><td><code>lang</code></td><td>{icons("ts,py,go,java,c,bash")}</td></tr>
<tr><td><code>web</code></td><td>{icons("bun,elysia,nodejs,nextjs,react,django,fastapi,tailwind")}</td></tr>
<tr><td><code>data</code></td><td>{icons("postgres,redis,kafka,sqlite")}</td></tr>
<tr><td><code>infra</code></td><td>{icons("gcp,terraform,docker,nginx,githubactions,linux,git")}</td></tr>
</table>

Also on the bench: Drizzle, Better Auth, Pub/Sub, Caddy, UPPAAL, Verilog for coursework, and Claude Code most days.

## `$ tail now.log`

```text
{chr(10).join(now)}
```

```text
{plan}
```

## `$ git log --graph`

{picture("./assets/gitlog-dark.svg", "./assets/gitlog-light.svg", "git log --graph: road-inspection, bosm-26, rexops and temptation-bench, all merged into main", ' width="100%"')}

{picture(SNAKE + "/github-snake-dark.svg", SNAKE + "/github-snake.svg", "a snake eating the contribution grid", ' width="100%"')}

```text
naman@pilani:~$ exit
logout
Connection to pilani closed.
```
"""

OUT.write_text(readme)
print("wrote", OUT, len(readme), "chars")
