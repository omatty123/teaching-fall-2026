# HIST 212 · October 13 visual lesson

## Overview

This record applies only to `hist-212-resources/class-2026-10-13.html`, with `_kit/hist-212-oct13.css` and `_kit/hist-212-oct13.js`. It records the implemented October 13 surface; it does not replace the site's global `DESIGN.md` or change `PRODUCT.md`.

The lesson follows the existing HIST paper, rust, and Source Sans 3 design. Documentary objects and assigned passages explain Buddhism, family obligations, and royal authority. Its opening combines the Pensive Bodhisattva with short definitions. The page then uses museum-object comparison, named people and source passages, a petition chronology, and a historical writing model.

## Colors

The warm paper background (`#fcfbf7`), dark ink (`#252e35`), muted source text (`#50585e`), and thin gray rules (`#cbd0d1`) come from the shared lesson stylesheet. Rust (`#713744`) marks section titles, dates, and selected glyphs. Blue links (`#065da2`) retain underlines. A blue outline (`#235a92`) marks keyboard focus. The orange rectangle on the writing model identifies a selected character; it is a locator, not decoration.

## Typography

Source Sans 3 supplies the main text, with sans-serif fallbacks. Chinese and Korean text use sans-serif system fallbacks; the printed character controls are modern type, distinct from the photographed historical handwriting. No serif display face or decorative heading break is introduced.

Body text is 20px with a 1.55 line height. The desktop title scales from 30px to 44px; section titles are 32px. Quotations are 24px with a 1.5 line height. Captions and citations remain subordinate. The large-text control increases paragraphs, definitions, and quotations for classroom display.

## Layout

The page has a compact utility navigation, title, reading metadata, and wrapping section links. Main content is limited to 1280px with 32px horizontal padding. Thin rules separate sections. The layout uses content-sized space, without oversized filled panels or a decorative hero.

Desktop pairs the opening object and definitions, source passages, petition explanation and chronology, and historical handwriting and printed characters. Museum objects use contained images to preserve their outlines and prevent cropping. The temple photograph supplies place context.

At 650px and below, main padding becomes 16px and most comparisons stack. The five-date chronology becomes ruled date rows. The two museum objects remain side by side at 390px, then stack below 360px. Headings wrap naturally.

## Elevation & Depth

The surface is flat. Rules, spacing, and text hierarchy organize content. The writing locator has a white outline around its orange border for visibility against the dark facsimile. No decorative card shadows are added.

## Components

- **Object opener:** The museum image links to its full file. The caption records object identity, collection, dimensions, and image source. Uncertain original provenance remains explicit.
- **Museum comparison:** Buddha and Maitreya images have independent captions and Met collection links. The heading states that objects are not shown at the same scale. Clothing conventions are explained without presenting the sculptures as portraits of the reading's authors.
- **People and passages:** Mouzi and Huiyuan have names, context, and assigned-source quotations. The Mouzi/Mozi distinction is explicit. The modern Donglin photograph is labeled as a present-day view.
- **Foreign practices (`#foreign-affairs`):** Three PRO / CON paired rows distinguish residence among foreigners, learning from foreign teachings, and adopting foreign dress. They reuse the existing passage comparison layout, source citations, and compact explanatory notes. The dress pair identifies the king of Zhao and his uncle as an earlier reading; the residence note preserves the assigned translation and identifies its disputed status.
- **War and killing (`#war-killing`):** Two paired rows place Laozi 31 beside Wŏn’gwang’s preserved reply and lay commandments, relocated from the petition section. The first compares force under constraint; the second compares victory and mourning with battlefield duty. Citations identify Ivanhoe’s translation and SKT pages. A source note identifies lines restored from the full assigned Laozi source. The section uses the same responsive passage layout and adds no discussion questions.
- **Petition:** The lost-text notice distinguishes Wŏn’gwang's reported reply from the missing petition. Separate 608, 611, and 612 rows avoid implying a single-event chronology. Academy of Korean Studies and Samguk sagi links accompany the explanation. A direct link from `#petition` to `#war-killing` leads to the preserved reply and commandments.
- **Writing comparison:** The National Palace Museum modelbook reproduction is labeled as later than Wang Xizhi, not his original sheet. Four printed characters have pronunciation and meaning. Clicking a native button moves the locator to its corresponding position, sets `aria-pressed`, and updates a polite live region. Native buttons preserve keyboard activation and visible focus.
- **Reading controls:** Highlights and large text are independent pressed-state toggles. Native details elements hold supplementary vocabulary. Image links provide full-size inspection. A skip link leads to the main content.
- **Calligraphy procedure:** The numbered copying and comparison activity remains separate from explanatory prose. It contains no assistant-written discussion questions.

## Do's and Don'ts

- Do retain provenance, source-page references, uncertainty, and distinctions between quotation and modern explanation.
- Do use authentic documentary graphics, legible sans-serif text, natural heading wrapping, and compact controls.
- Do check both 1440px and 390px rendered views when changing this surface, including actual fonts, object proportions, glyph locator placement, and keyboard focus.
- Don't imply that a later reproduction is an original autograph, a modern building is a surviving ancient view, or a historical reply is the lost petition itself.
- Don't add oversized filled panels, decorative empty space, invented portraits, or unsolicited discussion questions.

Documentation inspection: current `hist-212-resources/days/2026-10-13.json`, built HTML, scoped CSS/JavaScript, shared lesson CSS/JavaScript, and `PRODUCT.md`, October 11, 2026. This record describes implementation; screenshot review and deployment verification belong to the parent task's delivery checks.
