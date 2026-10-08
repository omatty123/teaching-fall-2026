#!/usr/bin/env python3
"""Build one HIST 212 class page from hist-212-resources/days/YYYY-MM-DD.json.

One file per class day. The builder fixes only the shell: address, top bar
(course page, Class notes, reader, previous class), title, section links, and the
readings at the end. The body is whatever the day needs (passages side by side,
images, video, lists, a question where one helps), in HIST's own lesson style. The day is then listed as "Class page" on its date in
data/hist-212.json, and build.py is run, so the course site and today.html pick
it up. Refuses to build if a quotation repeats, a passage has more than one highlight, or a quotation is not found in the readers/Ebrey
(a quotation that runs across a reader page break may carry "pageBreak": true
after it has been read on the page).

Usage: python3 scripts/build-hist-class.py 2026-10-13 [--no-site]
"""
import datetime, hashlib, html, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DAYS = ROOT / "hist-212-resources/days"
DATA = ROOT / "data/hist-212.json"
CLASS_NOTES = "https://docs.google.com/document/d/1fTh1Ot139V6GaPa1appr1EyLq4vbwi2Oy_VPTUDr_Mo/edit"
SOURCES = pathlib.Path.home() / "workspaces/teaching-fall-2026-roster/prep-agent/cache/hist212-sources.txt"
e = html.escape


def norm(t):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"<[^>]+>", "", t).lower().replace("’", "'"))


def words(t):
    return re.sub(r"<[^>]+>", " ", t).lower().replace("’", "'").split()


def quote_found(q, corpus, flat):
    parts = [p for p in re.split(r"\.\.\.|…", q) if len(p.split()) >= 3]
    for p in parts:
        if norm(p) in corpus:
            continue
        w = [re.sub(r"[^a-z0-9']", "", x) for x in words(p)]
        runs = [" ".join(w[i:i + 3]) for i in range(len(w) - 2)]
        if not runs or sum(r in flat for r in runs) < 0.9 * len(runs):
            return False
    return True


def passage(p):
    who = f'<h3>{e(p["who"])}</h3>' if p.get("who") else ""
    link = f' <a href="{e(p["link"])}">{e(p.get("linkLabel", "Reader"))}</a>' if p.get("link") else ""
    return (f'<article class="passage">{who}<blockquote>“{p["quote"]}”</blockquote>'
            f'<p class="citation">{e(p["cite"])}.{link}</p></article>')


def block(b):
    if "html" in b:
        return b["html"]
    if "p" in b:
        return f"<p>{b['p']}</p>"
    if "board" in b:
        return f'<p><strong>{b["board"]}</strong></p>'
    if "list" in b:
        return "<ul>" + "".join(f"<li>{x}</li>" for x in b["list"]) + "</ul>"
    if "passage" in b:
        return passage(b["passage"])
    if "pair" in b:
        return '<div class="comparison">' + "".join(passage(p) for p in b["pair"]) + "</div>"
    if "figure" in b:
        f = b["figure"]
        src = f' <a href="{e(f["source"])}">Image source</a>' if f.get("source") else ""
        return (f'<figure><img src="{e(f["src"])}" alt="{e(f["alt"])}" style="max-width:100%;max-height:{f.get("maxHeight", 520)}px;width:auto;height:auto;display:block" loading="lazy" decoding="async">'
                f'<figcaption>{f["caption"]}{src}</figcaption></figure>')
    if "video" in b:
        v = b["video"]
        return (f'<figure><iframe width="960" height="540" style="width:100%;aspect-ratio:16/9;height:auto;border:0" '
                f'src="https://www.youtube-nocookie.com/embed/{e(v["id"])}?start={v.get("start", 0)}&amp;end={v.get("end", "")}" '
                f'title="{e(v["title"])}" allowfullscreen loading="lazy"></iframe>'
                f'<figcaption>{v["caption"]} <a href="https://www.youtube.com/watch?v={e(v["id"])}&amp;t={v.get("start", 0)}s">Open video</a></figcaption></figure>')
    raise SystemExit(f"unknown block {list(b)}")


def check(day):
    probs, seen = [], {}
    corpus_txt = SOURCES.read_text(errors="ignore") if SOURCES.exists() else ""
    corpus, flat = norm(corpus_txt), " ".join(re.sub(r"[^a-z0-9']", "", x) for x in words(corpus_txt))
    for s in day["sections"]:
        ps = []
        for b in s["body"]:
            ps += [b["passage"]] if "passage" in b else b.get("pair", [])
        for p in ps:
            k = norm(p["quote"])
            if k in seen:
                probs.append(f'{s["id"]}: quotation repeats from {seen[k]}')
            seen[k] = s["id"]
            if p["quote"].count("<mark>") > 1:
                probs.append(f'{s["id"]}: more than one highlight in a passage')
            if corpus and not p.get("pageBreak") and not quote_found(p["quote"], corpus, flat):
                probs.append(f'{s["id"]}: not found in readers/Ebrey: {re.sub("<[^>]+>", "", p["quote"])[:70]}')
    return probs


