---
version: 1
slug: "blood-dazzler-oct7"
primary_target: "frst-110-resources/blood-dazzler-oct-7.html"
related_targets: ["_kit/blood-dazzler-oct7.css", "scripts/build-blood-dazzler-oct7.py", "scripts/check-blood-dazzler-oct7.py"]
name: "Blood Dazzler · October 7 · FRST 110"
description: "October 7 reading page with three native videos and the pp. 25–49 frequency cloud."
colors:
  paper: "#f7f6f2"
  ink: "#202f35"
  muted: "#4a5c64"
  blue: "#245a8d"
  rule: "#cbd3d5"
  focus: "#0765ca"
  nav-slate: "#1e2a35"
  nav-text: "#ffffff"
  nav-crumb: "#dbe6ec"
  cloud-fill: "#dbe9f1"
  cloud-stroke: "#7393a4"
typography:
  display:
    fontFamily: "'Source Sans 3', sans-serif"
    fontSize: "40px"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-.02em"
  display-phone:
    fontFamily: "'Source Sans 3', sans-serif"
    fontSize: "34px"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-.02em"
  headline:
    fontFamily: "'Source Sans 3', sans-serif"
    fontSize: "26px"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "'Source Sans 3', sans-serif"
    fontSize: "20px"
    fontWeight: 400
    lineHeight: 1.5
  body-phone:
    fontFamily: "'Source Sans 3', sans-serif"
    fontSize: "19px"
    fontWeight: 400
    lineHeight: 1.5
  caption:
    fontFamily: "'Source Sans 3', sans-serif"
    fontSize: "17px"
    lineHeight: 1.4
  caption-phone:
    fontFamily: "'Source Sans 3', sans-serif"
    fontSize: "16px"
    lineHeight: 1.4
spacing:
  gutter: "24px"
  gutter-phone: "16px"
  clip-gap: "28px"
  section: "45px"
components:
  course-navigation:
    backgroundColor: "{colors.nav-slate}"
    textColor: "{colors.nav-text}"
    padding: "6px 24px"
  native-player:
    backgroundColor: "{colors.nav-slate}"
    width: "100%"
  disclosure:
    textColor: "{colors.ink}"
    padding: "11px 0"
---

# Design System: Blood Dazzler · Wednesday, October 7

## October 7 correction: remove the duplicate player

At the user's request, the current page has three videos in this order: federal response in When the Levees Broke (4:18), Barbara Bush at the Astrodome (19 seconds), and evacuation testimony (2:12). The separate 18-second Brownie player and its jump link were removed because the federal-response excerpt already contains that footage. The film's own sequence and three repetitions remain untouched. All media assets and source ledgers remain saved; the exact canonical cloud is unchanged.

All three sections now use the existing 960px wide-player treatment, stacked vertically on desktop and phones. Barbara no longer sits in an empty two-column wrapper or reserves 90px for alignment with the removed player. No CSS, palette, type, narration, or video edit changed. Four jump links remain: Federal response, Barbara Bush, Evacuation clip, and Word cloud. The existing Teaching HQ route reaches the same public page.

The October 7 removal is checked through the deterministic builder, scoped checker, media-hash preservation, and desktop/phone inspection. Current captures are `.impeccable/review/no-repeat/desktop.png` and `mobile.png`. Earlier playback and listening limits still apply; unchanged media were not re-edited or independently auditioned. The records below describe the historical October 6 four-player page and do not establish current player counts or geometry.

# Historical design and verification record — October 6

## Overview

Mode: **Read**. This record applies only to `frst-110-resources/blood-dazzler-oct-7.html`. The existing October 5 Blood Dazzler reading page is the fixed visual authority. The built October 7 page preserves its warm paper, slate ink, self-hosted Source Sans 3, blue links, compact dark FRST navigation, and direct section links.

The title names the work. Author, Wednesday October 7, 2026, and pp. 25–49 follow it. The longer federal-response passage appears first, followed by the Barbara Bush and Brownie pair, the separate evacuation excerpt, and the canonical section cloud. Documentary posters, clear captions, dates, sources, and direct media links carry the content. No new identity, slogan, task, or character analysis was added.

**Evidence:** primary HTML, `_kit/blood-dazzler-oct7.css`, inherited `_kit/blood-dazzler-1.css` and `_kit/blood-dazzler-words.css`, and `.impeccable/review/longer/desktop.png` (1265 × 4053) and `.impeccable/review/longer/mobile.png` (375 × 4061). Both current captures show the complete four-player page through the footer. This record follows built code and those captures, not a proposed concept.

