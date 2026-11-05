# November 5 geographic locators

Prepared November 4, 2026. These are teaching locators, not historical territorial maps. No empire boundaries, campaign routes, modern national borders, or implied continuous steppe belt are drawn. Geography and river courses are modern reference data. The lower Yellow River changed course historically.

## Assets and reproduction

- `eurasia-map.svg`: 1600 × 850, Mongolia/Central Asia/north China/Goryeo; dashed rectangle locates the Korean detail.
- `goryeo-map.svg`: 1200 × 1050, peninsula detail. Open Kuju marker means approximate locator near modern Kusŏng. Haeinsa marks today's repository, not the original carving location.
- `scripts/build-hist-nov5-maps.py` produces both with Python's standard library. `--data-dir` accepts a cache containing the three Natural Earth GeoJSON files. Default `/tmp/hist-nov5-map-data`; absent files download from the Natural Earth upstream repository. The source cache stays out of Git.
- Equirectangular projection with longitude scaled by cosine of the center latitude: Eurasia 39°N, Korea 37.9°N. Extents respectively 48–144°E / 20–58°N and 122–132.5°E / 33.1–42.7°N. North is up. Scale bars apply at the center latitude. WGS84 geographic coordinates in longitude, latitude order.

## Geographic substrate

[Natural Earth, public domain](https://www.naturalearthdata.com/about/terms-of-use/), 1:10m land, lakes, rivers/lake centerlines. Source files [upstream GeoJSON directory](https://github.com/nvkelso/natural-earth-vector/tree/master/geojson): `ne_10m_land.geojson`, `ne_10m_lakes.geojson`, `ne_10m_rivers_lake_centerlines.geojson`, retrieved November 4, 2026. Geometry is clipped to the view and simplified in pixel space; no hand-drawn coastlines or rivers. Major displayed rivers: Yellow, Yangzi, Wei, Syr Darya, Yalu, Tumen, Han/Namhan, Nakdong. Upstream does not provide an Amu Darya feature under the requested English name, so no invented Amu Darya geometry is substituted.

## Locator coordinates

| Place | Longitude, latitude | Source / precision |
|---|---|---|
| Karakorum | 102.847989, 47.209540 | [German Archaeological Institute, iDAI gazetteer 2042953](https://gazetteer.dainst.org/doc/2042953.html), archaeological-site locator. Cross-checked against modern mapped ruins 47.21453, 102.84784; difference is below map symbol size. |
| Bukhara | 64.428610, 39.774720 | [UNESCO Historic Centre of Bukhara](https://whc.unesco.org/en/list/602/), World Heritage locator rounded to five decimals. |
| Samarkand | 67.000000, 39.668890 | [UNESCO Samarkand](https://whc.unesco.org/en/list/603/), World Heritage locator; also within the plate source map's Samarkand anchor 66.96, 39.65. |
| Herat | 62.20, 34.35 | Existing course Plate 15 source ledger, modern city locator at two-decimal precision. |
| Beijing | 116.40, 39.90 | Existing Plate 15 and northern-powers source ledgers, modern city locator. Label refers to the Jin capital captured in 1215 (Ebrey p.164), not a precise medieval palace location. |
| Kaesong / Gaegyeong | 126.55, 37.97 | Existing Plate 15 ledger, two-decimal city locator. Checked against [OpenStreetMap/GeoNames city location](https://mapcarta.com/Kaesong), 126.5528, 37.9717. |
| Kuju / Kusŏng | 125.24, 39.98 | Existing Plate 15 ledger. Approximate modern town locator; no claim that the marker surveys Pak Sŏ's fortress wall. |
| Ganghwa | 126.485237, 37.751632 | [Incheon Tourism Organization guide](https://www.ito.or.kr/foreign/img/publications_en.pdf), p.25, Goryeo Palace Site. Cross-check: [Academy of Korean Studies heritage entry](https://dh.aks.ac.kr/Edu/wiki/index.php/%EA%B0%95%ED%99%94%EA%B3%A0%EB%A0%A4%EA%B6%81%EC%A7%80), 126.485334, 37.751994. This replaces the older, broad island locator for accuracy. |
| Haeinsa | 128.098711, 35.801672 | [UNESCO Haeinsa](https://whc.unesco.org/en/list/737), N35 48 6.019 E128 5 55.36. |

Historical labels are supported by Ebrey & Walthall, *Pre-Modern East Asia*, pp.164–168, 176–178, and SKT pp.201–203 in the assigned November 5 reader. “Mongol imperial center” avoids assigning the later capital's full development to Chinggis Khan. Goryeo remains a regional label, not a colored empire province.

## Verification

Both SVGs rendered to PNG with macOS `sips`, then visually inspected at full output size. No label overlap or clipped text in the final renders. Sans-serif declared explicitly in SVG; Arial rendered. Korea detail separates Kaesong and Ganghwa with fine leader lines. No fabricated routes or borders; East Sea label used. Full-page/mobile integration is checked by the parent class-page build.

### Source checksums (SHA-256)

- `ne_10m_lakes.geojson`: `2d036f53dedec578001c5c30c2959ee7d4eebc1306900fa4367c49929ec8f2d9`
- `ne_10m_land.geojson`: `1ac90796408bc6ad6911d69448485d3c4dbf2190370080368a09976e1c9f7416`

## Revision, November 5, 2026

Both maps rebuilt to show every place named in the November 5 readings (letter to Changchun; Morgan pp.73–83; SKT 200–205) and the Chungji poems. Labels in Revised Romanization. Added locators (approximate, modern coordinates): Zhongxing (Yinchuan) 38.49N 106.23E; Chang’an (Xi’an) 34.34N 108.94E; Hangzhou 30.27N 120.16E; Balkh 36.76N 66.90E; Nishapur 36.21N 58.80E; Baghdad 33.31N 44.36E; Delhi 28.61N 77.21E; Uiju 40.20N 124.53E; Sakju 40.38N 125.05E; Cheolju (Cheolsan) 39.76N 124.64E; Taeju 39.90N 125.62E; Jeongju 39.69N 125.33E; Jukju (Juksan) 37.07N 127.43E; Songgwangsa 35.00N 127.28E; Happo (Masan) 35.20N 128.57E; Jindo 34.48N 126.26E; Jeju 33.43N 126.53E; Tsushima 34.42N 129.33E; Iki 33.79N 129.72E; Hakata Bay 33.59N 130.40E.

Gurganj (Kunya-Urgench), capital of the Khwarazm-shahs: 42.33N 59.15E (added November 5, 2026).
