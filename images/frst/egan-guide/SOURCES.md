# Egan guide images and map

Accessed September 13, 2026. Original sources; no generated portraits.

- **lake-trout.jpg**: H. L. Todd historical US fishery plate; public domain. https://commons.wikimedia.org/wiki/File:FMIB_51076_Namaycush_or_Lake_Trout.jpeg
- **sea-lamprey.jpg**: Ellen Edmonson, New York biological survey; public domain in US per source. https://commons.wikimedia.org/wiki/File:Petromyzon_marinus.jpg
- **alewife.jpg**: Ellen Edmonson, New York biological survey; public domain in US per source. https://commons.wikimedia.org/wiki/File:Alosa_pseudoharengus_(NY).jpg
- **hawley.jpg**: Grove S. Gilbert historical portrait of Jesse Hawley; public-domain painting. https://commons.wikimedia.org/wiki/File:Jesse_Hawley_(1773–1842)_1832_1.jpeg
- **clinton.jpg**: Rembrandt Peale, DeWitt Clinton, 1823; public-domain painting. https://commons.wikimedia.org/wiki/File:DeWitt_Clinton_by_Rembrandt_Peale.jpg
- **applegate.png**: Vernon Applegate. USGS John Van Oosten Library photograph. Extracted from PDF page 4 (printed p28), clip [218,21.2,576.7,287], at 2x, excluding article text. https://www.glfc.org/pubs/pdfs/SavingShipsSavingFish_MichiganHistoryMagazine.pdf
- **tanner.jpg**: Michigan DNR downloadable press photograph, Howard Tanner. https://www.michigan.gov/dnr/about/newsroom/releases/2026/08/24/dnr-remembers-the-legacy-of-dr-howard-tanner

## Map source and coordinate ledger
- Five lake polygons: classroom handout’s workbook/work-icons/great-lakes.geojson, OpenStreetMap relations 4039486, 1205149, 1205151, 4039900, 1206310, retrieved 2026-09-03. ODbL, https://www.openstreetmap.org/copyright .
- Connecting water and Niagara/Welland detail: existing Great Lakes Map Challenge pageConfig geometry, 2026-09-08. Niagara relation 2245991; Welland relation 7762554. Modern geometry, not a reconstruction of nineteenth-century alignments.
- Coordinates longitude/latitude WGS84. Render north-up equirectangular at 45N, 49 SVG units/degree longitude and 69.3/degree latitude. Scale approximate at 45N. No invented canal routes. Niagara detail uses the same coordinates at greater scale.
- Chicago (-87.6244,41.8756), Buffalo (-78.8781,42.8864), Niagara/Welland region (-79.15,43.07): existing class map; Niagara overview symbol offset with visible leader.
- Hammond Bay station (-84.03589,45.49654): OSM way 1039896695, corroborated USGS address 11188 Ray Road and https://mapcarta.com/W1039896695 .
- Albany (-73.7562,42.6526): approximate city location; original canal endpoint corroborated NPS https://home.nps.gov/tripideas/15-miles-on-the-erie-canal.htm . No route drawn between endpoints.
- Lost Villages (-74.9,45.0): approximate Long Sault region, not precise Moulinette or Hickey home. Historical location corroborated https://lostvillages.ca/history/the-lost-villages/moulinette/ .
- Niagara Falls detail (-79.074,43.079): geographic falls location. Read in relation to existing OSM Niagara River and Welland route.
- Fallback: all map geometry is inline SVG; no tile service required. Full setting descriptions available without JavaScript. On narrow screens, map scrolls horizontally; selection also centers the corresponding marker.

## Reading
Dan Egan, The Death and Life of the Great Lakes, 2017 first edition, chapters 1–2, printed pp. 3–74. Source text read locally, not redistributed. Guide prose is original paraphrase; philosophical labels are explicitly interpretive.

## Wednesday / Friday companion guides — added 2026-09-13

