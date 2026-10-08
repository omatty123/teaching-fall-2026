#!/usr/bin/env python3
"""Build the three Delta blues listening pages (Oct 14, 16, 19): player beside lyrics, lines marked A / A / B.

Lyrics data lives in frst-110-resources/blues-lyrics.json. Each line is [mark, text]:
A, A2 (A changed on the repeat), B, X (outside the pattern), T (spoken), "" (verse break).
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "frst-110-resources"
SRC = (RES / "blues-form.html").read_text(encoding="utf-8")
style = SRC[SRC.index("<style>") + 7:SRC.index("</style>")]
style += (".song{margin:0 0 20px}.song .stage{margin-top:6px}"
          ".patton .B2{background:var(--b-t);box-shadow:inset 4px 0 0 var(--b)}"
          ".days{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:16px}.days b{font-weight:700}")
DATA = json.loads((RES / "blues-lyrics.json").read_text(encoding="utf-8"))
e = html.escape
LABEL = {"A": "A", "A2": "A′", "B": "B", "B2": "B′", "X": "", "T": ""}
KEYS = {"A": '<span><i style="background:var(--a-t)"></i>A</span>',
        "A2": '<span><i style="background:var(--a-t);box-shadow:inset 4px 0 0 var(--a2)"></i>A′, changed on the repeat</span>',
        "B": '<span><i style="background:var(--b-t)"></i>B</span>',
        "B2": '<span><i style="background:var(--b-t);box-shadow:inset 4px 0 0 var(--b)"></i>B′, changed on the repeat</span>',
        "X": '<span><i style="background:var(--off)"></i>outside the pattern</span>',
        "T": '<span><i style="background:transparent"></i><em>spoken</em></span>'}


def key(lines):
    used = {m for m, _ in lines}
    return '<div class="key">' + "".join(v for k, v in KEYS.items() if k in used) + "</div>"


def lyrics(lines):
    out = []
    for mark, text in lines:
        if mark == "":
            out.append('<li class="gap"></li>')
        else:
            out.append(f'<li class="{mark}"><b>{LABEL[mark]}</b>{e(text)}</li>')
    return '<ul class="patton">' + "\n".join(out) + "</ul>"


def song(s):
    body = lyrics(s["lines"]) if s.get("lines") else ""
    note = f'<p>{s["note"]}</p>' if s.get("note") else ""
    return (f'<section class="song" id="{s["id"]}" style="--c:var(--{s.get("color", "b")})">\n'
            f'<h2>{e(s["artist"])}, “{e(s["title"])}”</h2>\n{note}\n<div class="stage">\n<div>'
            f'<div class="video"><iframe src="https://www.youtube.com/embed/{s["yt"]}?rel=0" title="{e(s["artist"])}, {e(s["title"])}" '
            'loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>\n'
            f'<p class="status">{e(s["made"])}</p>\n{key(s["lines"]) if s.get("lines") else ""}</div>\n{body}\n</div>\n</section>')


def page(day):
    slug = f'blues-oct-{day["n"]}'
    others = " ".join(f'<a href="blues-oct-{d["n"]}.html">{e(d["short"])}</a>' if d["n"] != day["n"] else f'<b>{e(d["short"])}</b>'
                      for d in DATA["days"])
    url = f"https://omatty123.github.io/teaching-fall-2026/frst-110-resources/{slug}.html"
    desc = e(day["intro"])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(day["title"])} · FRST 110</title>
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(day["title"])} · FRST 110">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://omatty123.github.io/teaching-fall-2026/images/frst/delta-blues.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://omatty123.github.io/teaching-fall-2026/images/frst/delta-blues.jpg">
<style>{style}</style></head>
<body>
<nav class="nav" aria-label="Breadcrumb"><div class="nav-inner"><a class="brand" href="../courses/frst-110.html">FRST 110</a><a href="../courses/frst-110.html">← Course materials</a><a href="blues-form.html">What are the blues?</a></div></nav>
<main>
<h1>{e(day["title"])}</h1>
<p class="meta">Delta blues · {e(day["date"])}</p>
<p class="days">{others}</p>
<p class="lead">{day["intro"]}</p>
{chr(10).join(song(s) for s in day["songs"])}
<p class="src">{day["sources"]}</p>
</main>
</body></html>
"""


for day in DATA["days"]:
    (RES / f'blues-oct-{day["n"]}.html').write_text(page(day), encoding="utf-8")
    print("wrote", f'blues-oct-{day["n"]}.html')