**Review:** `.impeccable/review/longer/finish-review.json` returned `ship` with no material fixes. A fresh general subagent used the finish-reviewer workflow because the shipped role was unavailable. That verdict applies to the LOCAL artifact; LIVE deployment and Teaching HQ linking were not checked by this review. A general documenter reconciled this scoped record because the shipped documenter role was unavailable. The shared `DESIGN.md`, global `.impeccable/design.json`, `PRODUCT.md`, and configuration are outside this record; their stale metadata was not repaired.

## Colors

Paper supports the reading field; ink carries titles and prose; muted ink carries metadata and credits. Blue marks links. The dark navigation has white links and a lighter breadcrumb. Thin rules divide section navigation, disclosures, and the footer. The frequency circles use the existing pale blue fill and blue-gray stroke. These tokens describe this Blood Dazzler surface only.

## Typography

Source Sans 3 loads locally from `_kit/fonts/SourceSans3VF-Upright.woff2`, with sans-serif fallback. The frontmatter records the desktop and phone heading, body, and caption roles. Section headings retain one size across those captures. Weight, spacing, and explicit headings establish hierarchy; no second display family is introduced.

Section links use semibold type (18px desktop, 17px phone) and a minimum height of 44px. Phone metadata is 18px. Native disclosure summaries are 16px. Cloud words use weight 800 and counts weight 700 with tabular numerals. The verified smallest cloud word is 20.012 screen pixels; the underlying SVG font sizes vary to fit their circles.

## Layout

Main content centers within a 1460px maximum width. Desktop padding is 22px at the top and 55px at the bottom, with the gutter token at each side. At 600px and below, padding becomes 19px at the top and 35px at the bottom, with the phone gutter. Navigation and section links wrap.

The longer federal-response section uses the existing wide-player treatment at a 960px maximum width. The two official remarks follow in equal columns with the clip-gap token. Introductory paragraphs reserve 90px on desktop to align the paired players. At 800px and below, the columns stack and that reserved height is removed. The evacuation section remains separate below them and also has a 960px maximum width. Videos preserve a 16:9 frame with `object-fit: contain`; outside-player captions stay directly beneath each player.

The cloud region fills the available content width. Its SVG has a 999px minimum width and a square viewBox of `0 0 867.651609 867.651609`. The region scrolls horizontally while the page remains within the phone width. Current `.impeccable/review/longer/mobile-geometry.json` records body client and scroll widths both 375px, player width 343px, 19px body text, 26px section headings, cloud client width 343px and scroll width 999px, four players, and 50 words. The count list uses four columns, becoming two at 600px and below.

## Elevation & Depth

The surface adds no shadows. Paper, the dark navigation, documentary frames, and thin horizontal rules provide grouping. There is no decorative depth or motion. Inherited smooth section scrolling becomes automatic scrolling when the browser requests reduced motion.

## Shapes

Navigation, video frames, and ruled disclosures are rectangular without decorative rounded containers. Circles belong to the frequency chart because their areas encode counts. They do not introduce a new card or control shape for other pages.

## Components

### Navigation and section links

The compact dark course navigation links to FRST 110 course materials and October 5. Five section links follow the date and reading scope: Federal response, Barbara Bush, Brownie clip, Evacuation clip, and Word cloud. The skip link becomes visible on focus. Links, summaries, and the focusable cloud region retain a blue 3px keyboard outline; video focus has a 4px offset. Ordinary source links remain underlined, with thicker underlines on hover.

### Native video players

All four players have local posters, native `controls`, `playsinline`, `preload="none"`, accessible labels, and descriptions attached to their outside-player captions. Each has an Open video link and an attributed source. No player autoplays. Original framing is preserved.

**The Native Player Rule.** Keep browser controls and direct-file access with each video.

The federal-response container is 258.066667 seconds, displayed as 4 minutes 18 seconds, from a continuous 258.05-second source selection. Its source link preserves the supplied `t=4864` passage; the copy attributes judgments to interviewees. Barbara Bush is 19 seconds, including the closing book reference. The page identifies original audio with illustrative Astrodome photographs and captions and connects it to “Thankful,” pp. 48–49. Brownie is 17.8 seconds, displayed as 18 seconds. Its caption attributes the three repetitions to Spike Lee’s documentary; the classroom edit adds no repetition. The official September 2 transcript and supplied CNN record remain linked. The evacuation container is 131.666667 seconds, displayed as 2 minutes 12 seconds; it is a separate continuous excerpt with residents’ claims attributed to them.

