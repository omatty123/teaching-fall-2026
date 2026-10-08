from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
root=Path(__file__).resolve().parents[1]
page=root/'hist-212-resources/class-2026-10-08.html'
class Check(HTMLParser):
 def __init__(self): super().__init__(); self.ids=set(); self.links=[]; self.marks=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   assert a['id'] not in self.ids, 'Duplicate ID'; self.ids.add(a['id'])
  if tag=='mark': self.marks+=1
  for key in ('href','src'):
   if key in a:self.links.append(a[key])
c=Check(); text=page.read_text(); c.feed(text)
for url in c.links:
 u=urlsplit(url)
 if u.scheme or u.netloc:continue
 if not u.path:assert u.fragment in c.ids, url
 else:assert (page.parent/unquote(u.path)).is_file(), url
assert c.marks>=10
assert all(x in text for x in ('thirteen numbers','Li Si','Lu Jia','Jia Yi','Dong Zhongshu','Lady Dai','Salt and Iron'))
assert all(x not in text for x in ('/Users/','private-data','only you','Review this draft'))
print('HIST lesson: anchors, local assets, highlights and public-content boundaries passed.')
