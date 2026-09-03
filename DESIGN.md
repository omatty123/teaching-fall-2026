---
name: Fall 2026 Teaching Sites
description: Editorial seminar pages built from dark course rails, warm paper, literary display type, and documentary course portraits.
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
    fontFamily: '"Newsreader", Georgia, serif'
    fontSize: "clamp(2.4rem, 6.5vw, 5.7rem)"
    fontWeight: 400
    lineHeight: 0.94
    letterSpacing: "-0.035em"
  headline:
    fontFamily: '"Newsreader", Georgia, serif'
    fontSize: "clamp(2.35rem, 5.6vw, 5.3rem)"
    fontWeight: 400
    lineHeight: 0.96
    letterSpacing: "-0.035em"
  title:
    fontFamily: '"Outfit", "Source Sans 3", sans-serif'
    fontSize: "clamp(1.45rem, 2.35vw, 2.05rem)"
    fontWeight: 600
    lineHeight: 1.12
    letterSpacing: "-0.025em"
  body:
    fontFamily: '"Outfit", "Source Sans 3", sans-serif'
    fontSize: "1rem"
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

**Creative North Star: “The Seminar Screen”**

The site is an editorial threshold into class rather than a miniature learning-management system. Its closest authority is the pinned *Modern Korea through Literature and Film* dashboard and student directory: a thin black utility rail, a deep slate title field, literary serif headlines, warm paper, and documentary images large enough to establish the intellectual world before administrative details appear.

The student-facing index uses course portraits, not dashboard cards. Each course home begins with the live question, then moves into image, preparation, tools, schedule, and record. Serif is deliberately rare: it appears only in the leading editorial statement or current question, while course names, navigation, sections, and working text remain sans-serif.

**Key Characteristics:**

- Questions and images lead; administration follows.
- Newsreader carries only leading editorial statements and intellectual prompts; Outfit carries course names, navigation, sections, and working text.
- Dark chrome is thin and functional; slate fields are reserved for major orientation.
- Documentary images retain visible credits and meaningful crops.
- Public pages never expose roster data, student names, or portraits.

## Colors

Charcoal and slate establish the seminar environment; warm off-white paper and white reading surfaces keep long pages calm. Gold marks course-level navigation, while blue, rust, and moss identify the three courses without flooding shared surfaces.

**The Gold Signal Rule.** Gold belongs to small navigational and identity signals, never large fills or long text.

**The Legible Ink Rule.** Supporting text uses dark gray (`ink-soft`), not low-contrast pale gray.

## Typography

**Display Font:** Newsreader, with Georgia and serif fallbacks  
**Body Font:** Outfit, with Source Sans 3 and sans-serif fallbacks

Newsreader gives questions and course titles a humane, literary cadence. Outfit keeps schedules, labels, controls, and practical directions compact and unambiguous.

- **Display:** Student-index promise; two or three balanced lines at most.
- **Headline:** Current course question in the slate field.
- **Title:** Course portraits and principal section names.
- **Body:** Explanatory copy, generally held to 62–72 characters per line.
- **Label:** Small uppercase course codes and utility context; use sparingly.

**The Two-Voice Rule.** Serif type is reserved for one governing idea or question per page; sans-serif type carries everything operational and all secondary headings.

## Layout

Shared content centers at 1200–1248px with a fluid gutter. The student index uses three tall image-led course portraits on desktop, two plus one spanning portrait on tablet, and one continuous column on phones. Course pages move from a full-width slate question field to an asymmetric main resource and compact “coming next” rail, then to tools and the schedule record.

Responsive layouts reflow instead of shrinking. Mobile retains the question and image as the first two strong impressions, keeps practical targets at least 44px where repeated actions require it, and moves supporting rails below the main content.

## Elevation & Depth

The system is mostly tonal. Course portraits and the main session resource receive one soft, low-opacity shadow to separate white paper from the warm ground; navigation, schedules, and facts use borders and color fields instead. No hard offset shadows or decorative glow.

## Shapes

The page field and title bands remain square and architectural. Small utility controls use 4px corners. Image-led course portraits and major white resource panels use an 8px radius, reflecting the Korean reference without turning every section into a card.

## Components

### Utility rail

A 52px charcoal bar holds the course or term identity in small gold type and a few restrained outlined destinations. It remains sticky where course navigation benefits from persistence.

### Editorial title field

A deep slate field presents the page’s governing question or promise in large Newsreader type. Supporting information is short, high contrast, and subordinate.

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
- Use generous space around major serif titles and tighter rhythm inside practical groups.
- Keep public/private boundaries absolute.
- Preserve strong contrast and obvious keyboard focus.

### Don't

- Revert to equal dashboard tiles, metric panels, or a generic LMS inventory.
- Add decorative icons, fake texture, or imagery unrelated to the course material.
- Use pale gray for required reading text.
- Put serif type on buttons, schedules, or dense operational metadata.
- Let the private roster visual language justify publishing roster content.
