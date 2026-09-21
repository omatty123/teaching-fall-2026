#!/usr/bin/env python3
"""Copy the HIST 212 ancient-China pages and the Sep 22 annotated reader into
hist-212-resources/ for the PUBLIC site, adding what the deploy checklist needs
(OG/Twitter tags with an absolute image, and a back breadcrumb to the course).

Whitelisted files only. Source roots are never modified.

    python3 publish-hist212-resources.py
"""
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).parent
BASE = "https://omatty123.github.io/teaching-fall-2026/"
SRC = pathlib.Path("/Users/wegehaum/workspaces/hist-212-ancient-china-quiz")
READER = pathlib.Path("/Users/wegehaum/Documents/ChatGPT/FALL 2026/course-materials/hist-212/readings/annotated/hist-212-0922-annotated-reader.html")
OUT = ROOT / "hist-212-resources"
IMG = BASE + "images/hist-212-banner.jpg"

PAGES = {
    "index.html": (SRC / "index.html", "Ancient China illustrated chronology",
                   "Clickable chart of the rulers, dynasties and sources from the Sanhuang to Eastern Zhou."),
    "quiz.html": (SRC / "quiz.html", "Ancient China practice quiz",
                  "Forty practice questions on early Chinese rulers and dynasties."),
    "history-notes.html": (SRC / "history-notes.html", "China history notes",
                           "Xia, Shang and Western Zhou compared, with primary sources in English."),
    "0922-reader.html": (READER, "Tuesday Sep 22 annotated reader",
                         "The Tang declarations and Kongzi passages, with a note beside each phrase you click."),
}

CRUMB = ('<nav class="breadcrumb" style="font:600 13px/1.4 Inter,system-ui,sans-serif;padding:10px 16px;'
         'background:#f4efe9;border-bottom:1px solid #d9d0c5"><a href="../courses/hist-212.html" '
         'style="color:#7a3030">&larr; Back to HIST 212</a></nav>')


def meta(title, desc, name):
    url = f"{BASE}hist-212-resources/{name}"
    t = f"{title} · HIST 212"
    rows = [("property", "og:title", t), ("property", "og:description", desc),
            ("property", "og:image", IMG), ("property", "og:url", url), ("property", "og:type", "website"),
            ("name", "twitter:card", "summary_large_image"), ("name", "twitter:title", t),
            ("name", "twitter:description", desc), ("name", "twitter:image", IMG)]
    return "".join(f'<meta {k}="{n}" content="{v}">' for k, n, v in rows)


shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir()
for name, (path, title, desc) in PAGES.items():
    h = path.read_text(encoding="utf-8")
    h = h.replace("</head>", meta(title, desc, name) + "</head>", 1)
    h = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + CRUMB, h, count=1)
    (OUT / name).write_text(h, encoding="utf-8")
for f in ("app.js", "data.js", "primary-sources.js", "timeline.js", "style.css", "timeline.css", "history-notes.css"):
    shutil.copy(SRC / f, OUT / f)
(OUT / "assets").mkdir()
for d in ("original", "history-notes", "wuliang"):
    shutil.copytree(SRC / "assets" / d, OUT / "assets" / d)
shutil.rmtree(OUT / "assets/wuliang/raw", ignore_errors=True)
(OUT / "assets/wuliang/provenance.json").unlink(missing_ok=True)
print("wrote", OUT, sorted(p.name for p in OUT.iterdir()))
