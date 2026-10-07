#!/usr/bin/env python3
"""Build the October 7 classroom clips and the canonical pp. 25–49 word cloud."""

import argparse
import hashlib
import json
from pathlib import Path

from blood_dazzler_word_graph import render_graph

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "frst-110-resources/blood-dazzler-oct-7.html"
ASSETS = ROOT / "frst-110-resources/blood-dazzler-assets"


def versioned(path):
    digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:12]
    return f"../{path}?v={digest}"


def player(filename, label, caption_id):
    return f'''<video controls playsinline preload="none" width="1280" height="720" poster="blood-dazzler-assets/oct7/{filename}-poster.jpg" aria-label="{label}" aria-describedby="{caption_id}"><source src="blood-dazzler-assets/oct7/{filename}.mp4" type="video/mp4"><p><a href="blood-dazzler-assets/oct7/{filename}.mp4">Open video</a>.</p></video>'''


def build():
    frequency = json.loads((ASSETS / "frequency-25-49.json").read_text(encoding="utf-8"))
    graph = render_graph(frequency, minimum_word_pixels=20, id_prefix="second", title="Word cloud · pp. 25–49")
    graph = graph.replace("</h2>", '</h2>\n<p class="cloud-links"><a href="blood-dazzler-words.html#words-second">Word clouds by section and whole book</a></p>', 1)
    mobile_note = '<p class="bd-frequency-mobile-note">Scroll sideways to read every circle.</p>'
    graph = graph.replace(mobile_note + "\n", "", 1).replace('<div class="bd-frequency-chart"', mobile_note + '\n<div class="bd-frequency-chart"', 1)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Blood Dazzler · October 7 · FRST 110</title>
<meta name="description" content="Patricia Smith, pp. 25–49: federal response in When the Levees Broke, Barbara Bush’s Astrodome remarks, George W. Bush’s Brownie remarks, evacuation testimony, and the section’s word frequencies.">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-1.css')}">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-words.css')}">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-oct7.css')}">
<meta property="og:title" content="Blood Dazzler · October 7"><meta property="og:description" content="Official remarks, evacuation testimony, and word frequencies for pp. 25–49."><meta property="og:type" content="website"><meta property="og:url" content="https://omatty123.github.io/teaching-fall-2026/frst-110-resources/blood-dazzler-oct-7.html">
</head><body><a class="skip" href="#content">Skip to class materials</a>
<nav class="nav" aria-label="Breadcrumb"><div class="nav-inner"><a class="brand" href="../courses/frst-110.html">FRST 110</a><a class="crumb" href="../courses/frst-110.html">Course materials</a><a href="blood-dazzler-oct-5.html">October 5 · pp. vii–24</a></div></nav>
<main id="content"><header><h1>Blood Dazzler</h1><p class="meta">Patricia Smith · Wednesday, October 7, 2026 · pp. 25–49</p>
<nav class="section-nav" aria-label="Page sections"><a href="#federal-response">Federal response</a><a href="#barbara-bush">Barbara Bush</a><a href="#brownie">Brownie clip</a><a href="#evacuation">Evacuation clip</a><a href="#words-second">Word cloud</a></nav></header>
<section id="federal-response" class="evacuation-clip" aria-labelledby="federal-response-title"><h2 id="federal-response-title">Federal response in <cite>When the Levees Broke</cite></h2>
<p>Interviewees discuss the government’s information and response; archival footage includes Bush’s praise, the flyover, and questions to Michael Brown. Read alongside “What to Tweak,” pp. 25–28, and “The President Flies Over,” p. 36.</p>
<figure>{player('levees-federal-response', 'Federal response in When the Levees Broke', 'federal-response-caption')}
<figcaption id="federal-response-caption">4 minutes 18 seconds · A continuous excerpt from Spike Lee’s <cite>When the Levees Broke</cite> (2006). <a href="https://youtu.be/CTVy-JC-Lag?t=4864">Documentary source at the requested passage</a> · <a href="blood-dazzler-assets/oct7/levees-federal-response.mp4">Open video</a></figcaption></figure></section>
<div class="official-clips">
<section id="barbara-bush" aria-labelledby="barbara-title"><h2 id="barbara-title">Barbara Bush at the Astrodome</h2>
<p><a href="https://transcripts.cnn.com/show/lkl/date/2005-09-05/segment/01">September 5, 2005</a>. Read alongside “Thankful,” pp. 48–49.</p>
<figure>{player('barbara-bush-katrina', 'Barbara Bush’s Astrodome remarks', 'barbara-caption')}
<figcaption id="barbara-caption">19 seconds · Original audio with Astrodome photographs and captions. <a href="https://x.com/tariqnasheed/status/986455710434082816">Audio source</a> · <a href="blood-dazzler-assets/oct7/barbara-bush-katrina.mp4">Open video</a></figcaption></figure></section>
<section id="brownie" aria-labelledby="brownie-title"><h2 id="brownie-title">George W. Bush: the Brownie clip</h2>
<p><a href="https://georgewbush-whitehouse.archives.gov/news/releases/2005/09/20050902-2.html">September 2, 2005</a>. President George W. Bush praises FEMA director Michael Brown. Read alongside the official language in this section.</p>
<figure>{player('george-bush-brownie', 'George W. Bush praising Michael Brown', 'brownie-caption')}
<figcaption id="brownie-caption">18 seconds · Excerpt from Spike Lee’s <cite>When the Levees Broke</cite> (2006). The film repeats the Brownie line three times. <a href="https://www.youtube.com/watch?v=CTVy-JC-Lag&amp;t=4900">Documentary source at the passage</a> · <a href="https://www.cnn.com/videos/politics/2017/10/26/george-w-bush-hurricane-katrina-fema-michael-brown.cnn">CNN record</a> · <a href="blood-dazzler-assets/oct7/george-bush-brownie.mp4">Open video</a></figcaption></figure></section>
</div>
<section id="evacuation" class="evacuation-clip" aria-labelledby="evacuation-title"><h2 id="evacuation-title">Evacuation orders and the means to leave</h2>
<p>Residents discuss transportation, evacuation orders, and government responsibility. A separate excerpt from Spike Lee’s <cite>When the Levees Broke</cite> (2006).</p>
<figure>{player('levees-evacuation', 'Residents discussing evacuation orders and the means to leave', 'evacuation-caption')}
<figcaption id="evacuation-caption">2 minutes 12 seconds · <a href="https://www.youtube.com/watch?v=CTVy-JC-Lag&amp;t=5300">Documentary source at the passage</a> · <a href="blood-dazzler-assets/oct7/levees-evacuation.mp4">Open video</a></figcaption></figure></section>
{graph}
<footer><p><a href="blood-dazzler-assets/oct7/SOURCES.md">Video sources and excerpt details</a> · <a href="blood-dazzler-assets/SOURCES.md">Word-count source and method</a> · <a href="../courses/frst-110.html">FRST 110 course materials</a></p></footer>
</main></body></html>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check that the saved page matches the deterministic build.")
    args = parser.parse_args()
    page = build()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != page:
            parser.exit(1, "October 7 page is stale. Run scripts/build-blood-dazzler-oct7.py.\n")
        print("October 7 page matches its builder and canonical word counts.")
    else:
        OUTPUT.write_text(page, encoding="utf-8")
        print("Built Blood Dazzler October 7: four classroom clips and 50 word counts, pp. 25–49.")


if __name__ == "__main__":
    main()
