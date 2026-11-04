#!/usr/bin/env python3
"""Modern-reference locator maps, no territorial/route reconstruction.
Natural Earth public-domain vectors; coordinates/provenance in map-sources.md.
Run: python3 scripts/build-hist-nov5-maps.py [--data-dir CACHE]
Default cache is outside the repository. Source downloads are only made if absent.
"""
import argparse,html,json,math,tempfile,urllib.request
from pathlib import Path
P=argparse.ArgumentParser();P.add_argument('--data-dir',type=Path,default=Path(tempfile.gettempdir())/'hist-nov5-map-data');A=P.parse_args()
A.data_dir.mkdir(parents=True,exist_ok=True)
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'images/hist/nov5';OUT.mkdir(parents=True,exist_ok=True)
NE={}
for name in ['land','lakes','rivers_lake_centerlines']:
 path=A.data_dir/f'ne_10m_{name}.geojson'
 if not path.exists():path.write_bytes(urllib.request.urlopen('https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'+path.name).read())
 NE[name]=json.loads(path.read_text())['features']
INK='#23323a';MUTED='#56666b';LAND='#f1efe7';WATER='#eff6f8';COAST='#a6b6ba';RIVER='#40849d';DOT='#7a3030'
def text(x,y,s,size=25,color=INK,anchor='start',weight=400):
 attrs=f'x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}"'
 return f'<g><text {attrs} fill="none" stroke="white" stroke-width="5" stroke-linejoin="round" aria-hidden="true">{html.escape(s)}</text><text {attrs} fill="{color}">{html.escape(s)}</text></g>' 
def points(g):
 c=g['coordinates'];t=g['type']
 return c if t in ['Polygon','MultiLineString'] else [r for p in c for r in p] if t=='MultiPolygon' else [c] if t=='LineString' else []
