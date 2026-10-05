#!/usr/bin/env python3
"""Validate the full-book count-only resource and its generated public page."""
import argparse
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "frst-110-resources/blood-dazzler-words.html"
ASSETS = PAGE.parent / "blood-dazzler-assets"
PUBLIC_URL = "https://omatty123.github.io/teaching-fall-2026/" + PAGE.relative_to(ROOT).as_posix()
SCOPE = "Whole book: pp. vii–viii, 1–77"
PARTITIONS = (
    ("first", "frequency-cluster.json", "pp. vii–24", 0, 22, 3117),
    ("second", "frequency-25-49.json", "pp. 25–49", 22, 39, 3148),
    ("third", "frequency-50-77.json", "pp. 50–77", 39, 55, 3128),
    ("whole", "frequency-whole-book.json", SCOPE, 0, 55, 9393),
)

# Register the module before executing it: its dataclass definitions need the
# module in sys.modules. Share the original resource and circle regressions.
SPEC = importlib.util.spec_from_file_location("blood_dazzler_page_checks", ROOT / "scripts/check-blood-dazzler-page.py")
shared = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = shared
SPEC.loader.exec_module(shared)
require = shared.require
clean = shared.clean


def read_data(filename):
    return json.loads((ASSETS / filename).read_text(encoding="utf-8"))


def shape(value, keys, label):
    require(isinstance(value, dict), f"{label} must be an object.")
    require(set(value) == set(keys), f"{label} has missing or unapproved public fields: {sorted(set(value) ^ set(keys))}")


def nonempty(value, label):
    require(isinstance(value, str) and value.strip(), f"{label} must be nonempty text.")


def count_dictionary(counts, label):
    require(isinstance(counts, dict) and counts, f"{label} must be a nonempty count dictionary.")
    for word, count in counts.items():
        require(isinstance(word, str) and word == word.casefold().replace("’", "'")
                and re.fullmatch(r"[^\W_]+(?:['-][^\W_]+)*", word), f"Invalid exact-word form in {label}: {word!r}")
        require(type(count) is int and count > 0, f"Invalid positive integer count in {label}: {word}")


def title_identity(title):
    return "".join(character for character in title.casefold() if character.isalnum())


