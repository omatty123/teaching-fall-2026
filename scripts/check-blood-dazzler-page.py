#!/usr/bin/env python3
"""Check the reading boundary, local resources, credits, and generated class page.

No network or third-party Python packages are needed. --check-generated also
reruns the builder and checks the committed page for an outstanding Git diff.
"""
import argparse
import hashlib
import json
import math
import re
import struct
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

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



# The full explicit stop list is source data, but it must remove the common
# function words and pronouns rather than silently rank them as content words.
REQUIRED_STOP_WORDS = set("a an and of the to in with as at for but is was are it its that this these those my i you your he she her we our they their them him his me us be can will from".split())


def inline_styles(node):
    """Read the element's own styles, independently of a cached stylesheet."""
    return {name.strip().casefold(): value.strip().removesuffix("!important").strip()
            for declaration in node.attrs.get("style", "").split(";")
            if ":" in declaration
            for name, value in [declaration.split(":", 1)]}


def style_number(value, message):
    require(re.fullmatch(r"\d+(?:\.\d+)?(?:px)?", value or ""), message)
    number = float(value.removesuffix("px"))
    require(math.isfinite(number) and number > 0, message)
    return number


def color_luminance(value, message):
    # Explicit hex colors remain usable even if the stylesheet cannot load.
    require(re.fullmatch(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?", value or ""), message)
    digits = value[1:]
    if len(digits) == 3:
        digits = "".join(digit * 2 for digit in digits)
    channels = [int(digits[index:index + 2], 16) / 255 for index in (0, 2, 4)]
    linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
              for channel in channels]
    return sum(channel * weight for channel, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def check_word_stylesheet(document):
    stylesheet = ROOT / "_kit/blood-dazzler-words.css"
    links = [node for node in document.root.all("link")
             if "stylesheet" in node.attrs.get("rel", "").split()
             and local_path(node.attrs.get("href", ""), PAGE)[0] == stylesheet]
    require(len(links) == 1, "The word cloud needs one versioned words stylesheet.")
    version = parse_qs(urlsplit(links[0].attrs["href"]).query).get("v", [])
    expected = hashlib.sha256(stylesheet.read_bytes()).hexdigest()[:12]
    require(version == [expected], "Word-cloud stylesheet URL lacks the current CSS content hash; a cached older style can hide its labels.")


def check_frequency_data(data, counts):
    require(isinstance(data, dict), "Frequency cluster data must be an object.")
    scope = json.dumps(data.get("scope", ""), ensure_ascii=False)
    require(re.search(r"vii\s*[–-]\s*24", scope), "Frequency cluster scope must be the printed reading pp. vii–24.")
    require(isinstance(data.get("method"), str) and data["method"].strip(), "Frequency cluster must explain its counting/filtering method.")
    stops = data.get("stop_words")
    require(isinstance(stops, list) and all(isinstance(word, str) and word for word in stops), "Frequency cluster needs an explicit stop-word list.")
    require(len(stops) == len(set(stops)), "The stop-word list contains duplicates.")
    require(all(word == word.casefold().replace("’", "'") for word in stops), "Stop words must use the audited lowercase/apostrophe convention.")
    stop_words = set(stops)
    missing = (REQUIRED_STOP_WORDS & set(counts)) - stop_words
    require(not missing, f"Common function words/pronouns missing from the stop list: {sorted(missing)}")
    require(type(data.get("max_words")) is int and data["max_words"] == 50, "Frequency cluster must use the top 50 words after filtering.")
    expected = [{"word": word, "count": count} for word, count in sorted(
        ((word, count) for word, count in counts.items() if word not in stop_words),
        key=lambda item: (-item[1], item[0]))[:50]]
    words = data.get("words")
    require(isinstance(words, list) and words == expected, "Frequency cluster differs from the audited top 50 words sorted by descending count, then word.")
    require(all(type(item["count"]) is int and item["count"] > 0 for item in words), "Frequency cluster contains a nonpositive or invalid count.")
    return words


def check_frequency_cluster(document, section, counts):
    check_word_stylesheet(document)
    data = json.loads((ASSETS / "frequency-cluster.json").read_text(encoding="utf-8"))
    words = check_frequency_data(data, counts)
    require(any(clean(node.text()).casefold() == "word cloud" for node in section.all("h2")), "The frequency circles lack their Word cloud title.")
    elements = list(section.all())
    embedded = next((node for node in elements if node.attrs.get("id") == "bd-word-data"), None)
    require(embedded is not None and embedded.tag == "script" and embedded.attrs.get("type") == "application/json", "Frequency cluster lacks its embedded source data.")
    require(json.loads(embedded.text()) == data, "Rendered frequency data differs from frequency-cluster.json.")
    charts = [node for node in elements if node.tag == "svg"]
    require(len(charts) == 1, "The page needs one packed-circle frequency diagram.")
    chart = charts[0]
    chart_descriptions = [node for node in chart.children if isinstance(node, Element) and node.tag == "desc"]
    require(len(chart_descriptions) == 1 and clean(chart_descriptions[0].text()), "Frequency diagram lacks its native SVG description.")
    view_box = chart.attrs.get("viewbox", "").replace(",", " ").split()
    require(len(view_box) == 4, "The frequency SVG lacks a usable viewBox.")
    left, top, width, height = map(float, view_box)
    require(all(math.isfinite(value) for value in (left, top, width, height)) and width > 0 and height > 0, "Invalid frequency SVG bounds.")
    chart_style = inline_styles(chart)
    require(chart_style.get("display") == "block" and chart_style.get("width") == "100%"
            and chart_style.get("height") == "auto", "Frequency SVG lacks self-contained responsive sizing.")
    minimum_width = style_number(chart_style.get("min-width"), "Frequency SVG lacks a readable inline minimum width.")
    wrappers = [node for node in elements if "bd-frequency-chart" in node.attrs.get("class", "").split()]
    require(len(wrappers) == 1 and inline_styles(wrappers[0]).get("overflow-x") == "auto",
            "Frequency chart lacks self-contained horizontal scrolling for its large labels.")
    items = [node for node in chart.all() if "bd-frequency-word" in node.attrs.get("class", "").split()]
    require(len(items) == len(words) and len(list(chart.all("circle"))) == len(words), "Packed diagram must show exactly one circle per counted word.")
    expected_by_word = {item["word"]: item for item in words}
    identities = [item.attrs.get("data-word") for item in items]
    require(len(identities) == len(set(identities)) and set(identities) == set(expected_by_word), "Packed diagram omits or repeats a frequency word.")
    geometry = []
    for item in items:
        word = item.attrs["data-word"]
        expected = expected_by_word[word]
        require(item.attrs.get("data-count") == str(expected["count"]), f"Rendered frequency count is incorrect: {word}")
        circles = list(item.all("circle"))
        require(len(circles) == 1, f"Word does not have one native SVG circle: {word}")
        circle = circles[0]
        # Native presentation attributes are sufficient for the circles; text
        # uses inline CSS so an older external text rule cannot realign it.
        circle_style = {**circle.attrs, **inline_styles(circle)}
        circle_fill = color_luminance(circle_style.get("fill"), f"Circle lacks an explicit fill: {word}")
        require(circle_fill >= 0.5, f"Circle fill is too dark for its dark labels: {word}")
        color_luminance(circle_style.get("stroke"), f"Circle lacks an explicit stroke: {word}")
        style_number(circle_style.get("stroke-width"), f"Circle lacks a positive stroke width: {word}")
        x, y, radius = (float(circle.attrs.get(key, "0")) for key in ("cx", "cy", "r"))
        for transformed in (item, circle):
            transform = transformed.attrs.get("transform", "").strip()
            if transform:
                match = re.fullmatch(r"translate\(\s*([^()]*)\s*\)", transform)
                require(match is not None, f"Unsupported circle transform in frequency diagram: {word}")
                offsets = match.group(1).replace(",", " ").split()
                require(len(offsets) in (1, 2), f"Invalid circle translation: {word}")
                x += float(offsets[0])
                y += float(offsets[1]) if len(offsets) == 2 else 0
        require(all(math.isfinite(value) for value in (x, y, radius)) and radius > 0, f"Invalid circle geometry: {word}")
        require(x - radius >= left - 0.02 and y - radius >= top - 0.02 and x + radius <= left + width + 0.02 and y + radius <= top + height + 0.02, f"Frequency circle is clipped by the SVG bounds: {word}")
        titles, descriptions = list(item.all("title")), list(item.all("desc"))
        require(len(titles) == 1, f"Circle lacks its native SVG title: {word}")
        accessible = clean(titles[0].text() + " " + " ".join(node.text() for node in descriptions)).casefold()
        require(re.search(rf"\b{re.escape(word)}\b", accessible) and re.search(rf"\b{expected['count']}\b", accessible), f"Circle's accessible name omits its word or count: {word}")
        aria_label = item.attrs.get("aria-label", "").casefold()
        require(item.attrs.get("role") == "img" and re.search(rf"\b{re.escape(word)}\b", aria_label) and re.search(rf"\b{expected['count']}\b", aria_label), f"Circle's assistive label omits its word or count: {word}")
        labels = [node for node in item.all("text") if "bd-frequency-text" in node.attrs.get("class", "").split()]
        count_labels = [node for node in item.all("text") if "bd-frequency-count" in node.attrs.get("class", "").split()]
        # A long word may use separate tspan lines. Rejoin those lines rather
        # than treating the visual line break as a change to the counted word.
        require(len(labels) == 1 and re.sub(r"\s+", "", labels[0].text()).casefold() == word.casefold(), f"Circle does not visibly label its exact word: {word}")
        require(len(count_labels) == 1 and clean(count_labels[0].text()) == str(expected["count"]), f"Circle does not visibly label its exact count: {word}")
        for text, minimum_weight, kind in ((labels[0], 800, "word"), (count_labels[0], 700, "count")):
            styles = inline_styles(text)
            require(styles.get("text-anchor") == "middle", f"Circle {kind} lacks self-contained centered alignment: {word}")
            family = styles.get("font-family", "").casefold()
            require("source sans 3" in family and "sans-serif" in family, f"Circle {kind} lacks its inline legible font family: {word}")
            size = style_number(styles.get("font-size"), f"Circle {kind} lacks a positive inline font size: {word}")
            require(size * minimum_width / width >= 18 - 0.02, f"Circle {kind} becomes smaller than 18 screen pixels at its minimum chart width: {word}")
            weight = style_number(styles.get("font-weight"), f"Circle {kind} lacks an explicit inline font weight: {word}")
            require(weight >= minimum_weight, f"Circle {kind} is not bold enough: {word}")
            ink = color_luminance(styles.get("fill"), f"Circle {kind} lacks an explicit inline text color: {word}")
            require((circle_fill + 0.05) / (ink + 0.05) >= 4.5, f"Circle {kind} has insufficient contrast against its circle: {word}")
        geometry.append((word, expected["count"], x, y, radius))
    # r/sqrt(count) must be constant: therefore circle AREA, not radius or
    # lettering, represents frequency. 0.02 SVG units allows decimal rounding.
    scales = sorted(radius / math.sqrt(count) for _, count, _, _, radius in geometry)
    scale = (scales[(len(scales) - 1) // 2] + scales[len(scales) // 2]) / 2
    for word, count, _, _, radius in geometry:
        require(abs(radius - scale * math.sqrt(count)) <= 0.02, f"Circle area is not proportional to frequency: {word}")
    for index, (word, _, x, y, radius) in enumerate(geometry):
        for other, _, other_x, other_y, other_radius in geometry[index + 1:]:
            require(math.hypot(x - other_x, y - other_y) + 0.02 >= radius + other_radius, f"Frequency circles overlap: {word}, {other}")
    fallbacks = [node for node in elements if node.tag == "details" and "bd-frequency-count-list" in node.attrs.get("class", "").split()]
    require(len(fallbacks) == 1, "Frequency circles lack their readable word/count list.")
    readable = list(fallbacks[0].all("li"))
    require(len(readable) == len(words), "Readable frequency list omits or duplicates a word.")
    for item, expected in zip(readable, words):
        labels, values = list(item.all("span")), list(item.all("strong"))
        require(len(labels) == 1 and clean(labels[0].text()) == expected["word"], f"Readable list has the wrong word or order: {expected['word']}")
        require(len(values) == 1 and clean(values[0].text()) == str(expected["count"]), f"Readable list has the wrong count: {expected['word']}")
    require(not any(node.attrs.get("id") == "bd-word-selected" or "bd-word-group" in node.attrs.get("class", "").split() for node in elements), "The replaced interpretive graph remains in the frequency section.")
    return len(words)


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
    expected = {"map", "photographs", "video", "words", "characters", "poems", "discussion"}
    require(expected <= sections.keys(), f"Missing class sections: {sorted(expected - sections.keys())}")
    require("important-words" not in sections, "The replaced important-words section remains visible; retain its legacy anchor only inside the words section if needed.")
    for node in nodes:
        if node.tag in {"h1", "h2", "h3", "h4", "h5", "h6", "summary"}:
            label = clean(node.text())
            require(not re.search(r"\bmost\s+(?:common|used|important)\s+words\b|\blong[ -]+words?\b", label, re.I), f"Replaced word-ranking analysis remains visible: {label}")
    poem_text = clean(sections["poems"].text())
    require("What to Tweak" not in poem_text, "The rendered poem list includes unassigned reading.")
    require(all(poem["title"] in poem_text for poem in poems), "The rendered poem list omits an assigned poem.")
    page_text = clean(document.root.text())
    require("Monday, October 5, 2026" in page_text and "pp. vii–24" in page_text, "Displayed session date or assigned reading is incorrect.")
    require("pdf_pages_included" not in page_text and "total_tokens" not in page_text, "Internal audit metadata was printed in the class page.")
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
        require(counts.get(word["word"]) == word["count"], f"Archived frequency metadata disagrees with its source count for {word['word']}.")
    if "total_tokens" in counts_record:
        require(sum(counts.values()) == counts_record["total_tokens"], "Full word counts do not sum to their declared total.")
    if "pdf_pages_included" in counts_record:
        require(set(counts_record["pdf_pages_included"]) == {9, 10, *range(15, 39)}, "Word counts include an unassigned PDF page or omit an assigned page.")
    word_nodes = check_frequency_cluster(document, sections["words"], counts)
    return duration, word_nodes


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
        duration, word_nodes = check_content(document)
    except (OSError, ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as error:
        print(f"Blood Dazzler check failed: {error}", file=sys.stderr)
        return 1
    print(f"Blood Dazzler check passed: 22 poems through p. 24; {word_nodes} filtered frequency words; {resources} local resources; complete {duration:.2f}s rescue video.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
