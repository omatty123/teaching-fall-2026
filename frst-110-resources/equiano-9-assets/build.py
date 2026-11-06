#!/usr/bin/env python3
"""Build equiano-chapter-9.html: voyage maps + seven-word quiz for Equiano, Chapter IX.

Map: Leaflet with Esri Light Gray Base tiles. Routes were checked against
Natural Earth 10m land so they stay on open water (Thames excepted).
Places and dates: Equiano, Interesting Narrative, Vol. II, Ch. IX
(Project Gutenberg #15399). Routes are drawn through open-water waypoints;
they show the order of ports, not exact tracks.
"""
import html, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "equiano-chapter-9.html"

# ---------- places (lon, lat) ----------
P = {
    "Savannah": (-81.09, 32.08), "St. Pierre": (-61.18, 14.74), "Grenada": (-61.75, 12.05),
    "St. Eustatius": (-62.98, 17.48), "Basseterre": (-62.72, 17.30), "Montserrat": (-62.20, 16.72),
    "London": (-0.08, 51.50), "Villefranche": (7.31, 43.70), "Nice": (7.27, 43.70),
    "Leghorn": (10.31, 43.55), "Smyrna": (27.14, 38.42), "Oporto": (-8.61, 41.15),
    "Genoa": (8.93, 44.41), "Naples": (14.25, 40.84), "Madeira": (-16.91, 32.65),
    "Barbados": (-59.62, 13.10), "Nevis": (-62.62, 17.14), "Kingston": (-76.79, 17.97),
    "Port Morant": (-76.33, 17.89), "Sheerness": (0.76, 51.44), "Shetland": (-1.2, 60.3),
    "Farthest north": (19.5, 80.6), "Orfordness": (1.57, 52.08),
}

# ---------- shared sea lanes ----------
CHANNEL_OUT = [P["London"], (1.4, 51.45), (1.5, 51.0), (-1.5, 50.2), (-5.8, 48.7)]
TO_GIB = CHANNEL_OUT + [(-10.0, 43.5), (-10.0, 38.7), (-9.4, 36.6), (-5.6, 35.95)]
GIB_TO_LIGURIA = [(-2.0, 36.4), (1.2, 37.6), (5.0, 39.2), (6.8, 42.0)]
TO_SMYRNA = [(15.55, 38.75), (15.70, 38.31), (15.67, 38.265), (15.63, 38.235), (15.60, 38.19), (15.58, 38.10),
             (15.56, 37.98), (15.75, 37.75), (16.4, 37.45), (21.0, 36.2), (23.4, 36.1), (24.8, 36.05), (26.0, 36.15), (26.22, 36.7), (26.28, 37.15), (25.75, 37.45),
             (25.7, 37.8), (25.7, 38.35), (25.85, 38.75), (26.4, 38.8), (26.8, 38.55), P["Smyrna"]]
HOME_FROM_WEST = [(-60.0, 22.0), (-48.0, 34.0), (-28.0, 45.0), (-10.0, 48.8),
                  (-5.8, 48.9), (-1.5, 50.2), (1.5, 51.0), (1.4, 51.45), P["London"]]

