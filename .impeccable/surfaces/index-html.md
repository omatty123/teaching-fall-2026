---
version: 1
slug: "index-html"
primary_target: "index.html"
related_targets: ["students.html","courses/frst-110.html","courses/hist-212.html","courses/buen-594.html"]
---

# Fall 2026 teaching surfaces

- **Scope and modes:** `index.html`, `students.html`, and the three primary `courses/*.html` pages are public Read/Operate surfaces; `.private-build/index.html` remains the private instructor launchpad.
- **Audience and job:** Students need to recognize their course, see its current question and next meeting, then reach Canvas, syllabus, and the schedule without navigating an LMS-style dashboard.
- **Chosen direction:** Seminar Screen — a direct code-led adaptation of the user-pinned Modern Korea dashboard and student directory, using charcoal utility rails, slate editorial fields, warm paper, Newsreader display type, Outfit controls, ochre signals, and large documentary course portraits.
- **Memorable moment:** the student index opens with a dark literary title field and then three tall course portraits whose images dominate the first viewport; each course home carries the same rail and question-first title field.
- **Constraints:** static generated HTML; preserve verified data and links; never publish roster data, student names, or portraits; maintain visible source credits, WCAG 2.2 AA contrast, clear focus, desktop/tablet/mobile reflow, and meaningful course imagery.
- **User-pinned references:** `https://omatty123.github.io/Modern-Korea-through-Lit-and-Film/dashboard.html` and `https://omatty123.github.io/Modern-Korea-through-Lit-and-Film/students.html` are the visual authority. No comp round was needed because the exact live reference was supplied.
- **Unresolved decisions:** none for this redesign.

## Implementation inventory

| Ingredient | Commitment | Medium |
|---|---|---|
| Utility rail | 52px charcoal bar, gold term/course identity, restrained outlined destinations | Generated HTML/CSS |
| Editorial field | Deep slate environment with large Newsreader question or student-facing promise | Generated HTML/CSS |
| Student course portraits | Three image-dominant white surfaces, 8px corners, soft lift, visible credits, course title and direct actions | Generated HTML/data imagery |
| Course first viewport | Current question, date and meeting context followed by documentary image, preparation copy, and coming meetings | Generated HTML/CSS |
| Typography | Newsreader for ideas and questions; Outfit for actions, schedules, metadata, and body copy | Google Fonts with resilient local fallbacks |
| Palette | Warm paper `#f4f3f0`, charcoal `#1a1a1a`, slate `#1e2a35`/`#2c3e50`, ochre `#a67c00`, dark supporting ink | CSS tokens |
| Responsive behavior | Three portraits desktop, two-plus-one tablet, one column phone; course side rail moves below main resource | CSS media queries |
| Privacy boundary | Public pages contain course data only; roster destinations remain private and appear only on the instructor HQ | Generator logic/data links |