class Map:
 def __init__(self,w,h,b,title,desc):
  self.w,self.h,self.b=w,h,b;self.k=math.cos(math.radians((b[1]+b[3])/2));self.s=min((w-76)/((b[2]-b[0])*self.k),(h-148)/(b[3]-b[1]));self.ox=(w-(b[2]-b[0])*self.k*self.s)/2;self.oy=66;self.mw=(b[2]-b[0])*self.k*self.s;self.mh=(b[3]-b[1])*self.s
  self.o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc><style>text{{font-family:Arial,Helvetica,sans-serif}}</style><rect width="{w}" height="{h}" fill="white"/><defs><clipPath id="extent"><rect x="{self.ox}" y="{self.oy}" width="{self.mw}" height="{self.mh}"/></clipPath></defs>',text(38,38,title,29,weight=600),f'<g clip-path="url(#extent)"><rect x="{self.ox}" y="{self.oy}" width="{self.mw}" height="{self.mh}" fill="{WATER}"/>']
 def proj(self,lon,lat):return self.ox+(lon-self.b[0])*self.k*self.s,self.oy+(self.b[3]-lat)*self.s
 def poly(self,ring):
  q=[tuple(p[:2]) for p in ring]
  for axis,val,pos in [(0,self.b[0],True),(0,self.b[2],False),(1,self.b[1],True),(1,self.b[3],False)]:
   if not q:break
   out=[];prev=q[-1];pi=(prev[axis]>=val if pos else prev[axis]<=val)
   for cur in q:
    ci=(cur[axis]>=val if pos else cur[axis]<=val)
    if ci!=pi:
     t=(val-prev[axis])/(cur[axis]-prev[axis]);out.append(tuple(prev[i]+t*(cur[i]-prev[i]) for i in [0,1]))
    if ci:out.append(cur)
    prev,pi=cur,ci
   q=out
  return [q] if q else []
 def lines(self,line):
  groups=[];current=[]
  for p0,p1 in zip(line,line[1:]):
   x0,y0=p0[:2];x1,y1=p1[:2];dx=x1-x0;dy=y1-y0;lo,hi=0.,1.;ok=True
   for u,v in [(-dx,x0-self.b[0]),(dx,self.b[2]-x0),(-dy,y0-self.b[1]),(dy,self.b[3]-y0)]:
    if u==0:
     if v<0:ok=False;break
    else:
     r=v/u
     if u<0:lo=max(lo,r)
     else:hi=min(hi,r)
     if lo>hi:ok=False;break
   if ok:
    aa=(x0+lo*dx,y0+lo*dy);bb=(x0+hi*dx,y0+hi*dy)
    if current and abs(current[-1][0]-aa[0])+abs(current[-1][1]-aa[1])<1e-8:current.append(bb)
    else:
     if current:groups.append(current)
     current=[aa,bb]
   elif current:groups.append(current);current=[]
  if current:groups.append(current)
  return groups
 def geom(self,g,fill,stroke,sw):
  paths=[];poly='Polygon' in g['type']
  for ring in points(g):
   # Skip distant geometry before clipping.
   if not ring:continue
   if max(p[0] for p in ring)<self.b[0] or min(p[0] for p in ring)>self.b[2] or max(p[1] for p in ring)<self.b[1] or min(p[1] for p in ring)>self.b[3]:continue
   for cut in (self.poly(ring) if poly else self.lines(ring)):
    pp=[];last=None
    for ll in cut:
     p=self.proj(*ll[:2])
     if last is None or math.hypot(p[0]-last[0],p[1]-last[1])>.45:pp.append(p);last=p
    if len(pp)>1:paths.append('M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pp)+(' Z' if poly else ''))
  if paths:self.o.append(f'<path d="{" ".join(paths)}" fill="{fill}" fill-rule="evenodd" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')
 def base(self,rivers):
  for f in NE['land']:self.geom(f['geometry'],LAND,COAST,1.15)
  for f in NE['lakes']:
   if f['properties'].get('featurecla')=='Lake':self.geom(f['geometry'],WATER,COAST,.7)
  for f in NE['rivers_lake_centerlines']:
   if f['properties'].get('name') in rivers:self.geom(f['geometry'],'none',RIVER,2)
  self.o.append('</g>')
 def label(self,lon,lat,s,**kw):self.o.append(text(*self.proj(lon,lat),s,**kw))
 def city(self,lon,lat,label,dx=14,dy=-12,detail=None,approx=False):
  x,y=self.proj(lon,lat);tx,ty=x+dx,y+dy;anchor='end' if dx<0 else 'start'
  if abs(dx)>30 or abs(dy)>30:self.o.append(f'<path d="M{x:.1f},{y:.1f} L{tx:.1f},{ty-8:.1f}" stroke="{DOT}" stroke-width="1.3" fill="none"/>')
  self.o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{"white" if approx else DOT}" stroke="{DOT}" stroke-width="2"/>');self.o.append(text(tx,ty,label,27,anchor=anchor,weight=600))
  if detail:self.o.append(text(tx,ty+29,detail,23,color=MUTED,anchor=anchor))
 def finish(self,filename,caption,scale):
  self.o.append(f'<rect x="{self.ox}" y="{self.oy}" width="{self.mw}" height="{self.mh}" fill="none" stroke="#c3cdd0"/>')
  self.o.append(text(self.ox+self.mw-22,self.oy+38,'N',22,anchor='middle',weight=600))
  self.o.append(f'<path d="M{self.ox+self.mw-22} {self.oy+74} v-26 m-5 7 l5 -7 l5 7" fill="none" stroke="{INK}" stroke-width="2"/>')
  x=self.ox+28;y=self.oy+self.mh-22;length=scale/111.195*self.s
  self.o.append(f'<path d="M{x} {y-6} v12 m0 -6 h{length} m0 -6 v12" stroke="{INK}" stroke-width="2" fill="none"/>');self.o.append(text(x+length/2,y-12,f'{scale:,} km at {((self.b[1]+self.b[3])/2):.0f}°N',20,anchor='middle'))
  self.o.extend([text(38,self.h-49,caption,22,color=MUTED),text(38,self.h-19,'Natural Earth · modern coastlines and river courses · locator points, not political boundaries',20,color=MUTED),'</svg>'])
  (OUT/filename).write_text('\n'.join(self.o))
m=Map(1600,850,(48,20,144,58),'Mongolia, Central Asia and Goryeo','Modern-reference locator of the places in the November 5 readings: Karakorum, Central Asian cities, north China and Goryeo. No territorial boundaries or routes are reconstructed.')
m.base({'Huang','Yangtze','Chang Jiang','Wei','Amu Darya','Syr  Darya','Yalu','Tumen'})
m.label(90,52.7,'MONGOLIAN PLATEAU',size=30,color=MUTED,weight=600)
m.label(68,47,'CENTRAL ASIA',size=29,color=MUTED,weight=600)
m.label(110,34,'NORTH CHINA',size=25,color=MUTED,weight=600)
m.label(130,32,'GORYEO',size=25,color=MUTED,weight=600)
m.label(75,25,'INDIA',size=25,color=MUTED)
m.label(54,27.3,'Persian Gulf',size=23,color=RIVER)
m.label(132,41,'East Sea',size=23,color=RIVER)
m.label(107,42.7,'Yellow River',size=22,color=RIVER)
m.label(107,28.4,'Yangzi River',size=22,color=RIVER)
m.city(102.847989,47.20954,'Karakorum',dy=-14,detail='Mongol imperial center')
m.city(64.42861,39.77472,'Bukhara',dx=-16,dy=-14)
m.city(67,39.66889,'Samarkand',dx=20,dy=31)
m.city(62.20,34.35,'Herat',dx=-15,dy=24)
m.city(116.40,39.90,'Beijing',dx=-10,dy=-15,detail='Jin capital taken in 1215')
m.city(126.55,37.97,'Kaesong',dx=17,dy=22)
x1,y1=m.proj(122,42.7);x2,y2=m.proj(132.5,33.1);m.o.append(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="none" stroke="#7a3030" stroke-dasharray="7 5" stroke-width="1.5"/>')
m.finish('eurasia-map.svg','Dashed box: Korean peninsula detail below. Cities are locators; no campaign routes are implied.',1000)
k=Map(1200,1050,(122,33.1,132.5,42.7),'Goryeo: court, fortress and surviving woodblocks','The Korean peninsula with Kuju near modern Kusong, Kaesong, Ganghwa Island and Haeinsa. Yalu, Tumen, Han and Nakdong rivers provide modern reference geography. The map does not show a reconstructed Goryeo frontier.')
k.base({'Yalu','Tumen','Han','Namhan','Nakdong'})
k.label(127.1,40.3,'KOREAN PENINSULA',size=27,color=MUTED,weight=600)
k.label(123.4,36.1,'Yellow Sea',size=25,color=RIVER)
k.label(130.5,38.3,'East Sea',size=25,color=RIVER)
k.label(124.8,41.6,'Yalu River',size=23,color=RIVER)
k.label(129.45,42.1,'Tumen',size=23,color=RIVER)
k.label(128.55,37.3,'Han River',size=23,color=RIVER)
k.label(129,35,'Nakdong',size=23,color=RIVER)
k.city(125.24,39.98,'Kuju',dx=-20,dy=-13,detail='near modern Kusŏng',approx=True)
k.city(126.55,37.97,'Kaesong',dx=26,dy=-38,detail='Gaegyeong: royal capital')
k.city(126.485237,37.751632,'Ganghwa Island',dx=-66,dy=62,detail='court moved here in 1232')
k.city(128.098711,35.801672,'Haeinsa',dx=18,dy=-12,detail='woodblocks preserved here today')
k.finish('goryeo-map.svg','Open circle: approximate Kuju locator. Haeinsa is the present repository, not the carving site.',100)
print('Built',OUT/'eurasia-map.svg',OUT/'goryeo-map.svg')
