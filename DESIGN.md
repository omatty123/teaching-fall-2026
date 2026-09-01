---
name: Fall 2026 Teaching HQ
description: An evidence-aware academic field desk built from warm paper, deep ink, fine rules, and documentary course signals.
colors:
  hq-paper: "#f3efe5"
  hq-paper-deep: "#e8e1d2"
  hq-ink: "#14263a"
  hq-ink-soft: "#526174"
  hq-rule: "#aeb5b4"
  hq-rule-dark: "#74808a"
  hq-rust: "#91462f"
  hq-moss: "#3f6653"
  hq-ochre: "#765c21"
  hq-white: "#fffdf7"
  focus-blue: "#0b63ce"
  course-frst-blue: "#245a8d"
  course-hist-rust: "#7a3030"
  course-buen-moss: "#2d5a50"
  atlas-bg: "oklch(1 0 0)"
  atlas-course-blue: "oklch(0.48 0.15 260)"
  atlas-course-ink: "oklch(0.29 0.09 260)"
  atlas-course-soft: "oklch(0.94 0.035 260)"
  atlas-ink: "oklch(0.2 0.025 28)"
  atlas-faint: "oklch(0.62 0.018 28)"
  atlas-line: "oklch(0.88 0.008 28)"
  atlas-line-strong: "oklch(0.76 0.012 28)"
  atlas-muted: "oklch(0.46 0.025 28)"
  atlas-surface: "oklch(0.975 0.003 28)"
  atlas-surface-strong: "oklch(0.946 0.006 28)"
  atlas-water-blue: "oklch(0.5 0.14 244)"
  atlas-water-ice: "oklch(0.955 0.026 227)"
  atlas-water-night: "oklch(0.22 0.055 248)"
  atlas-water-paper: "oklch(0.955 0.035 78)"
  atlas-water-rust: "oklch(0.52 0.17 32)"
typography:
  display:
    fontFamily: "\"Source Sans 3\", \"Segoe UI\", sans-serif"
    fontSize: "clamp(2.25rem, 5vw, 5.4rem)"
    fontWeight: 520
    lineHeight: 0.93
    letterSpacing: "-0.06em"
  headline:
    fontFamily: "\"Source Sans 3\", \"Segoe UI\", sans-serif"
    fontSize: "clamp(1.65rem, 3.4vw, 3.2rem)"
    fontWeight: 550
    lineHeight: 1.02
    letterSpacing: "-0.045em"
  title:
    fontFamily: "\"Source Sans 3\", \"Segoe UI\", sans-serif"
    fontSize: "clamp(1.2rem, 2vw, 1.55rem)"
    fontWeight: 650
    lineHeight: 1.1
    letterSpacing: "-0.025em"
  body:
    fontFamily: "\"Source Sans 3\", \"Segoe UI\", sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "\"Source Sans 3\", \"Segoe UI\", sans-serif"
    fontSize: "0.68rem"
    fontWeight: 750
    lineHeight: 1.5
    letterSpacing: "0.12em"
  data:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI Variable\", \"Segoe UI\", \"Helvetica Neue\", \"Apple SD Gothic Neo\", \"Noto Sans KR\", \"Noto Sans\", Arial, sans-serif"
    fontSize: "0.64rem"
    fontWeight: 400
    lineHeight: 1.35
    letterSpacing: "normal"
rounded:
  square: "0"
  map-marker: "50%"
spacing:
  gutter: "clamp(18px, 4vw, 64px)"
  gutter-mobile: "16px"
  control-padding: "8px 12px"
  section-rhythm: "clamp(35px, 6vw, 68px)"
components:
  action-primary:
    backgroundColor: "{colors.hq-ink}"
    textColor: "{colors.hq-white}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "10px 16px"
    height: "46px"
  action-primary-hover:
    backgroundColor: "{colors.hq-rust}"
    textColor: "{colors.hq-white}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "10px 16px"
    height: "46px"
  action-outline:
    backgroundColor: "transparent"
    textColor: "{colors.hq-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "{spacing.control-padding}"
    height: "44px"
  filter-selected:
    backgroundColor: "{colors.hq-ink}"
    textColor: "{colors.hq-white}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "{spacing.control-padding}"
    height: "44px"
---

# Design System: Fall 2026 Teaching HQ

## Overview

**Creative North Star: "The Academic Field Desk"**

The system should feel like a well-used field notebook opened on an instructor's desk: warm paper, deep navy ink, precise rules, compact annotations, and evidence arranged for consequential reading. Its authority comes from hierarchy, provenance, and editorial judgment rather than from decorative polish.

