#!/usr/bin/env python3
"""Check the October 7 reading boundary, sourced local media, and exact word counts."""

import importlib.util
import json
import math
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "frst-110-resources/blood-dazzler-oct-7.html"
ASSETS = PAGE.parent / "blood-dazzler-assets"

# Share the established no-dependency HTML/link/MP4 checks with the first page.
spec = importlib.util.spec_from_file_location("reading_page_checks", ROOT / "scripts/check-blood-dazzler-page.py")
common = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = common
spec.loader.exec_module(common)
require = common.require


def jpeg_dimensions(path):
    """Read intrinsic JPEG dimensions without adding a third-party dependency."""
    blob = path.read_bytes()
    require(blob[:2] == b"\xff\xd8", f"{path.name}: not a JPEG image.")
    offset = 2
    frame_markers = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while offset < len(blob):
        require(blob[offset] == 0xFF, f"{path.name}: invalid JPEG marker.")
        while offset < len(blob) and blob[offset] == 0xFF:
            offset += 1
        require(offset < len(blob), f"{path.name}: truncated JPEG marker.")
        marker = blob[offset]
        offset += 1
        if marker in {0x01, 0xD8, 0xD9} or 0xD0 <= marker <= 0xD7:
            continue
        require(offset + 2 <= len(blob), f"{path.name}: truncated JPEG segment.")
        length = int.from_bytes(blob[offset:offset + 2], "big")
        require(length >= 2 and offset + length <= len(blob), f"{path.name}: invalid JPEG segment length.")
        if marker in frame_markers:
            require(length >= 8, f"{path.name}: truncated JPEG frame.")
            height = int.from_bytes(blob[offset + 3:offset + 5], "big")
            width = int.from_bytes(blob[offset + 5:offset + 7], "big")
            require(width > 0 and height > 0, f"{path.name}: missing intrinsic image dimensions.")
            return width, height
        require(marker != 0xDA, f"{path.name}: JPEG scan precedes its dimensions.")
        offset += length
    raise ValueError(f"{path.name}: JPEG has no image dimensions.")


