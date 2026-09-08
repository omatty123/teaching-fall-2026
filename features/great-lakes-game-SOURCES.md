# Great Lakes map game: sources and maintenance

This practice game adapts the 21-place FRST 110 Great Lakes identification worksheet approved September 8, 2026. Names, numbering, point coordinates, and schematic connecting waters are retained. Fox River and Detroit River are not answer items; Detroit the city remains.

The five Great Lakes outlines were obtained from OpenStreetMap relations through Nominatim on September 3, 2026 for the course worksheet. © OpenStreetMap contributors, [ODbL](https://www.openstreetmap.org/copyright). The game projects the worksheet's preserved coordinates at standard parallel 45° N, retaining north-up orientation and geographic anchors. Numbered symbols for small features are offset with leader lines. Channels and the added Lake St. Clair outline are schematic. The Seaway marker indicates the route east of Lake Ontario, not the whole navigation system.

The game dataset is the `great-lakes-game` entry under `extraPages` in `data/frst-110.json`. To synchronize future worksheet changes, run `workbook/export_great_lakes_game.py SITE_ROOT` from the FRST course-materials project, then build this site. The exporter verifies lake-marker containment.

Game source: `features/great-lakes-game.fragment`, `_kit/great-lakes-game.css`, `_kit/great-lakes-game.js`. Output: `courses/great-lakes-game.html`. The generator adds its course tool link through `greatLakesGamePage`. Never edit generated HTML directly.

Validation: `python3 build.py --strict` and `./deploy.sh`. With Playwright installed and this directory served on port 8781, run `node tests/great-lakes-game.cjs`; optional `CHROME_PATH` selects a local browser and `GAME_BASE_URL` selects another server. Tests check all 21 markers, wrong answers, answer reveal, study pause/resume, Enter/Space activation, round scoring, retrying only missed places, reset, and mobile panning. Evidence is saved under the ignored `.impeccable/review/great-lakes/` directory.

The browser keeps a round only in memory. Reloading starts a fresh round; the game submits no scores or personal information.
