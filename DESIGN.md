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
