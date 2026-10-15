# October 15 HIST teaching page

## Overview

Mode: **Read**. This surface supports classroom projection and individual student reading in ordinary classroom light. It extends the existing HIST lesson design through warm paper, Source Sans 3, thin rules, underlined blue links, documentary images, and short cited passages. The compact title wraps naturally. There is no decorative hero.

Scope: `hist-212-resources/class-2026-10-15.html`, generated from `days/2026-10-15.json`, with shared `_kit/hist-212-lesson.css/js` and scoped `_kit/hist-212-oct15.css/js`. Image provenance is recorded in `images/hist/oct15/SOURCES.md`. This brief describes the current local implementation, not verified deployment. It does not replace project `DESIGN.md` or its sidecar; the older shared template values are not the typography authority for this lesson.

Nine topics cover rebuilding empire; Chang’an; Tang culture and Buddhist patronage; military crisis and poetry; Silla and Balhae; Silla Buddhist places and Wŏlmyŏng; Japanese court, land and households; Shōmu; and a concluding comparison. Readings are a separate navigation destination. Shōmu remains a brief example within Japan, not the lesson’s organizing center. No assistant-written discussion questions are added.

## Colors

The shared lesson stylesheet supplies warm paper (`#fcfbf7`), dark text (`#252e35`), supporting gray (`#50585e`), and thin rules (`#cbd0d1`). Blue links (`#065da2`) remain underlined; muted burgundy (`#713744`) identifies section headings and sequence rules. Selected utility buttons use dark blue-gray (`#233e4a`) with white text. Passage highlighting uses pale yellow (`#f6df93`) and can be turned off. Visible keyboard focus uses blue (`#235a92`). These are surface observations, not replacements for global tokens.

## Typography

The lesson uses `"Source Sans 3", Arial, sans-serif`. Body text is 20px with 1.55 line height. The title scales from 28px to 40px; section titles are 30px, reducing to 26px below 760px. Quoted passages are 26px with 1.4 line height and preserved line breaks, reducing to 23px on phones; Large text raises them to 32px. Captions are 15px with 1.4 line height. Heading width is unrestricted so words wrap with the available space. Image labels use sans-serif adaptations where identified in the source ledger.

## Layout

Main content has a 1360px maximum width and 20px by 32px padding, reducing to 16px padding below 760px. At 1000px and wider, enhanced topic navigation occupies a fixed 210px rail within a 250px grid column. At intermediate widths the links wrap above the content. On phones a labeled topic selector replaces the individual navigation links.

Image-and-text studies use two columns in a 1.1:1 ratio with a 32px gap. Three-part sequences use three columns. Both stack below 760px. Images retain their proportions with `object-fit: contain`, a maximum height of 650px, and a 520px phone limit. Maps have direct enlargement links for detailed inspection. The concluding comparison uses a compact three-column table with smaller cell padding and 16px cell text on phones.

## Elevation & Depth

Thin rules, whitespace, and type establish hierarchy. The scoped stylesheet introduces no shadows, decorative panels, or oversized filled banners. White utility controls remain small and functional.

## Shapes

Images are rectangular and uncropped. Shared buttons have 5px corners and a thin border. Native selects and disclosures remain recognizable controls. Avoid extending these lesson details into a project-wide component redesign.

## Components

- Topic navigation shows one topic at a time when JavaScript is available. Hash links support direct navigation; the current link receives `aria-current="page"`. The mobile selector mirrors the selected topic.
- Previous and Next links follow lesson order. Hash navigation moves keyboard focus to the selected topic heading, including after pager replacement. Read all topics reveals the complete lesson and exposes its pressed state; View one topic restores the focused reading layout.
- Without JavaScript, the static page retains every topic and its anchor links. Print styling reveals all topics and hides topic controls.
- Highlights and Large text reuse the shared lesson controls. Buttons, topic links, disclosure summaries, and the mobile selector provide at least 44px minimum height. Focus outlines and a skip link support keyboard use.
- Figures pair meaningful alternative text with visible captions, provenance links, and enlargement links. Captions distinguish modern reconstructions, models, photographs, and later rebuilding from the historical material they illustrate.
- Source passages keep attribution adjacent to the quotation. A native disclosure holds the supplementary court-history note.

## Do's and Don'ts

- Do preserve the compact Read layout, sans-serif typography, naturally wrapping headings, source credits, and proportional images.
- Do retain Tang, Silla, and Japan coverage and the nine-topic sequence when making narrow visual fixes.
- Do keep historical verification separate from design review. This brief does not certify quotation accuracy, historical claims, copyright status, or external destinations.
- Don't add discussion questions, slogans, oversized heroes, or decorative color fields.
- Don't apply stale global Inter-only language to this established Source Sans 3 lesson.

### Review evidence and limits

The implementation team reports desktop and mobile screenshots in `.impeccable/review/oct15/`, no visual blockers, all 11 image elements decoded, no browser errors, and passing strict build and local-link checks. The keyboard-focus advisory was addressed in the topic-navigation JavaScript. Detailed maps remain available through enlargement links. These are the supplied review results; this documentation pass inspected the built HTML and styles/scripts rather than rerunning browser verification. External links and historical claims are outside this design-review scope. Deployment must be confirmed separately before describing this version as LIVE.

Not canonized: older project-wide decorative-header and question-led guidance conflicts with the user's later compact-layout and no-added-questions requirements. It is not adopted for this surface.

### October 15 source-slide addition

At the user's explicit request, the Silla and Japan topics now begin with exact rendered excerpts from the existing Google Drive presentation [Chinese influence on Japan and Korea](https://docs.google.com/presentation/d/1lBYGWuY8__S9YI5WSfsYSXYUq7kMsITtEvH0wAAHPTo/edit). Slide p19 (slide 7) supplies the Gyeongju reconstruction; slide p27 (slide 15) supplies the Nara–Chang’an comparison. Local assets are `images/hist/oct15/silla-capital-source-slide.png` and `images/hist/oct15/nara-changan-source-slide.png`. Figures provide enlargement and original-slide links; the page also links to the whole presentation.

Original slide labels, questions, and embedded typography remain intact as source material. This is the source-preservation exception to the sans-serif rule, not permission to introduce serif typography into page controls, captions, or new prose. Preserving the user's original questions does not authorize assistant-written questions. The detailed Nara plan remains available in an expandable disclosure within the Japan topic.

The image ledger records the author-supplied course excerpts and explicitly notes that the deck does not state underlying image provenance. These excerpts are not assigned an open license. The original Google Drive presentation is unchanged. The earlier 11-image browser result predates this addition and must not be read as verification of the two new images; this documentation update confirms the local HTML and ledger changes only.
