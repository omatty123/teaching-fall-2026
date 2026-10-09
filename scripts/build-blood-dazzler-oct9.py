#!/usr/bin/env python3
"""Build the October 9 Blood Dazzler page: form cards, Katrina recitation, St. Rita's footage, search-marking photos, 2005 season map, pp. 50-77 word cloud."""
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
<p><a href="blood-dazzler-lords-prayer.html">The Lord’s Prayer · full prayer and its words in “34”</a> · <a href="blood-dazzler-divinity.html">How do we understand divinity? And why?</a></p>
{chorus}
<div class="key"><span><i style="background:#cfe3f7"></i>the Lord’s Prayer</span><span><i style="background:#a23b4a"></i>“Leave them.”</span><span><i style="border:2px dashed #4a5c64"></i>empty</span></div>
<ul>
<li><strong>Section 18 is empty.</strong> A number, then nothing. One voice we never hear.</li>
<li><strong>The prayer comes in pieces.</strong> 14: “Our father / which art in heaven . . .” 21: “Hallowed be thy name.” 32: “Thy will be done.” Right after 21, section 22 bends it: “Hollow be <em>our</em> names.”</li>
<li><strong>The prayer skips a line.</strong> Between “Hallowed be thy name” and “Thy will be done,” the prayer says “Thy kingdom come.” Smith leaves it out.</li>
<li><strong>“Leave them.” comes three times,</strong> and it changes. 13: on its own line. 27: “And this scripture: <em>Leave them.</em>” 34: lowercase, split in two, the poem’s last words: “leave / them.”</li>
</ul>
<p class="reading"><strong>Ask:</strong> who says “Leave them”? The page never tells you. What does the poem gain by not naming the voice?</p>
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

<section id="search"><header class="sec-head"><h2>Background: the search markings</h2><p class="poem">“Looking for Bodies” · pp. 60–61 · “Give Me My Name” · p. 74</p></header>
<p>After the flood, search teams went house to house and spray-painted an X on each one they entered. The four corners of the X recorded the date, the team, any hazards, and how many people were found inside, living or dead. “Looking for Bodies” is written as instructions to the person opening that door: “Slowly push the door open with your foot.”</p>
<div class="photo-pair"><figure><img src="blood-dazzler-assets/oct9/chalmette-search.jpg" alt="A search and rescue worker steps out of a mud-filled doorway; an orange X is painted beside the door." width="1280" height="853" loading="lazy" decoding="async"><figcaption>Chalmette, St. Bernard Parish, September 17, 2005. Bob McMillan/FEMA. <a href="https://commons.wikimedia.org/wiki/File:FEMA_-_15605_-_Photograph_by_Bob_McMillan_taken_on_09-17-2005_in_Louisiana.jpg">Photograph source</a></figcaption></figure>
<figure><img src="blood-dazzler-assets/oct9/search-markings.jpg" alt="An orange search X painted on the siding of a house standing in floodwater, reflected in the water below." width="1280" height="1960" loading="lazy" decoding="async"><figcaption>Search markings on a flooded house, New Orleans, September 10, 2005. Jocelyn Augustino/FEMA. <a href="https://commons.wikimedia.org/wiki/File:FEMA_-_19427_-_Photograph_by_Jocelyn_Augustino_taken_on_09-10-2005_in_Louisiana.jpg">Photograph source</a></figcaption></figure></div>
<p class="reading"><strong>Ask:</strong> the X turns a home into a record: a date, a team, a number. Which poems in these pages push back against being turned into a number?</p>
<p class="content-note">Content note: pp. 60–61 and 74 describe bodies.</p></section>

<section id="buried"><header class="sec-head"><h2>A work chant: “Plunge. Push. Lift. Toss it.”</h2><p class="poem">“Buried” · pp. 63–64</p></header>
<p><a href="persona-three-pillars.html"><strong>Three Pillars of Crafting Personas · instructions and working example</strong></a></p>
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

<section id="katrina"><header class="sec-head"><h2>Katrina · Clair de lune</h2><p class="poem">“Weather is nothing until it reaches skin” · p. 76</p></header>
<figure>{player("katrina-recitation-final", "Katrina: Patricia Smith’s words recited over NOAA satellite imagery and Debussy’s Clair de lune", "katrina-caption")}
<figcaption id="katrina-caption">1 minute 39 seconds · Words by Patricia Smith, read by Teacher Ma, with synchronized poem lines. NOAA satellite imagery, set to Claude Debussy’s <cite>Clair de lune</cite>. <a href="https://www.nesdis.noaa.gov/news/hurricane-katrina-animation">NOAA source</a> · <a href="blood-dazzler-assets/oct9/katrina-recitation-final.mp4">Open video</a></figcaption></figure></section>

