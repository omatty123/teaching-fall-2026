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


def payload(data):
    return json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')


def main():
    book = read_data('whole-book-counts.json')
    frequency = read_data('frequency-whole-book.json')
    hips = read_data('hips-analysis.json')
    word = hips['word']
    matched = [poem for poem in book['poems'] if int(poem['counts'].get(word, 0))]
    if sum(int(poem['counts'].get(word, 0)) for poem in matched) != int(hips['count']):
        raise ValueError('The hips analysis must agree with the poem counts.')
    if int(book['counts'].get(word, 0)) != int(hips['count']) or len(matched) != int(hips['poem_count']):
        raise ValueError('The hips analysis must agree with the full-book count.')
    lookup_rows = ''.join(
        f'<tr><th scope="row">{e(poem["title"])}</th><td>{e(poem["pages"])}</td><td>{int(poem["counts"][word])}</td></tr>'
        for poem in matched
    )
    context_rows = ''.join(
        f'<tr><th scope="row">{e(item["title"])}</th><td>{e(item["page"])}</td><td><strong>{e(item["subject"])}</strong> {e(item["context"])}</td></tr>'
        for item in hips['occurrences']
    )
    related = ''.join(f'<li><span>{e(item["word"])}</span><strong>{int(item["count"])}</strong></li>' for item in hips.get('related', []))
    graph = render_graph(frequency, minimum_word_pixels=20)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Blood Dazzler · Whole-book word counts · FRST 110</title>
<meta name="description" content="Exact-word frequencies across Patricia Smith’s Blood Dazzler, with a word cloud, searchable counts by poem, and the eight uses of hips.">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-1.css')}">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-words.css')}">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-full-words.css')}">
<meta property="og:title" content="Blood Dazzler · Whole-book word counts"><meta property="og:description" content="A word cloud and exact counts by poem, with a closer look at hips."><meta property="og:type" content="website"><meta property="og:url" content="https://omatty123.github.io/teaching-fall-2026/frst-110-resources/blood-dazzler-words.html">
</head><body><a class="skip" href="#content">Skip to word counts</a>
<nav class="nav" aria-label="Breadcrumb"><div class="nav-inner"><a class="brand" href="../courses/frst-110.html">FRST 110</a><a href="blood-dazzler-oct-5.html#words">October 5 reading · pp. vii–24</a><a href="../courses/frst-110.html">Course materials</a></div></nav>
<main id="content"><header><h1>Blood Dazzler: whole-book word counts</h1><p class="meta">Patricia Smith · {e(book['scope'])} · {int(book['poem_count'])} poems · {int(book['total_tokens']):,} words</p>
<nav class="section-nav" aria-label="Page sections"><a href="#words">Whole-book word cloud</a><a href="#lookup">Count a word</a><a href="#hips">Hips in context</a></nav></header>
<section id="lookup" aria-labelledby="bd-lookup-title"><h2 id="bd-lookup-title">Count a word</h2>
<p class="bd-lookup-note">Search any exact word, including common words. Word forms stay separate: <strong>hip</strong> and <strong>hips</strong> have different counts.</p>
<form id="bd-word-search" class="bd-word-search" action="#lookup" hidden>
<div class="bd-search-field"><label for="bd-lookup-word">Word</label><input type="search" id="bd-lookup-word" name="word" value="{e(word)}" autocomplete="off" spellcheck="false" maxlength="80" aria-describedby="bd-search-help bd-search-error" required></div><button type="submit">Count word</button>
</form><p id="bd-search-help" class="note">Capitalization is ignored. Contractions and hyphenated words stay intact.</p><p id="bd-search-error" class="bd-search-error" role="alert"></p>
<div id="bd-lookup-result" class="bd-lookup-result" aria-live="polite" aria-atomic="true"><h3 id="bd-result-title">{e(word)}: {int(hips['count'])} uses in {int(hips['poem_count'])} poems</h3>
<p id="bd-result-note" class="note">Counts below refer to poem bodies. Pages are printed book pages.</p>
<div id="bd-result-table-wrap" class="bd-result-table-wrap"><table class="bd-result-table"><caption class="bd-frequency-sr">Poems containing {e(word)}</caption><thead><tr><th scope="col">Poem</th><th scope="col">Pages</th><th scope="col">Count</th></tr></thead><tbody id="bd-result-rows">{lookup_rows}</tbody></table></div></div>
<noscript><p class="note">The search needs JavaScript. The hips counts and context below remain available.</p></noscript>
</section>
<section id="hips" aria-labelledby="bd-hips-title"><h2 id="bd-hips-title">Hips in context</h2><p class="bd-hips-reading">{e(hips['interpretation'])}</p><p class="note">The context descriptions are paraphrases. Read the complete poems in your book.</p>
<div class="bd-context-table-wrap"><table class="bd-context-table"><thead><tr><th scope="col">Poem</th><th scope="col">Page</th><th scope="col">Whose hips, and what happens?</th></tr></thead><tbody>{context_rows}</tbody></table></div>
<details class="bd-related"><summary>Related exact-word counts</summary><ul>{related}</ul><p class="note">These are separate exact-word counts across the whole book. They are not added to the count for hips.</p></details></section>
{graph}
<footer><p>{e(book['method'])}</p><p><a href="blood-dazzler-assets/SOURCES.md">Source and method record</a> · <a href="blood-dazzler-oct-5.html#words">October 5 reading · pp. vii–24</a> · <a href="../courses/frst-110.html">FRST 110 course materials</a></p></footer>
</main><script type="application/json" id="bd-whole-book-data">{payload(book)}</script><script src="{versioned('_kit/blood-dazzler-full-words.js')}" defer></script></body></html>'''
    OUTPUT.write_text(page)
    print(f'Built Blood Dazzler whole-book word counts: {book["poem_count"]} poems, {book["total_tokens"]:,} words.')


if __name__ == '__main__':
    main()