The world is shared by the instructor HQ, student course doorways, and the FRST course atlas. The atlas may widen the vocabulary with water-specific OKLCH colors and immersive documentary sequences, but it retains the same sans-serif voice, rule-led structure, source credits, and flat material logic. Nothing should resemble a generic LMS dashboard or an AI-generated collection of glossy cards.

**Key Characteristics:**

- Warm paper and deep ink establish a quiet, authored working surface.
- Hairline and double rules organize comparison before boxes or cards do.
- Blue, rust, and moss course signals orient without becoming decoration.
- Documentary images remain connected to visible, readable source credits.
- Strong sans-serif hierarchy carries density without sacrificing legibility.
- Motion is minimal, purposeful, and suppressed when reduced motion is requested.

## Colors

The palette behaves like paper, ink, annotation, and course tabs. The HQ hex tokens in the frontmatter are normative for shared surfaces; the scoped atlas OKLCH tokens are normative inside the FRST water journey.

### Primary

- **Deep Navy Ink** (`hq-ink`): Primary text, major rules, dark actions, and the strongest information-bearing marks.
- **Warm Field Paper** (`hq-paper`): The continuous page ground; it should remain visually present between sections.

### Secondary

- **FRST Water Blue** (`course-frst-blue`): FRST identity, schedule blocks, and course-specific link states.
- **HIST Archive Rust** (`course-hist-rust`): HIST identity and timetable orientation.
- **BUEN Workshop Moss** (`course-buen-moss`): BUEN identity and timetable orientation.

### Tertiary

- **Editorial Rust** (`hq-rust`): Risk, consequential emphasis, and the primary-action hover state.
- **Editorial Moss** (`hq-moss`): Confirmed change and constructive state signals.
- **Ledger Ochre** (`hq-ochre`): Tentative schedule notes and restrained caution.

### Neutral

- **Porcelain Paper** (`hq-white`): A small amount of surface lift for controls and schedule blocks.
- **Deepened Paper** (`hq-paper-deep`): Scrollbar tracks and subtle paper differentiation.
- **Soft Ink** (`hq-ink-soft`): Explanatory copy, captions, metadata, and supporting information.
- **Hairline Rule** (`hq-rule`) and **Dark Rule** (`hq-rule-dark`): The main structural separators.
- **Focus Blue** (`focus-blue`): Keyboard focus only; never repurpose it as general decoration.

### Atlas Extension

The FRST atlas uses the `atlas-*` tokens as a scoped documentary extension. Water blue, ice, night, paper, and rust distinguish concepts and environments while the near-black ink, faint metadata, and restrained line tokens preserve the Field Desk's editorial discipline.

**The Course Signal Rule.** A course color identifies ownership or state; it does not flood an entire shared surface.

**The Evidence Color Rule.** Color must clarify course, risk, change, or concept before it is allowed to decorate.

## Typography

**Display Font:** Source Sans 3 (with Segoe UI and sans-serif fallbacks)<br>
**Body Font:** Source Sans 3 (with Segoe UI and sans-serif fallbacks)<br>
**Label/Mono Font:** The system data stack recorded as `typography.data`

**Character:** One variable sans-serif family carries the shared world with a compact, humanist, editorial tone. Scale, weight, tracking, and rule placement create distinction; novelty typefaces do not.

### Hierarchy

- **Display** (`typography.display`): Course hero statements and rare atlas thesis moments; keep the line count short and the shape decisive.
- **Headline** (`typography.headline`): Current questions and section-defining statements.
- **Title** (`typography.title`): Section headings, dispatch titles, and compact content landmarks.
- **Body** (`typography.body`): Explanatory prose, with typical measures between 56ch and 78ch depending on context.
- **Label** (`typography.label`): Uppercase situation labels, course codes, context labels, and table annotations.
- **Data** (`typography.data`): ISBNs, times, and numeric facts that benefit from tabular alignment.

**The Hierarchy, Not Ornament Rule.** Use weight, scale, tracking, and position to create hierarchy; do not introduce a decorative display face to manufacture personality.

## Layout

The shared canvas is centered at a maximum width of 1440px with the fluid `gutter` spacing token. The spatial model is editorial: aligned columns for comparison, horizontal rows for destinations and schedules, and rules that continue across related information. Major sections breathe through `section-rhythm`, while internal content stays compact enough to support frequent scanning.

