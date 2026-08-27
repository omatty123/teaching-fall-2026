# Teaching site — Fall 2026

Lawrence University · FRST 110, HIST 212, BUEN 594.

Static HTML on GitHub Pages. No npm, no build server, no framework.
`python3 build.py` and you are done.

## The one rule

**Every fact about a course lives in `data/<slug>.json`, once.**

If a room number, meeting time, reading, or CRN is wrong on the site, it is wrong
in `data/`. Fix it there and rebuild. Never edit `index.html` or `courses/*.html`
by hand — they are generated and your edit will be overwritten on the next build.

## Run it

```bash
python3 build.py                 # regenerate index.html + courses/*.html
python3 -m http.server 8765      # preview at http://localhost:8765/
./deploy.sh                      # run the deploy checklist (never pushes)
./deploy.sh --push               # checklist, confirm you previewed, commit, push
```

## Layout

```
data/term.json          term dates, campus, schedule window, archive link
data/<slug>.json        ONE course: identity, meeting, theme, registrar,
                        final, links, prep tasks, schedule[]
features/<slug>.html    optional editorial block for a course that earns one
_kit/hq.css             shared design system (the HQ look)
_kit/course.css         course-page layout
_kit/hq.js              next-session logic for the HQ cards
_kit/<slug>-feature.css optional styles for that course's feature
images/                 all images, both HQ and course pages
build.py                the only build step
deploy.sh               checklist + push
```

Generated, do not edit: `index.html`, `courses/*.html`, `favicon.svg`.

## Adding a course

1. `cp data/buen-594.json data/new-course.json` and edit it.
2. Add its slug to `courseOrder` in `data/term.json`.
3. Drop a banner image in `images/` and point `theme.banner.src` at it.
4. `python3 build.py`.

No CSS changes are needed. Course colour, gradient, and banner all come from
`theme` in the JSON and are injected as custom properties. A fourth course costs
one file and one line.

## Starting a new term

1. Copy this repo to `teaching-<term>-<year>`.
2. Rewrite `data/term.json`.
3. For each course, update `meeting`, `registrar`, `final`, and `schedule`.
4. Keep or drop `features/` per course.

The previous term's repo stays live at its own URL, frozen, as the archive.

## What `build.py` computes so you don't

- Week-grid block positions from `meeting.start`/`meeting.end`. No hand-typed
  pixel offsets. `PX_PER_MIN` reproduces the geometry of the hand-built grid
  this replaced.
- 12-hour clock labels from 24-hour times.
- Meeting counts, day-of-week labels, workspace readiness states.
- Every `<head>`: favicon, OG tags, Twitter tags, absolute `og:image`.
- Breadcrumbs on every course page.

## Checks that run on every build

`build.py` warns (never blocks) about: meeting times outside the week-grid
window, unknown meeting days, out-of-order or duplicate schedule dates, missing
banner images, and anything listed in a course's `unverified` array.

Put a fact you have not confirmed in `unverified` rather than silently shipping
it. It will be printed on every single build until you resolve it.

## Gotcha worth remembering

Do not put `url()` inside a CSS custom property. Chrome resolves it against the
stylesheet that substitutes the variable, not the document, so a relative path
silently 404s. `build.py` writes `background-image` directly onto the element
for this reason — see `banner_style()`.

## What this replaced

Three courses were previously described in four places at once: a TypeScript
file in a Next.js app deployed to `*.chatgpt.site` with no git remote, inline JS
in a separate GitHub Pages repo (with the meeting times re-encoded a second time
as hand-computed pixel offsets), the per-course `STATUS.md` files, and the
Google Docs syllabi. Changing a room meant remembering all four.

The Google Docs syllabi and Canvas remain the authoritative student-facing
documents. This site is the launch surface, and `data/` is its single source.
