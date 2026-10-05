"""Check the concise classroom resource and its deployable local links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "frst-110-resources/summary-explainer.html"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings, self.links, self.ids, self.text = [], [], [], []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("style", "script", "head"):
            self.hidden += 1
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h2":
            self.headings.append(attrs.get("id"))
        if tag == "a":
            self.links.append(attrs.get("href", ""))

    def handle_endtag(self, tag):
        if tag in ("style", "script", "head"):
            self.hidden -= 1

    def handle_data(self, text):
        if not self.hidden:
            self.text.append(text)


p = Page()
html = PAGE.read_text()
p.feed(html)
assert set(p.headings) == {"place", "causes", "thesis", "ending"}
assert len(p.ids) == len(set(p.ids)), "Duplicate IDs break in-page navigation"
assert "<script" not in html, "This classroom screen must remain static"
assert len(" ".join(p.text).split()) <= 230, "Keep the five-minute explainer concise"
assert not any(x in html for x in ("/Users/", "private-data", "student_id=")), "Private/local data must not ship"
for href in p.links:
    u = urlparse(href)
    if u.fragment and not u.path:
        assert u.fragment in p.ids
    elif not u.scheme:
        assert (PAGE.parent / u.path).resolve().is_file(), f"Broken link: {href}"
assert (ROOT / "_kit/fonts/SourceSans3VF-Upright.woff2").is_file()
assert (ROOT / "frst-110-resources/summary-explainer.pdf").read_bytes().startswith(b"%PDF-")
print("Summary explainer: concise copy, required explanations, static fallback, links, and public-safe paths pass")
