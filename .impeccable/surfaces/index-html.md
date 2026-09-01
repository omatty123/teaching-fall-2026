---
version: 1
slug: "index-html"
primary_target: "index.html"
related_targets: ["students.html","courses/frst-110.html","courses/hist-212.html","courses/buen-594.html","courses/water-in-the-news.html"]
---

# Fall 2026 teaching surfaces

- **Scope and modes:** `index.html` is the instructor-only/public-safe Operate surface; `students.html` and `courses/*.html` are student-facing Operate/Read surfaces.
- **Audience and job:** Matty needs immediate teaching orientation and the next consequential move. Students need the next meeting and a short path to Canvas, syllabus, current work, and schedule.
- **Chosen direction:** Field Desk — paper, ink, rules, documentary imagery, compact comparative rows, explicit provenance, and state labels. It refuses generic dashboard cards, gradients, points, and decorative motion.
- **Memorable moment:** the instructor first viewport uses a persistent day rail for Now and the next three meetings, while the working canvas leads with one consequential move, a compact Next / At risk / Changed ledger, and dense course dispatch rows. The student index remains a clean three-course dispatch board; each course home then opens as a compact session console with persistent course tools, the next meeting as the primary workspace, and upcoming meetings alongside it.
- **Constraints:** static generated HTML; preserve verified data and links; never surface private student information or local destinations; WCAG 2.2 AA; 44px interaction floor; desktop and mobile; no invented academic facts.
- **Unresolved decisions:** none in the current publication gate; future uncertain facts return to the private source layer until confirmed.
- **Approved comp:** `.impeccable/mocks/hq-field-desk-approved.png`; the topology is binding, but generated course titles, dates, links, and imagery are not factual sources and must be replaced from `data/`.

## Implementation inventory

| Ingredient | Commitment | Medium |
|---|---|---|
| Page ground | Warm paper `#f3efe5`, full viewport | CSS |
| Ink and rules | Navy-black `#14263a`, 1–2px rules, no shadows | CSS |
| Status signals | Rust `#9a4b32`, moss `#3e6752`, ochre `#8a6a25` | CSS tokens and text labels |
| Typography | Compact humanist sans; 15–17px body, restrained scale, tabular times | Self-hosted/system sans stack and CSS |
| First viewport | Sticky day rail, one prioritized move, compact three-part ledger | Semantic aside plus CSS grid |
| Course dispatches | Three ruled comparison rows with documentary image strip and factual next-session data | Generated HTML plus existing course images |
| Student index | Separate route with three student-forward course rows | Generated HTML/CSS |
| Course homes | Sticky course/tool rail above a dense next-session panel, compact documentary image, upcoming meetings, and public-safe student destinations | Generated HTML/CSS |
| Controls | Underlined links and square checks, at least 44px practical target | Semantic links, buttons, checkboxes |
| Motion | State-only disclosure and check completion; reduced-motion safe | CSS/JavaScript |