<section id="dakar"><header class="sec-head"><h2>Dakar · video from home</h2></header>
<p>A friend of Teacher Ma sent this video from his own home in Dakar, Senegal.</p>
<figure style="max-width:270px"><video style="aspect-ratio:9/16" controls playsinline preload="none" width="360" height="640" poster="blood-dazzler-assets/oct9/dakar-home-poster.jpg" aria-label="Water being scooped into buckets at a home in Dakar" aria-describedby="dakar-caption"><source src="blood-dazzler-assets/oct9/dakar-home.mp4" type="video/mp4"><a href="blood-dazzler-assets/oct9/dakar-home.mp4">Open video</a></video><figcaption id="dakar-caption">1 minute 20 seconds · Scooping standing water into buckets. <a href="blood-dazzler-assets/oct9/dakar-home.mp4">Open video</a></figcaption></figure></section>

<section id="smith"><header class="sec-head"><h2>A question for Smith on Monday</h2></header>
<p>Patricia Smith joins us by Zoom on Monday, October 12. Bring one question about a choice she made, with its page. A strong one names what she did and what she could have done instead.</p>
<ul>
<li>On p. 54, why leave section 18 empty rather than give every number a voice?</li>
<li>On pp. 53–57, why leave “Thy kingdom come” out of the prayer?</li>
<li>On p. 70, why a sonnet, and why print it as one block?</li>
<li>On p. 75, why leave Katrina’s letter out of the list rather than give her a line?</li>
</ul>
<p>Write your own. These show the shape: “On p. __, why ___ rather than ___?”</p></section>
<section id="author-questions"><header class="sec-head"><h2>“Why did you write this?” · Preparing to talk with Patricia Smith</h2></header>
<p>That question can ask about an event, a purpose, a word, or a formal choice. Decide which you want to understand. These are familiar author-interview questions, not a measured ranking. The answers below summarize and briefly quote Smith’s published interviews; they do not predict what she will say on Monday.</p>
<h3>Questions authors often receive—and what Smith has already said</h3>
<dl>
<dt><strong>Why did you write this book? What inspired you?</strong></dt>
<dd><p>Smith says the deaths of the nursing-home residents stayed with her. Writing “34” led to more poems and eventually a book. <a href="https://knpr.org/show/knprs-state-of-nevada/2016-08-25/poet-patricia-smith-on-storytelling-in-a-controlled-space">KNPR interview</a></p><p><strong>Follow-up:</strong> What changed when “34” became part of a whole book rather than a poem on its own?</p></dd>
<dt><strong>What made you keep writing about Katrina?</strong></dt>
<dd><p>Smith describes reading “34” at the Palm Beach Poetry Festival in winter 2007. After noticing restlessness, she spoke with an audience member who said, “they just had Mardi Gras, didn’t they? Things are better now.” Smith understood this response as a wish to put the catastrophe behind them. That encounter helped turn a single poem into a continuing project. <a href="https://isthmus.com/arts/books/wisconsin-book-festival-2008-patricia-smith-speaks/">Smith’s account in <cite>Isthmus</cite> (2008)</a></p><p><strong>Follow-up:</strong> How did that encounter change what you wanted the poems to make readers hear?</p></dd>
<dt><strong>What did you want readers to understand?</strong></dt>
<dd><p>She describes Katrina as a human catastrophe that exposed the country’s abandonment of poor, mostly brown people. <a href="https://thevoltablog.wordpress.com/2016/01/04/interview-dazzle-roll-call-patricia-smith/">The Volta interview</a></p><p><strong>Follow-up:</strong> In “34,” what can separate voices make us understand that the headnote’s number cannot?</p></dd>
<dt><strong>Why is it called <cite>Blood Dazzler</cite>?</strong></dt>
<dd><p><strong>Sound first:</strong> In 2008, Smith said, “I have no idea what those two words mean.” She loved how the phrase felt in her mouth and what remained after she spoke it. It comes from the end of “Siblings,” where it names Katrina. <a href="https://isthmus.com/arts/books/wisconsin-book-festival-2008-patricia-smith-speaks/">David Medaris’s interview, <cite>Isthmus</cite> (2008)</a></p>
<p><strong>Meaning developing:</strong> In 2016, she explained that the phrase began as a placeholder she intended to replace. By the time she finished the book, it could encompass the narrative without fixing its meaning. <a href="https://thevoltablog.wordpress.com/2016/01/04/interview-dazzle-roll-call-patricia-smith/">Jon Riccio’s interview, <cite>The Volta</cite> (2016)</a></p>
<p><strong>For our reading:</strong> A phrase can begin with its sound and acquire meaning through the poems around it. Our readings of blood, kinship, attraction, and impaired sight still need evidence from the book; they are not necessarily meanings Smith planned in advance.</p><p><strong>Follow-up:</strong> What did those words come to hold that they did not hold when you first wrote them?</p></dd>
<dt><strong>Why make the hurricane speak?</strong></dt>
<dd><p>Smith wanted an unexpected perspective. Katrina’s voice helped shape the collection and gave the storm a changing emotional life. <a href="https://thevoltablog.wordpress.com/2016/01/04/interview-dazzle-roll-call-patricia-smith/">The Volta interview</a></p><p><strong>Follow-up:</strong> How did you decide when we should hear Katrina and when we should hear someone suffering because of her?</p></dd>
<dt><strong>Why use strict forms for such painful events?</strong></dt>
<dd><p>She says the tanka’s syllable limits slowed her approach to death and helped her manage overwhelming emotion. <a href="https://thevoltablog.wordpress.com/2016/01/04/interview-dazzle-roll-call-patricia-smith/">The Volta interview</a></p><p><strong>Follow-up:</strong> In “Ethel’s Sestina,” p. 46, how did you decide that “Come” needed to interrupt the six-line pattern?</p></dd>
</dl>
<h3>Questions from our reading</h3>
<p>These are interpretations to test with Smith, not answers we already know.</p>
<ul>
<li><strong>The unnamed verb:</strong> In “Tankas,” p. 38, did you have a particular verb in mind? We connected the unnamed word with “Come” in “Ethel’s Sestina,” p. 46. How did those passages develop?</li>
<li><strong>Voices beyond death:</strong> When Ethel says “They don’t hear Come,” we read her as hearing something the living cannot. How did you decide what her voice could tell us?</li>
<li><strong>Prayer and poetry:</strong> “34” includes prayer, and Ethel hears a summons. What relationship, if any, do you see between prayer and giving the dead a voice in these poems?</li>
<li><strong>The title and the reader:</strong> In “Siblings,” p. 75, we read “blood” as both injury and family, and “dazzler” as both attraction and impaired sight. How does that reading compare with what you heard in the phrase?</li>
<li><strong>Research and imagination:</strong> In writing Ethel’s voice, how did you decide what to research and what to imagine?</li>
</ul>
<h3>Listen to the answer before choosing the next question</h3>
<ul>
<li><strong>If she describes an event:</strong> ask which detail became the first line or image.</li>
<li><strong>If she names a purpose:</strong> ask how one choice on the page serves it.</li>
<li><strong>If she says the sound came first:</strong> ask what changed as she revised or read it aloud.</li>
<li><strong>If she says she did not plan the connection:</strong> ask when she noticed it, if she did.</li>
<li><strong>If her reading differs from ours:</strong> explain the line that led us there, then ask how she reads it. Her account of writing adds evidence; we still need to explain our textual evidence.</li>
</ul>
<p><strong>Prepare one main question and one follow-up.</strong> Keep the book open to the passage. Ask one question at a time. If another person asks yours, listen for what remains unanswered. You do not need a long introduction or specialist vocabulary.</p>
<p class="source-note">Published answers: David Medaris, <cite>Isthmus</cite>, October 13, 2008; Jon Riccio, <cite>The Volta</cite>, January 4, 2016; Fred Wasser, KNPR, August 25, 2016. Text check: <a href="https://poets.org/poem/ethels-sestina">“Ethel’s Sestina,” Academy of American Poets</a>. <a href="blood-dazzler-come.html">Our reasoning about “come”</a>.</p>
</section>