Responsive behavior is reflow, not shrinkage. Four-column ledgers become two columns and then one; course dispatch rows progressively move links and meeting information below identity; two-column course heroes and content/sidebar layouts become single columns. The principal shared breakpoints are 1040px, 980px, 760/720px, and 420/430px, with the mobile gutter fixed by `gutter-mobile`. Practical interactive targets remain at least 44px.

**The Rows Before Cards Rule.** When information is comparative or sequential, use aligned rows and continuous rules before introducing a bounded container.

## Elevation & Depth

The system is flat by default. Depth comes from paper tone, ink contrast, documentary image fields, borders, and occasional dark environmental sections in the atlas. The inset rust and moss marks on situation cells are status rules, not floating shadows. The only conventional lift is the quiet shadow on atlas book-cover imagery, where it helps the physical object read as an object.

**The Flat-by-Default Rule.** Surfaces rest on the page; shadows never substitute for hierarchy, grouping, or state.

## Shapes

The core form language is square and rectilinear. Buttons, filters, rows, disclosures, and content containers use straight edges and one- or two-pixel rules. Double rules may close major editorial divisions. Circles are reserved for inherently point-like atlas map markers; they are not a license for pill-shaped tags or rounded dashboard cards.

**The Square Surface Rule.** Keep shared controls and containers square; use a rounded silhouette only when the information itself is point-like or circular.

## Components

Components should read as parts of one document, not as a gallery of isolated widgets. Every interactive state must preserve visible focus and the 44px practical target floor.

### Buttons

- **Primary:** A square dark-ink action with light paper text and compact, confident type. Rust on hover marks consequence rather than spectacle.
- **Outline:** Transparent paper, a one-pixel ink or dark-rule border, and no radius. It belongs beside content, not above it as decoration.
- **Filters:** Rectangular toggles with a dark filled selected state and a quiet transparent unselected state; never render them as pills.
- **Focus:** A three-pixel blue outline with three-pixel offset remains visible against both paper and dark fills.

### Navigation

Navigation is text-led, underlined when it behaves like a destination, and arranged with enough gap to scan quickly. Masthead links and breadcrumb links use practical 44px heights. Sticky atlas navigation is a thin horizontal current with color change only.

### Cards / Containers

Generic cards are not a shared primitive. Course dispatches, workspace destinations, facts, schedules, and decision items are ruled rows. A bounded atlas container is appropriate only when it represents a distinct documentary object or conceptual environment, and it remains mostly square and shadowless.

### Situation Ledger

Ledger cells share a continuous grid and place the short uppercase state label above a stronger sentence and supporting detail. Risk and changed states receive an inset top rule in rust or moss; neutral cells do not gain extra decoration.

### Course Dispatch Row

A documentary image strip with visible credit leads into course identity, next-session information, and underlined destinations. The course color appears in the code and relevant hover/state marks, while the row itself stays on warm paper.

### Schedule Block

Schedule entries are compact paper blocks with a three-pixel course-colored top edge, dark type, and tabular time information. On narrow screens, the weekly grid becomes a readable day-by-day list.

### Atlas Markers and Reading Rows

Circular numbered markers are the atlas's one recurring rounded primitive and scale slightly on hover or focus. Reading rows pair a documentary cover with indexed metadata and a concise invitation; their small cover shadow is object-specific, not a general card treatment.

**The State-Only Motion Rule.** Movement may confirm hover, focus, disclosure, or checklist completion; it may not run as ambient decoration.

## Do's and Don'ts

### Do:

- **Do** preserve warm paper as the continuous ground and deep ink as the primary information color.
- **Do** use aligned rows, hairline rules, and double rules to expose comparison and hierarchy.
- **Do** keep documentary imagery factual, relevant, and accompanied by a visible credit.
- **Do** use course colors sparingly for identity, schedule orientation, and meaningful state.
- **Do** maintain visible keyboard focus, reduced-motion support, and at least 44px practical targets.
- **Do** let responsive layouts reflow into a clear reading order.

### Don't:

- **Don't** introduce glossy gradients, glass effects, ambient glows, or floating dashboard cards.
- **Don't** turn labels, filters, or metadata into pill clutter.
- **Don't** use oversized hero type where a compact situation or next action should lead.
- **Don't** add decorative icons, stock illustration, or uncited imagery to simulate personality.
- **Don't** animate for atmosphere; motion must communicate an interaction or state change.
- **Don't** make page-specific composition trivia into a global rule when the Field Desk principles already govern it.
