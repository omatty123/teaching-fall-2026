#!/usr/bin/env python3
"""Build the October 9 Blood Dazzler page: form cards, Smith performing "34", St. Rita's footage, search-marking photos, 2005 season map, pp. 50-77 word cloud."""
import hashlib, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from blood_dazzler_word_graph import render_graph
ASSETS = ROOT / "frst-110-resources/blood-dazzler-assets"


def versioned(path):
    return f"../{path}?v={hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:12]}"


def player(name, label, cap):
    return (f'<video controls playsinline preload="none" width="1280" height="720" poster="blood-dazzler-assets/oct9/{name}-poster.jpg" '
            f'aria-label="{label}" aria-describedby="{cap}"><source src="blood-dazzler-assets/oct9/{name}.mp4" type="video/mp4">'
            f'<p><a href="blood-dazzler-assets/oct9/{name}.mp4">Open video</a>.</p></video>')


frequency = json.loads((ASSETS / "frequency-50-77.json").read_text(encoding="utf-8"))
graph = render_graph(frequency, minimum_word_pixels=20, id_prefix="third", title="Word cloud · pp. 50–77")
mobile_note = '<p class="bd-frequency-mobile-note">Scroll sideways to read every circle.</p>'
graph = graph.replace(mobile_note + "\n", "", 1).replace('<div class="bd-frequency-chart"', mobile_note + '\n<div class="bd-frequency-chart"', 1)
top = frequency["words"]
assert top[0]["word"] == "name" and top[1]["word"] == "left", top[:2]
graph = graph.replace("</h2>", f'</h2>\n<p class="cloud-links">The most common word in these pages is <strong>name</strong> ({top[0]["count"]} times). Second is <strong>left</strong> ({top[1]["count"]}). Where do they come? · <a href="blood-dazzler-words.html">Word clouds by section and whole book</a></p>', 1)
SRC = (ROOT / "frst-110-resources/blood-dazzler-form-style.html").read_text()
style = SRC[SRC.index("<style>") + 7:SRC.index("</style>")]

# section colors reuse the Wednesday palette by id
style = (style.replace("#chain{", "#buried{").replace("#forms{", "#sonnet{")
         .replace("#reaction{", "#refrain{").replace("#whole{", "#siblings{"))
style += ("#storm{--c:#2f7a6b;--t:#e2f0ec}#smith{--c:#20303a;--t:#e9ecee}#search{--c:#4a5c64;--t:#eef1f2}"
          "main>section video,main>section figure img{width:100%;height:auto;border-radius:4px;background:#000;display:block}"
          "main>section figure{margin:14px 0 18px}main>section figcaption{font-size:16px;color:var(--muted);margin-top:6px}"
          ".photo-pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:600px){.photo-pair{grid-template-columns:1fr}}"
          ".chorus{display:grid;grid-template-columns:repeat(17,minmax(0,1fr));gap:5px;margin:12px 0}"
          ".chorus span{display:flex;align-items:center;justify-content:center;min-height:40px;border-radius:4px;"
          "border:1px solid rgba(32,47,53,.18);background:#fff;font-weight:600;font-size:15px}"
          ".chorus .pray{background:#cfe3f7}.chorus .leave{background:#a23b4a;color:#fff}"
          ".chorus .blank{background:transparent;border:2px dashed #4a5c64;color:#4a5c64}"
          ".key{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:16px;margin:4px 0 14px}"
          ".key i{display:inline-block;width:16px;height:16px;border-radius:3px;vertical-align:-2px;margin-right:6px;border:1px solid rgba(32,47,53,.18);font-style:normal}"
          ".beats{font-size:24px;font-weight:700;letter-spacing:.02em;margin:10px 0}.beats span{color:var(--c)}"
          ".rhyme{max-width:460px;width:auto}.rhyme td,.rhyme th{padding:3px 10px;font-size:16px}.rhyme td.l{text-align:left;font-weight:400}.r-A{background:#f6d7b0}.r-B{background:#fbe9a0}.r-C{background:#cfe3f7}"
          ".r-D{background:#ddd3f0}.r-E{background:#cfead9}.r-F{background:#f4c9cf}.r-G{background:#a23b4a;color:#fff}"
          ".abc{display:grid;grid-template-columns:repeat(11,minmax(0,1fr));gap:5px;margin:12px 0}"
          ".abc span{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:56px;border-radius:4px;"
          "background:var(--t);border:1px solid rgba(32,47,53,.18);font-weight:700;font-size:20px}"
          ".abc span small{font-weight:400;font-size:12px}.abc .gone{background:transparent;border:2px dashed var(--c);color:var(--c)}"
          ".content-note{font-size:16px;color:var(--muted)}"
          "@media(max-width:600px){.chorus{grid-template-columns:repeat(9,minmax(0,1fr))}.abc{grid-template-columns:repeat(6,minmax(0,1fr))}.beats{font-size:20px}}")