- `coho.png`, `chinook.png`: NOAA Fisheries species illustrations by Jack Hornady, downloaded from the official [coho](https://www.fisheries.noaa.gov/species/coho-salmon) and [chinook](https://www.fisheries.noaa.gov/species/chinook-salmon) pages. Unmodified images, displayed with `object-fit:contain`; not to a common size scale.
- `mussels.png`: [USGS comparison](https://www.usgs.gov/media/images/detailed-view-a-quagga-mussel-right-and-a-zebra-mussel), zebra LEFT, quagga RIGHT; USGS public-domain image. Lossless GIF-to-PNG conversion; original wording retained.
- `four-carp.jpg`: [USGS Bighead Carp Photo Gallery](https://www.usgs.gov/centers/columbia-environmental-research-center/bighead-carp-photo-gallery), `MediumCarps2.jpg`, public domain. Silver top left; grass top right; bighead bottom left; black bottom right. Juveniles about 200 mm long, not adult-size comparison. Unmodified.
- `chicago-waterway.png`: [USGS Open-File Report 2016–1011](https://pubs.usgs.gov/of/2016/1011/ofr20161011.pdf), figure 1 (printed p. 3), public domain. Render of original geographic figure, including its original map attribution and scale. The image records 2013 spawning observations, not current distribution. It shows the electric dispersal barrier and upstream/downstream lock geography; lakefront Chicago locks are outside its extent.
- `settings-3-4.svg`, `settings-5-6.svg`: classroom locator maps generated from geographic geometry, longitude/latitude WGS84 input, north-up equirectangular projection with standard parallel at each map's middle latitude. Scale bars use that parallel. Map date 2026-09-13, not an invasion-status date.
  - Great Lakes shoreline polygons: same OpenStreetMap relation geometry used in the course's classroom map (`great-lakes.geojson`, retrieved 2026-09-03). © OpenStreetMap contributors, [ODbL](https://www.openstreetmap.org/copyright). Geometry repaired for topology and lightly simplified for SVG rendering; small islands omitted at this scale.
  - Continental land, state boundaries, river lines and reservoir polygons: Natural Earth 1:50m data, [public domain](https://www.naturalearthdata.com/about/terms-of-use/); GeoJSON from [Natural Earth vector repository](https://github.com/nvkelso/natural-earth-vector/tree/master/geojson), retrieved 2026-09-13. Only Mississippi and Colorado river centerlines emphasized; no overland boat route is inferred or drawn.
  - Platte River marker: [NPS Platte River Point water access](https://www.nps.gov/places/000/platte-river-point-water-access.htm), 44.7296 N, 86.1562 W. Locates river mouth, not exact stocking site.
  - Isle Royale: regional island-area marker at 48 N, 88.9 W, compared with [NPS park maps](https://www.nps.gov/isro/planyourvisit/maps.htm); not a dock or exact sampling point. Small island shape omitted in classroom shoreline source.
  - Lake Huron (-82.4,44.55), Lake St. Clair (-82.67,42.5), Seaway entrance (-76.1618,44.2807), Chicago (-87.6244,41.8756): existing course map coordinate ledger, regional setting markers. Seaway marker denotes its entrance near Lake Ontario, not the whole shipping route.
  - Mead / Powell: representative interior points computed from each named Natural Earth lake geometry; locate reservoirs, not exact dam sites. Dam names paired in captions for reading orientation.

## Round goby — added September 15, 2026; photo replaced September 16, 2026

- `round-goby.jpg`: photographed by Alex R (iNaturalist username flsandhills_ar), Onondaga Lake, Syracuse NY, August 30, 2018; Research Grade observation of Round Goby (Neogobius melanostomus). Licensed CC BY-NC. https://www.inaturalist.org/photos/24046034 . Replaces the original U.S. Fish & Wildlife Service hand-held photo (still public domain, no longer used here) at the user's request for a cleaner studio-style image; original file was https://commons.wikimedia.org/wiki/File:Neogobius_melanostomus2.jpg .
- Species and food-web context: https://www.nps.gov/slbe/learn/nature/invasivespecies.htm ; botulism pathway uncertainty: https://www.nps.gov/slbe/learn/nature/sick-birds.htm .