def main():
    date = sys.argv[1]
    day = json.loads((DAYS / f"{date}.json").read_text())
    probs = check(day)
    if probs:
        raise SystemExit("NOT BUILT:\n  " + "\n  ".join(probs))
    course = json.loads(DATA.read_text())
    sched = course["schedule"]
    me = next(s for s in sched if s["date"] == date)
    reader = next((m["href"] for m in me.get("materials", []) if m["label"] == "Reader PDF"), None)
    prev = None
    for s in sched:
        if s["date"] >= date:
            break
        for m in s.get("materials", []):
            if m["label"] == "Class page":
                prev = (s["date"], m["href"].replace("../hist-212-resources/", ""), s["topic"])
    d = datetime.date.fromisoformat(date)
    when = d.strftime("%A, %B ") + str(d.day) + ", " + str(d.year)
    kit = lambda f: f"../_kit/{f}?v=" + hashlib.sha256((ROOT / "_kit" / f).read_bytes()).hexdigest()[:12]
    nav = [f'<a href="../courses/hist-212.html">HIST 212 · Course materials</a>', f'<a href="{CLASS_NOTES}">Class notes</a>']
    if reader:
        nav.append(f'<a href="{e(reader)}">Reader PDF</a>')
    if prev:
        p = datetime.date.fromisoformat(prev[0])
        nav.append(f'<a href="{e(prev[1])}">{p.strftime("%B")} {p.day} class</a>')
    chips = "".join(f'<a href="#{e(s["id"])}">{e(s.get("short") or s["title"])}</a>' for s in day["sections"])
    secs = []
    for s in day["sections"]:
        src = f'<p class="meta">{e(s["source"])}</p>' if s.get("source") else ""
        ask = f'<p class="question">{s["ask"]}</p>' if s.get("ask") else ""
        secs.append(f'<section id="{e(s["id"])}"><h2>{e(s["title"])}</h2>{src}{"".join(block(b) for b in s["body"])}{ask}</section>')
    readings = "".join(f"<li>{r}</li>" for r in day.get("readings", []))
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(day["title"])} · {d.strftime("%B")} {d.day} · HIST 212</title><link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta name="description" content="{e(day["description"])}">
<meta property="og:title" content="{e(day["title"])} · HIST 212"><meta property="og:description" content="{e(day["description"])}">
<meta property="og:image" content="https://omatty123.github.io/teaching-fall-2026/images/hist-212-banner.jpg">
<meta property="og:url" content="https://omatty123.github.io/teaching-fall-2026/hist-212-resources/class-{date}.html"><meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://omatty123.github.io/teaching-fall-2026/images/hist-212-banner.jpg">
<link rel="stylesheet" href="{kit("hist-212-lesson.css")}"></head>
<body><a class="skip" href="#content">Skip to class materials</a><nav class="top">{"".join(nav)}<button id="highlights" aria-pressed="true">Highlights on</button><button id="project" aria-pressed="false">Large text</button></nav>
<main id="content"><header><h1>{e(day["title"])}</h1><p class="meta">{when} · {e(day["meta"])}</p>
<nav class="sections" aria-label="Lesson sections">{chips}<a href="#resources">Readings</a></nav></header>
{"".join(secs)}
<section id="resources"><h2>Today’s readings</h2><ul>{readings}</ul></section>
<footer>{("<p>" + day["footnote"] + "</p>") if day.get("footnote") else ""}<p><a href="{CLASS_NOTES}">Class notes</a> · <a href="../courses/hist-212.html">All classes and readings</a></p></footer>
</main><script src="{kit("hist-212-lesson.js")}"></script></body></html>
"""
    out = ROOT / f"hist-212-resources/class-{date}.html"
    out.write_text(doc)
    print("built", out.relative_to(ROOT))
    href = f"../hist-212-resources/class-{date}.html"
    mats = me.setdefault("materials", [])
    if not any(m.get("label") == "Class page" for m in mats):
        mats.insert(0, {"label": "Class page", "href": href, "kind": "guide"})
        DATA.write_text(json.dumps(course, ensure_ascii=False, indent=2) + "\n")
        print("listed on", date, "in data/hist-212.json")
    if "--no-site" not in sys.argv:
        subprocess.run([sys.executable, str(ROOT / "build.py")], check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
        print("course site rebuilt")


if __name__ == "__main__":
    main()