# "34": which sections carry what (checked against scan pp. 50-57)
PRAY = {14, 21, 32}
LEAVE = {13, 27, 34}
BLANK = {18}
cells = []
for n in range(1, 35):
    cls = "pray" if n in PRAY else "leave" if n in LEAVE else "blank" if n in BLANK else ""
    cells.append(f'<span class="{cls}">{n}</span>' if cls else f"<span>{n}</span>")
chorus = '<div class="chorus" role="img" aria-label="Sections 1 to 34. Prayer lines in 14, 21, 32. Leave them in 13, 27, 34. Section 18 is empty.">' + "".join(cells) + "</div>"

# Rebuilding: end words and rhyme letters (p. 70)
ENDS = [("yields", "A"), ("faces", "B"), ("reveals", "A"), ("traces", "B"), ("wind", "C"), ("nails", "D"),
        ("thick-skinned", "C"), ("fails", "D"), ("work", "E"), ("damned", "F"), ("berserk", "E"),
        ("programmed", "F"), ("stain", "G"), ("rain", "G")]
rows = ""
for i, (w, r) in enumerate(ENDS, 1):
    rows += f'<tr><th scope="row">Line {i}</th><td class="l">{w}</td><td class="r-{r}">{r}</td></tr>'
rhyme = ('<table class="sestina-grid rhyme"><caption>The last word of each line in “Rebuilding”</caption>'
         '<thead><tr><th scope="col"></th><th scope="col">Last word</th><th scope="col">Rhyme</th></tr></thead>'
         f"<tbody>{rows}</tbody></table>")

# Siblings: 2005 names in order, K left out (p. 75)
NAMES = ["Arlene", "Bret", "Cindy", "Dennis", "Emily", "Franklin", "Gert", "Harvey", "Irene", "José", None,
         "Lee", "Maria", "Nate", "Ophelia", "Philippe", "Rita", "Stan", "Tammy", "Vince", "Wilma"]
abc = []
for n in NAMES:
    if n is None:
        abc.append('<span class="gone">K<small>no line</small></span>')
    else:
        abc.append(f"<span>{n[0]}<small>{n}</small></span>")
abc = '<div class="abc" role="img" aria-label="One line per storm, Arlene to Wilma. The K line is missing.">' + "".join(abc) + "</div>"

