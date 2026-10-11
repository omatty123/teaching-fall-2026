# HIST 212 · October 13 visual lesson

## Overview

This record applies only to `hist-212-resources/class-2026-10-13.html`, with `_kit/hist-212-oct13.css` and `_kit/hist-212-oct13.js`. It records the implemented October 13 surface; it does not replace the site's global `DESIGN.md` or change `PRODUCT.md`.

The approved option 2 implementation uses a compact visual reference layout with paper, ink, rust, and Source Sans 3. Documentary objects and assigned passages explain Buddhism, family obligations, and royal authority. Its opening combines the full Pensive Bodhisattva photograph with object facts. A full-width Three Jewels and Four Noble Truths diagram follows, with brief vocabulary inside a native details element. All 23 quotations and the existing timeline are retained. The page then uses museum-object comparison, named people and source passages, a petition chronology, and a historical writing model.

## Colors

The scoped page palette uses warm paper (`#faf9f5`), dark ink (`#202c30`), thin gray rules (`#bcc5c4`), blue links and focus outlines (`#075d96`), and rust emphasis (`#91401e`). Links retain underlines. The orange rectangle on the writing detail identifies a selected character; it is a locator, not decoration. The teaching SVG uses the same paper and ink with its own teal labels and rust connector lines.

## Typography

Source Sans 3 supplies the main text, with sans-serif fallbacks. Chinese and Korean text use sans-serif system fallbacks; the printed character controls are modern type, distinct from the photographed historical handwriting. No serif display face or decorative heading break is introduced.

Body text is 21px with a 1.45 line height. The desktop title scales from 30px to 42px; section titles are 32px. Quotations are 25px with a 1.45 line height. Captions and citations remain subordinate. The large-text control increases paragraphs, definitions, and quotations for classroom display.

## Layout

The page has a compact utility navigation, title, reading metadata, and wrapping section links. Main content is limited to 1440px with 36px horizontal padding. Thin rules separate sections. The layout uses content-sized space, without oversized filled panels or a decorative hero.

Desktop pairs the opening object and object facts, source passages, petition explanation and chronology, and historical handwriting and printed characters. Museum objects use contained images to preserve their outlines and prevent cropping. The temple photograph supplies place context.

At 650px and below, main padding becomes 16px and most comparisons stack. The graphic chronology becomes a readable vertical chronology with a thin line and event dots; its full-size SVG link remains available. The two museum objects stack below 650px. The teaching diagram retains a 960px minimum width inside a keyboard-focusable horizontal scroll region, with an explicit sideways-scroll caption. Mobile body text is 20px and quotations are 23px. Headings wrap naturally.

## Elevation & Depth

The surface is flat. Rules, spacing, and text hierarchy organize content. The writing locator has a white outline around its orange border for visibility against the dark facsimile. No decorative card shadows are added.

## Components