VOYAGES = [
    dict(n=1, year="1767", title="Leaving the West Indies",
         stops="Georgia · Martinique · the Grenades · St. Eustatius · St. Kitts · Montserrat · London",
         text="In St. Kitts a captain will not take him on board until he will “advertise” himself “like a slave.” "
              "Robert King writes him a certificate. Seven weeks later he is back in London.",
         path=[P["Savannah"], (-78.0, 30.0), (-68.0, 22.0), (-61.75, 15.35), P["St. Pierre"], (-61.6, 13.6),
               (-61.9, 12.6), P["Grenada"], (-62.2, 13.5), (-62.6, 16.0), (-63.15, 17.3), P["St. Eustatius"],
               P["Basseterre"], (-62.70, 16.98), P["Montserrat"], (-61.9, 17.6)] + HOME_FROM_WEST,
         badge={"overview": (-40, 39.0), "caribbean": (-62.25, 14.2)}),
    dict(n=2, year="1768–69", title="Italy and Turkey",
         stops="London · Villefranche · Nice · Leghorn · the Archipelago · Smyrna · London",
         text="Hairdresser to Captain John Jolly on the Delawar. About five months in Smyrna, where he sees the Greeks "
              "“kept under by the Turks, as the negroes are in the West Indies by the white people.”",
         path=TO_GIB + GIB_TO_LIGURIA + [P["Villefranche"], (8.0, 43.6), (9.3, 43.6), P["Leghorn"],
               (10.0, 43.25), (9.95, 42.6), (10.4, 41.9), (12.3, 39.6), (14.4, 39.1)] + TO_SMYRNA,
         badge={"overview": (20.0, 36.2), "med": (12.0, 38.8)}),
    dict(n=3, year="1769", title="Oporto",
         stops="London · Oporto · London",
         text="Carnival time. The Inquisition searches the ship for Bibles; anyone hiding one could be "
              "“imprisoned and flogged, and sent into slavery for ten years.”",
         path=CHANNEL_OUT + [(-9.8, 44.0), (-9.4, 41.15), P["Oporto"]],
         badge={"overview": (-13.0, 44.5), "med": (-7.6, 45.0)}),
    dict(n=4, year="1769–70", title="Genoa, Naples, Smyrna",
         stops="London · Genoa · Naples · Smyrna · London",
         text="Genoa’s marble is “disgraced by the galley slaves.” Vesuvius erupts at Naples and the ash lies on deck. "
              "Plague in Smyrna. Going home, a cook’s pan of fat nearly burns the ship.",
         path=TO_GIB + GIB_TO_LIGURIA + [(8.4, 43.9), P["Genoa"], (9.3, 43.9), (9.9, 43.3), (9.95, 42.6), (10.4, 41.9),
               (13.0, 40.5), (14.05, 40.62), P["Naples"], (14.1, 40.5), (14.7, 39.7)] + TO_SMYRNA,
         badge={"overview": (8.0, 39.0), "med": (5.6, 42.2)}),
    dict(n=5, year="1771", title="Madeira, Barbados, Grenada",
         stops="London · Madeira · Barbados · Grenada · London",
         text="Steward on the Grenada Planter. A white buyer will not pay, and a justice of the peace gives free Black "
              "men no remedy. Equiano and three unpaid white sailors collect by force.",
         path=CHANNEL_OUT + [(-11.0, 45.0), (-16.6, 33.4), P["Madeira"], (-30.0, 22.0), (-50.0, 14.5),
               P["Barbados"], (-60.6, 12.6), P["Grenada"], (-61.3, 12.3), (-60.3, 13.6), (-59.9, 16.0)] + HOME_FROM_WEST,
         badge={"overview": (-34.0, 18.5), "caribbean": (-60.2, 12.4)}),
    dict(n=6, year="1771–72", title="Nevis and Jamaica",
         stops="London · Nevis · Jamaica (Port Morant, Kingston) · London",
         text="Steward on the Jamaica. Cruel punishments; a buyer at Port Morant who threatens instead of paying; "
              "Sunday dances at Spring Path, Kingston, where Africans “retain most of their native customs.”",
         path=CHANNEL_OUT + [(-12.0, 45.0), (-30.0, 27.0), (-55.0, 18.0), (-62.0, 17.8), P["Nevis"],
               (-63.0, 16.9), (-68.0, 16.5), (-74.0, 17.2), (-76.2, 17.75), P["Port Morant"],
               (-76.8, 17.85), P["Kingston"], (-75.6, 17.6), (-74.3, 19.0), (-73.9, 20.2), (-73.4, 22.6),
               (-70.0, 27.5), (-50.0, 38.0), (-22.0, 47.5), (-10.0, 48.8)] + HOME_FROM_WEST[4:],
         badge={"overview": (-58.0, 27.5), "caribbean": (-71.5, 16.2)}),
    dict(n=7, year="1773", title="Toward the North Pole",
         stops="Deptford · Sheerness · Shetland · Spitsbergen (his “Greenland”) · Deptford",
         text="With Dr. Irving on the Race Horse under Captain Phipps, looking for a passage to India. A fire in the tow "
              "and aquafortis off Shetland, sea-horses, nine bears, and eleven days frozen in the ice near 80° north.",
         path=[P["London"], P["Sheerness"], (2.2, 52.6), (2.0, 56.0), (0.3, 59.6), (0.0, 61.2), (3.0, 65.0),
               (6.5, 70.0), (9.0, 75.5), (9.8, 78.2), (11.0, 79.95), (15.5, 80.45), P["Farthest north"]],
         badge={"overview": (-2.5, 70.0)}),
]

