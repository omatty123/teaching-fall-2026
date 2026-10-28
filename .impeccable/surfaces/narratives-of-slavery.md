# Narratives of Slavery

Mode: Read. Scoped extension of the established FRST/Equiano course materials, with the user’s existing design rules as authority. Code-led; no new visual identity, comp or concept-selection round.

THESIS: Distinguish firsthand accounts, biography, fiction and film adaptation using only the four examples already named in class. Students find additional examples.

OWN-WORLD: Inherit the Equiano course page’s white reading surface, blue underlined links, dark ink, sans-serif typography and thin horizontal rules. No decorative panels, oversized header or forced heading breaks.

STORY: Direct film-clip access; four works already named in class; the user’s discussion of historical and present forms of slavery, with sourced distinctions.

FIRST VIEWPORT: Compact title, direct course/film links, and the beginning of the named works. Reading content is visible without scrolling past a decorative opening.

FORM: Precisely scoped course-resource extension; no concept roll under new-work’s narrow-request exception. Rows and responsive columns separate titles and factual descriptions. All content remains available without JavaScript.

Truth boundaries: The collection is selected, not comprehensive. Preserve the single user-supplied question. Distinguish adaptation from primary testimony, fictional Django from a historical individual, African settings from Equiano’s particular account, and legal definitions from broad modern terminology. No new assignments, deadlines, or student submission requirements.

## Implemented values · October 28, 2026

- Static source: `frst-110-resources/narratives-of-slavery.html`; scoped styles: `frst-110-resources/narratives-of-slavery-assets/page.css`. No JavaScript or motion.
- Self-hosted Source Sans 3 variable roman and italic fonts (`_kit/fonts/SourceSans3VF-Upright.woff2` and `SourceSans3VF-Italic.woff2`), with Helvetica Neue, Arial, and sans-serif fallbacks. Body is 18px/1.5, becoming 17px on phones. The title is 38px/1.15 at weight 650, becoming 33px. Headings wrap naturally.
- White paper (`#fff`), dark ink (`#202f35`), muted gray (`#4a5c64`), blue underlined links (`#245a8d`), and thin gray rules (`#cbd3d5`). Focus outlines use `#0b63ce`. No shadows, decorative panels, or rounded cards.
- The container is 1260px wide at most, with 28px horizontal padding. Each starting work has three desktop columns: title/metadata, setting/story, and relation to evidence. At 900px and below, the title occupies the first of two columns and the two descriptions share the second. At 620px and below, entries stack with 16px page gutters.
- Definitions use two columns, becoming one at 620px.
- Source links beside entries and `narratives-of-slavery-assets/sources.json` retain provenance.
- Course and section navigation have 48px minimum-height links, with 44px section links on phones. A skip link, semantic headings, underlined source links, and visible keyboard focus support navigation. Print styles retain the reading text and omit navigation and footer.

## Verification

Fresh independent reviewer verdict: **ship**, with no fixes requested (October 28, 2026). Reviewed evidence covers desktop, mobile, natural heading wrapping, sans-serif rendering, links/anchors, and privacy. Screenshots: `.impeccable/review/narratives-of-slavery/desktop.png`, `mobile.png`, and `user-374.png`. The page retains only the user-supplied discussion question. This record documents the verified local implementation; publication status belongs in the deployment handoff.

## October 28 correction
Removed the five assistant-supplied additional examples and their associated reading-section portrait. The four class-named works remain. Students will find further examples; do not fill in their work. Earlier screenshots record the superseded version.

## Videos directly on the page · October 28
The existing Equiano film section now precedes the four starting works. Three YouTube privacy-enhanced players are 16:9, lazy-loaded and titled; two age-restricted ship excerpts retain thumbnail/direct links and explicit YouTube sign-in notices. Two columns become one below900px. Videos are hidden in print while their links and context remain. No additional narrative works or questions.