def check_corpus(book):
    # Whitelists protect the public payload from an accidental source-text field.
    # Counts may naturally contain the word 'text'; count keys are not prose.
    shape(book, {"scope", "total_tokens", "poem_count", "unique_words", "method", "counts", "source", "poems"}, "Whole-book count payload")
    require(book["scope"] == SCOPE, "Whole-book scope must be printed pp. vii–viii and 1–77.")
    require(book["poem_count"] == 55 and book["total_tokens"] == 9393 and book["unique_words"] == 2998,
            "Whole-book totals differ from the frozen 55-poem, 9,393-token, 2,998-form audit.")
    nonempty(book["method"], "Whole-book counting method")
    shape(book["source"], {"author", "title", "publisher", "year", "supplied_pdf_sha256"}, "Source record")
    require(book["source"]["author"] == "Patricia Smith" and book["source"]["title"] == "Blood Dazzler", "The corpus identifies the wrong source book.")
    require(re.fullmatch(r"[0-9a-f]{64}", book["source"]["supplied_pdf_sha256"]), "Source PDF lacks a valid SHA-256 audit identifier.")
    count_dictionary(book["counts"], "Full-book counts")
    require(len(book["counts"]) == book["unique_words"] and sum(book["counts"].values()) == book["total_tokens"], "Full-book totals disagree with its word dictionary.")
    poems = book["poems"]
    require(isinstance(poems, list) and len(poems) == book["poem_count"], "The corpus omits or duplicates a poem record.")
    aggregate = Counter()
    numeric_pages = []
    for index, poem in enumerate(poems, 1):
        shape(poem, {"id", "title", "pages", "total_tokens", "counts"}, f"Poem {index} count-only record")
        require(poem["id"] == f"poem-{index:02}", "Poem IDs must be unique and follow the source order.")
        nonempty(poem["title"], f"Poem {index} title")
        count_dictionary(poem["counts"], poem["id"])
        require(type(poem["total_tokens"]) is int and sum(poem["counts"].values()) == poem["total_tokens"], f"Poem total disagrees with its counts: {poem['id']}")
        aggregate.update(poem["counts"])
        if index == 1:
            require(poem["pages"] == "vii–viii", "The corpus must start with the prologue on pp. vii–viii.")
            continue
        match = re.fullmatch(r"(\d+)(?:[–-](\d+))?", poem["pages"])
        require(match is not None, f"Invalid printed page span: {poem['id']}")
        start, end = int(match[1]), int(match[2] or match[1])
        require(1 <= start <= end <= 77, f"Poem page span leaves the source boundary: {poem['id']}")
        numeric_pages.extend(range(start, end + 1))
    require(numeric_pages == list(range(1, 78)), "Poem spans must cover printed pp. 1–77 exactly once in source order.")
    require(dict(aggregate) == book["counts"], "Aggregated poem counts differ from the full-book dictionary.")
    require(sum(poem["total_tokens"] for poem in poems) == book["total_tokens"], "Aggregated poem totals differ from the full-book token total.")
    opening = read_data("counts-vii-24.json")
    opening_counts = Counter()
    for poem in poems[:22]:
        opening_counts.update(poem["counts"])
    require(dict(opening_counts) == opening["counts"] and sum(opening_counts.values()) == opening["total_tokens"] == 3117,
            "The first 22 poem dictionaries differ from the existing pp. vii–24 audit.")
    reading = read_data("reading-data.json")["poems"]
    require(len(reading) == 22, "The opening-reading baseline has an unexpected poem count.")
    for poem, baseline in zip(poems[:22], reading):
        # The existing class table gives only the opening page for two poems
        # whose count audit already includes the following page.
        same_pages = baseline["pages"] in {poem["pages"], poem["pages"].split("–")[0]}
        require(same_pages and title_identity(poem["title"]) == title_identity(baseline["title"]),
                f"Opening poem identity/order differs from the existing reading: {poem['id']}")
    return poems


def check_partitions(book):
    opening = read_data("frequency-cluster.json")
    basic_fields = {"scope", "method", "stop_words", "words", "max_words"}
    partitions = []
    for key, filename, scope, start, end, tokens in PARTITIONS:
        frequency = read_data(filename)
        fields = basic_fields if key == "first" else basic_fields | {"poem_count", "total_tokens"}
        shape(frequency, fields, f"{key.capitalize()} frequency payload")
        selected = book["poems"][start:end]
        counts = Counter()
        for poem in selected:
            counts.update(poem["counts"])
        require(len(selected) == end - start and sum(counts.values()) == tokens,
                f"The {key} section differs from its frozen poem/token partition.")
        require(frequency["scope"] == scope, f"Wrong printed page range for the {key} cloud.")
        require(len(frequency["stop_words"]) == 206 and frequency["stop_words"] == opening["stop_words"],
                f"The {key} cloud must use the same explicit 206-word stop list as the opening cloud.")
        if key != "first":
            require(frequency["poem_count"] == end - start and frequency["total_tokens"] == tokens,
                    f"Declared {key} frequency totals differ from its source partition.")
        shared.check_frequency_data(frequency, counts, expected_scope=scope)
        partitions.append((key, frequency, counts))
    return partitions


def check_version(document, relative, tag, attribute):
    target = ROOT / relative
    nodes = [node for node in document.root.all(tag) if shared.local_path(node.attrs.get(attribute, ""), PAGE)[0] == target]
    require(len(nodes) == 1, f"The full-book page needs one local {relative} reference.")
    versions = parse_qs(urlsplit(nodes[0].attrs[attribute]).query).get("v", [])
    expected = hashlib.sha256(target.read_bytes()).hexdigest()[:12]
    require(versions == [expected], f"Full-book {relative} lacks its current content-hash URL.")


