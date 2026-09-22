---
name: Fall 2026 Teaching Sites
description: Compact teaching pages built from a dark daily-prep header, image-and-color course cards, Inter typography, and direct next-class actions.
colors:
  paper: "#f4f3f0"
  paper-deep: "#e9e6df"
  surface: "#ffffff"
  ink: "#1a1a1a"
  ink-soft: "#575757"
  rule: "#d7d3cb"
  rule-dark: "#aaa59c"
  slate: "#1e2a35"
  slate-light: "#2c3e50"
  signal-gold: "#a67c00"
  focus-blue: "#0b63ce"
  course-frst-blue: "#245a8d"
  course-hist-rust: "#7a3030"
  course-buen-moss: "#2d5a50"
typography:
  display:
    fontFamily: '"Inter", -apple-system, sans-serif'
    fontSize: "28px"
    fontWeight: 300
    lineHeight: 1.2
    letterSpacing: "0.5px"
  headline:
    fontFamily: '"Inter", -apple-system, sans-serif'
    fontSize: "17px"
    fontWeight: 500
    lineHeight: 1.3
  title:
    fontFamily: '"Inter", -apple-system, sans-serif'
    fontSize: "14px"
    fontWeight: 500
    lineHeight: 1.3
  body:
    fontFamily: '"Inter", -apple-system, sans-serif'
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: '"Outfit", "Source Sans 3", sans-serif'
    fontSize: "0.7rem"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.16em"
rounded:
  control: "4px"
  portrait: "8px"
  point: "50%"
spacing:
  gutter: "clamp(18px, 4vw, 64px)"
  gutter-mobile: "16px"
  section: "clamp(1.5rem, 3vw, 2.5rem)"
components:
  utility-control:
    backgroundColor: "transparent"
    textColor: "#bbbbbb"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "4px 10px"
    height: "30px"
  course-portrait:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.portrait}"
---

# Design System: Fall 2026 Teaching Sites

## Overview

**Creative North Star: “Today’s Prep Cards”**

The preserved Spring 2026 Teaching Today page is the literal template authority. The system uses its compact centered dark header, cool gray page field, three image-and-color course cards, small outlined buttons, direct next-class status, and dense Inter typography.

The instructor HQ and student index share the same card skeleton. Course data, links, and privacy boundaries change by audience; geometry and typographic scale do not. Individual course pages may expand the card language into schedules and records but should remain compact and sans-serif-led.

**Key Characteristics:**

- Questions and images lead; administration follows.
- Inter carries every layer; size, weight, course color, and grouping create hierarchy.
- Dark chrome is thin and functional; slate fields are reserved for major orientation.
- Documentary images retain visible credits and meaningful crops.
- Public pages never expose roster data, student names, or portraits.

## Colors

Charcoal and slate establish the seminar environment; warm off-white paper and white reading surfaces keep long pages calm. Gold marks course-level navigation, while blue, rust, and moss identify the three courses without flooding shared surfaces.

**The Gold Signal Rule.** Gold belongs to small navigational and identity signals, never large fills or long text.

**The Legible Ink Rule.** Supporting text uses dark gray (`ink-soft`), not low-contrast pale gray.

## Typography

**Display Font:** Inter, with the system sans-serif stack  
**Body Font:** Inter, with the system sans-serif stack

Inter keeps the entire system compact, familiar, and quick to scan. Do not introduce serif display type into this template.

- **Display:** Student-index promise; two or three balanced lines at most.
- **Headline:** Current course question in the slate field.
- **Title:** Course portraits and principal section names.
- **Body:** Explanatory copy, generally held to 62–72 characters per line.
- **Label:** Small uppercase course codes and utility context; use sparingly.

**The One-Family Rule.** Inter carries the whole interface; hierarchy comes from a restrained 9–28px scale, weight, spacing, and course-color bands.

## Layout

Shared content centers at 1400px with 24px page padding and 20px gaps. Course cards use a 112px image strip, a compact colored identity/action band, and a white next-session body. Three columns become two and then one at 980px and 720px.

Responsive layouts reflow instead of shrinking. Mobile retains the question and image as the first two strong impressions, keeps practical targets at least 44px where repeated actions require it, and moves supporting rails below the main content.

## Elevation & Depth

Cards use the original restrained `0 2px 12px rgba(0,0,0,.08)` shadow on the cool gray ground. Internal hierarchy comes from course-color bands and light gray dividers.

## Shapes

Course cards use 12px corners, supporting panels 8–10px, and small action buttons 6px. The geometry is soft but compact, never pill-shaped.

## Components

### Utility rail

A 52px charcoal bar holds the course or term identity in small gold type and a few restrained outlined destinations. It remains sticky where course navigation benefits from persistence.

### Editorial title field

A deep slate field presents the page’s governing question or promise in compact, medium-weight Inter. Supporting information is short, high contrast, and subordinate.

### Course portrait

The image occupies most of the component and keeps its credit attached along its lower edge. Beneath it, title, course code, meeting pattern, next meeting, and direct destinations form a quiet white caption structure.

### Course resource panel

The principal documentary image and preparation text share a white bounded surface. A compact next-meeting rail sits alongside on wide screens and drops below on narrow ones.

### Schedules and records

