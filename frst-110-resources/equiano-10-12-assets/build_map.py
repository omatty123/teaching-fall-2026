#!/usr/bin/env python3
"""Insert the voyages map into equiano-chapters-10-12.html.

Places and dates: Equiano, Interesting Narrative, Vol. II, Ch. X-XII
(Project Gutenberg #15399). Routes run through open-water waypoints and show
the order of ports, not exact tracks. Same Leaflet + Esri Light Gray setup as
the Chapter 9 page. Re-run after editing; it replaces the block between the
map markers.
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE.parent / "equiano-chapters-10-12.html"

P = {  # (lon, lat)
    "London": (-0.08, 51.50), "Plymouth": (-4.14, 50.37), "Cadiz": (-6.29, 36.53),
    "Gibraltar": (-5.35, 36.14), "Malaga": (-4.42, 36.72), "Antigua": (-61.80, 17.07),
    "Montserrat": (-62.20, 16.72), "Kingston, Jamaica": (-76.79, 17.97),
    "Cape Gracias a Dios": (-83.16, 15.00), "Carthagena": (-75.51, 10.39),
    "New York": (-74.01, 40.70), "Philadelphia": (-75.14, 39.95), "Sierra Leone": (-13.23, 8.48),
}
CHANNEL_OUT = [P["London"], (1.4, 51.45), (1.5, 51.0), (-1.5, 50.2), (-5.8, 49.0)]
TO_CADIZ = CHANNEL_OUT + [(-10.0, 44.0), (-10.0, 38.7), (-9.0, 36.7), (-6.6, 36.45), P["Cadiz"]]
HOME_FROM_SPAIN = [(-9.4, 36.6), (-10.6, 40.0), (-10.0, 44.5), (-5.8, 48.9), (-1.5, 50.2), (1.5, 51.0), (1.4, 51.45), P["London"]]

VOYAGES = [
    dict(n=1, year="1774", title="Cadiz, on the Hope",
         stops="London · Cadiz · London",
         text="Steward under Captain Richard Strange. They reach Cadiz on 23 September. In October, at Cadiz, he is converted.",
         path=TO_CADIZ, badge=(-12.5, 41.0), labels=["London", "Cadiz"]),
    dict(n=2, year="1775", title="Cadiz, Gibraltar, Malaga",
         stops="London · Cadiz · Gibraltar · Malaga · London",
         text="The ship strikes a rock entering the Bay of Cadiz. At Malaga he admires the cathedral and argues with a priest. Going home they pick up eleven Portuguese sailors whose brig has sunk.",
         path=TO_CADIZ + [(-6.1, 36.2), (-5.45, 36.03), P["Gibraltar"], (-5.0, 36.3), P["Malaga"],
                          (-5.0, 36.25), (-5.6, 35.95)] + HOME_FROM_SPAIN,
         badge=(-2.0, 38.6), labels=["Cadiz", "Gibraltar", "Malaga"]),
    dict(n=3, year="1775–76", title="Jamaica and the Miskito Shore",
         stops="London · Antigua · Montserrat · Jamaica · Cape Gracias a Dios",
         text="With Dr. Irving and Prince George on the Morning Star. In Jamaica they buy enslaved Africans for the plantation; Equiano chooses his own countrymen.",
         path=CHANNEL_OUT + [(-12.0, 45.0), (-30.0, 28.0), (-55.0, 18.5), (-61.4, 17.4), P["Antigua"],
                             (-62.0, 16.95), P["Montserrat"], (-63.0, 16.4), (-68.0, 16.3), (-74.0, 17.2),
                             (-76.3, 17.75), P["Kingston, Jamaica"], (-77.2, 17.6), (-79.5, 16.4),
                             (-82.0, 15.4), (-82.9, 15.1), P["Cape Gracias a Dios"]],
         badge=(-40.0, 25.5), labels=["London", "Antigua", "Montserrat", "Kingston, Jamaica", "Cape Gracias a Dios"]),
    dict(n=4, year="1776", title="Toward Carthagena, then Jamaica",
         stops="Miskito Shore · nearly to Carthagena · Kingston",
         text="Hughes hoists him by ropes and swears he will sell him at Carthagena; he escapes in a canoe. The next captain also trades south along the coast. In Kingston nine magistrates refuse his oath.",
         path=[P["Cape Gracias a Dios"], (-82.9, 14.0), (-82.8, 12.6), (-82.0, 11.3), (-79.5, 10.2),
               (-77.0, 10.35), (-76.4, 10.75), (-76.2, 11.4), (-76.4, 14.0),
               (-76.85, 17.4), P["Kingston, Jamaica"]],
         badge=(-80.5, 12.2), labels=["Cape Gracias a Dios", "Carthagena", "Kingston, Jamaica"]),
    dict(n=5, year="1776–77", title="Home to England",
         stops="Kingston · Plymouth · London",
         text="He sails home with a fleet and lands at Plymouth on 7 January 1777, then goes to London.",
         path=[P["Kingston, Jamaica"], (-75.6, 17.6), (-74.3, 19.0), (-73.9, 20.2), (-73.4, 22.6),
               (-70.0, 27.5), (-50.0, 38.5), (-22.0, 47.0), (-8.0, 49.4), (-4.3, 50.2), P["Plymouth"],
               (-3.0, 50.2), (-1.5, 50.4), (1.5, 51.0), (1.4, 51.45), P["London"]],
         badge=(-47.0, 41.0), labels=["Kingston, Jamaica", "Plymouth", "London"]),
    dict(n=6, year="1784–86", title="New York and Philadelphia",
         stops="London · New York (1784) · Philadelphia (1785 and 1786)",
         text="Steward on the London to New York, then twice to Philadelphia, where he is glad to see the Quakers “freeing and easing the burthens” of Africans.",
         path=CHANNEL_OUT + [(-12.0, 48.5), (-30.0, 46.0), (-50.0, 42.0), (-68.0, 39.8), (-72.5, 40.2),
                             (-73.9, 40.45), P["New York"], (-73.6, 40.2), (-74.4, 39.2), (-74.9, 38.8),
                             (-75.25, 39.2), (-75.45, 39.6), P["Philadelphia"]],
         badge=(-35.0, 48.5), labels=["London", "New York", "Philadelphia"]),
    dict(n=7, year="1787", title="Sierra Leone, without him",
         stops="England · Sierra Leone",
         text="He is commissary for the expedition, reports the missing stores, and is dismissed in March 1787. The ships sail without him.",
         path=CHANNEL_OUT + [(-10.0, 45.0), (-15.0, 35.0), (-18.5, 22.0), (-17.8, 14.7), (-15.0, 9.6), P["Sierra Leone"]],
         badge=(-21.0, 18.0), labels=["Sierra Leone"], dashed=True),
]


def sample(pts, n=10):
    out = []
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        for k in range(n):
            t = k / n
            x, y = (0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                           + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1))
            out.append([round(y, 3), round(x, 3)])
    out.append([pts[-1][1], pts[-1][0]])
    return out


def block():
    data = {"voyages": [{"n": v["n"], "line": sample(v["path"]), "badge": [v["badge"][1], v["badge"][0]],
                         "labels": v["labels"], "dashed": v.get("dashed", False)} for v in VOYAGES],
            "places": {k: [lat, lon] for k, (lon, lat) in P.items()}}
    items = "\n".join(
        f'<li><button type="button" data-v="{v["n"]}" aria-pressed="false"><span class="num">{v["n"]}</span>'
        f'<span><b>{v["year"]} · {v["title"]}</b><span class="stops">{v["stops"]}</span></span></button>'
        f'<p>{v["text"]}</p></li>' for v in VOYAGES)
    return f'''<!-- map:start -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<style>
#voyages .map-top{{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:22px;align-items:start}}
#voyage-map{{height:560px;border:1px solid #c4cecb;background:#f4f4f4}}
#voyages .leaflet-container{{font:inherit}}#voyages .leaflet-control-attribution{{font-size:10px!important}}
#voyages ol{{list-style:none;margin:0;padding:0}}#voyages li{{border-bottom:1px solid #dce2e0;padding:6px 0}}
#voyages li button{{display:flex;gap:10px;align-items:flex-start;width:100%;text-align:left;background:none;border:0;padding:4px 0;font:inherit;color:inherit;cursor:pointer}}
#voyages li button[aria-pressed="true"] b{{text-decoration:underline}}
#voyages .num,.vbadge{{flex:none;display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;background:#203136;color:#fff;font-size:12px;font-weight:700}}
.vbadge{{border:2px solid #fff;cursor:pointer}}.vbadge.on{{background:#000;transform:scale(1.15)}}
#voyages .stops{{display:block;font-size:13.5px;color:#4c5859}}#voyages li p{{margin:2px 0 4px 32px;font-size:14.5px}}
#voyages .lbl{{font-size:12px;padding:1px 5px}}
#voyages .note{{font-size:13px;color:#4c5859}}
@media(max-width:820px){{#voyages .map-top{{grid-template-columns:minmax(0,1fr)}}#voyage-map{{height:420px}}}}
@media print{{#voyage-map{{height:420px}}}}
</style>
<section id="voyages">
<h2>Voyages, 1774–1787</h2>
<p class="note">Choose a voyage to see its route and ports. Routes show the order of ports, not the exact tracks. The dashed line is the Sierra Leone expedition, which sailed without him.</p>
<div class="map-top">
<div id="voyage-map" role="region" aria-label="Map of Equiano’s voyages in Chapters X to XII"></div>
<ol>
{items}
</ol>
</div>
</section>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
(function(){{
const D={json.dumps(data, ensure_ascii=False, separators=(",", ":"))};
const map=L.map('voyage-map',{{scrollWheelZoom:false,zoomSnap:0.25}});
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}',
 {{maxZoom:10,attribution:'Base map: Esri, HERE, Garmin, © OpenStreetMap contributors'}}).addTo(map);
map.attributionControl.setPrefix(false);
const lines={{}},badges={{}},all=[];
D.voyages.forEach(v=>{{
 lines[v.n]=L.polyline(v.line,{{color:'#2f3b3d',weight:2,opacity:.85,dashArray:v.dashed?'6 6':null}}).addTo(map).on('click',()=>pick(v.n));
 badges[v.n]=L.marker(v.badge,{{icon:L.divIcon({{className:'',html:'<div class="vbadge" data-v="'+v.n+'">'+v.n+'</div>',iconSize:[22,22],iconAnchor:[11,11]}}),keyboard:false}}).addTo(map).on('click',()=>pick(v.n));
 all.push(...v.line);
}});
Object.values(D.places).forEach(ll=>L.circleMarker(ll,{{radius:4,color:'#111',weight:1.5,fillColor:'#fff',fillOpacity:1}}).addTo(map));
const tips=L.layerGroup().addTo(map);
const full=L.latLngBounds(all).pad(0.04);map.fitBounds(full);
let cur=null;
function pick(n){{
 n=(cur===n)?null:n;cur=n;tips.clearLayers();
 document.querySelectorAll('#voyages li button').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.v===n)));
 Object.entries(lines).forEach(([k,l])=>l.setStyle({{color:n===null||+k===n?'#000':'#9aa5a4',weight:n!==null&&+k===n?3.5:2,opacity:n===null||+k===n?.9:.5}}));
 document.querySelectorAll('.vbadge').forEach(b=>b.classList.toggle('on',+b.dataset.v===n));
 if(n===null){{map.fitBounds(full);return}}
 const v=D.voyages.find(x=>x.n===n);
 v.labels.forEach(p=>tips.addLayer(L.tooltip({{permanent:true,direction:'right',offset:[6,0],className:'lbl'}}).setLatLng(D.places[p]).setContent(p)));
 map.fitBounds(L.latLngBounds(v.line).pad(0.15));
}}
document.querySelectorAll('#voyages li button').forEach(b=>b.addEventListener('click',()=>pick(+b.dataset.v)));
}})();
</script>
<!-- map:end -->
'''


def main():
    s = PAGE.read_text()
    s = re.sub(r"<!-- map:start -->.*?<!-- map:end -->\n", "", s, flags=re.S)
    s = s.replace('<section id="passages">', block() + '\n<section id="passages">', 1)
    if '<a href="#voyages">' not in s:
        s = s.replace('<a href="#passages">Passages</a>', '<a href="#voyages">Voyages</a>\n<a href="#passages">Passages</a>', 1)
    PAGE.write_text(s)
    print(PAGE, f"{len(s)/1024:.0f} KB")


if __name__ == "__main__":
    main()