Prior `.impeccable/review/oct7/playback.json` records the original three players at readyState 4, correct durations, no media errors, and advanced playback positions after play/pause checks. The new first player was checked separately: `.impeccable/review/longer/playback.json` records duration 258.066667, readyState 4, currentTime 55.983497, and paused true after playback. No media error was observed in that check. This does not claim that all four players were newly played. Independent listening remains unverified. Paused native controls cover part of Barbara Bush’s burned-in caption in the current screenshots. The outside-player caption remains clear; this record does not claim unobstructed subtitles throughout playback.

### Canonical frequency cloud

The inline circle chart reuses `frst-110-resources/blood-dazzler-assets/frequency-25-49.json` and the deterministic renderer. All 50 canonical word/count pairs are exact: 17 poems, 3148 tokens, with common words excluded. Circle area encodes frequency; the visible number gives the count. Scope, source links, and the existing method text remain available.

**The Count Preservation Rule.** Preserve every canonical word/count pair and the count and method disclosures when changing layout.

The region is keyboard focusable and labeled for horizontal scrolling. Narrow screens show “Scroll sideways to read every circle.” Keyboard scrolling and the full count-list alternative were verified. Native Read all word counts and Counting method disclosures retain 44px summary targets. They require no page script.

### Sources and build maintenance

Video provenance and excerpt details are in `frst-110-resources/blood-dazzler-assets/oct7/SOURCES.md`; broader word-count provenance is in `frst-110-resources/blood-dazzler-assets/SOURCES.md`. The footer keeps both records and course materials accessible. No private class plan, student information, full book text, or page scan appears on this surface.

Maintain the generated page through `scripts/build-blood-dazzler-oct7.py`, the scoped stylesheet, and canonical data. `scripts/check-blood-dazzler-oct7.py` checks date, reading boundaries, counts, identifiers, local media, local links, and sources. The mechanical detector ran once for this addition; `.impeccable/review/longer/detector.json` retains its results. Its inferred unused text/background pairs and native-video padding warnings are not actual defects in the inspected page. Shared-token advisories concern metadata outside this scoped record. The fresh review found no material fixes, and the detector was not rerun.

## Do's and Don'ts

### Do

- Do preserve the existing Blood Dazzler palette and local Source Sans 3 typography.
- Do keep official remarks together on desktop and stacked on phones, with evacuation testimony separate below.
- Do keep the cloud words at least 20 screen pixels and confine sideways scrolling to the cloud region.
- Do keep source dates, credits, direct media links, canonical counts, and native disclosures visible or available.

### Don't

- Don't add a hero, slogan, new identity, task, or character analysis to this requested resource page.
- Don't substitute a remote embed for the verified local native players or add autoplay.
- Don't describe the Brownie repetitions as repeated statements at the original event.
- Don't turn this surface record into a replacement for the shared design system.
- Don't treat unverified listening or obscured paused subtitles as verified quality guarantees.


## October 6 addition: longer federal-response passage

The user supplied https://youtu.be/CTVy-JC-Lag?t=4864 and selected the onward passage. A fourth native player appears first under “Federal response in When the Levees Broke,” followed by the existing Barbara/Brownie pair, evacuation excerpt, and unchanged canonical cloud. The additional section inherits the same wide evacuation-player style; no stylesheet or global identity changes. Its source and direct MP4 links, accessible label/caption, poster, native controls, inline playback and preload none match the established players. The copy attributes viewpoints to interviewees and connects the passage to verified poem locators. Duration: 4 minutes 18 seconds.

The new continuous source-local selection is 4.800–262.850 seconds. It retains the full opening interview sentence and final journalist sentence, ending before the next appointment-topic voice. Tesseract’s native filmstrip shows the original opening transition, the praise, flyover, historical comparison, Brown news interview and closing journalist; no graphics or repeated footage were added. Fine source waveforms and local ASR checked the two speech edges. The new render has 7742 frames at 1280 × 720 and 30 fps, duration 258.066667 seconds, and audio retained at unity gain (1.0). The native and web AAC audio bytes are identical. Independent listening remains unverified. Updated browser proof and delivery receipt are retained in the private levees-federal-response-2026-10-06 project. The current four-player review is `.impeccable/review/longer/finish-review.json`; the earlier three-player playback proof remains historical evidence.