body = f"""
<section id="chorus"><header class="sec-head"><h2>A numbered chorus: thirty-four sections</h2><p class="poem">“34” · pp. 50–57</p></header>
<p><strong>The headnote counts the dead: “Thirty-four bodies were found drowned in a nursing home.”</strong> The poem answers with thirty-four numbered sections. Many voices, one number.</p>
{chorus}
<div class="key"><span><i style="background:#cfe3f7"></i>the Lord’s Prayer</span><span><i style="background:#a23b4a"></i>“Leave them.”</span><span><i style="border:2px dashed #4a5c64"></i>empty</span></div>
<ul>
<li><strong>Section 18 is empty.</strong> A number, then nothing. One voice we never hear.</li>
<li><strong>The prayer comes in pieces.</strong> 14: “Our father / which art in heaven . . .” 21: “Hallowed be thy name.” 32: “Thy will be done.” Right after 21, section 22 bends it: “Hollow be <em>our</em> names.”</li>
<li><strong>The prayer skips a line.</strong> Between “Hallowed be thy name” and “Thy will be done,” the prayer says “Thy kingdom come.” Smith leaves it out.</li>
<li><strong>“Leave them.” comes three times,</strong> and it changes. 13: on its own line. 27: “And this scripture: <em>Leave them.</em>” 34: lowercase, split in two, the poem’s last words: “leave / them.”</li>
</ul>
<p class="reading"><strong>Ask:</strong> who says “Leave them”? The page never tells you. What does the poem gain by not naming the voice?</p>
<h3>Hear Smith perform “34”</h3>
<p>Before she reads, Smith says why she wrote it: “we forgot names and faces, we just started talking in statistics. So this is my attempt to give each one of those 34 people a few seconds of their voice back.” Listen for section 18, at about 7:25. She says the number and then says nothing.</p>
<figure>{player('smith-34', 'Patricia Smith performing 34 at the Vancouver Poetry Slam', 'smith-34-caption')}
<figcaption id="smith-34-caption">12 minutes 17 seconds · Patricia Smith with C.R. Avery, Vancouver Poetry Slam, February 11, 2013, including her introduction. <a href="https://www.youtube.com/watch?v=OZqIqrKjdkk">Vancouver Poetry House video</a> · <a href="blood-dazzler-assets/oct9/smith-34.mp4">Open video</a></figcaption></figure>
<h3>St. Rita’s Nursing Home, September 2005</h3>
<p>The real place behind the headnote, in St. Bernard Parish. The footage shows the empty rooms after the bodies were removed: wheelchairs in mud, photographs still on the walls. It ends with FEMA’s medical commander: “As long as there is one body floating in that water we are not doing a good enough job.”</p>
<figure>{player('st-ritas-ap', 'AP footage inside St. Rita’s Nursing Home, September 2005', 'st-ritas-caption')}
<figcaption id="st-ritas-caption">2 minutes 18 seconds · AP Archive, September 2005, natural sound. <a href="https://www.youtube.com/watch?v=A5vfgqbi17U">AP Archive video and shot list</a> · <a href="blood-dazzler-assets/oct9/st-ritas-ap.mp4">Open video</a></figcaption></figure>
<p>The owners, Salvador and Mabel Mangano, were charged that month for not evacuating. Their lawyer said they had waited for a mandatory evacuation order from the parish that never came. In 2007 a jury acquitted them. The final count was 35 dead. Smith’s headnote keeps the first wire report’s 34. <span class="source-note">Sources: <a href="https://www.youtube.com/watch?v=A5vfgqbi17U">AP Archive</a>, <a href="https://www.nbcnews.com/id/wbna20649744">NBC News, Sept. 7, 2007</a>, <a href="https://www.npr.org/2007/09/08/14261612/nursing-home-owners-acquitted-of-patient-deaths">NPR, Sept. 8, 2007</a>.</span></p>
<p class="content-note">Content note: the footage shows empty body bags on beds.</p></section>

<section id="storm"><header class="sec-head"><h2>Persona: the storm hears the prayer</h2><p class="poem">“Their Savior Was Me” · p. 58</p></header>
<p><strong>A persona poem gives the “I” to someone who is not the poet.</strong> Here the “I” is Katrina, and she has been listening to “34.”</p>
<div class="excerpt">Instead, I listened, bemused, to thirty-four<br>snotty pleas addressed to the idea of <em>Him</em></div>
<p>The number comes back from the headnote on p. 50, but now the storm is counting. The prayer comes back too: “They called / <em>Lord, Lord, Lord</em>.” The only one who hears it is the one doing the killing.</p>
<p class="reading"><strong>Ask:</strong> on p. 50 a wire report counts the dead. On p. 58 the storm counts them. What changes when the killer keeps the count?</p></section>

<section id="buried"><header class="sec-head"><h2>A work chant: “Plunge. Push. Lift. Toss it.”</h2><p class="poem">“Buried” · pp. 63–64</p></header>
<p><strong>The epigraph is the official word.</strong> The city’s cemetery administrator: “families and funeral homes would have to supply grave-digging personnel.” The poem is what that sentence means for one man with a shovel.</p>
<p class="beats"><span>PLUNGE.</span> <span>PUSH.</span> <span>LIFT.</span> <span>TOSS</span> it.</p>
<p><strong>Four words, four motions, four beats.</strong> The speaker names his own device: “I craft a chant purely for downbeat” (p. 63). A work song keeps a body moving when the work is too big.</p>
<ul>
<li><strong>The chant runs whole three times:</strong> twice on p. 63, once more on p. 64.</li>
<li><strong>The fourth time it breaks:</strong> “<em>Plunge. Push. Lift. Toss—</em>” Just before, the memory of his boy has come in: “Where are yoooou?”</li>
<li><strong>The last line has no chant left:</strong> “I have to dig.”</li>
</ul>
<p class="reading"><strong>Ask:</strong> what keeps him digging, and what breaks the beat? Find the line where the chant stops working.</p>
<p class="content-note">Content note: p. 64 is about a child.</p></section>

<section id="search"><header class="sec-head"><h2>Background: the search markings</h2><p class="poem">“Looking for Bodies” · pp. 60–61 · “Give Me My Name” · p. 74</p></header>
<p>After the flood, search teams went house to house and spray-painted an X on each one they entered. The four corners of the X recorded the date, the team, any hazards, and how many people were found inside, living or dead. “Looking for Bodies” is written as instructions to the person opening that door: “Slowly push the door open with your foot.”</p>
<div class="photo-pair"><figure><img src="blood-dazzler-assets/oct9/chalmette-search.jpg" alt="A search and rescue worker steps out of a mud-filled doorway; an orange X is painted beside the door." width="1280" height="853" loading="lazy" decoding="async"><figcaption>Chalmette, St. Bernard Parish, September 17, 2005. Bob McMillan/FEMA. <a href="https://commons.wikimedia.org/wiki/File:FEMA_-_15605_-_Photograph_by_Bob_McMillan_taken_on_09-17-2005_in_Louisiana.jpg">Photograph source</a></figcaption></figure>
<figure><img src="blood-dazzler-assets/oct9/search-markings.jpg" alt="An orange search X painted on the siding of a house standing in floodwater, reflected in the water below." width="1280" height="1960" loading="lazy" decoding="async"><figcaption>Search markings on a flooded house, New Orleans, September 10, 2005. Jocelyn Augustino/FEMA. <a href="https://commons.wikimedia.org/wiki/File:FEMA_-_19427_-_Photograph_by_Jocelyn_Augustino_taken_on_09-10-2005_in_Louisiana.jpg">Photograph source</a></figcaption></figure></div>
<p class="reading"><strong>Ask:</strong> the X turns a home into a record: a date, a team, a number. Which poems in these pages push back against being turned into a number?</p>
<p class="content-note">Content note: pp. 60–61 and 74 describe bodies.</p></section>

<section id="sonnet"><header class="sec-head"><h2>Sonnet: rebuilding in fourteen lines</h2><p class="poem">“Rebuilding” · p. 70</p></header>
<p><strong>A sonnet is fourteen lines with a fixed rhyme pattern.</strong> This one follows the English (Shakespearean) pattern: three groups of four lines, ABAB CDCD EFEF, then a rhyming pair, GG. Most lines have ten syllables, da-DUM five times: a <strong>RA</strong>-zored <strong>SKY</strong>, un-<strong>SURE</strong> of <strong>WHAT</strong> it <strong>YIELDS</strong>.</p>
{rhyme}
<p class="source-note">“Yields / reveals” and “damned / programmed” are near rhymes: close in sound, not exact.</p>
<ul>
<li><strong>One of the most orderly forms in the book, for a poem about putting things back.</strong> The rhyme keeps every line in its place, the way the builders try to.</li>
<li><strong>But Smith prints it as one block,</strong> with no break before the last pair, and her sentences spill over the line ends: “Each day reveals / inane thoughts of dance.” Order on the outside, spill inside.</li>
<li><strong>The rhyming pair lands the point:</strong> “to set chaos upright, scrub at the stain, / build our homes on rivers, waltz in the rain.”</li>
</ul>
<p class="reading"><strong>Ask:</strong> is that tidy ending hopeful, or foolish? Who builds a home on a river?</p></section>

<section id="refrain"><header class="sec-head"><h2>Refrain: “They keep touching him”</h2><p class="poem">“Golden Rule Days,” section I · p. 71</p></header>
<p><strong>A refrain is a line that keeps coming back.</strong> “They keep touching him” comes four times in one stanza, and it is the stanza’s last sentence.</p>
<ul>
<li><strong>The line breaks cut it up:</strong> “They keep touching / him,” and “They keep / touching him.” You keep running into it.</li>
<li><strong>The apology repeats too,</strong> in italics: “<em>We’re sorry, we’re sorry</em>,” “<em>sorry, so sorry</em>.”</li>
<li><strong>The repetition does to us what the hands do to him.</strong> It never stops. He is kept in “his role as child who drowns, again / and again.”</li>
</ul>
<p>On Wednesday the repeated “and” piled things up. Here repetition holds someone in place. The poem calls it “soft rescues.”</p>
<p class="reading"><strong>Ask:</strong> what do the hands give him, and what don’t they? What would one sentence, said once, lose?</p>
<p class="content-note">Content note: stay on p. 71. Section III of this poem (p. 73) prints a racial slur.</p></section>

<section id="siblings"><header class="sec-head"><h2>An alphabet list: the storms of 2005</h2><p class="poem">“Siblings” · p. 75</p></header>
<p><strong>Atlantic hurricanes are named in alphabetical order each season.</strong> Smith gives one line to each storm of 2005, Arlene to Wilma. One letter has no line.</p>
{abc}
<p>The list jumps from José to Lee. Katrina is left out of her own family, then named in the last three lines: “None of them talked about Katrina. / She was their odd sister, / the blood dazzler.” The book’s title arrives two poems before the end.</p>
<figure><img src="blood-dazzler-assets/oct9/2005-season-map.jpg" alt="Map of the Atlantic Ocean crossed by the tracks of every 2005 storm, many converging on the Gulf of Mexico." width="1280" height="792" loading="lazy" decoding="async"><figcaption>Every storm track of the 2005 Atlantic season. NOAA, public domain. <a href="https://commons.wikimedia.org/wiki/File:2005_Atlantic_hurricane_season_summary_map.png">Map source</a></figcaption></figure>
<p>2005 used up the whole list. After Wilma, six more storms were named with Greek letters, Alpha to Zeta. Smith’s list stops at Wilma.</p>
<p class="reading"><strong>Ask:</strong> why keep her out of the list? What does it mean that her siblings won’t talk about her?</p></section>

<section id="smith"><header class="sec-head"><h2>A question for Smith on Monday</h2></header>
<p>Patricia Smith joins us by Zoom on Monday, October 12. Bring one question about a choice she made, with its page. A strong one names what she did and what she could have done instead.</p>
<ul>
<li>On p. 54, why leave section 18 empty rather than give every number a voice?</li>
<li>On pp. 53–57, why leave “Thy kingdom come” out of the prayer?</li>
<li>On p. 70, why a sonnet, and why print it as one block?</li>
<li>On p. 75, why leave Katrina’s letter out of the list rather than give her a line?</li>
</ul>
<p>Write your own. These show the shape: “On p. __, why ___ rather than ___?”</p></section>
"""

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blood Dazzler · October 9 · FRST 110</title><link rel="icon" href="../favicon.svg" type="image/svg+xml"><meta name="description" content="Patricia Smith, pp. 50–77: forms and style, Smith performing “34,” St. Rita’s Nursing Home footage, search markings, the 2005 storm season, and word frequencies."><link rel="stylesheet" href="{versioned('_kit/blood-dazzler-1.css')}"><link rel="stylesheet" href="{versioned('_kit/blood-dazzler-words.css')}"><link rel="stylesheet" href="{versioned('_kit/blood-dazzler-oct7.css')}"><meta property="og:title" content="Blood Dazzler · October 9"><meta property="og:description" content="Forms and style in pp. 50–77, Smith performing “34,” St. Rita’s, search markings, and word frequencies."><meta property="og:type" content="website"><meta property="og:url" content="https://omatty123.github.io/teaching-fall-2026/frst-110-resources/blood-dazzler-oct-9.html"><meta property="og:image" content="https://omatty123.github.io/teaching-fall-2026/frst-110-resources/blood-dazzler-assets/oct9/2005-season-map.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://omatty123.github.io/teaching-fall-2026/frst-110-resources/blood-dazzler-assets/oct9/2005-season-map.jpg"><style>{style}</style></head>
<body><a class="skip" href="#content">Skip to class materials</a><nav class="nav" aria-label="Breadcrumb"><div class="nav-inner"><a class="brand" href="../courses/frst-110.html">FRST 110</a><a class="crumb" href="../courses/frst-110.html">Course materials</a><a href="blood-dazzler-oct-7.html">October 7 · pp. 25–49</a></div></nav>
<main id="content"><header><h1>Blood Dazzler</h1><p class="meta">Patricia Smith · Friday, October 9, 2026 · pp. 50–77 · Content notes: pp. 60–61 and 74 describe bodies; p. 73 prints a racial slur.</p><p class="cloud-links"><a href="https://lawrence.instructure.com/courses/14726/pages/song-of-the-day-do-you-know-what-it-means-to-miss-new-orleans-louis-armstrong">Song of the Day · Louis Armstrong, “Do You Know What It Means to Miss New Orleans”</a></p><nav class="section-nav" aria-label="Page sections"><a href="#katrina">Katrina film</a><a href="#chorus">Numbered chorus</a><a href="#storm">Persona</a><a href="#buried">Work chant</a><a href="#search">Search markings</a><a href="#sonnet">Sonnet</a><a href="#refrain">Refrain</a><a href="#siblings">Alphabet list</a><a href="#smith">Question for Smith</a><a href="#words-third">Word cloud</a><a href="#next-class">Monday and Wednesday</a></nav></header>
<section id="katrina"><header class="sec-head"><h2>Katrina · Clair de lune</h2></header>
<figure>{player("katrina-clair-de-lune", "Hurricane Katrina satellite animation with Debussy’s Clair de lune", "katrina-caption")}
<figcaption id="katrina-caption">1 minute 38 seconds · NOAA satellite imagery, set to Claude Debussy’s <cite>Clair de lune</cite>. <a href="https://www.nesdis.noaa.gov/news/hurricane-katrina-animation">NOAA source</a> · <a href="blood-dazzler-assets/oct9/katrina-clair-de-lune.mp4">Open video</a></figcaption></figure></section>
{body}
{graph}
<section id="next-class"><header class="sec-head"><h2>Monday’s community event · Wednesday’s listening</h2></header>
<p><strong>Monday, October 12: community event with Patricia Smith, via Zoom.</strong> Bring your question about a choice in <cite>Blood Dazzler</cite>, with its page number.</p>
<p><strong>Before Wednesday, October 14: listen to all three recordings on the <a href="blues-oct-14.html">Wednesday listening page</a>.</strong></p>
<ul><li>Charley Patton, “High Water Everywhere, Part 1”</li><li>Charley Patton, “High Water Everywhere, Part 2”</li><li>Kansas Joe McCoy and Memphis Minnie, “When the Levee Breaks”</li></ul>
<p>Listen to the recordings; the lyrics are there to help you follow them.</p></section>
<footer><p class="source-note">Poem excerpts: Patricia Smith, <cite>Blood Dazzler</cite> (Coffee House Press, 2008), pp. 50–77. Readings are offered as possible readings. <a href="blood-dazzler-assets/oct9/SOURCES.md">Video and photograph sources</a> · <a href="blood-dazzler-assets/SOURCES.md">Word-count source and method</a> · <a href="blood-dazzler-form-style.html">Form and style, pp. 5–49</a></p></footer></main></body></html>
"""
out = ROOT / "frst-110-resources/blood-dazzler-oct-9.html"
out.write_text(html)
print(out, len(html))
