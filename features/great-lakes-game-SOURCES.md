# Great Lakes satellite map game — sources and maintenance

Revised September 8, 2026 at the instructor's request: all numbers now sit on the represented feature; seven cities have actual municipal outlines; the game has 24 places, including the restored Detroit River, Wisconsin Fox River, and a separate Welland Canal. The printed worksheet remains a separate 21-place edition.

## Fullscreen satellite map

The September 8 follow-up replaces the title/sidebar layout with a viewport-filling satellite map and small floating controls. Esri World Imagery tiles are loaded directly from `https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`. The service metadata identifies attribution as “Source: Esri, Vantor, Earthstar Geographics, and the GIS User Community.” Dates and contributing imagery vary by area and zoom; this is imagery, not a live feed. Attribution remains visible on the map. Imagery requires a network connection; failed initial loading produces an explicit notice.

Leaflet 1.9.4, the official stable release, is vendored under `_kit/vendor/leaflet/` with its BSD license. JS and CSS SHA256 hashes were verified against the [official download page](https://leafletjs.com/download.html). Leaflet handles Web Mercator projection, geographic anchoring, drag/pinch/wheel zoom, and scale. No API key, paid account, or uploaded imagery is required. City boundaries and waterways are vector overlays on the satellite imagery; the earlier filled lake silhouettes are no longer displayed.

## Geographic data

All geometry is derived from OpenStreetMap through Nominatim, © OpenStreetMap contributors, [ODbL](https://www.openstreetmap.org/copyright). Five lake source responses were preserved September 3, 2026; municipal outlines, Lake St. Clair, river centerlines, and canals were retrieved September 8, 2026. Raw responses are preserved in the course-materials project's `workbook/map-game-data/` and existing `workbook/work-icons/sources/`. Each source identity also appears in the page's `geography.sources` dataset.

| Layer | OSM source |
| --- | --- |
| Duluth | relation 136669 |
| Milwaukee | relation 251075 |
| Chicago | relation 122604 |
| Detroit | relation 134591 |
| Cleveland | relation 182130 |
| Buffalo | relation 175031 |
| Toronto | relation 324211 |
| Lake St. Clair | relation 4228055 |
| St. Marys River | relation 2189719 |
| Detroit River | relation 7730524 |
| St. Clair River (connecting geography, no separate question) | relation 4229869 |
| Niagara River | relation 2245991 |
| Fox River, Wisconsin | relation 4064352; display clipped to lower river leading into Green Bay |
| Welland Canal | relation 7762554 (active canal; excludes the separate disused-canal search result) |
| Chicago Sanitary and Ship Canal | relation 6099393 |
| St. Lawrence River / Seaway reference | relation 6122656; river-centerline reference east of Lake Ontario, not a full navigation-route dataset |

Coordinates are WGS84, longitude then latitude. Leaflet renders the satellite map in Web Mercator (EPSG:3857), north up, with its local scale control. Topology-preserving simplification tolerances: lakes 0.001°, municipal boundaries/Lake St. Clair 0.0005°, river/canal centerlines 0.00025°. Polygon holes are preserved. These are teaching-scale boundaries, not survey data. Municipal limits can include water; they are not urban footprints. City anchors are Nominatim's city-center coordinates and are checked inside the corresponding boundary. Connecting-water and canal anchors are snapped onto the source centerline. All numbers are Leaflet markers at those latitude/longitude anchors, with no leader lines or offsets. Close labels shrink slightly in the regional overview and return to full size when zoomed.

The Chicago canal number is placed on the canal near Lockport to distinguish it from Chicago at regional scale. The Welland number is on the active canal near Port Colborne. The St. Lawrence Seaway number locates one reference point on the river east of Lake Ontario; the full seaway system is larger and includes the separately identified Welland Canal.

Cross-checks: the Seaway authority's [Welland map](https://greatlakes-seaway.com/wp-content/uploads/2019/10/welland-1.pdf) and [locks and channels](https://greatlakes-seaway.com/en/the-seaway/our-locks-and-channels/) confirm the separate Welland route between Lakes Erie and Ontario; the [Library of Congress canal survey](https://www.loc.gov/resource/hhh.il0976.sheet/?sp=2&st=image) locates the Chicago–Lockport canal; [Michigan EGLE](https://www.michigan.gov/egle/about/organization/water-resources/aoc/detroit-river-aoc) confirms the Detroit River connection between Lake St. Clair and Lake Erie.

## Build and game behavior

The page config is the `great-lakes-game` entry under `extraPages` in `data/frst-110.json`. Synchronize it with `workbook/export_great_lakes_game.py SITE_ROOT` from the course-materials project (requires Shapely), then build this site. The exporter uses the print worksheet's original shared names plus the three explicit online-game additions, and does not edit the print worksheet.

Source: `features/great-lakes-game.fragment`, `_kit/great-lakes-game.css`, `_kit/great-lakes-game.js`; generated output: `courses/great-lakes-game.html`. Course link uses `greatLakesGamePage`. Do not edit generated HTML.

The question card is a small, centered overlay above the map (292px wide in the usual desktop and phone views), with feedback and celebrations kept beside the prompt. Redundant supporting text remains available to assistive technology.

Success tones rise half a semitone with each consecutive first-try answer, bounded across the 24-place round. Five-answer milestones add a fourth note; ten-answer milestones add a six-note flourish. Maximum sound duration is 0.69 seconds; volume remains modest and mute is preserved.

A correct answer scores 100 points on the first attempt or 50 after a miss, plays a short synthesized chime if sound is enabled, highlights the feature, then advances after 1.15 seconds. Wrong answers reset the streak and remain on the same question. Revealed answers score zero and wait for “Keep going.” Explore pauses the active round and pending advance; returning to play resumes it. Missed-only rounds and full replays reset their round scores. Sound is generated locally with Web Audio; the mute button prevents new notes. No audio files, analytics, user accounts, score submission, or persistent score storage.

`node tests/great-lakes-game.cjs` (Playwright required) checks all 24 markers, seven municipal layers, restored names, direct anchoring, sound/mute, automatic advance and pause, reveal, points/streaks, retry, keyboard, zoom, mobile tapping, and page overflow. `CHROME_PATH` selects an installed browser; `GAME_BASE_URL` selects a test server (default localhost:8782). Also run `python3 build.py --strict` and `./deploy.sh` and inspect full-viewport desktop, mobile, and zoomed city/canal screenshots, confirming that the imagery tiles loaded.