Use ruled rows, not nested cards. Dates align in a stable first column, details read in the second, and the complete schedule stays progressively disclosed.

## Do's and Don'ts

### Do

- Lead each student page with a real course question, work, or documentary image.
- Keep source credits visible and readable.
- Give major sans-serif titles enough space to lead while keeping practical groups tight.
- Keep public/private boundaries absolute.
- Preserve strong contrast and obvious keyboard focus.

### Don't

- Revert to equal dashboard tiles, metric panels, or a generic LMS inventory.
- Add decorative icons, fake texture, or imagery unrelated to the course material.
- Use pale gray for required reading text.
- Put serif type on buttons, schedules, or dense operational metadata.
- Let the private roster visual language justify publishing roster content.

## September 13 Egan reading guide addendum

This addendum records the implemented Egan chapters 1–2 guide only. It preserves the shared teaching-site identity and records the guide’s current values where the global template description above differs. Sources are `features/egan-reading-guide.fragment`, `_kit/egan-reading-guide.css`, `_kit/egan-reading-guide.js`, and the desktop/mobile evidence in `.impeccable/review/egan-guide/`.

### Colors

The guide uses light paper (`#faf9f5`), slate text (`#1e2a35`), FRST blue links and roles (`#245a8d`), supporting text (`#55636d`), and quiet rules (`#d9dfdf`). White fish plates retain the source illustrations. The science grouping uses a pale slate field (`#eef2f3`). Map water uses pale blue (`#d4e3e8`); rust (`#a95031`) identifies the selected location, canal detail, and focus outline.

### Typography

Browser-computed body and h1 both inherit `Outfit, "Source Sans 3", sans-serif` from course CSS. The global Inter-only description is stale for this surface; do not change the guide’s inherited family to match it. The guide body is 16px with 1.6 line height; most descriptive entries are 14px. The h1 uses `clamp(32px, 4.3vw, 52px)`, weight 750, line height 1.1, and tracking `-.035em`, with a 37px mobile size. Section headings are 30px, becoming 27px on mobile. Names precede their 12px blue role lines. Course/date metadata follows the reading title. Actual section titles and the Hall of Fame use h2 elements. The map keeps its embedded system-sans labels.

### Layout

The guide centers within 1180px and uses 40px horizontal padding, reducing to 24px at 900px and 18px at 650px. Three equal fish plates enable side-by-side identification on desktop and stack on phones. Human portraits accompany names and short prose; unpictured witnesses occupy a ruled row. The science group contains two illustrated entries and a shared team credit. Settings pair a regional locator with a numbered list and Niagara inset. Six philosophical comparisons use two columns, becoming one on mobile; emotional effects use ruled rows.

### Elevation & Depth

The guide introduces no shadows. Paper, white illustration fields, pale science/map fields, and thin borders provide grouping.

### Shapes

Fish plates have square corners. Portraits and map frames use 3px corners; the science field uses 4px corners. Numbered map markers and list badges are circular.

### Components

Section navigation and disclosure summaries have a 44px minimum height. Links, buttons, summaries, and the focusable map expose visible focus outlines. Setting buttons update `aria-pressed` and the matching marker state. On narrow screens the map scrolls horizontally within its frame; visible swipe guidance explains this. Selecting a setting brings its marker into the available view and scrolls the map into view, respecting reduced-motion preference. The Erie Canal choice highlights both endpoints; its initial horizontal positioning follows Buffalo. Full setting descriptions remain available without JavaScript.

Use the classroom handout’s OpenStreetMap lake contours and the class map game’s Niagara/Welland geometry. The north-up regional map uses an equirectangular projection at 45°N and a labeled approximate scale. The inset shows modern waterways; its caption explicitly distinguishes them from historical canal alignments. Keep the existing attribution, approximate-location notes, and undisplayed Erie Canal route boundary.

### Do's and Don'ts

- Preserve identification cues, Latin names, and the notice that fish images are not at the same scale.
- Retain seven sourced raster assets and their ledger at `images/frst/egan-guide/SOURCES.md`; keep source credits available from the page.
- State when a human portrait is unverified; do not substitute an invented likeness.
- Keep philosophical pairings explicitly interpretive and emotional moves tied to the writing.
- Keep these surface-specific values scoped to the Egan guide; this addendum does not replace the shared template.

## HIST 212 materials page · September 22, 2026

`courses/hist-212.html` now prioritizes opening materials. Its `materialsHome`
data in `data/hist-212.json` supplies grouped reading/source and practice links,
with course systems alongside on desktop and below on phones. Jump links remain
near the title. The former repeated question, generic preparation prose, cropped
map banner, duplicate upcoming meetings, and registrar panel are removed from
this route. The complete schedule has one native disclosure; meeting time and
place remain beneath the course name. Other course pages retain their layout.

Scoped styling lives in `_kit/materials-home.css`: Inter, a warm paper field,
rust links, a dark compact navigation bar, ruled resource rows, and a white
course-links column. Body text is 14–16px, resource titles 16–17px, section titles
18–19px, and the course heading 24–32px. No animation is needed for this index.
Detector exceptions: the established Inter face is intentional; the side-stripe
warnings refer to unused shared HQ selectors, not elements on this route. The
old design sidecar is stale and was not regenerated as part of this change.