- **Object opener:** The full `pensive-83.jpg` photograph is contained in a 640px-high desktop image area, preserving the entire sculpture; it links to its full file. The caption records object identity, collection, dimensions, and image source. Uncertain original provenance remains explicit.
- **Teaching diagram (`#teachings`):** The full-width `buddhist-teachings.svg` connects the Three Jewels to the Four Noble Truths within Dharma, then groups the Eightfold Path under wisdom, ethical conduct, and meditation. It includes accessible title and description text, sans-serif labels, a full-size link, and cited sources. A compact details disclosure holds brief definitions in place of the previous sparse glossary layout.
- **Graphic timeline (`#spread`):** A transparent SVG places China, people, and Silla / Sui on a shared 200–650 CE scale. Rust dots mark events; teal lines mark the overlapping lifespans of Wang Xizhi and Huiyuan. Dashed guides and short leaders align labels without filled panels. SVG text uses Arial/Helvetica sans-serif, with an accessible title and description. Mouzi’s debated date is explained separately, without a precise marker. The desktop legend identifies dots as events and lines as lifespans. At 650px and below, an eight-entry vertical chronology replaces the graphic, with an explicit note that spacing is not to scale; a full-size SVG link remains available at every width. Citations identify conventional lifespan dating and distinguish temporal alignment from causation.
- **Museum comparison:** Buddha and Maitreya images use 560px-high contained desktop image areas and have independent captions and Met collection links. The heading states that objects are not shown at the same scale. Clothing conventions are explained without presenting the sculptures as portraits of the reading's authors.
- **People and passages:** Mouzi and Huiyuan have names, context, and assigned-source quotations. The Mouzi/Mozi distinction is explicit. The modern Donglin photograph is labeled as a present-day view.
- **Foreign practices (`#foreign-affairs`):** Three PRO / CON paired rows distinguish residence among foreigners, learning from foreign teachings, and adopting foreign dress. They reuse the existing passage comparison layout, source citations, and compact explanatory notes. The dress pair identifies the king of Zhao and his uncle as an earlier reading; the residence note preserves the assigned translation and identifies its disputed status.
- **War and killing (`#war-killing`):** Two paired rows place Laozi 31 beside Wŏn’gwang’s preserved reply and lay commandments, relocated from the petition section. The first compares force under constraint; the second compares victory and mourning with battlefield duty. Citations identify Ivanhoe’s translation and SKT pages. A source note identifies lines restored from the full assigned Laozi source. The section uses the same responsive passage layout and adds no discussion questions.
- **Petition:** The lost-text notice distinguishes Wŏn’gwang's reported reply from the missing petition. Separate 608, 611, and 612 rows avoid implying a single-event chronology. Academy of Korean Studies and Samguk sagi links accompany the explanation. A direct link from `#petition` to `#war-killing` leads to the preserved reply and commandments.
- **Seasonal killing (`#seasonal-killing`):** The existing paired-passage layout places the Liji spring rule beside Wŏn’gwang’s spring–summer and observance-day rule. A three-column concept row supplies dated summaries of Xunzi, Lüshi chunqiu, and Wŏn’gwang, with citations and explicit summary labels. The section identifies earlier parallels without claiming demonstrated borrowing, distinguishes “birthing season” as explanatory wording, and notes the later transmission of Wŏn’gwang’s account. It reuses the page’s responsive styles and adds no discussion questions.
- **Writing comparison:** The National Palace Museum’s *Timely Clearing after Snowfall* image is identified as a Tang tracing copy, not Wang Xizhi’s autograph. CSS enlarges the right-hand letter leaf from the intact album photograph in a 760:1100 detail viewport. A full-album link and a separate native details disclosure preserve inspection of the entire image, later inscriptions, seals, provenance, and image terms. The later modelbook rubbing remains an additional reference. Four modern sans-serif characters (快, 雪, 時, 晴) have pronunciation and meaning. Clicking a native button moves the locator to vertical positions 38%, 49%, 60%, and 71%, sets `aria-pressed`, and updates a polite live region. Native buttons preserve keyboard activation and visible focus.
- **Historical name links:** The optional day-level `nameLinks` mapping supplies source destinations for historical personal names and selected named references. The builder emits ordinary static links in the lesson; these do not depend on a client-side linking script.
- **Reading controls:** Highlights and large text are independent pressed-state toggles. Native details elements hold supplementary vocabulary. Image links provide full-size inspection. A skip link leads to the main content.
- **Calligraphy procedure:** The numbered copying and comparison activity remains separate from explanatory prose. It contains no assistant-written discussion questions.

## Do's and Don'ts

- Do retain provenance, source-page references, uncertainty, and distinctions between quotation and modern explanation.
- Do use authentic documentary graphics, legible sans-serif text, natural heading wrapping, and compact controls.
- Do check both 1440px and 390px rendered views when changing this surface, including actual fonts, object proportions, glyph locator placement, and keyboard focus.
- Don't imply that a later reproduction is an original autograph, a modern building is a surviving ancient view, or a historical reply is the lost petition itself.
- Don't add oversized filled panels, decorative empty space, invented portraits, or unsolicited discussion questions.

Documentation inspection: current `hist-212-resources/days/2026-10-13.json`, `images/hist/oct13/buddhist-teachings.svg`, scoped CSS/JavaScript, and `PRODUCT.md`, October 11, 2026. Updated after the parent task’s visual SHIP review for approved option 2. This scoped brief leaves global `DESIGN.md` unchanged. This record describes implementation; screenshot review and deployment verification belong to the parent task's delivery checks.
