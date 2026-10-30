#!/usr/bin/env python3
"""Render fallback SVG maps from the same data and place ledger as Leaflet."""
from pathlib import Path
import json,math,html
ROOT=Path(__file__).resolve().parent
VIEWS=json.loads((ROOT/'map-config.json').read_text())
COUNTRIES=json.loads((ROOT/'map-data/atlantic-50m.geojson').read_text())
DETAIL=json.loads((ROOT/'map-data/europe-islands-10m.geojson').read_text())
THAMES=json.loads((ROOT/'map-data/thames-natural-earth.geojson').read_text())
def esc(s):return html.escape(str(s),quote=True)
def merc(lon,lat):return lon,math.degrees(math.log(math.tan(math.pi/4+math.radians(lat)/2)))
def rings(feature):
 g=feature['geometry'];coords=g['coordinates']
 if g['type']=='Polygon':return [coords]
 if g['type']=='MultiPolygon':return coords
 return []
for key,view in VIEWS.items():
 w,h=1200,650
 (south,west),(north,east)=view['bounds'];xmin,ymin=merc(west,south);xmax,ymax=merc(east,north)
 scale=min((w-100)/(xmax-xmin),(h-155)/(ymax-ymin))
 left=(w-(xmax-xmin)*scale)/2;top=80+(h-160-(ymax-ymin)*scale)/2
 def xy(lon,lat):
  x,y=merc(lon,lat);return left+(x-xmin)*scale,top+(ymax-y)*scale
 # Clip to the actual SVG viewport, including the margin around the requested bounds.
 visible_west=xmin+(20-left)/scale;visible_east=xmin+(1180-left)/scale
 def inverse_lat(y):return math.degrees(2*math.atan(math.exp(math.radians(ymax-(y-top)/scale)))-math.pi/2)
 visible_south=inverse_lat(578);visible_north=inverse_lat(78)
 def path(coords,close=False):
  return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in (xy(*p[:2]) for p in coords))+(' Z' if close else '')
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',f'<title id="title">{esc(view["title"])}</title>', '<desc id="desc">Selected places in Equiano chapters III and IV. Modern Natural Earth geography. No voyage routes or exact battle positions are drawn.</desc>', '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#243a44}.label{font-size:22px;font-weight:600;paint-order:stroke;stroke:#fff;stroke-width:6px;stroke-linejoin:round}.context{font-size:19px;letter-spacing:1px;fill:#4b6673;paint-order:stroke;stroke:#eef5f7;stroke-width:4px}</style>', '<rect width="1200" height="650" fill="#fff"/>',f'<text x="28" y="35" font-size="25" font-weight="600">{esc(view["title"])}</text>', '<text x="28" y="61" font-size="17">Selected place locators · modern outlines · no reconstructed sailing track</text>', '<defs><clipPath id="frame"><rect x="20" y="78" width="1160" height="500"/></clipPath></defs><g clip-path="url(#frame)"><rect x="20" y="78" width="1160" height="500" fill="#eaf3f6"/>']
 features=COUNTRIES['features'] if key=='atlantic' else DETAIL['features']
 if key=='atlantic':features=[f for f in features if f['properties'].get('ADM0_A3')!='BRB']+[f for f in DETAIL['features'] if f['properties'].get('ADM0_A3')=='BRB']
 for f in features:
  for poly in rings(f):
   outer=poly[0]
   if not outer:continue
   xs=[p[0] for p in outer];ys=[p[1] for p in outer]
   if max(xs)<visible_west or min(xs)>visible_east or max(ys)<visible_south or min(ys)>visible_north:continue
   d=' '.join(path(r,True) for r in poly)
   parts.append(f'<path d="{d}" fill="#e3e8dd" stroke="#879c9e" stroke-width="1" fill-rule="evenodd"/>')
 if key=='thames':
  for f in THAMES['features']:
   for line in f['geometry']['coordinates']:
    parts.append(f'<path d="{path(line)}" fill="none" stroke="#4384a3" stroke-width="4" stroke-linecap="round"/>')
 for item in view['labels']:
  x,y=xy(item['lon'],item['lat']);parts.append(f'<text class="context" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{esc(item["text"])}</text>')
 for p in view['points']:
  x,y=xy(p['lon'],p['lat']);dx=14;dy=7;anchor='start'
  if p['direction']=='left':dx=-14;anchor='end'
  elif p['direction']=='top':dx=0;dy=-19;anchor='middle'
  elif p['direction']=='bottom':dx=0;dy=32;anchor='middle'
  if p['kind']!='region':parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#a44127" stroke="#fff" stroke-width="2"/>')
  style='font-style="italic"' if p['kind']=='region' else ''
  parts.append(f'<text class="label" {style} x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anchor}">{esc(p["label"])}</text>')
 parts.append('</g><rect x="20" y="78" width="1160" height="500" fill="none" stroke="#cbd5d7"/>')
 parts.append('<text x="1150" y="109" text-anchor="middle" font-size="20" font-weight="600">N ↑</text>')
 # Scale uses the mid-latitude of this map; Mercator true scale changes with latitude.
 lat=(south+north)/2;km_per_degree=111.195*math.cos(math.radians(lat));km=(xmax-xmin)*km_per_degree
 step=1000 if km>3000 else 200 if km>900 else 50 if km>250 else 10
 px=step/km_per_degree*scale
 parts.append(f'<path d="M40,555 v-8 M40,555 h{px:.1f} M{40+px:.1f},555 v-8" stroke="#243a44" stroke-width="2" fill="none"/><text x="40" y="541" font-size="16">{step} km at {lat:.1f}° N</text>')
 note='Generalized Thames centerline; town/district locators, not a known ship anchorage.' if key=='thames' else 'Dots: approximate place locators. Virginia: regional label only.' if key=='atlantic' else 'Dots: approximate place locators, not exact ships, landing beaches or battle positions.'
 parts.extend([f'<text x="28" y="607" font-size="17">{esc(note)}</text>','<text x="28" y="633" font-size="15">Geography: Natural Earth, public domain · WGS84 source data / Mercator projection · FRST 110 · 30 October 2026</text>','</svg>'])
 (ROOT/view['image']).write_text('\n'.join(parts)+'\n')
 print(view['image'],(ROOT/view['image']).stat().st_size)
