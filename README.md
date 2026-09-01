# Teaching site — Fall 2026

Lawrence University · FRST 110, HIST 212, BUEN 594.

A framework-free static site for GitHub Pages. It has two entry surfaces:

- `index.html` is Matty’s instructor Field Desk: current situation, priority move, course dispatches, recurring week, and the personal decision queue.
- `students.html` is the public student index: course homes, next meetings, syllabi, Canvas, and public course features. It intentionally omits roster destinations.

## Sources of truth

The Google Docs syllabi and Canvas courses remain authoritative for student instructions. `data/` is the site’s public-safe projection of those sources—not a replacement for them.

Edit `data/term.json` or `data/<slug>.json`, then rebuild. Never hand-edit `index.html`, `students.html`, `courses/*.html`, or `favicon.svg`; they are generated and will be overwritten.

Facts that are not confirmed belong in a course’s `unverified` array. A normal build prints them. A strict build refuses publication until they are resolved.

## Run it

```bash
python3 build.py                 # regenerate all public HTML
python3 build.py --strict        # publication gate; nonzero on unresolved facts
python3 -m http.server 8765      # preview at http://localhost:8765/
./deploy.sh                      # strict checklist; never pushes
./deploy.sh --push               # checklist, preview confirmation, commit, push
```

## Layout

```text
data/term.json             term dates, navigation, public-safe decision projection
data/<slug>.json           course identity, meeting, registrar, links, schedule
features/*.fragment        editorial source fragments (not standalone public pages)
_kit/hq.css                Field Desk design system and responsive index layouts
_kit/course.css            utility-first course-home layout
_kit/hq.js                 next-session logic and browser-local decision checks
_kit/*-feature.css         course-feature and Water in the News styles
images/                    credited course imagery and editorial media
build.py                   sole generator
deploy.sh                  strict publication checklist and optional push
```

Generated outputs include:

- `index.html`
- `students.html`
- `courses/<slug>.html`
- `courses/frst-110-atlas.html`
- `courses/water-in-the-news.html`
- `favicon.svg`

## Adding a course

1. Copy an existing `data/<slug>.json` and replace every public fact.
2. Add its slug to `courseOrder` in `data/term.json`.
3. Add a real banner image with alt text and a visible source credit.
4. Add only working, public-safe links. Roster links are instructor-only and must be Access-gated.
5. Run `python3 build.py --strict`, preview desktop and mobile, then use `./deploy.sh`.

The shared layout is intentionally rule-based rather than card-based: warm paper, navy ink, fine ledger rules, documentary image strips, and restrained course colors. Add new course content through the data schema before adding one-off components.

## Publication checks

Every strict build checks:

- meeting geometry, known weekdays, and ordered unique dates;
- missing banners and feature fragments;
- unresolved `unverified` facts;
- missing syllabus or Canvas destinations;
- stale `chatgpt.site` or local-only URLs.

`deploy.sh` additionally checks `.nojekyll`, metadata, breadcrumbs, navigation reachability, and local asset resolution. It cannot verify registrar facts or private-system access; those must be confirmed at their authority before removing an `unverified` entry.

## Privacy boundary

Do not put student names, roster data, private repository URLs, local filesystem paths, medical information, or non-public planning notes in `data/`, generated HTML, or screenshots. The student index never renders roster links. The instructor surface labels any authorized roster destination as **Authenticated**.
