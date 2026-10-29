"""Check the student resource's links, attribution, and audience boundary."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "buen-594-resources/internship-ethics-cases.html"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.cases = [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "article":
            self.cases.append(attrs.get("id"))


source = PAGE.read_text()
page = Page()
page.feed(source)
assert len(page.ids) == len(set(page.ids)), "Duplicate section IDs"
assert page.cases == ["full-disclosure", "scholarship-application", "gis-internship"]
for link in page.links:
    assert link, "Empty link"
    parts = urlsplit(link)
    if link.startswith("#"):
        assert parts.fragment in page.ids, f"Missing section: {link}"
    elif not parts.scheme:
        assert (PAGE.parent / parts.path).resolve().is_file(), f"Missing local target: {link}"
assert "teaching-fall-2026-roster" not in source, "Private HQ URL on student page"
assert "/Users/" not in source and "Teaching assessment" not in source
assert "ScholarshipTN" not in source, "Instructor notes on student page"
required_sources = {
    "https://ethicsunwrapped.utexas.edu/case-study/full-disclosure-manipulating-donors",
    "https://kenan.ethics.duke.edu/wp-content/uploads/2018/01/Scholarship20151.pdf",
    "https://cartographicperspectives.org/index.php/journal/article/view/1941",
    "https://cartographicperspectives.org/index.php/journal/article/download/1941/2335?inline=1",
}
assert required_sources <= set(page.links), "Missing original source link"
course = json.loads((ROOT / "data/buen-594.json").read_text())
relative = "../buen-594-resources/internship-ethics-cases.html"
assert any(x["href"] == relative for x in course.get("readingGuides", []))
assert relative in (ROOT / "courses/buen-594.html").read_text()
print("BUEN student page: three cases, original sources, navigation, and audience checks passed.")
