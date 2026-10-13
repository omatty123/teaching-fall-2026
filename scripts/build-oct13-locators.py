"""North-up classroom locators from Natural Earth 110m land (public domain)."""
import json, math
from pathlib import Path
root=Path(__file__).resolve().parents[1]; out=root/'images/hist/oct13'
data=json.loads((out/'locator-land.geojson').read_text())
def project(lon,lat):return ((lon-89)*10,(49-lat)*12.5)
paths=[]
for f in data['features']:
 polys=f['geometry']['coordinates']
 if f['geometry']['type']=='Polygon':polys=[polys]
 for poly in polys:
  if not any(85<x<150 and 15<y<55 for x,y in poly[0]):continue
  paths.append(' '.join(('M' if i==0 else 'L')+f'{project(x,y)[0]:.1f},{project(x,y)[1]:.1f}' for i,(x,y) in enumerate(poly[0]))+'Z')
places=[('Dunhuang',94.81667,40.13333,'#087f83',8,-14),('Yungang',113.12222,40.10972,'#087f83',-12,-14),('Mount Lu',115.86667,29.43333,'#087f83',-94,32),('Gyeongju',129.2,35.8,'#b44b2b',12,8)]
for focus in ['all','china','silla','dunhuang']:
 s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 550 350" role="img" aria-labelledby="title desc"><title id="title">East Asia: places in today’s lesson</title><desc id="desc">North-up locator: Dunhuang west of Yungang; Mount Lu in southern China; Gyeongju on the southeastern Korean peninsula. Generalized modern coastlines, no historical borders or routes.</desc><defs><clipPath id="extent"><rect width="550" height="350"/></clipPath></defs><style>text{font-family:Arial,Helvetica,sans-serif;fill:#25454a;font-size:23px}.place{font-weight:700;paint-order:stroke;stroke:#edf5f4;stroke-width:4;stroke-linejoin:round}.region{font-size:24px;fill:#607a7c}.note{font-size:16px}</style><rect width="550" height="350" fill="#e6f1f5"/><g clip-path="url(#extent)" fill="#f2eee1" stroke="#9caeac" stroke-width="1.2">']
 s += [f'<path d="{p}"/>' for p in paths];s+=['</g><text class="region" x="140" y="218">CHINA</text><text class="region" x="442" y="254" transform="rotate(-40 442 254)">JAPAN</text>']
 for name,lon,lat,color,dx,dy in places:
  active=focus=='all' or focus=='china' and name in ['Mount Lu','Yungang'] or focus=='silla' and name=='Gyeongju' or focus=='dunhuang' and name=='Dunhuang'
  x,y=project(lon,lat);c=color if active else '#667b7c'
  s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{7 if active else 4}" fill="{c}" stroke="white" stroke-width="2"/><text class="place" x="{x+dx:.1f}" y="{y+dy:.1f}" style="fill:{c}">{name}</text>')
 s+=['<text class="note" x="18" y="324">N ↑ · 1,000 km at 35°N</text><path d="M18 294v6h110v-6" fill="none" stroke="#25454a" stroke-width="2"/><text class="note" x="300" y="324">Generalized coastlines</text></svg>']
 (out/f'locator-{focus}.svg').write_text(''.join(s))
