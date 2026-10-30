#!/usr/bin/env python3
"""Check October 30 resources, sources, and public course attachment."""
import json, runpy
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.images=[];self.text=[];self.controls=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  for key in ('src','href'):
   if a.get(key):self.links.append(a[key])
  if tag=='img':self.images.append(a)
  if tag=='button' and a.get('data-view'):self.controls.append(a['data-view'])
 def handle_data(self,s):self.text.append(s)
checks=[('equiano-chapters-3-4.html','build-equiano-3-4.py',{'maps','chapter-three','chapter-four','water','context','vocabulary','images','sources'}),('equiano-and-omar-ibn-said.html','build-equiano-omar.py',{'works','comparison','reading-links','sources'})]
urls=[]
for name,builder,ids in checks:
 p=ROOT/'frst-110-resources'/name;s=p.read_text();c=Page();c.feed(s)
 assert s==runpy.run_path(str(ROOT/'scripts'/builder))['render'](),f'Stale generated page: {name}'
 assert ids<=set(c.ids) and len(c.ids)==len(set(c.ids)),f'Page anchors: {name}'
 assert len(c.images)>=2 and all(x.get('alt') and x.get('width') and x.get('height') for x in c.images),f'Image descriptions/dimensions: {name}'
 for link in c.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  assert target.is_relative_to(ROOT) and target.is_file(),f'Missing/public path: {link}'
  if target==p and u.fragment:assert u.fragment in c.ids,f'Anchor: {link}'
 for forbidden in ('/Users/','127.0.0.1','teaching-notes/private','Mock-Filled','{{'):
  assert forbidden not in s,f'Private/unbuilt content: {name}: {forbidden}'
 if name.startswith('equiano-chapters'):
  assert len(c.controls)==4 and len(set(c.controls))==4,'Four distinct map views required'
 else:
  assert 'data-label="Equiano"' in s and 'data-label="Omar ibn Said"' in s,'Mobile comparison labels required'
 urls.append('https://omatty123.github.io/teaching-fall-2026/frst-110-resources/'+name)
for folder in ('equiano-3-4-assets','equiano-omar-assets'):
 assets=ROOT/'frst-110-resources'/folder
 for p in assets.rglob('*.json'):json.loads(p.read_text())
 assert (assets/'images/sources.json').is_file()
for p in (ROOT/'frst-110-resources/equiano-3-4-assets/map-data').glob('*.geojson'):
 j=json.loads(p.read_text());assert j.get('type')=='FeatureCollection' and j.get('features'),p.name
# Missing neighboring countries previously made coastline context look like water.
geo=ROOT/'frst-110-resources/equiano-3-4-assets/map-data'
for filename,required in [('atlantic-50m.geojson',{'CAN','USA','GBR'}),('europe-islands-10m.geojson',{'IRL','ITA','MAR','DZA','TUN','FRA','ESP','GBR'})]:
 data=json.loads((geo/filename).read_text())
 assert required<={f['properties'].get('ADM0_A3') for f in data['features']},f'Missing geographic context: {filename}'
import xml.etree.ElementTree as ET
for view in ('atlantic','channel','mediterranean','thames'):
 ET.parse(geo.parent/f'map-{view}.svg')
course=json.loads((ROOT/'data/frst-110.json').read_text())
day=[x for x in course['schedule'] if x.get('date')=='2026-10-30'];assert len(day)==1
for url in urls:
 assert sum(x['href']==url for x in day[0]['materials'])==1,'Exact-date course link missing/duplicated'
 assert url in (ROOT/'courses/frst-110.html').read_text(),'Generated course link missing'
print('October30 pages: generated source, links, image metadata, map views/data, comparison labels, public boundaries, and dated course links passed.')
