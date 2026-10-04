#!/usr/bin/env python3
"""Check the reading boundary, local resources, credits, and generated class page.

No network or third-party Python packages are needed. --check-generated also
reruns the builder and checks the committed page for an outstanding Git diff.
"""
import argparse
import json
import re
import struct
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "frst-110-resources/blood-dazzler-oct-5.html"
ASSETS = PAGE.parent / "blood-dazzler-assets"
PUBLIC_URL = "https://omatty123.github.io/teaching-fall-2026/" + PAGE.relative_to(ROOT).as_posix()
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


@dataclass
class Element:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def all(self, tag=None):
        for child in self.children:
            if isinstance(child, Element):
                if tag is None or child.tag == tag:
                    yield child
                yield from child.all(tag)

    def text(self):
        return " ".join(child.text() if isinstance(child, Element) else child for child in self.children)


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = Element("document")
        self.stack = [self.root]
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        node = Element(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def clean(text):
    return " ".join(text.split())


def local_path(url, origin):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc:
        return None, ""
    path = unquote(parsed.path)
    if not path:
        target = origin
    elif path.startswith("/"):
        # GitHub Pages uses a repository prefix rather than the host's root.
        target = ROOT / path.removeprefix("/teaching-fall-2026/").lstrip("/")
    else:
        target = origin.parent / path
    target = target.resolve()
    require(target.is_relative_to(ROOT), f"Local link leaves the website: {url}")
    return target, unquote(parsed.fragment)


def check_local_resources(document):
    documents = {PAGE: document}
    checked = set()
    stylesheets = set()
    ids = [node.attrs["id"] for node in document.root.all() if "id" in node.attrs]
    require(len(ids) == len(set(ids)), "The page contains duplicate HTML IDs.")
    for node in document.root.all():
        for attribute in ("href", "src", "poster"):
            value = node.attrs.get(attribute)
            if not value:
                continue
            target, fragment = local_path(value, PAGE)
            if target is None:
                continue
            require(target.is_file(), f"Missing local {node.tag} {attribute}: {value}")
            checked.add(target)
            if node.tag == "link" and "stylesheet" in node.attrs.get("rel", "").split():
                stylesheets.add(target)
            if fragment and target.suffix.lower() == ".html":
                if target not in documents:
                    documents[target] = Document(target.read_text(encoding="utf-8"))
                target_ids = {item.attrs.get("id") for item in documents[target].root.all()}
                require(fragment in target_ids, f"Missing local HTML anchor: {value}")
    # Vendored Leaflet CSS also refers to local control/marker images.
    pending = list(stylesheets)
    seen_stylesheets = set()
    while pending:
        stylesheet = pending.pop()
        if stylesheet in seen_stylesheets:
            continue
        seen_stylesheets.add(stylesheet)
        text = stylesheet.read_text(encoding="utf-8")
        refs = re.findall(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", text)
        refs += re.findall(r"@import\s+['\"]([^'\"]+)['\"]", text)
        for value in refs:
            target, _ = local_path(value.strip(), stylesheet)
            if target is None or not urlsplit(value).path:
                continue
            require(target.is_file(), f"Missing CSS resource in {stylesheet.name}: {value}")
            checked.add(target)
            if target.suffix.lower() == ".css":
                pending.append(target)
    return len(checked)


def mp4_duration(path):
    """Read the movie duration from an MP4 mvhd box, without ffprobe."""
    blob = path.read_bytes()

    def boxes(start, end):
        while start + 8 <= end:
            size, kind = struct.unpack_from(">I4s", blob, start)
            header = 8
            if size == 1:
                require(start + 16 <= end, "Truncated MP4 extended box.")
                size = struct.unpack_from(">Q", blob, start + 8)[0]
                header = 16
            elif size == 0:
                size = end - start
            require(size >= header and start + size <= end, "Invalid or truncated MP4 box.")
            yield kind, start + header, start + size
            start += size

    top = list(boxes(0, len(blob)))
    require({b"ftyp", b"moov", b"mdat"} <= {kind for kind, _, _ in top}, "Video is not a complete MP4 movie.")
    for kind, start, end in top:
        if kind != b"moov":
            continue
        for child, payload, stop in boxes(start, end):
            if child != b"mvhd":
                continue
            require(stop - payload >= 32, "Truncated MP4 movie header.")
            version = blob[payload]
            require(version in (0, 1), "Unsupported MP4 movie-header version.")
            offset = payload + (20 if version else 12)
            timescale = struct.unpack_from(">I", blob, offset)[0]
            duration = struct.unpack_from(">Q" if version else ">I", blob, offset + 4)[0]
            require(timescale > 0, "MP4 movie has no usable duration.")
            return duration / timescale
    raise ValueError("MP4 has no movie duration.")


def check_content(document):
    reading = json.loads((ASSETS / "reading-data.json").read_text(encoding="utf-8"))
    poems = reading["poems"]
    require(len(poems) == 22, "Assigned reading must contain exactly 22 poems.")
    require(poems[0]["pages"] == "vii–viii" and "Prologue" in poems[0]["title"], "Reading must begin with the prologue on pp. vii–viii.")
    require(poems[-1]["pages"] == "24" and poems[-1]["title"] == "Voodoo II: Money", "Reading must end with Voodoo II: Money on p. 24.")
    for poem in poems:
        require("What to Tweak" not in poem["title"], "What to Tweak is outside this assigned reading.")
        require(all(int(number) <= 24 for number in re.findall(r"\d+", poem["pages"])), f"Out-of-scope assigned page: {poem['title']}")
    nodes = list(document.root.all())
    sections = {node.attrs["id"]: node for node in nodes if node.tag == "section" and "id" in node.attrs}
    expected = {"map", "photographs", "video", "words", "important-words", "characters", "poems", "discussion"}
    require(expected <= sections.keys(), f"Missing class sections: {sorted(expected - sections.keys())}")
    poem_text = clean(sections["poems"].text())
    require("What to Tweak" not in poem_text, "The rendered poem list includes unassigned reading.")
    require(all(poem["title"] in poem_text for poem in poems), "The rendered poem list omits an assigned poem.")
    page_text = clean(document.root.text())
    require("Monday, October 5, 2026" in page_text and "pp. vii–24" in page_text, "Displayed session date or assigned reading is incorrect.")
    require("pdf_pages_included" not in page_text and "total_tokens" not in page_text, "Internal count data was printed instead of the word ranking.")
    title = clean(next(document.root.all("title")).text())
    require(all(value in title for value in ("Blood Dazzler", "October 5", "FRST 110")), "Page title does not identify this class resource.")
    metadata = {node.attrs.get("property", node.attrs.get("name")): node.attrs.get("content", "") for node in nodes if node.tag == "meta"}
    require(metadata.get("og:url") == PUBLIC_URL, "Open Graph URL does not point to the published class page.")
    require(metadata.get("og:image", "").startswith(PUBLIC_URL.rsplit("/", 1)[0] + "/blood-dazzler-assets/"), "Social preview image does not point to this page's assets.")
    for key in ("description", "og:description"):
        require("vii–24" in metadata.get(key, ""), f"Incorrect reading boundary in {key} metadata.")
    for place in ("Mississippi River", "Lake Pontchartrain", "Industrial Canal", "French Quarter", "Lower Ninth Ward"):
        require(place in clean(sections["map"].text()), f"Map fallback omits {place}.")
    for source in ("SOURCES.md", "MAP-SOURCES.md", "media-sources.json"):
        path = ASSETS / source
        require(path.is_file() and path.stat().st_size > 100, f"Missing or empty public source record: {source}")
    sources = json.loads((ASSETS / "media-sources.json").read_text(encoding="utf-8"))
    photos = list(sections["photographs"].all("img"))
    require(len(photos) >= 2, "The class page needs both rooftop photographs.")
    for photo in photos:
        require(bool(photo.attrs.get("alt", "").strip()), "A rooftop photograph lacks an accessible description.")
        image, _ = local_path(photo.attrs["src"], PAGE)
        require(image is not None and image.stat().st_size > 10_000, "A rooftop photograph is missing or only a placeholder.")
    photo_text = clean(sections["photographs"].text())
    for record in sources["images"]:
        formatted = date.fromisoformat(record["date"]).strftime("%B %d, %Y").replace(" 0", " ")
        require(formatted in photo_text, f"Missing source date for rooftop photograph {record['id']}.")
    require("Public domain" in photo_text and "FEMA" in photo_text and "Coast Guard" in photo_text, "Rooftop photograph rights or agency credits are missing.")
    video_section = sections["video"]
    videos = list(video_section.all("video"))
    require(len(videos) == 1 and "controls" in videos[0].attrs, "Rescue footage needs one video player with controls.")
    video_sources = list(videos[0].all("source"))
    require(bool(video_sources), "Rescue video player has no source.")
    video, _ = local_path(video_sources[0].attrs["src"], PAGE)
    require(video is not None and video.stat().st_size >= 1_000_000, "Rescue video is missing, remote-only, or a tiny placeholder.")
    duration = mp4_duration(video)
    require(duration >= 30 and abs(duration - sources["video"]["duration_seconds"]) < 2, "Video is truncated or does not match the sourced rescue footage.")
    video_text = clean(video_section.text())
    require("September 12, 2005" in video_text and "1st Combat Camera Squadron" in video_text and "Public domain" in video_text, "Rescue footage date, credit, or rights is incorrect.")
    source_url = sources["video"]["source_page_url"]
    require(any(node.attrs.get("href") == source_url for node in video_section.all("a")), "Rescue footage lacks its official source link.")
    tracks = list(videos[0].all("track"))
    require(any(track.attrs.get("kind") == "descriptions" for track in tracks), "Rescue footage lacks its visual-description track.")
    for track in tracks:
        path, _ = local_path(track.attrs["src"], PAGE)
        require(path is not None and path.read_text(encoding="utf-8").startswith("WEBVTT"), "Video track is not a valid local WebVTT file.")
    counts_record = json.loads((ASSETS / "counts-vii-24.json").read_text(encoding="utf-8"))
    counts = counts_record.get("counts", counts_record)
    for word in reading["frequency"]["words"] + reading["frequency"]["pronouns"]:
        require(counts.get(word["word"]) == word["count"], f"Frequency table disagrees with its source count for {word['word']}.")
    if "total_tokens" in counts_record:
        require(sum(counts.values()) == counts_record["total_tokens"], "Full word counts do not sum to their declared total.")
    if "pdf_pages_included" in counts_record:
        require(set(counts_record["pdf_pages_included"]) == {9, 10, *range(15, 39)}, "Word counts include an unassigned PDF page or omit an assigned page.")
    return duration


def check_generated():
    before = PAGE.read_bytes()
    subprocess.run([sys.executable, "scripts/build-blood-dazzler-page.py"], cwd=ROOT, check=True)
    require(PAGE.read_bytes() == before, "Builder changed the generated page. Rebuild and save the updated HTML before committing.")
    relative = PAGE.relative_to(ROOT).as_posix()
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", "--", relative], cwd=ROOT, capture_output=True).returncode == 0
    if tracked:
        result = subprocess.run(["git", "diff", "--exit-code", "--", relative], cwd=ROOT)
        require(result.returncode == 0, "Generated HTML differs from its Git index. Commit the rebuilt page with its inputs.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-generated", action="store_true", help="rerun the builder and check generated HTML against Git")
    args = parser.parse_args()
    try:
        if args.check_generated:
            check_generated()
        document = Document(PAGE.read_text(encoding="utf-8"))
        resources = check_local_resources(document)
        duration = check_content(document)
    except (OSError, ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as error:
        print(f"Blood Dazzler check failed: {error}", file=sys.stderr)
        return 1
    print(f"Blood Dazzler check passed: 22 poems through p. 24; {resources} local resources; complete {duration:.2f}s rescue video.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
