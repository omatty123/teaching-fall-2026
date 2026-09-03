---
version: 1
slug: "index-html"
primary_target: "index.html"
related_targets: ["students.html","courses/frst-110.html","courses/hist-212.html","courses/buen-594.html"]
---

# Fall 2026 teaching surfaces

- **Scope and modes:** `index.html`, `students.html`, and the three primary `courses/*.html` pages are public Read/Operate surfaces; `.private-build/index.html` remains the private instructor launchpad.
- **Audience and job:** Students need to recognize their course, see its current question and next meeting, then reach Canvas, syllabus, and the schedule without navigating an LMS-style dashboard.
- **Chosen direction:** Compact Teaching HQ — a direct reuse of the preserved Spring 2026 Teaching Today source: centered dark daily-prep header, cool gray field, three equal image-and-color course cards, compact bordered actions, and a white next-session body.
- **Memorable moment:** the full teaching term reads in one glance: date and purpose above three complete course cards, with image, identity, destinations, and next meeting all visible without oversized type or ornamental space.
- **Constraints:** static generated HTML; preserve verified data and links; never publish roster data, student names, or portraits; maintain visible source credits, WCAG 2.2 AA contrast, clear focus, desktop/tablet/mobile reflow, and meaningful course imagery.
- **User-pinned reference:** the preserved Spring 2026 Teaching Today page and its exact source at commit `f4836a4` are the template authority. The code is also packaged as `$artifact-template-compact-teaching-hq`.
- **Unresolved decisions:** none for this redesign.

## Implementation inventory

| Ingredient | Commitment | Medium |
|---|---|---|
| Compact header | Centered dark gradient with 11px gold date/term label, 28px light title, and 13px subtitle | Generated HTML/CSS |
| Course cards | Three equal 12px-radius cards with 112px image strip, course-color identity/actions, and white next-session body | Generated HTML/data imagery |
| Student course index | The same course-card template without private roster actions or instructor-only planning content | Generated HTML/CSS |
| Course first viewport | Current question, date and meeting context followed by documentary image, preparation copy, and coming meetings | Generated HTML/CSS |
| Typography | Inter only; 28px page title, 17px session, 14px course name, 9–13px metadata and actions | Google Fonts with system fallbacks |
| Palette | Cool gray `#f5f5f7`, white cards, charcoal header, gold context, and course-specific blue/rust/moss bands | CSS tokens |
| Responsive behavior | Three portraits desktop, two-plus-one tablet, one column phone; course side rail moves below main resource | CSS media queries |
| Privacy boundary | Public pages contain course data only; roster destinations remain private and appear only on the instructor HQ | Generator logic/data links |
