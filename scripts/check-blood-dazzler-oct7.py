#!/usr/bin/env python3
"""Check the October 7 reading boundary, sourced local clips, and exact word counts."""

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
    require(set(("barbara-bush", "brownie", "evacuation", "words-second")) <= by_id.keys(), "A requested classroom resource is missing its jump target.")
    require("“Thankful,” pp. 48–49" in body_text, "Barbara Bush's clip needs its verified poem reference.")
    require("September 5, 2005" in body_text and "September 2, 2005" in body_text, "The two official remarks need their event dates.")
    require("The film repeats the Brownie line three times." in body_text, "Identify the three Brownie repetitions as the documentary's editing.")
    require(not list(document.root.all("iframe")), "Classroom clips must be local native players, not remote embeds.")
    require(not list(document.root.all("script")) or all(node.attrs.get("type") == "application/json" for node in document.root.all("script")), "This static page should not add remote or executable scripts.")

    videos = list(document.root.all("video"))
    require(len(videos) == 3, "Expected the Barbara Bush, Brownie, and separate evacuation players.")
    expected = (
        ("barbara-bush-katrina", 18.9, 19.1),
        ("george-bush-brownie", 17.7, 17.9),
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
    print(f"October 7 checks passed: exact reading date, three local players, all 50 canonical counts, {checked} local resources.")
    print("; ".join(durations))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError, StopIteration) as error:
        print(f"October 7 check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
