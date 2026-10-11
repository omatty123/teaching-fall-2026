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
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
DAYS = ROOT / "hist-212-resources/days"
DATA = ROOT / "data/hist-212.json"
CLASS_NOTES = "https://docs.google.com/document/d/1fTh1Ot139V6GaPa1appr1EyLq4vbwi2Oy_VPTUDr_Mo/edit"
SOURCES = pathlib.Path.home() / "workspaces/teaching-fall-2026-roster/prep-agent/cache/hist212-sources.txt"
e = html.escape


def link_names(doc, names):
    """Link a day's named references without changing text or existing links."""
    if not names:
        return doc
    pattern = re.compile(r"(?<![\w])(" + "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True)) + r")(?![\w])")
    class Linker(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.out, self.stack = [], []
        def handle_starttag(self, tag, attrs):
            self.out.append(self.get_starttag_text())
            if tag not in {'img', 'meta', 'link', 'br', 'hr', 'input', 'source', 'wbr'}:
                self.stack.append(tag)
        def handle_startendtag(self, tag, attrs):
            self.out.append(self.get_starttag_text())
        def handle_endtag(self, tag):
            self.out.append(f'</{tag}>')
            if tag in self.stack:
                self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]
        def handle_data(self, data):
            if 'body' in self.stack and not any(t in self.stack for t in ('a', 'script', 'style', 'nav', 'svg', 'button')):
                data = pattern.sub(lambda m: f'<a class="name-link" href="{e(names[m[0]], quote=True)}">{m[0]}</a>', data)
            self.out.append(data)
        def handle_entityref(self, name): self.out.append(f'&{name};')
        def handle_charref(self, name): self.out.append(f'&#{name};')
        def handle_decl(self, decl): self.out.append(f'<!{decl}>')
        def handle_comment(self, data): self.out.append(f'<!--{data}-->')
    parser = Linker()
    parser.feed(doc)
    return ''.join(parser.out)


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
    parts = day.get("parts", [])
    if parts:
        members = [sid for part in parts for sid in part["sections"]]
        expected = [s["id"] for s in day["sections"]]
        if len(members) != len(set(members)) or set(members) != set(expected):
            raise SystemExit("Lesson parts must include every section exactly once")
    chips = "".join(f'<a href="#{e(s["id"])}">{e(s.get("short") or s["title"])}</a>' for s in (parts or day["sections"]))
    rendered = {}
    for s in day["sections"]:
        src = f'<p class="meta">{e(s["source"])}</p>' if s.get("source") else ""
        ask = f'<p class="question">{s["ask"]}</p>' if s.get("ask") else ""
        body = "".join(block(b) for b in s["body"])
        level = 3 if parts else 2
        if parts:
            body = re.sub(r"<(/?)h3>", r"<\1h4>", body)
        rendered[s["id"]] = f'<section id="{e(s["id"])}"><h{level}>{e(s["title"])}</h{level}>{src}{body}{ask}</section>'
    if parts:
        secs = []
        for part in parts:
            links = "".join(f'<a href="#{e(sid)}">{e(next(s.get("short") or s["title"] for s in day["sections"] if s["id"] == sid))}</a>' for sid in part["sections"])
            summary = f'<p class="part-summary">{part["summary"]}</p>' if part.get("summary") else ""
            secs.append(f'<section class="lesson-part" id="{e(part["id"])}"><h2>{e(part["title"])}</h2>{summary}<nav class="part-links" aria-label="{e(part["title"])}">{links}</nav>{"".join(rendered[sid] for sid in part["sections"])}</section>')
    else:
        secs = list(rendered.values())
    readings = "".join(f"<li>{r}</li>" for r in day.get("readings", []))
    extra_css = "".join(f'<link rel="stylesheet" href="{kit(f)}">' for f in day.get("styles", []))
    extra_js = "".join(f'<script src="{kit(f)}"></script>' for f in day.get("scripts", []))
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(day["title"])} · {d.strftime("%B")} {d.day} · HIST 212</title><link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta name="description" content="{e(day["description"])}">
<meta property="og:title" content="{e(day["title"])} · HIST 212"><meta property="og:description" content="{e(day["description"])}">
<meta property="og:image" content="https://omatty123.github.io/teaching-fall-2026/images/hist-212-banner.jpg">
<meta property="og:url" content="https://omatty123.github.io/teaching-fall-2026/hist-212-resources/class-{date}.html"><meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://omatty123.github.io/teaching-fall-2026/images/hist-212-banner.jpg">
<link rel="stylesheet" href="{kit("hist-212-lesson.css")}">{extra_css}</head>
<body class="{e(day.get("bodyClass", ""))}"><a class="skip" href="#content">Skip to class materials</a><nav class="top">{"".join(nav)}<button id="highlights" aria-pressed="true">Highlights on</button><button id="project" aria-pressed="false">Large text</button></nav>
<main id="content"><header><h1>{e(day["title"])}</h1><p class="meta">{when} · {e(day["meta"])}</p>
<nav class="sections" aria-label="Lesson sections">{chips}<a href="#resources">Readings</a></nav>{day.get("overview", "")}</header>
{"".join(secs)}
<section id="resources"><h2>Today’s readings</h2><ul>{readings}</ul></section>
<footer>{("<p>" + day["footnote"] + "</p>") if day.get("footnote") else ""}<p><a href="{CLASS_NOTES}">Class notes</a> · <a href="../courses/hist-212.html">All classes and readings</a></p></footer>
</main><script src="{kit("hist-212-lesson.js")}"></script>{extra_js}</body></html>
"""
    out = ROOT / f"hist-212-resources/class-{date}.html"
    out.write_text(link_names(doc, day.get("nameLinks", {})))
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
