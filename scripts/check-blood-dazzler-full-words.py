#!/usr/bin/env python3
"""Validate the full-book count-only resource and its generated public page."""
import argparse
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
HIPS_PAGES = {
    "poem-01": "viii", "poem-02": "1", "poem-06": "6", "poem-36": "44",
    "poem-39": "48", "poem-40": "56", "poem-45": "63", "poem-51": "72",
}

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


def check_hips(hips, book):
    shape(hips, {"word", "count", "poem_count", "related", "interpretation", "occurrences"}, "Hips analysis payload")
    require(hips["word"] == "hips" and hips["count"] == hips["poem_count"] == 8, "Hips analysis must count eight uses in eight poems.")
    matched = [poem for poem in book["poems"] if poem["counts"].get("hips", 0)]
    require(book["counts"].get("hips") == 8 and len(matched) == 8 and all(poem["counts"]["hips"] == 1 for poem in matched), "The full source does not support eight single hips occurrences.")
    require({poem["id"] for poem in matched} == set(HIPS_PAGES), "Hips poem identities differ from the audited source locators.")
    related = hips["related"]
    require(related == [{"word": word, "count": 1} for word in ("hip", "hipped", "world-hipped")], "Related hip forms must remain three separate exact-word counts of one.")
    require(all(book["counts"].get(item["word"]) == item["count"] for item in related), "Related hip forms disagree with the full-book source counts.")
    nonempty(hips["interpretation"], "Hips interpretation")
    occurrences = hips["occurrences"]
    require(isinstance(occurrences, list) and len(occurrences) == 8, "Hips context must contain exactly eight occurrence records.")
    require([item.get("poem_id") for item in occurrences] == [poem["id"] for poem in matched], "Hips context omits, duplicates, or reorders a source poem.")
    for occurrence in occurrences:
        shape(occurrence, {"poem_id", "title", "page", "count", "subject", "context"}, "Hips occurrence")
        require(occurrence["page"] == HIPS_PAGES[occurrence["poem_id"]] and occurrence["count"] == 1, f"Hips context has the wrong exact page or count: {occurrence['poem_id']}")
        for field in ("title", "subject", "context"):
            nonempty(occurrence[field], f"Hips {field} for {occurrence['poem_id']}")
    return matched


def check_version(document, relative, tag, attribute):
    target = ROOT / relative
    nodes = [node for node in document.root.all(tag) if shared.local_path(node.attrs.get(attribute, ""), PAGE)[0] == target]
    require(len(nodes) == 1, f"The full-book page needs one local {relative} reference.")
    versions = parse_qs(urlsplit(nodes[0].attrs[attribute]).query).get("v", [])
    expected = hashlib.sha256(target.read_bytes()).hexdigest()[:12]
    require(versions == [expected], f"Full-book {relative} lacks its current content-hash URL.")


