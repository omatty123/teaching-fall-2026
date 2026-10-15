"""Add sourced modern rivers to the existing October 15 locator. Idempotent.
Source: Natural Earth 1:10m rivers/lake centerlines, public domain.
EPSG:4326 longitude/latitude; projection matches the original locator.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
def tag(t): return '{'+NS+'}'+t
def pos(lon,lat):return (lon-95)*1100/48,(51-lat)*750/31
p=ROOT/'images/hist/oct15/east-asia.svg'
r=E.fromstring(p.read_text())
for el in list(r):
    if el.get('id') in {'rivers','river-labels'}:r.remove(el)
g=E.Element(tag('g'),{'id':'rivers','clip-path':'url(#frame)','fill':'none','stroke':'#287ba4','stroke-linejoin':'round','stroke-linecap':'round'})
for f in json.loads((ROOT/'scripts/data/oct15-rivers.geojson').read_text())['features']:
    geom=f['geometry'];lines=[geom['coordinates']] if geom['type']=='LineString' else geom['coordinates']
    major=f['properties'].get('name') in {'Huang','Jinsha','Chang Jiang','Yangtze'}
    for line in lines:
        pts=[pos(x,y) for x,y,*_ in line]
        d='M'+' L'.join(f'{x:.2f},{y:.2f}' for x,y in pts)
        E.SubElement(g,tag('path'),{'d':d,'stroke-width':'3.7' if major else '2.3'})
land=next(e for e in r if e.tag==tag('g') and e.get('fill')=='#f7f5ed')
r.insert(list(r).index(land)+1,g)
l=E.SubElement(r,tag('g'),{'id':'river-labels'})
for label,x,y in [('Yellow River',210,318),('Yangzi River',405,558),('Huai',440,435),('Wei',255,388),('Liao',655,210),('Yalu',760,290)]:
    e=E.SubElement(l,tag('text'),{'x':str(x),'y':str(y),'style':'font-family:Arial,sans-serif;font-size:23px;fill:#176082;paint-order:stroke;stroke:#f7f5ed;stroke-width:4px;stroke-linejoin:round'})
    e.text=label
for e in r.iter(tag('text')):
    if e.text == 'Tang China':
        e.set('x','440'); e.set('y','275')
    if e.text and e.text.startswith('Natural Earth ·'):
        e.text='Natural Earth · modern coastlines and river courses · equirectangular'
r.find(tag('title')).text='East Asia: capitals, major rivers and regional setting'
p.write_text(E.tostring(r,encoding='unicode')+'\n')