def main():
    subprocess.run([sys.executable, str(ROOT / "scripts/build-blood-dazzler-oct7.py"), "--check"], check=True)
    document = common.Document(PAGE.read_text(encoding="utf-8"))
    nodes = list(document.root.all())
    by_id = {node.attrs["id"]: node for node in nodes if "id" in node.attrs}
    body_text = common.clean(document.root.text())
    require(date(2026, 10, 7).strftime("%A") == "Wednesday", "The class date does not fall on Wednesday.")
    require("Patricia Smith · Wednesday, October 7, 2026 · pp. 25–49" in body_text, "Missing the exact October 7 reading date and page range.")
    schedule = json.loads((ROOT / "data/frst-110.json").read_text(encoding="utf-8"))["schedule"]
    meeting = next(item for item in schedule if item["date"] == "2026-10-07")
    class_url = "https://omatty123.github.io/teaching-fall-2026/frst-110-resources/blood-dazzler-oct-7.html"
    require(meeting["detail"] == "pp. 25–49" and any(item.get("href") == class_url for item in meeting["materials"]), "The October 7 course schedule must link to this reading page.")
    require(len(list(document.root.all("h1"))) == 1, "The page needs one main title.")
    section_ids = ("what-is-tanka", "write-tanka", "sestina", "federal-response", "barbara-bush", "evacuation", "superdome-photos", "ethel-freeman", "words-second")
    require(set(section_ids) <= by_id.keys(), "A requested classroom resource is missing its jump target.")
    section_order = tuple(node.attrs["id"] for node in document.root.all("section") if node.attrs.get("id") in section_ids)
    require(section_order == section_ids, "The requested photographs must follow evacuation and precede the unchanged word cloud.")
    section_navs = [node for node in document.root.all("nav") if node.attrs.get("class") == "section-nav"]
    require(len(section_navs) == 1, "The page needs one section navigation.")
    nav_links = list(section_navs[0].all("a"))
    require(tuple(node.attrs.get("href") for node in nav_links) == tuple(f"#{item}" for item in section_ids), "The section navigation must link to all nine resources in page order.")
    require(tuple(common.clean(node.text()) for node in nav_links)[6:8] == ("Superdome", "Ethel Freeman"), "The photographs need the requested navigation labels.")
    require("5–7–5–7–7" in body_text and "“Tankas,” pp. 38–39" in body_text, "Missing the tanka pattern or book locator.")
    require(len(list(by_id["write-tanka"].all("li"))) == 4, "Expected four short writing steps.")
    require("brownie" not in by_id, "The standalone Brownie player duplicates the longer documentary excerpt.")
    require("Federal response in When the Levees Broke" in body_text, "The longer excerpt needs its requested subject heading.")
    require("“What to Tweak,” pp. 25–28" in body_text and "“The President Flies Over,” p. 36" in body_text, "The longer excerpt needs its verified poem references.")
    require(any(node.attrs.get("href") == "https://youtu.be/CTVy-JC-Lag?t=4864" for node in by_id["federal-response"].all("a")), "The longer excerpt needs the exact supplied documentary link.")
    require("“Thankful,” pp. 48–49" in body_text, "Barbara Bush's clip needs its verified poem reference.")
    require("September 5, 2005" in body_text, "Barbara Bush's remarks need their event date.")
    require(not list(document.root.all("iframe")), "Classroom clips must be local native players, not remote embeds.")
    require(not list(document.root.all("script")) or all(node.attrs.get("type") == "application/json" for node in document.root.all("script")), "This static page should not add remote or executable scripts.")

    videos = list(document.root.all("video"))
    require(len(videos) == 3, "Expected only federal-response, Barbara Bush, and separate evacuation players.")
    expected = (
        ("levees-federal-response", 258.0, 258.15),
        ("barbara-bush-katrina", 18.9, 19.1),
        ("levees-evacuation", 131.55, 131.75),
    )
    durations = []
    for video, (filename, minimum, maximum) in zip(videos, expected):
        require("controls" in video.attrs and "playsinline" in video.attrs, f"{filename}: missing native player controls or inline playback.")
        require(video.attrs.get("preload") == "none", f"{filename}: do not preload full classroom clips.")
        require(not {"autoplay", "loop", "muted"} & video.attrs.keys(), f"{filename}: playback must start only when selected, with its original audio.")
        require(video.attrs.get("aria-label") and video.attrs.get("aria-describedby") in by_id, f"{filename}: missing an accessible label or caption.")
        require(video.attrs.get("poster") == f"blood-dazzler-assets/oct7/{filename}-poster.jpg", f"{filename}: missing its own visible poster.")
        sources = list(video.all("source"))
        require(len(sources) == 1 and sources[0].attrs.get("type") == "video/mp4", f"{filename}: expected one MP4 source.")
        require(sources[0].attrs.get("src") == f"blood-dazzler-assets/oct7/{filename}.mp4", f"{filename}: unexpected video source.")
        duration = common.mp4_duration(ASSETS / "oct7" / f"{filename}.mp4")
        require(minimum <= duration <= maximum, f"{filename}: duration {duration:.3f}s is outside the reviewed excerpt range {minimum}–{maximum}s.")
        durations.append(f"{filename}: {duration:.3f}s")

    photos = (
        ("superdome-photos", "superdome-roof-close.jpg",
         "https://commons.wikimedia.org/wiki/File:Superdome_Roof_Damage_FEMA.jpg"),
        ("superdome-photos", "superdome-roof-aerial.jpg",
         "https://commons.wikimedia.org/wiki/File:FEMA_-_17670_-_Photograph_by_Jocelyn_Augustino_taken_on_09-04-2005_in_Louisiana.jpg"),
        ("ethel-freeman", "ethel-freeman-wheelchair.jpg",
         "https://www.ctinsider.com/news/article/Hurricane-Katrina-Sept-2-2005-in-photos-6465422.php"),
    )
    images = list(document.root.all("img"))
    require(len(images) == 3, "Expected exactly the two Superdome photographs and one Ethel Freeman photograph.")
    for image, (section_id, filename, source) in zip(images, photos):
        require(image.attrs.get("src") == f"blood-dazzler-assets/oct7/{filename}", f"{filename}: unexpected still-image source.")
        alt = common.clean(image.attrs.get("alt", ""))
        require(alt and alt.casefold() not in {"image", "photo", "photograph", "picture", filename.casefold()}, f"{filename}: missing a descriptive, accessible alt text.")
        require(image.attrs.get("loading") == "lazy" and image.attrs.get("decoding") == "async", f"{filename}: use lazy loading and asynchronous decoding.")
        width, height = jpeg_dimensions(ASSETS / "oct7" / filename)
        require(image.attrs.get("width") == str(width) and image.attrs.get("height") == str(height), f"{filename}: HTML dimensions must match the complete JPEG frame ({width}×{height}).")
        figures = [node for node in by_id[section_id].all("figure") if image in list(node.all("img"))]
        require(len(figures) == 1, f"{filename}: image must belong to its requested section and figure.")
        captions = list(figures[0].all("figcaption"))
        require(len(captions) == 1 and common.clean(captions[0].text()), f"{filename}: missing its photograph caption.")
        require(any(node.attrs.get("href") == source for node in captions[0].all("a")), f"{filename}: missing its supplied photograph source link.")
        if section_id == "ethel-freeman":
            caption_text = common.clean(captions[0].text())
            require(all(credit in caption_text for credit in ("©", "Eric Gay", "Associated Press")), "Ethel Freeman's photograph needs its AP copyright credit.")
    for section_id, heading, reference in (
        ("superdome-photos", "Superdome roof damage", "Read alongside “Superdome,” p. 40."),
        ("ethel-freeman", "Ethel Freeman", "Read alongside “Ethel’s Sestina,” pp. 45–46."),
    ):
        headings = list(by_id[section_id].all("h2"))
        require(len(headings) == 1 and common.clean(headings[0].text()) == heading, f"{section_id}: missing the requested photograph heading.")
        require(reference in common.clean(by_id[section_id].text()), f"{section_id}: missing its verified poem reference.")

    # Remote links are credits only. Media and stylesheet requests stay local.
    for node in nodes:
        for attribute in ("src", "poster"):
            if attribute in node.attrs:
                parsed = urlsplit(node.attrs[attribute])
                require(not parsed.scheme and not parsed.netloc, f"External {attribute} request: {node.attrs[attribute]}")
        if node.tag == "link" and node.attrs.get("rel") == "stylesheet":
            parsed = urlsplit(node.attrs["href"])
            require(not parsed.scheme and not parsed.netloc, "Stylesheets must use the existing local font and visual system.")

    canonical = json.loads((ASSETS / "frequency-25-49.json").read_text(encoding="utf-8"))
    require(canonical["scope"] == "pp. 25–49" and len(canonical["words"]) == 50, "Unexpected canonical reading scope or count coverage.")
    embedded = json.loads(by_id["bd-second-word-data"].text())
    require(embedded == canonical, "The page's embedded word data differs from the canonical section counts.")
    groups = [node for node in document.root.all("g") if node.attrs.get("class") == "bd-frequency-word"]
    rendered = [{"word": node.attrs.get("data-word"), "count": int(node.attrs.get("data-count", -1))} for node in groups]
    require(rendered == canonical["words"], "The visible circles omit or change one of the canonical 50 counts.")
    count_lists = [node for node in document.root.all("details") if node.attrs.get("class") == "bd-frequency-count-list"]
    require(len(count_lists) == 1, "The cloud needs one readable list of all counts.")
    expected_counts = [f'{item["word"]} {item["count"]}' for item in canonical["words"]]
    actual_counts = [common.clean(node.text()) for node in count_lists[0].all("li")]
    require(actual_counts == expected_counts, "The readable list differs from the visible canonical counts.")
    require(len([node for node in document.root.all("details") if node.attrs.get("class") == "bd-frequency-method"]) == 1, "The counting method disclosure is missing.")
    charts = [node for node in document.root.all("div") if node.attrs.get("class") == "bd-frequency-chart"]
    require(len(charts) == 1 and charts[0].attrs.get("role") == "region" and charts[0].attrs.get("tabindex") == "0", "The wide cloud needs its own keyboard-accessible scroll region.")
    svg = next(charts[0].all("svg"))
    scale = float(svg.attrs["width"]) / float(svg.attrs["viewbox"].split()[2])
    word_texts = [node for node in svg.all("text") if node.attrs.get("class") == "bd-frequency-text"]
    require(len(word_texts) == 50 and min(float(node.attrs["font-size"]) * scale for node in word_texts) >= 19.99, "A displayed word is smaller than the required 20 screen pixels.")
    # Geometric area, rather than font size, must continue to encode each count.
    area_ratios = []
    for group, item in zip(groups, canonical["words"]):
        circle = next(group.all("circle"))
        area_ratios.append(math.pi * float(circle.attrs["r"]) ** 2 / item["count"])
    require(max(area_ratios) - min(area_ratios) < 0.001, "Circle area is no longer proportional to word count.")

    checked = common.check_local_resources(document, page=PAGE)
    source_record = (ASSETS / "oct7/SOURCES.md").read_text(encoding="utf-8")
    for source in (
        "https://x.com/tariqnasheed/status/986455710434082816",
        "https://www.cnn.com/videos/politics/2017/10/26/george-w-bush-hurricane-katrina-fema-michael-brown.cnn",
        "https://www.youtube.com/watch?v=CTVy-JC-Lag",
    ):
        require(source in source_record, f"Missing supplied source in the video record: {source}")
    for filename, _, _ in expected:
        require(f"{filename}.mp4" in source_record, f"Missing excerpt file mapping in the source record: {filename}")
    for _, filename, source in photos:
        require(filename in source_record and source in source_record, f"Missing photograph file mapping or source in the source record: {filename}")
    print(f"October 7 checks passed: exact reading date, three local players, three sourced local photographs, all 50 canonical counts, {checked} local resources.")
    print("; ".join(durations))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError, StopIteration) as error:
        print(f"October 7 check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