def check_page(document, book, frequency, hips, matched):
    nodes = list(document.root.all())
    by_id = {node.attrs["id"]: node for node in nodes if "id" in node.attrs}
    require({"words", "lookup", "hips", "bd-word-search", "bd-lookup-word", "bd-result-title", "bd-result-rows", "bd-whole-book-data"} <= by_id.keys(), "Full-book page omits its chart, lookup, hips context, or source data.")
    metadata = {node.attrs.get("property", node.attrs.get("name")): node.attrs.get("content", "") for node in nodes if node.tag == "meta"}
    require(metadata.get("og:url") == PUBLIC_URL, "Full-book page metadata points to the wrong public address.")
    require("Whole-book word counts" in clean(next(document.root.all("title")).text()), "Full-book browser title is missing.")
    summary = clean(next(document.root.all("header")).text())
    require(book["scope"] in summary and "55 poems" in summary and "9,393 words" in summary, "Full-book heading omits or changes its source scope/totals.")
    embedded = by_id["bd-whole-book-data"]
    require(embedded.tag == "script" and embedded.attrs.get("type") == "application/json" and json.loads(embedded.text()) == book, "Embedded lookup source differs from the count-only corpus.")
    require({node.attrs.get("id") for node in nodes if node.tag == "script" and node.attrs.get("type") == "application/json"} == {"bd-whole-book-data", "bd-word-data"}, "The page embeds an unapproved public data payload.")
    require(by_id["bd-lookup-word"].attrs.get("value") == "hips", "The static lookup does not start with hips.")
    require(clean(by_id["bd-result-title"].text()) == "hips: 8 uses in 8 poems", "Static hips lookup title disagrees with its source count.")
    actual = [[clean(cell.text()) for cell in row.children if isinstance(cell, shared.Element) and cell.tag in {"th", "td"}] for row in by_id["bd-result-rows"].all("tr")]
    expected = [[poem["title"], poem["pages"], str(poem["counts"]["hips"])] for poem in matched]
    require(actual == expected, "Static hips lookup rows differ from their eight source-poem counts.")
    context_tables = [node for node in by_id["hips"].all("table") if "bd-context-table" in node.attrs.get("class", "").split()]
    require(len(context_tables) == 1, "The hips section needs one readable context table.")
    bodies = list(context_tables[0].all("tbody"))
    require(len(bodies) == 1, "Hips context table lacks its body.")
    actual = [[clean(cell.text()) for cell in row.children if isinstance(cell, shared.Element) and cell.tag in {"th", "td"}] for row in bodies[0].all("tr")]
    expected = [[item["title"], item["page"], clean(item["subject"] + " " + item["context"])] for item in hips["occurrences"]]
    require(actual == expected, "Rendered hips context differs from the eight approved paraphrases and page locators.")
    require(hips["interpretation"] in clean(by_id["hips"].text()), "The rendered hips interpretation differs from its data.")
    related = [node for node in by_id["hips"].all("details") if "bd-related" in node.attrs.get("class", "").split()]
    require(len(related) == 1, "Hips section omits its separate related-word counts.")
    require([clean(node.text()) for node in related[0].all("li")] == [f"{item['word']} {item['count']}" for item in hips["related"]], "Rendered related hip counts differ from their source data.")
    check_version(document, "_kit/blood-dazzler-full-words.css", "link", "href")
    check_version(document, "_kit/blood-dazzler-full-words.js", "script", "src")
    return shared.check_frequency_cluster(document, by_id["words"], book["counts"], data=frequency, page=PAGE, expected_scope=book["scope"])


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
        book, frequency, hips = (read_data(filename) for filename in ("whole-book-counts.json", "frequency-whole-book.json", "hips-analysis.json"))
        poems = check_corpus(book)
        shape(frequency, {"scope", "method", "stop_words", "words", "poem_count", "total_tokens", "max_words"}, "Whole-book frequency payload")
        opening_frequency = read_data("frequency-cluster.json")
        require(len(frequency["stop_words"]) == 206 and frequency["stop_words"] == opening_frequency["stop_words"], "The full-book cloud must use the same explicit 206-word stop list as the opening cloud.")
        require(frequency["poem_count"] == book["poem_count"] and frequency["total_tokens"] == book["total_tokens"], "Frequency payload totals differ from its corpus.")
        shared.check_frequency_data(frequency, book["counts"], expected_scope=book["scope"])
        matched = check_hips(hips, book)
        document = shared.Document(PAGE.read_text(encoding="utf-8"))
        resources = shared.check_local_resources(document, page=PAGE)
        words = check_page(document, book, frequency, hips, matched)
    except (OSError, ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as error:
        print(f"Blood Dazzler full-book check failed: {error}", file=sys.stderr)
        return 1
    print(f"Blood Dazzler full-book check passed: {len(poems)} poems; {book['total_tokens']:,} tokens; {book['unique_words']:,} forms; first 22 agree exactly; {words} frequency circles; 8 hips references; {resources} local resources.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