def check_public_scope(document):
    require(not (ASSETS / "hips-analysis.json").exists(), "The private hips analysis remains in public assets.")
    private_material = re.compile(r"hips-analysis\.json|\bhips\s+in\s+context\b|\bwhose\s+hips\b|\bhips\s*:\s*8\b|\b(?:world-hipped|hipped)\b|\bbd-(?:word-search|lookup|result-rows)\b|\bcount\s+a\s+word\b", re.I)
    # Count dictionaries may contain these exact words. Check presentation
    # material only; the strict public count schema above protects source data.
    require(not private_material.search(clean(document.root.text())), "The public clouds page exposes private word-context analysis or lookup content.")
    require(not any(node.attrs.get("id", "") in {"hips", "lookup", "bd-whole-book-data", "bd-word-search"}
                    for node in document.root.all()), "Private context/search controls remain on the public clouds page.")
    for path in (ASSETS / "SOURCES.md", ROOT / ".impeccable/surfaces/frst-110-resources-blood-dazzler-words-html.md",
                 ROOT / "_kit/blood-dazzler-full-words.js", ROOT / "_kit/blood-dazzler-full-words.css"):
        require(path.is_file(), f"Missing cloud source/design record: {path.relative_to(ROOT)}")
        require(not private_material.search(path.read_text(encoding="utf-8")), f"Private context analysis remains in {path.relative_to(ROOT)}.")
    class_page = shared.Document(shared.PAGE.read_text(encoding="utf-8"))
    companions = [node for node in class_page.root.all("a")
                  if shared.local_path(node.attrs.get("href", ""), shared.PAGE)[0] == PAGE]
    require(companions and all(clean(node.text()) == "Word clouds by section and whole book" for node in companions),
            "The class-page companion link must say Word clouds by section and whole book.")


