#!/usr/bin/env python3
"""Build a public word-count resource without publishing the poem text."""
import hashlib
import html
import json
from pathlib import Path

from blood_dazzler_word_graph import render_graph

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'frst-110-resources/blood-dazzler-assets'
OUTPUT = ROOT / 'frst-110-resources/blood-dazzler-words.html'
e = lambda value: html.escape(str(value), quote=True)


def read_data(name):
    return json.loads((ASSETS / name).read_text())


def versioned(path):
    digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:12]
    return f'../{path}?v={digest}'


def main():
    book = read_data('whole-book-counts.json')
    scopes = [
        ('first', 'pp. vii–24', 'pp. vii–24', 'frequency-cluster.json', 22, 3117),
        ('second', 'pp. 25–49', 'pp. 25–49', 'frequency-25-49.json', 17, 3148),
        ('third', 'pp. 50–77', 'pp. 50–77', 'frequency-50-77.json', 16, 3128),
        ('whole', 'Whole book', 'Whole book: pp. vii–viii, 1–77', 'frequency-whole-book.json', 55, 9393),
    ]
    graphs = []
    links = []
    for prefix, label, scope, filename, poem_count, total_tokens in scopes:
        frequency = {**read_data(filename), 'scope': scope}
        graph = render_graph(frequency, minimum_word_pixels=20, id_prefix=prefix, title=label)
        graph = graph.replace('</h2>', f'</h2>\n<p class="bd-cloud-meta">{poem_count} poems · {total_tokens:,} words in poem bodies</p>', 1)
        mobile_note = '<p class="bd-frequency-mobile-note">Scroll sideways to read every circle.</p>'
        graph = graph.replace(mobile_note + '\n', '', 1).replace('<div class="bd-frequency-chart"', mobile_note + '\n<div class="bd-frequency-chart"', 1)
        graphs.append(graph)
        links.append(f'<a href="#words-{prefix}" data-cloud="words-{prefix}">{e(label)}</a>')
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Blood Dazzler · Word clouds · FRST 110</title>
<meta name="description" content="Exact-word frequency clouds for three course reading sections and the whole of Patricia Smith’s Blood Dazzler, excluding common function words.">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-1.css')}">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-words.css')}">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-full-words.css')}">
<meta property="og:title" content="Blood Dazzler · Word clouds"><meta property="og:description" content="Word frequencies by course reading section and across the whole book."><meta property="og:type" content="website"><meta property="og:url" content="https://omatty123.github.io/teaching-fall-2026/frst-110-resources/blood-dazzler-words.html">
</head><body><a class="skip" href="#content">Skip to word counts</a>
<nav class="nav" aria-label="Breadcrumb"><div class="nav-inner"><a class="brand" href="../courses/frst-110.html">FRST 110</a><a href="blood-dazzler-oct-5.html#words">October 5 reading · pp. vii–24</a><a href="../courses/frst-110.html">Course materials</a></div></nav>
<main id="content"><header><h1>Blood Dazzler: word clouds</h1><p class="meta">Patricia Smith · Whole book: pp. vii–viii, 1–77</p>
<p class="bd-cloud-intro">The three ranges follow the course reading sections. Each cloud shows the 50 most frequent words after common words are removed. Circle scales differ between clouds; compare the printed counts.</p></header>
<nav class="bd-cloud-nav" aria-label="Choose a reading scope">{''.join(links)}</nav>
{''.join(graphs)}
<footer><p>{e(book['method'])}</p><p><a href="blood-dazzler-assets/SOURCES.md">Source and method record</a> · <a href="blood-dazzler-oct-5.html#words">October 5 reading · pp. vii–24</a> · <a href="../courses/frst-110.html">FRST 110 course materials</a></p></footer>
</main><script src="{versioned('_kit/blood-dazzler-full-words.js')}" defer></script></body></html>'''
    OUTPUT.write_text(page)
    print(f'Built four Blood Dazzler word clouds: {book["poem_count"]} poems, {book["total_tokens"]:,} words in the whole book.')


if __name__ == '__main__':
    main()