# ---------- quiz ----------
# chapter order; letter = position in DEFS
WORDS = [
    ("victuals", "we on board had little or no <b>victuals</b> allowed us, and I could not get my money nor wages"),
    ("advertising", "this degrading necessity, which every black freeman is under, of <b>advertising</b> himself like a slave, when he leaves an island"),
    ("assiduity", "he has always behaved himself well, and discharged his duty with honesty and <b>assiduity</b>"),
    ("aquafortis", "This little place was stuffed with all manner of combustibles, particularly with tow and <b>aquafortis</b>, and many other dangerous things."),
    ("tow", "a spark having touched a single thread of the <b>tow</b>, all the rest caught the flame"),
    ("sea-horses", "One morning we had vast quantities of <b>sea-horses</b> about the ship, which neighed exactly like any other horses."),
    ("blasphemers", "many, who had been before <b>blasphemers</b>, in this our distress began to call on the good God of heaven for his help"),
]
DEFS = [
    ("tow", "loose, coarse fibers of flax or hemp, used for rope and stuffing; they catch fire easily"),
    ("blasphemers", "people who speak with disrespect of God or sacred things"),
    ("victuals", "food and drink; provisions"),
    ("sea-horses", "walruses"),
    ("advertising", "giving public notice, posted or printed, that a person is leaving the island"),
    ("aquafortis", "nitric acid (“strong water”), a corrosive liquid"),
    ("assiduity", "steady, careful attention to one’s work"),
]


def quiz_html():
    rows = []
    for i, (w, q) in enumerate(WORDS):
        rows.append(f'<li class="qrow"><input class="letter" id="q{i}" maxlength="1" autocomplete="off" '
                    f'autocapitalize="characters" spellcheck="false" aria-describedby="q{i}-ctx q{i}-fb">'
                    f'<div><label for="q{i}">{w}</label><p class="ctx" id="q{i}-ctx">“{q}”</p>'
                    f'<p class="fb" id="q{i}-fb"></p></div></li>')
    defs = "".join(f"<li>{html.escape(d)}</li>" for _, d in DEFS)
    return rows, defs


def sample(pts, n=12):
    """Catmull-Rom through (lon, lat) waypoints -> [lat, lon] polyline for Leaflet."""
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


STOPS = {  # place names each voyage stops at, for labels when it is selected
    1: ["Savannah", "St. Pierre", "Grenada", "St. Eustatius", "Basseterre", "Montserrat", "London"],
    2: ["London", "Villefranche", "Leghorn", "Smyrna"],
    3: ["London", "Oporto"],
    4: ["London", "Genoa", "Naples", "Smyrna"],
    5: ["London", "Madeira", "Barbados", "Grenada"],
    6: ["London", "Nevis", "Port Morant", "Kingston"],
    7: ["London", "Sheerness", "Shetland", "Farthest north"],
}
SHOWN = {"Villefranche": "Villefranche, Nice", "Basseterre": "Basseterre, St. Kitts", "St. Pierre": "St. Pierre, Martinique",
         "Farthest north": "Farthest north, 80°37′ (Spitsbergen)", "Grenada": "the Grenades"}


def main():
    rows, defs = quiz_html()
    key = [chr(65 + [d[0] for d in DEFS].index(w)) for w, _ in WORDS]
    data = {
        "voyages": [{"n": v["n"], "line": sample(v["path"]), "stops": STOPS[v["n"]],
                     "badge": [v["badge"]["overview"][1], v["badge"]["overview"][0]]} for v in VOYAGES],
        "places": {SHOWN.get(n, n): [lat, lon] for n, (lon, lat) in P.items()
                   if n not in ("Nice", "Orfordness")},
        "alias": SHOWN,
    }
    vlist = "\n".join(
        f'<li><button type="button" data-v="{v["n"]}" aria-pressed="false"><span class="num">{v["n"]}</span>'
        f'<span><b>{v["year"]} · {v["title"]}</b><span class="stops">{v["stops"]}</span></span></button>'
        f'<p>{v["text"]}</p></li>' for v in VOYAGES)
    page = (HERE / "page.template.html").read_text()
    page = (page.replace("{{CHAPTER10}}", (HERE / "chapter10.html").read_text()).replace("{{MAPDATA}}", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
                .replace("{{VOYAGES}}", vlist)
                .replace("{{QROWS}}", "\n".join(rows)).replace("{{DEFS}}", defs)
                .replace("{{KEY}}", json.dumps(key)).replace("{{MEANINGS}}", json.dumps([d for _, d in DEFS])))
    assert "{{" not in page
    OUT.write_text(page)
    print(OUT, f"{len(page)/1024:.0f} KB", "key", "".join(key))


if __name__ == "__main__":
    main()
