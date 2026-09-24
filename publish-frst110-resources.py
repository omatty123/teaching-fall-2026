#!/usr/bin/env python3
"""Copy the FRST 110 Gilgamesh XI page (companion + annotated Helle reader) into
frst-110-resources/ for the PUBLIC site, adding what the deploy checklist needs
(OG/Twitter tags with an absolute image, and a back breadcrumb to the course).
Sibling of publish-hist212-resources.py. Source files are never modified.

    python3 publish-frst110-resources.py
"""
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).parent
BASE = "https://omatty123.github.io/teaching-fall-2026/"
SRC = pathlib.Path("/Users/wegehaum/Documents/ChatGPT/FALL 2026/course-materials/frst-110/readings/annotated")
OUT = ROOT / "frst-110-resources"
ASSETS = "gilgamesh-xi-assets"
NAME = "gilgamesh-xi.html"
PDF = "frst-110-0925-gilgamesh-reader.pdf"          # the page links this name relatively
IMG = BASE + f"frst-110-resources/{ASSETS}/flood-tablet.jpg"

TITLE = "Gilgamesh, Tablet XI · FRST 110"
DESC = ("The flood tablet: Helle's translation with notes, the cuneiform read aloud in Akkadian, "
        "and a map of the places in the story.")

CRUMB = ('<nav class="breadcrumb" style="font:600 13px/1.4 Inter,system-ui,sans-serif;padding:10px 16px;'
         'background:#f4efe9;border-bottom:1px solid #d9d0c5"><a href="../courses/frst-110.html" '
         'style="color:#7a3030">&larr; Back to FRST 110</a></nav>')


def meta():
    url = BASE + "frst-110-resources/" + NAME
    rows = [("property", "og:title", TITLE), ("property", "og:description", DESC),
            ("property", "og:image", IMG), ("property", "og:url", url), ("property", "og:type", "website"),
            ("name", "twitter:card", "summary_large_image"), ("name", "twitter:title", TITLE),
            ("name", "twitter:description", DESC), ("name", "twitter:image", IMG)]
    return "".join(f'<meta {k}="{n}" content="{v}">' for k, n, v in rows)


OUT.mkdir(exist_ok=True)
h = (SRC / "frst-110-0925-gilgamesh-reader.html").read_text(encoding="utf-8")
assert "og:image" not in h, "source already carries OG tags; check before doubling them"
h = h.replace("</head>", meta() + "</head>", 1)
h = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + CRUMB, h, count=1)
(OUT / NAME).write_text(h, encoding="utf-8")
shutil.copy(SRC / PDF, OUT / PDF)
shutil.rmtree(OUT / ASSETS, ignore_errors=True)
shutil.copytree(SRC / ASSETS, OUT / ASSETS)

# every local reference in the page must exist in the published folder
refs = set(re.findall(r'(?:src|href)="(?!https?:|data:|#|mailto:|\.\./)([^"#?]+)', h))
missing = sorted(r for r in refs if not (OUT / r).exists())
if missing:
    raise SystemExit("missing from frst-110-resources/: %s" % missing)
print("wrote", OUT / NAME, "| local refs ok:", len(refs), "| assets:", len(list((OUT / ASSETS).iterdir())))


# Sample filled workbook pages (the instructor's model sheet for each class day),
# the colour/blue-ink PDFs from the workbook builder. Meeting n -> meeting-NN.pdf.
WB = pathlib.Path("/Users/wegehaum/Documents/ChatGPT/FALL 2026/course-materials/frst-110/workbook")
SAMPLES = OUT / "workbook-samples"
SAMPLES.mkdir(exist_ok=True)
got = []
for pdf in sorted(WB.glob("FRST-110-Mock-Filled-Sheet-Meeting-*.pdf")):
    m = re.fullmatch(r"FRST-110-Mock-Filled-Sheet-Meeting-(\d+)\.pdf", pdf.name)
    if m:
        shutil.copy(pdf, SAMPLES / f"meeting-{int(m.group(1)):02d}.pdf")
        got.append(int(m.group(1)))
print("workbook samples:", got)
