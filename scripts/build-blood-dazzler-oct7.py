#!/usr/bin/env python3
"""Build the October 7 classroom clips, photographs, tanka activity, and canonical pp. 25–49 word cloud."""

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
<meta name="description" content="Patricia Smith, pp. 25–49: Barbara Bush’s Astrodome remarks, federal response and evacuation excerpts from When the Levees Broke, Superdome roof damage, Ethel Freeman, a tanka introduction and writing activity, and the section’s word frequencies.">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-1.css')}">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-words.css')}">
<link rel="stylesheet" href="{versioned('_kit/blood-dazzler-oct7.css')}">
<meta property="og:title" content="Blood Dazzler · October 7"><meta property="og:description" content="Official remarks, evacuation testimony, Superdome roof damage, Ethel Freeman, and word frequencies for pp. 25–49."><meta property="og:type" content="website"><meta property="og:url" content="https://omatty123.github.io/teaching-fall-2026/frst-110-resources/blood-dazzler-oct-7.html">
</head><body><a class="skip" href="#content">Skip to class materials</a>
<nav class="nav" aria-label="Breadcrumb"><div class="nav-inner"><a class="brand" href="../courses/frst-110.html">FRST 110</a><a class="crumb" href="../courses/frst-110.html">Course materials</a><a href="blood-dazzler-oct-5.html">October 5 · pp. vii–24</a></div></nav>
<main id="content"><header><h1>Blood Dazzler</h1><p class="meta">Patricia Smith · Wednesday, October 7, 2026 · pp. 25–49</p>
<p class="cloud-links"><a href="https://lawrence.instructure.com/courses/14726/pages/song-of-the-day-southern-nights-allen-toussaint">Song of the Day · Allen Toussaint, “Southern Nights”</a></p>
<nav class="section-nav" aria-label="Page sections"><a href="#what-is-tanka">What is Tanka?</a><a href="#write-tanka">Let’s Write Tanka</a><a href="#sestina">Ethel’s Sestina</a><a href="#federal-response">Federal response</a><a href="#barbara-bush">Barbara Bush</a><a href="#evacuation">Evacuation clip</a><a href="#superdome-photos">Superdome</a><a href="#ethel-freeman">Ethel Freeman</a><a href="#words-second">Word cloud</a></nav></header>
<section id="what-is-tanka" class="tanka-section" aria-labelledby="tanka-title"><h2 id="tanka-title">What is Tanka?</h2>
<p><strong>Tanka is a short Japanese poetic form.</strong> In English, it is usually written in five lines. A common syllable pattern is <strong>5–7–5–7–7</strong>.</p>
<p>A tanka can begin with something seen, heard, or felt, then shift toward a thought, memory, or different perspective. This shift is called a <strong>turn</strong>. The pattern is a starting point: English-language tanka do not always keep a strict syllable count.</p>
<p>In today’s reading: Patricia Smith, <strong>“Tankas,” pp. 38–39</strong>.</p>
<h3>Smith’s five lines: one tanka from the sequence</h3>
<table class="tanka-lines"><caption>“Tankas,” p. 38 · each row is one printed line</caption><thead><tr><th scope="col">Smith’s line</th><th scope="col">Syllables</th></tr></thead><tbody>
<tr><td>I have three children,</td><td>5</td></tr>
<tr><td>but only two arms. He falls</td><td>7</td></tr>
<tr><td>and barely splashes,</td><td>5</td></tr>
<tr><td>that’s how incredibly light</td><td>7</td></tr>
<tr><td>he <strong>is—was</strong>. How death whispers.</td><td>7</td></tr>
</tbody></table>
<p class="tanka-sources">Patricia Smith, <cite>Blood Dazzler</cite>, p. 38. Bold added to mark the change of tense.</p>
<p><strong>Where the turn happens:</strong> “is—was” changes present to past within the final line. The speaker corrects herself as she recognizes the loss.</p>
<p><strong>Form and content:</strong> the sentence continues across line breaks, while the five-line pattern contains the moment. “He falls” ends a line; “and barely splashes” begins the next. The small sound and the short space make the loss painfully immediate.</p>
<p class="tanka-sources">Sources: <a href="https://poets.org/glossary/tanka">Academy of American Poets: Tanka</a> · <a href="https://www.poetryfoundation.org/articles/157323/tanka-and-renga-looking-through-windows">Poetry Foundation: Tanka and Renga</a></p></section>
<section id="write-tanka" class="tanka-section" aria-labelledby="write-tanka-title"><h2 id="write-tanka-title">Let’s Write Tanka</h2>
<ol class="tanka-steps"><li><strong>Choose one moment involving water.</strong> Rain, a drink, a sink, snow, or a lake will do.</li>
<li><strong>Write five lines.</strong> Try 5, 7, 5, 7, and 7 syllables.</li>
<li><strong>Make a turn.</strong> One approach: describe the moment in the first three lines; add a thought, memory, or change of perspective in the last two.</li>
<li><strong>Read it aloud.</strong> Revise one word or line to make the image or sound clearer.</li></ol>
</section>
<section id="sestina" class="tanka-section" aria-labelledby="sestina-title"><h2 id="sestina-title">What is a Sestina? “Ethel’s Sestina”</h2>
<p><strong>A sestina repeats six end words in a changing order.</strong> Its usual structure is six six-line stanzas followed by a three-line ending, called an <strong>envoi</strong>, containing all six words. Smith adapts this structure in <strong>“Ethel’s Sestina,” pp. 45–46</strong>.</p>
<h3>First stanza: six lines, six end words</h3>
<blockquote class="poem-lines"><div>Gon’ be obedient in this here <strong>chair</strong>,</div><div>gon’ bide my time, fanning against this <strong>sun</strong>.</div><div>I ask my boy, and all he says is <strong>Wait</strong>.</div><div>He wipes my brow with steam, says I should <strong>sleep</strong>.</div><div>I trust his every word. Herbert my <strong>son</strong>.</div><div>I believe him when he says help gon’ <strong>come</strong>.</div></blockquote>
<p class="tanka-sources">Patricia Smith, <cite>Blood Dazzler</cite>, p. 45. Bold added to show the end words.</p>
<h3>The same words return in a different order</h3>
<div class="pattern-scroll" role="region" aria-label="Sestina end-word order" tabindex="0"><table class="sestina-pattern"><caption>Read across each row: line endings in stanzas 1–5</caption><thead><tr><th scope="col">Stanza</th><th scope="col">1</th><th scope="col">2</th><th scope="col">3</th><th scope="col">4</th><th scope="col">5</th><th scope="col">6</th></tr></thead><tbody>
<tr><th scope="row">1</th><td>chair</td><td>sun</td><td>Wait</td><td>sleep</td><td>son</td><td>come</td></tr>
<tr><th scope="row">2</th><td>come</td><td>chair</td><td>son</td><td>sun</td><td>sleep</td><td>Wait</td></tr>
<tr><th scope="row">3</th><td>wait</td><td>come</td><td>sleep</td><td>chair</td><td>sun</td><td>son</td></tr>
<tr><th scope="row">4</th><td>son</td><td>Wait</td><td>sun</td><td>come</td><td>chair</td><td>sleepin’</td></tr>
<tr><th scope="row">5</th><td>sleep</td><td>son</td><td>chair</td><td>wait</td><td>come</td><td>sun</td></tr>
</tbody></table></div>
<p><strong>Form and content:</strong> the returning words keep the speaker’s attention on her chair, the heat, her son, and the promised arrival of help. The poem moves forward, but keeps returning to waiting.</p>
<h3>Smith changes the pattern</h3>
<p>In the sixth stanza, <strong>“Come.”</strong> repeats on separate lines. The repeated call expands the stanza beyond six lines. Its last line places <strong>“chair”</strong> inside the phrase <strong>“chair no more.”</strong> In this reading, the formal change accompanies the speaker’s imagined departure from her body.</p>
<p>In the three-line envoi, all six words return in pairs: <strong>come / son · sun / sleep · wait / chair</strong>. The final chair is a <strong>“golden chair”</strong>: the same word now describes a different world. The imagined release does not erase the failure to bring help.</p>
<p class="tanka-sources">Form reference: <a href="https://poets.org/glossary/sestina">Academy of American Poets: Sestina</a>. Excerpt and word order: Smith, <cite>Blood Dazzler</cite>, pp. 45–46.</p></section>
<section id="federal-response" class="evacuation-clip" aria-labelledby="federal-response-title"><h2 id="federal-response-title">Federal response in <cite>When the Levees Broke</cite></h2>
<p>Interviewees discuss the government’s information and response; archival footage includes Bush’s praise, the flyover, and questions to Michael Brown. Read alongside “What to Tweak,” pp. 25–28, and “The President Flies Over,” p. 36.</p>
<figure>{player('levees-federal-response', 'Federal response in When the Levees Broke', 'federal-response-caption')}
<figcaption id="federal-response-caption">4 minutes 18 seconds · A continuous excerpt from Spike Lee’s <cite>When the Levees Broke</cite> (2006). <a href="https://youtu.be/CTVy-JC-Lag?t=4864">Documentary source at the requested passage</a> · <a href="blood-dazzler-assets/oct7/levees-federal-response.mp4">Open video</a></figcaption></figure></section>
<section id="barbara-bush" class="evacuation-clip" aria-labelledby="barbara-title"><h2 id="barbara-title">Barbara Bush at the Astrodome</h2>
<p><a href="https://transcripts.cnn.com/show/lkl/date/2005-09-05/segment/01">September 5, 2005</a>. Read alongside “Thankful,” pp. 48–49.</p>
<figure>{player('barbara-bush-katrina', 'Barbara Bush’s Astrodome remarks', 'barbara-caption')}
<figcaption id="barbara-caption">19 seconds · Original audio with Astrodome photographs and captions. <a href="https://x.com/tariqnasheed/status/986455710434082816">Audio source</a> · <a href="blood-dazzler-assets/oct7/barbara-bush-katrina.mp4">Open video</a></figcaption></figure></section>
<section id="evacuation" class="evacuation-clip" aria-labelledby="evacuation-title"><h2 id="evacuation-title">Evacuation orders and the means to leave</h2>
<p>Residents discuss transportation, evacuation orders, and government responsibility. A separate excerpt from Spike Lee’s <cite>When the Levees Broke</cite> (2006).</p>
<figure>{player('levees-evacuation', 'Residents discussing evacuation orders and the means to leave', 'evacuation-caption')}
<figcaption id="evacuation-caption">2 minutes 12 seconds · <a href="https://www.youtube.com/watch?v=CTVy-JC-Lag&amp;t=5300">Documentary source at the passage</a> · <a href="blood-dazzler-assets/oct7/levees-evacuation.mp4">Open video</a></figcaption></figure></section>
<section id="superdome-photos" class="class-photos" aria-labelledby="superdome-photos-title"><h2 id="superdome-photos-title">Superdome roof damage</h2>
<p>Read alongside “Superdome,” p. 40.</p>
<div class="class-photo-pair"><figure><img src="blood-dazzler-assets/oct7/superdome-roof-close.jpg" alt="Close view of the Superdome roof with its covering stripped away on the southwest side." width="1200" height="798" loading="lazy" decoding="async">
<figcaption>Roof covering stripped from the southwest side. September 5, 2005 · Win Henderson/FEMA. <a href="https://commons.wikimedia.org/wiki/File:Superdome_Roof_Damage_FEMA.jpg">Photograph source</a></figcaption></figure>
<figure><img src="blood-dazzler-assets/oct7/superdome-roof-aerial.jpg" alt="Aerial view of the Superdome with large areas of roof covering missing." width="1200" height="770" loading="lazy" decoding="async">
<figcaption>Aerial view of the damaged roof. September 4, 2005 · Jocelyn Augustino/FEMA. <a href="https://commons.wikimedia.org/wiki/File:FEMA_-_17670_-_Photograph_by_Jocelyn_Augustino_taken_on_09-04-2005_in_Louisiana.jpg">Photograph source</a></figcaption></figure></div></section>
<section id="ethel-freeman" class="class-photos" aria-labelledby="ethel-freeman-title"><h2 id="ethel-freeman-title">Ethel Freeman</h2>
<p>Read alongside “Ethel’s Sestina,” pp. 45–46.</p>
<figure class="class-photo-single"><img src="blood-dazzler-assets/oct7/ethel-freeman-wheelchair.jpg" alt="Ethel Freeman’s covered body seated in a wheelchair on the sidewalk outside the New Orleans Convention Center." width="900" height="635" loading="lazy" decoding="async">
<figcaption>Ethel Freeman’s covered body in her wheelchair outside the New Orleans Convention Center, September 2, 2005. © Eric Gay/Associated Press. <a href="https://www.ctinsider.com/news/article/Hurricane-Katrina-Sept-2-2005-in-photos-6465422.php">Photograph source</a></figcaption></figure></section>
{graph}
<footer><p><a href="blood-dazzler-assets/oct7/SOURCES.md">Video and photograph sources</a> · <a href="blood-dazzler-assets/SOURCES.md">Word-count source and method</a> · <a href="../courses/frst-110.html">FRST 110 course materials</a></p></footer>
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
        print("Built Blood Dazzler October 7: three classroom clips, three photographs, and 50 word counts, pp. 25–49.")


if __name__ == "__main__":
    main()
