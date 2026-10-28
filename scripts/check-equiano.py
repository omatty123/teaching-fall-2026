#!/usr/bin/env python3
"""Validate the public reading page, its downloadable assets, and course attachment."""
import json
import runpy
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'frst-110-resources/equiano-chapters-1-2.html'
URL = 'https://omatty123.github.io/teaching-fall-2026/frst-110-resources/equiano-chapters-1-2.html'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag in ('a','link','script','img'):
            value=a.get('href') or a.get('src')
            if value:self.links.append(value)
        if tag=='img':self.images.append(a)

text=PAGE.read_text(); parsed=Page(); parsed.feed(text)
assert text==runpy.run_path(str(ROOT/'scripts/build-equiano.py'))['render'](), 'Generated page is stale'
assert len(parsed.ids)==len(set(parsed.ids)), 'Duplicate page anchors'
assert set(('maps','chapter-one','chapter-two','water','films','images','identity','context','vocabulary','sources'))<=set(parsed.ids)
assert all(i.get('alt') and i.get('width') and i.get('height') for i in parsed.images), 'Images need descriptions and dimensions'
for link in parsed.links:
    url=urlsplit(link)
    if url.scheme or url.netloc:continue
    if not url.path:
        assert url.fragment in parsed.ids, f'Missing anchor: {link}'
    else:
        target=(PAGE.parent/unquote(url.path)).resolve()
        assert target.is_relative_to(ROOT) and target.exists(), f'Missing or non-public file: {link}'
for forbidden in ('/Users/','127.0.0.1','teaching-notes/private','Mock-Filled','{{CHAPTERS}}','{{SHIP}}','{{FILMS}}'):
    assert forbidden not in text, f'Unexpected private path or build token: {forbidden}'
assets=PAGE.parent/'equiano-assets'
for file in (assets/'map-data').glob('*.geojson'):
    data=json.loads(file.read_text());assert data['type']=='FeatureCollection' and data['features']
ledger=json.loads((assets/'images/sources.json').read_text())
assert len(ledger['images'])==3
for im in ledger['images']:
    assert (assets/'images'/im['file']).exists() and im['source_url'] and im['rights']
for pdf in ('meeting-20-worksheet.pdf','equiano-chapters-1-2-map.pdf'):
    assert (assets/pdf).read_bytes().startswith(b'%PDF'),f'Invalid PDF: {pdf}'
course=json.loads((ROOT/'data/frst-110.json').read_text())
def meetings(obj):
    if isinstance(obj,dict):
        if obj.get('date')=='2026-10-28' and 'materials' in obj:yield obj
        for item in obj.values():yield from meetings(item)
    elif isinstance(obj,list):
        for item in obj:yield from meetings(item)
day=list(meetings(course));assert len(day)==1
assert any(m['href']==URL for m in day[0]['materials']), 'Course-day link missing'
assert URL in (ROOT/'courses/frst-110.html').read_text(), 'Generated course-day link missing'
print('Equiano page: source build, anchors, images, downloads, map data, privacy boundaries, and October 28 course link verified.')