"""

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blood Dazzler · October 9 · FRST 110</title><link rel="icon" href="../favicon.svg" type="image/svg+xml"><meta name="description" content="Patricia Smith, pp. 50–77: forms and style, Katrina recitation, St. Rita’s Nursing Home footage, search markings, the 2005 storm season, and word frequencies."><link rel="stylesheet" href="{versioned('_kit/blood-dazzler-1.css')}"><link rel="stylesheet" href="{versioned('_kit/blood-dazzler-words.css')}"><link rel="stylesheet" href="{versioned('_kit/blood-dazzler-oct7.css')}"><meta property="og:title" content="Blood Dazzler · October 9"><meta property="og:description" content="Forms and style in pp. 50–77, Katrina recitation, St. Rita’s, search markings, and word frequencies."><meta property="og:type" content="website"><meta property="og:url" content="https://omatty123.github.io/teaching-fall-2026/frst-110-resources/blood-dazzler-oct-9.html"><meta property="og:image" content="https://omatty123.github.io/teaching-fall-2026/frst-110-resources/blood-dazzler-assets/oct9/2005-season-map.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://omatty123.github.io/teaching-fall-2026/frst-110-resources/blood-dazzler-assets/oct9/2005-season-map.jpg"><style>{style}</style></head>
<body><a class="skip" href="#content">Skip to class materials</a><nav class="nav" aria-label="Breadcrumb"><div class="nav-inner"><a class="brand" href="../courses/frst-110.html">FRST 110</a><a class="crumb" href="../courses/frst-110.html">Course materials</a><a href="blood-dazzler-oct-7.html">October 7 · pp. 25–49</a></div></nav>
<main id="content"><header><h1>Blood Dazzler</h1><p class="meta">Patricia Smith · Friday, October 9, 2026 · pp. 50–77 · Content notes: pp. 60–61 and 74 describe bodies; p. 73 prints a racial slur.</p><p class="cloud-links"><a href="https://lawrence.instructure.com/courses/14726/pages/song-of-the-day-do-you-know-what-it-means-to-miss-new-orleans-louis-armstrong">Song of the Day · Louis Armstrong, “Do You Know What It Means to Miss New Orleans”</a></p><nav class="section-nav" aria-label="Page sections"><a href="blood-dazzler-divinity.html">How do we understand divinity? And why?</a><a href="persona-three-pillars.html">Three Pillars of Crafting Personas</a><a href="blood-dazzler-background.html">Background vocabulary</a><a href="blood-dazzler-lords-prayer.html">The Lord’s Prayer · “34”</a><a href="#winnebago">Lake Winnebago</a><a href="#chorus">Numbered chorus</a><a href="#storm">Persona</a><a href="#search">Search markings</a><a href="#buried">Work chant</a><a href="#sonnet">Sonnet</a><a href="#refrain">Refrain</a><a href="#siblings">Alphabet list</a><a href="#katrina">Katrina film · p. 76</a><a href="#dakar">Dakar · video from home</a><a href="#smith">Question for Smith</a><a href="#author-questions">Prepare for the conversation</a><a href="#words-third">Word cloud</a><a href="#next-class">Monday and Wednesday</a><a href="#second-line">Second line · send-off</a></nav></header>
<section id="winnebago"><header class="sec-head"><h2>Lake Winnebago</h2></header>
<figure><iframe src="https://www.youtube-nocookie.com/embed/T3yc4W1na8M?start=760&amp;end=770&amp;rel=0" title="Lake Winnebago exchange at the October 2 FRST community event, 12:40–12:50" style="width:100%;aspect-ratio:16/9;border:0" loading="lazy" allow="encrypted-media;picture-in-picture;fullscreen" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe><figcaption><strong>Be the one who speaks.</strong><br>FRST community event · October 2, 2026 · 12:40–12:50 · <a href="https://www.youtube.com/watch?v=T3yc4W1na8M&amp;t=760s">Open at 12:40 on YouTube</a></figcaption></figure></section>
{body}
{graph}
<section id="next-class"><header class="sec-head"><h2>Monday’s community event · Wednesday’s listening</h2></header>
<p><strong>Monday, October 12: community event with Patricia Smith, via Zoom.</strong> Bring your question about a choice in <cite>Blood Dazzler</cite>, with its page number.</p>
<p><strong>Before Wednesday, October 14: listen to all three recordings on the <a href="blues-oct-14.html">Wednesday listening page</a>.</strong></p>
<ul><li>Charley Patton, “High Water Everywhere, Part 1”</li><li>Charley Patton, “High Water Everywhere, Part 2”</li><li>Kansas Joe McCoy and Memphis Minnie, “When the Levee Breaks”</li></ul>
<p>Listen to the recordings; the lyrics are there to help you follow them.</p></section>
<section id="second-line"><header class="sec-head"><h2>New Orleans second line</h2></header>
<p>The second line is the people who join behind the band and parade leaders, walking and dancing. <a href="https://www.nps.gov/jazz/learn/historyculture/history_early.htm">About the tradition</a>.</p>
<figure><iframe src="https://www.youtube-nocookie.com/embed/g32nkf0Wi2U?rel=0" title="New Orleans Second Line — Hurricane Katrina 20 Years Later — Historical 9th Ward Memorial" style="width:100%;aspect-ratio:16/9;border:0" loading="lazy" allow="encrypted-media;picture-in-picture;fullscreen" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe><figcaption>New Orleans Second Line · Hurricane Katrina 20 Years Later · Historical 9th Ward Memorial. Video: Subject Matter Experts. <a href="https://www.youtube.com/watch?v=g32nkf0Wi2U">Play on YouTube</a></figcaption></figure>
</section>
<footer><p class="source-note">Poem excerpts: Patricia Smith, <cite>Blood Dazzler</cite> (Coffee House Press, 2008), pp. 50–77. Readings are offered as possible readings. <a href="blood-dazzler-assets/oct9/SOURCES.md">Video and photograph sources</a> · <a href="blood-dazzler-assets/SOURCES.md">Word-count source and method</a> · <a href="blood-dazzler-form-style.html">Form and style, pp. 5–49</a></p></footer></main></body></html>
"""
out = ROOT / "frst-110-resources/blood-dazzler-oct-9.html"
out.write_text(html)
print(out, len(html))