def check_page(document, book, partitions):
    nodes = list(document.root.all())
    by_id = {node.attrs["id"]: node for node in nodes if "id" in node.attrs}
    sections = {f"words-{key}" for key, _, _ in partitions}
    require(sections <= by_id.keys(), "The page omits one of its four section/whole-book word clouds.")
    require(len([node for node in nodes if node.tag == "section" and "bd-frequency" in node.attrs.get("class", "").split()]) == 4,
            "The public page must contain exactly four frequency-cloud sections.")
    metadata = {node.attrs.get("property", node.attrs.get("name")): node.attrs.get("content", "") for node in nodes if node.tag == "meta"}
    require(metadata.get("og:url") == PUBLIC_URL, "Full-book page metadata points to the wrong public address.")
    title = clean(next(document.root.all("title")).text())
    require("Blood Dazzler" in title and "word cloud" in title.casefold(), "Word-cloud browser title is missing.")
    summary = clean(next(document.root.all("header")).text())
    require(book["scope"] in summary, "Full-book heading omits or changes its precise source scope.")
    expected_payloads = {f"bd-{key}-word-data" for key, _, _ in partitions}
    require({node.attrs.get("id") for node in nodes if node.tag == "script" and node.attrs.get("type") == "application/json"} == expected_payloads,
            "The page embeds missing or unapproved public data; only the four frequency payloads belong here.")
    anchors = {node.attrs.get("href") for node in nodes if node.tag == "a"}
    require({f"#{section}" for section in sections} <= anchors, "The page omits a native anchor for a section/whole-book cloud.")
    words = 0
    for key, frequency, counts in partitions:
        section = by_id[f"words-{key}"]
        stem = f"bd-{key}-"
        expected_ids = {stem + suffix for suffix in ("words-title", "frequency-chart-title", "frequency-chart-desc", "word-data")}
        section_ids = {node.attrs.get("id") for node in section.all()}
        require(section.tag == "section" and expected_ids <= section_ids, f"The {key} cloud lacks its uniquely prefixed chart/data IDs.")
        require(section.attrs.get("aria-labelledby") == stem + "words-title", f"The {key} cloud lacks its accessible section heading.")
        require("hidden" not in section.attrs and shared.inline_styles(section).get("display") != "none",
                f"The {key} cloud is unavailable before JavaScript runs.")
        heading = by_id[stem + "words-title"]
        heading_text = "Whole book" if key == "whole" else frequency["scope"]
        require(heading.tag == "h2" and clean(heading.text()) == heading_text, f"The {key} cloud heading has the wrong reading scope.")
        _, _, _, start, end, tokens = next(part for part in PARTITIONS if part[0] == key)
        totals = [node for node in section.all() if "bd-cloud-meta" in node.attrs.get("class", "").split()]
        require(len(totals) == 1 and clean(totals[0].text()) == f"{end - start} poems · {tokens:,} words in poem bodies",
                f"The {key} panel omits or changes its exact poem/token totals.")
        scope_labels = [node for node in section.all() if "bd-frequency-scope" in node.attrs.get("class", "").split()]
        require(len(scope_labels) == 1 and frequency["scope"] in clean(scope_labels[0].text()), f"The {key} cloud displays the wrong printed page range.")
        charts = list(section.all("svg"))
        require(len(charts) == 1 and charts[0].attrs.get("role") == "img"
                and charts[0].attrs.get("aria-labelledby") == stem + "frequency-chart-title " + stem + "frequency-chart-desc",
                f"The {key} cloud lacks its accessible SVG title and description references.")
        require(frequency["scope"] in clean(by_id[stem + "frequency-chart-title"].text()), f"The {key} SVG title has the wrong source range.")
        chart = charts[0]
        width = float(chart.attrs["viewbox"].replace(",", " ").split()[2])
        minimum = shared.style_number(shared.inline_styles(chart).get("min-width"), f"The {key} chart lacks its inline minimum width.")
        for text in chart.all("text"):
            if "bd-frequency-text" in text.attrs.get("class", "").split():
                size = shared.style_number(shared.inline_styles(text).get("font-size"), f"The {key} chart lacks an inline word font size.")
                require(size * minimum / width >= 20 - 0.02, f"The {key} word label is smaller than 20 screen pixels: {clean(text.text())}")
        # Adapt only a private in-memory copy to the class-page helper's old
        # IDs/heading. The real range metadata was checked above.
        cloned = copy.deepcopy(section)
        for node in [cloned, *cloned.all()]:
            identity = node.attrs.get("id", "")
            if identity.startswith(stem):
                node.attrs["id"] = "bd-" + identity[len(stem):]
            if node.tag == "h2":
                node.children = ["Word cloud"]
        words += shared.check_frequency_cluster(document, cloned, counts, data=frequency, page=PAGE, expected_scope=frequency["scope"])
    for relative in ("_kit/blood-dazzler-1.css", "_kit/blood-dazzler-words.css", "_kit/blood-dazzler-full-words.css"):
        check_version(document, relative, "link", "href")
    check_version(document, "_kit/blood-dazzler-full-words.js", "script", "src")
    check_public_scope(document)
    return words


def check_generated():
    before = PAGE.read_bytes()
    subprocess.run([sys.executable, "scripts/build-blood-dazzler-full-words.py"], cwd=ROOT, check=True)
    require(PAGE.read_bytes() == before, "Full-book builder changed the generated page; rebuild and save it before committing.")
    relative = PAGE.relative_to(ROOT).as_posix()
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", "--", relative], cwd=ROOT, capture_output=True).returncode == 0
    if tracked:
        result = subprocess.run(["git", "diff", "--exit-code", "--", relative], cwd=ROOT)
        require(result.returncode == 0, "Generated full-book HTML differs from its Git index; save the rebuilt page with its inputs.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-generated", action="store_true", help="rerun the builder and compare generated HTML with Git")
    args = parser.parse_args()
    try:
        if args.check_generated:
            check_generated()
        book = read_data("whole-book-counts.json")
        poems = check_corpus(book)
        partitions = check_partitions(book)
        document = shared.Document(PAGE.read_text(encoding="utf-8"))
        resources = shared.check_local_resources(document, page=PAGE)
        words = check_page(document, book, partitions)
    except (OSError, ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as error:
        print(f"Blood Dazzler full-book check failed: {error}", file=sys.stderr)
        return 1
    print(f"Blood Dazzler full-book check passed: {len(poems)} poems; {book['total_tokens']:,} tokens; {book['unique_words']:,} forms; first 22 agree exactly; 4 clouds with {words} frequency circles; {resources} local resources.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
