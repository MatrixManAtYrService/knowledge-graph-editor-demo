"""Build the first-ascents graph: the fourteen 8000-meter peaks and the
people who climbed them, 1895-2012.

The graph splits the story into what happened and who/where:

- **peaks** ride the **mountains** bundle — one rail per country (or border
  pair) the mountain actually stands in, ordered by `orderKey: elevation`.
  Each skewer node carries `data.nation` itself, so the rail wears its
  country's legend color.
- **events** ride the single **timeline** skewer, ordered by
  `orderKey: date` — from Mummery's birth in 1855 to Chogolisa's belated
  first ascent in 1975. An event, where relevant, points `on` its
  mountain, and one date can carry several stories (1957-06-27 on Chogolisa
  is Buhl's `died-ascending` and Diemberger's `attempt` in a single node).
- **climbers** float free, tied to their dates by typed edges: `born`,
  `attempt`, `ascent`, `first-ascent`, and `died-ascending`. Ordinary
  deaths never reach the timeline — a climber's data carries the date —
  only dying on one of THIS graph's mountains earns a timeline node.

Node color binds to `data.nation`: a peak's means where it stands, a
climber's their nationality, an event's the nation of the party involved —
so the first-ascent credit (the 1953 British Everest expedition, the 1954
Italian K2 one) colors the *event*, never the mountain.

All dates were verified against Wikipedia expedition/biography pages,
Himalayan Journal obituaries, and Wikidata (2026-09). Known imprecisions
are carried in captions, never silently rounded: Norgay's adopted birthday,
Mallory's 8-or-9 June, Merkl's mid-July, Hillary's early-May Cho Oyu
attempt. Climbers with year-only birth records (Pasang Dawa Lama, Imanishi,
Gyalzen Norbu, Xu Jing) get no `born` event; the year sits in their node
data instead.
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).parent / "graphs" / "first-ascents"

W = "https://en.wikipedia.org/wiki/"


def slug(name: str) -> str:
    return name.lower().replace("–", "-").replace(" ", "-")


# (id-suffix, name, meters, range, location, FA date, FA nation, FA party, url-slug, caption-or-None)
# `location` is the country (or border pair) the mountain stands in — it
# drives the mountains rails and the peak's color. The first-ascent CREDIT
# nation colors the timeline's FA event instead.
PEAKS = [
    ("annapurna", "Annapurna", 8091, "Himalaya", "Nepal", "1950-06-03", "France",
     "Maurice Herzog, Louis Lachenal", "Annapurna",
     "The first eight-thousander ever climbed — three years before Everest, "
     "without supplemental oxygen. Herzog and Lachenal paid with their fingers and toes."),
    ("everest", "Everest", 8849, "Himalaya", "Nepal–China", "1953-05-29", "United Kingdom",
     "Edmund Hillary, Tenzing Norgay", "Mount_Everest",
     "A British expedition put a New Zealander and a Sherpa on top; London got "
     "the news on coronation morning."),
    ("nanga-parbat", "Nanga Parbat", 8126, "Himalaya", "Pakistan", "1953-07-03", "Austria",
     "Hermann Buhl", "Nanga_Parbat",
     "Buhl reached the summit alone — no oxygen, no partner, 41 hours up and "
     "down with a standing bivouac. The only solo first ascent of an 8000er. "
     "(The expedition was German-led; the summiter was Austrian.)"),
    ("k2", "K2", 8611, "Karakoram", "Pakistan–China", "1954-07-31", "Italy",
     "Achille Compagnoni, Lino Lacedelli", "K2",
     "Compagnoni and Lacedelli summited; Walter Bonatti's overnight oxygen "
     "carry made it possible and stayed bitterly disputed for fifty years."),
    ("cho-oyu", "Cho Oyu", 8188, "Himalaya", "Nepal–China", "1954-10-19", "Austria",
     "Herbert Tichy, Joseph Jöchler, Pasang Dawa Lama", "Cho_Oyu", None),
    ("makalu", "Makalu", 8485, "Himalaya", "Nepal–China", "1955-05-15", "France",
     "Jean Couzy, Lionel Terray", "Makalu",
     "All nine expedition members and sirdar Gyalzen Norbu summited over "
     "three days — the first 8000er first ascent to put the whole team on top."),
    ("kangchenjunga", "Kangchenjunga", 8586, "Himalaya", "Nepal–India", "1955-05-25", "United Kingdom",
     "George Band, Joe Brown", "Kangchenjunga",
     "Band and Brown stopped a few steps below the top, keeping a promise to "
     "Sikkim that the summit itself stay untrodden. Every ascent since has honored it."),
    ("manaslu", "Manaslu", 8163, "Himalaya", "Nepal", "1956-05-09", "Japan",
     "Toshio Imanishi, Gyalzen Norbu", "Manaslu", None),
    ("lhotse", "Lhotse", 8516, "Himalaya", "Nepal–China", "1956-05-18", "Switzerland",
     "Fritz Luchsinger, Ernst Reiss", "Lhotse", None),
    ("gasherbrum-2", "Gasherbrum II", 8035, "Karakoram", "Pakistan–China", "1956-07-07", "Austria",
     "Fritz Moravec, Josef Larch, Hans Willenpart", "Gasherbrum_II", None),
    ("broad-peak", "Broad Peak", 8051, "Karakoram", "Pakistan–China", "1957-06-09", "Austria",
     "Marcus Schmuck, Fritz Wintersteller, Kurt Diemberger, Hermann Buhl", "Broad_Peak",
     "All four climbers summited without high-altitude porters or bottled "
     "oxygen — and Buhl collected his second 8000er first ascent."),
    ("gasherbrum-1", "Gasherbrum I", 8080, "Karakoram", "Pakistan–China", "1958-07-05", "United States",
     "Pete Schoening, Andy Kauffman", "Gasherbrum_I",
     "The only 8000er whose first ascent went to an American expedition."),
    ("dhaulagiri", "Dhaulagiri", 8167, "Himalaya", "Nepal", "1960-05-13", "Switzerland",
     "Kurt Diemberger, Peter Diener, Ernst Forrer, Albin Schelbert, "
     "Nawang Dorje, Nyima Dorje", "Dhaulagiri",
     "The Swiss flew a glacier plane onto the mountain to stock the camps; "
     "Diemberger joined Buhl in the two-first-ascents club."),
    ("shishapangma", "Shishapangma", 8027, "Himalaya", "China", "1964-05-02", "China",
     "Xu Jing and nine others", "Shishapangma",
     "The last 8000er climbed — it stands entirely inside Tibet, closed to "
     "foreign expeditions, so the Chinese team had the mountain, and the era's "
     "final first, to themselves."),
    # Not an 8000er, but the timeline needs it: Buhl died here (1957), and its
    # own first ascent is known like the rest.
    ("chogolisa", "Chogolisa", 7665, "Karakoram", "Pakistan", "1975-08-02", "Austria",
     "Fred Pressl, Gustav Ammerer", "Chogolisa",
     "Buhl's last mountain: the 1957 attempt ended with his death (see the "
     "timeline). The main summit finally fell to an Austrian pair in 1975 — "
     "the lower northeast summit had gone to a Japanese team in 1958."),
]

# (id-suffix, name, nation, born ISO-or-None, born note, url-slug, caption-or-None)
# born=None: only the year is reliably recorded (kept in the note) — such
# climbers get no `born` event, because the timeline's proportional order
# needs full dates.
CLIMBERS = [
    ("mummery", "Albert Mummery", "United Kingdom", "1855-09-10", "", "Albert_F._Mummery",
     "The great Victorian alpinist; the first person to attempt any 8000er, "
     "and the first to die on one."),
    ("mallory", "George Mallory", "United Kingdom", "1886-06-18", "", "George_Mallory",
     "Lost high on Everest's northeast ridge in 1924, twenty-nine years "
     "before the mountain was climbed. \"Because it's there.\""),
    ("merkl", "Willy Merkl", "Germany", "1900-10-06", "", "Willy_Merkl",
     "Led the 1932 and 1934 German Nanga Parbat expeditions; the second "
     "killed him and nine others."),
    ("irvine", "Andrew Irvine", "United Kingdom", "1902-04-08", "", "Andrew_Irvine_(mountaineer)",
     "Twenty-two, the youngest of the 1924 party, chosen by Mallory for the "
     "final attempt. Part of his remains surfaced in 2024."),
    ("tichy", "Herbert Tichy", "Austria", "1912-06-01", "", "Herbert_Tichy", None),
    ("pasang-dawa-lama", "Pasang Dawa Lama", "Nepal", None, "born 1912 (year only)", "Pasang_Dawa_Lama",
     "Nearly summited K2 with Wiessner in 1939; on top of Cho Oyu fifteen "
     "years later."),
    ("norgay", "Tenzing Norgay", "Nepal", "1914-05-29", "the birthday he adopted after Everest — only 'late May 1914' is recorded", "Tenzing_Norgay", None),
    ("compagnoni", "Achille Compagnoni", "Italy", "1914-09-26", "", "Achille_Compagnoni", None),
    ("imanishi", "Toshio Imanishi", "Japan", None, "born 1914 (year only)", "Toshio_Imanishi", None),
    ("gyalzen-norbu", "Gyalzen Norbu", "Nepal", None, "born ~1917 (year only)", "Gyalzen_Norbu",
     "Sirdar of the Makalu and Manaslu expeditions and the first person to "
     "climb two 8000ers — a distinction usually misremembered as Buhl's."),
    ("herzog", "Maurice Herzog", "France", "1919-01-15", "", "Maurice_Herzog", None),
    ("hillary", "Edmund Hillary", "New Zealand", "1919-07-20", "", "Edmund_Hillary", None),
    ("reiss", "Ernst Reiss", "Switzerland", "1920-02-24", "", "Ernst_Reiss", None),
    ("lachenal", "Louis Lachenal", "France", "1921-07-17", "", "Louis_Lachenal", None),
    ("terray", "Lionel Terray", "France", "1921-07-25", "", "Lionel_Terray",
     "Annapurna support, Makalu summiter, author of 'Conquistadors of the "
     "Useless' — killed on a weekend climb in the Vercors."),
    ("moravec", "Fritz Moravec", "Austria", "1922-04-27", "", "Fritz_Moravec", None),
    ("couzy", "Jean Couzy", "France", "1923-07-09", "", "Jean_Couzy",
     "Aeronautical engineer, Annapurna teammate, first up Makalu — killed at "
     "35 by a single falling stone."),
    ("buhl", "Hermann Buhl", "Austria", "1924-09-21", "", "Hermann_Buhl",
     "Two 8000er first ascents — Nanga Parbat solo, then Broad Peak. He died "
     "on Chogolisa three weeks after the second."),
    ("lacedelli", "Lino Lacedelli", "Italy", "1925-12-04", "", "Lino_Lacedelli", None),
    ("gilkey", "Art Gilkey", "United States", "1926-09-25", "", "Art_Gilkey",
     "Geologist on the 1953 K2 expedition; the storm-bound attempt to lower "
     "him became mountaineering's most famous retreat."),
    ("xu-jing", "Xu Jing", "China", None, "born 1927 (year only)", "Xu_Jing_(mountaineer)",
     "Deputy leader on Everest 1960, expedition leader on Shishapangma 1964."),
    ("schoening", "Pete Schoening", "United States", "1927-07-30", "", "Pete_Schoening",
     "Held six falling men on one ice axe during the K2 retreat — 'The "
     "Belay' — then made the first ascent of Gasherbrum I."),
    ("band", "George Band", "United Kingdom", "1929-02-02", "", "George_Band",
     "Youngest member of the 1953 Everest expedition; two years later, first "
     "up Kangchenjunga with Joe Brown."),
    ("diemberger", "Kurt Diemberger", "Austria", "1932-03-16", "", "Kurt_Diemberger",
     "The only living member of the two-first-ascents club: Broad Peak 1957, "
     "Dhaulagiri 1960."),
]

# Death dates land on the climber NODES (data.died / data.died_note), never
# on the timeline — except deaths while ascending one of this graph's
# mountains, which become DIED_ASCENDING events below.
DEATHS = [
    ("mummery", "1895-08-24", "vanished on Nanga Parbat"),
    ("mallory", "1924-06-08", "vanished high on Everest (8 or 9 June)"),
    ("irvine", "1924-06-08", "vanished high on Everest (8 or 9 June)"),
    ("merkl", "1934-07-16", "storm-bound high on Nanga Parbat (mid-July)"),
    ("gilkey", "1953-08-10", "lost in the K2 retreat"),
    ("lachenal", "1955-11-25", "hidden crevasse, skiing the Vallée Blanche above Chamonix"),
    ("buhl", "1957-06-27", "cornice collapse on Chogolisa"),
    ("couzy", "1958-11-02", "rockfall while climbing the Crête des Bergers, Dévoluy"),
    ("gyalzen-norbu", "1961-05-11", "died attempting Langtang Lirung"),
    ("terray", "1965-09-19", "roped fall while climbing in the Vercors"),
    ("pasang-dawa-lama", "1982-09-15", ""),
    ("norgay", "1986-05-09", ""),
    ("tichy", "1987-09-26", ""),
    ("imanishi", "1995-11-15", ""),
    ("moravec", "1997-03-17", ""),
    ("schoening", "2004-09-22", ""),
    ("hillary", "2008-01-11", ""),
    ("compagnoni", "2009-05-13", ""),
    ("lacedelli", "2009-11-20", ""),
    ("reiss", "2010-08-03", ""),
    ("band", "2011-08-26", ""),
    ("xu-jing", "2011-10-15", ""),
    ("herzog", "2012-12-13", "the last survivor of Annapurna 1950"),
]

# Deaths while ascending one of THIS graph's mountains: (event id-suffix,
# date, nation, peak, [(edge type, climber)], caption). Attempts by
# survivors of the same incident share the event node.
DIED_ASCENDING = [
    ("1895-nanga-parbat", "1895-08-24", "United Kingdom", "nanga-parbat",
     [("died-ascending", "mummery")],
     "Mummery and Gurkhas Ragobir Thapa and Goman Singh vanish reconnoitering "
     "the Rakhiot face — the first deaths on any 8000er."),
    ("1924-everest", "1924-06-08", "United Kingdom", "everest",
     [("died-ascending", "mallory"), ("died-ascending", "irvine")],
     "Last seen 'going strong for the top' on 8 June (or the 9th — the record "
     "allows either). Mallory was found in 1999; part of Irvine in 2024."),
    ("1934-nanga-parbat", "1934-07-16", "Germany", "nanga-parbat",
     [("died-ascending", "merkl")],
     "The 1934 disaster: trapped by storm high on the mountain, Merkl, Willo "
     "Welzenbach and six Sherpas died slowly over days (Merkl mid-July; "
     "conventionally the 16th). His body was found in 1938."),
    ("1953-k2", "1953-08-10", "United States", "k2",
     [("died-ascending", "gilkey"), ("attempt", "schoening")],
     "The American K2 retreat: Schoening's one-axe belay holds six falling "
     "men; Art Gilkey, storm-bound with thrombophlebitis, is swept away — or "
     "cut himself loose to save the others."),
    ("1957-chogolisa", "1957-06-27", "Austria", "chogolisa",
     [("died-ascending", "buhl"), ("attempt", "diemberger")],
     "Three weeks after Broad Peak, an unauthorized alpine-style side trip: "
     "descending unroped in a storm, Buhl steps through a cornice on the "
     "southeast ridge. Diemberger, just ahead, finds the breach in the snow."),
]

# Survived attempts: (event id-suffix, date, nation, peak, [climbers], caption).
ATTEMPTS = [
    ("1922-everest", "1922-05-21", "United Kingdom", "everest",
     ["mallory"],
     "Mallory, Somervell, Norton and Morshead reach ~8225 m without oxygen — "
     "higher than any human before them."),
    ("1950-dhaulagiri", "1950-05-14", "France", "dhaulagiri",
     ["herzog", "lachenal", "terray", "couzy"],
     "At Tukucha the French give up on Dhaulagiri as hopeless and turn to "
     "Annapurna — three weeks later they are on top of it."),
    ("1952-cho-oyu", "1952-05-01", "New Zealand", "cho-oyu",
     ["hillary"],
     "Shipton's party turns back around 6800 m (early May; the exact day went "
     "unrecorded). Hillary's consolation comes a year later."),
    ("1952-everest", "1952-05-28", "Nepal", "everest",
     ["norgay"],
     "Tenzing and Raymond Lambert, with the Swiss, reach ~8595 m — the "
     "highest anyone had ever climbed. He returns the next spring."),
    ("1960-everest", "1960-05-24", "China", "everest",
     ["xu-jing"],
     "Deputy leader Xu Jing exhausts himself around 8500 m on the north ridge "
     "and gives up his place; Wang Fuzhou, Gonpo and Qu Yinhua summit the "
     "next morning at 04:20."),
]

# Non-first ascents worth a node: (event id-suffix, date, nation, peak,
# [climbers], caption).
ASCENTS = [
    ("1955-makalu-2nd", "1955-05-16", "Nepal", "makalu",
     ["gyalzen-norbu"],
     "Sirdar Gyalzen Norbu summits with Guido Magnone the day after the "
     "first ascent — with Manaslu the next year, that made him the first "
     "person to climb two 8000ers."),
]

# First-ascent summiters who are in the cast (the full party, cast or not,
# is in the peak's data.first_ascent).
FA_PARTY = {
    "annapurna": ["herzog", "lachenal"],
    "everest": ["hillary", "norgay"],
    "nanga-parbat": ["buhl"],
    "k2": ["compagnoni", "lacedelli"],
    "cho-oyu": ["tichy", "pasang-dawa-lama"],
    "makalu": ["couzy", "terray"],
    "kangchenjunga": ["band"],
    "manaslu": ["imanishi", "gyalzen-norbu"],
    "lhotse": ["reiss"],
    "gasherbrum-2": ["moravec"],
    "broad-peak": ["buhl", "diemberger"],
    "gasherbrum-1": ["schoening"],
    "dhaulagiri": ["diemberger"],
    "shishapangma": ["xu-jing"],
    "chogolisa": [],  # Pressl and Ammerer are not in the cast
}

# Extra edges into first-ascent events: (peak, edge type, climber, caption
# appended to the event).
FA_EXTRAS = [
    ("everest", "attempt", "band",
     "George Band, the expedition's youngest, worked the icefall route and "
     "made no summit bid — his summit came two years later on Kangchenjunga."),
]

# The pinned nation colors (unlisted values get stable palette picks).
# Location pairs get their own colors, distinct from any single nation's.
NATION_COLORS = {
    "France": "#4e79a7",
    "United Kingdom": "#e15759",
    "Austria": "#f28e2c",
    "Italy": "#59a14f",
    "Switzerland": "#edc949",
    "Japan": "#b07aa1",
    "United States": "#76b7b2",
    "China": "#9c755f",
    "New Zealand": "#af7aa1",
    "Nepal": "#ff9da7",
    "Germany": "#8cd17d",
    "Pakistan": "#2a9d8f",
    "Nepal–China": "#8c6bb1",
    "Pakistan–China": "#66a61e",
    "Nepal–India": "#e6ab02",
}

# ---------------------------------------------------------------------------

nodes: list[dict] = []
edges: list[dict] = []

by_name = {c[0]: c[1] for c in CLIMBERS}
peak_name = {p[0]: p[1] for p in PEAKS}

for suffix, name, meters, range_, location, fa_date, fa_nation, party, wslug, caption in PEAKS:
    data = {
        "elevation": meters,
        "range": range_,
        "nation": location,  # where it stands (drives its rail and color)
        "date": fa_date,
        "first_ascent": party,
        "first_ascent_nation": fa_nation,
        "url": W + wslug,
    }
    if caption:
        data["key_event"] = True
        data["caption"] = caption
    nodes.append({"id": f"peak:{suffix}", "type": "peak", "label": f"{name} ({meters} m)", "data": data})

deaths = {c: (date, note) for c, date, note in DEATHS}
for suffix, name, nation, born, born_note, wslug, caption in CLIMBERS:
    data = {"nation": nation, "url": W + wslug}
    if born:
        data["born"] = born
    if born_note:
        data["born_note"] = born_note
    if suffix in deaths:
        data["died"] = deaths[suffix][0]
        if deaths[suffix][1]:
            data["died_note"] = deaths[suffix][1]
    if caption:
        data["key_event"] = True
        data["caption"] = caption
    nodes.append({"id": f"climber:{suffix}", "type": "climber", "label": name, "data": data})

nation_of = {c[0]: c[2] for c in CLIMBERS}


def event(eid: str, date: str, label: str, nation: str, what: str,
          peak: str | None, by: list[tuple[str, str]], caption: str | None) -> None:
    data: dict = {"date": date, "nation": nation, "what": what}
    if caption:
        data["key_event"] = True
        data["caption"] = caption
    nodes.append({"id": f"ev:{eid}", "type": "event", "label": label, "data": data})
    if peak:
        edges.append({"type": "on", "from": f"ev:{eid}", "to": f"peak:{peak}", "data": {}})
    for etype, climber in by:
        edges.append({"type": etype, "from": f"climber:{climber}", "to": f"ev:{eid}", "data": {}})


# Labels are bare years (a "† year" for deaths): the timeline stays legible
# and the edges + data.what carry the story.
for suffix, name, nation, born, _note, _wslug, _cap in CLIMBERS:
    if born:
        caption = None
        if suffix == "norgay":
            caption = ("The birthday Tenzing adopted after Everest — only 'late May 1914' "
                       "was ever recorded.")
        event(f"b-{suffix}", born, born[:4], nation,
              f"{name} born", None, [("born", suffix)], caption)

for eid, date, nation, peak, by, caption in DIED_ASCENDING:
    who = " and ".join(by_name[c] for _t, c in by if _t == "died-ascending")
    event(eid, date, f"† {date[:4]}", nation, f"{who} dies on {peak_name[peak]}", peak, by, caption)

for eid, date, nation, peak, climbers, caption in ATTEMPTS:
    who = ", ".join(by_name[c] for c in climbers)
    event(eid, date, date[:4], nation, f"{who}: attempt on {peak_name[peak]}", peak,
          [("attempt", c) for c in climbers], caption)

for eid, date, nation, peak, climbers, caption in ASCENTS:
    who = ", ".join(by_name[c] for c in climbers)
    event(eid, date, date[:4], nation, f"{who}: ascent of {peak_name[peak]}", peak,
          [("ascent", c) for c in climbers], caption)

fa_extra = {}
for peak, etype, climber, caption in FA_EXTRAS:
    fa_extra.setdefault(peak, []).append((etype, climber, caption))

for suffix, name, _m, _r, _loc, fa_date, fa_nation, _party, _w, _cap in PEAKS:
    by: list[tuple[str, str]] = [("first-ascent", c) for c in FA_PARTY[suffix]]
    caption = None
    for etype, climber, extra_cap in fa_extra.get(suffix, []):
        by.append((etype, climber))
        caption = extra_cap
    event(f"fa-{suffix}", fa_date, fa_date[:4], fa_nation,
          f"first ascent of {name}", suffix, by, caption)

# -- skewers ----------------------------------------------------------------

# mountains: one rail per country (or border pair) the peaks stand in,
# lowest to highest. The skewer node carries the bound color field too, so
# the rail wears the country's legend color.
for location in sorted({p[4] for p in PEAKS}):
    mine = sorted((p for p in PEAKS if p[4] == location), key=lambda p: p[2])
    sid = f"skewer:mountains-{slug(location)}"
    nodes.append({
        "id": sid, "type": "skewer", "label": location,
        "data": {"description": f"Peaks standing in {location}, lowest to highest.",
                 "orderKey": "elevation", "group": "mountains", "nation": location},
    })
    for i, p in enumerate(mine):
        edges.append({"type": "skewer-order", "from": sid, "to": f"peak:{p[0]}", "data": {"index": i}})

# timeline: every event, in date order, on one rail.
timeline = sorted((n for n in nodes if n["type"] == "event"), key=lambda n: (n["data"]["date"], n["id"]))
nodes.append({
    "id": "skewer:timeline", "type": "skewer", "label": "timeline",
    "data": {"description": "Everything that happened, in order: births, attempts, "
             "first ascents, and deaths — on and off the mountains.",
             "orderKey": "date", "group": "timeline"},
})
for i, n in enumerate(timeline):
    edges.append({"type": "skewer-order", "from": "skewer:timeline", "to": n["id"], "data": {"index": i}})

# ---------------------------------------------------------------------------

schema = {
    # One nation = one color. A peak's nation is where it STANDS, a
    # climber's their nationality, an event's the party involved — the
    # first-ascent credit colors the event, never the mountain.
    "colorKey": "nation",
    "colorValues": NATION_COLORS,
    "nodeTypes": {
        "peak": {"color": "#5b7fa6", "description": "A peak (8000ers, plus the mountains the story demands)", "family": "mountains"},
        "climber": {"color": "#b07aa1", "description": "A mountaineer of the first-ascent era", "family": "people"},
        "event": {"color": "#8f98a3", "description": "A dated happening on the timeline; edges say what and to whom", "family": "events"},
        "skewer": {"color": "#9aa0a6", "description": "An ordered colinearity group (layout intent, interpreted by the view)", "family": "layout"},
    },
    "edgeTypes": {
        "born": {"color": "#59a14f", "description": "Climber was born on this date", "family": "events"},
        "died-ascending": {"color": "#111111", "description": "Climber died on this date, ascending this graph's mountain", "family": "events"},
        "attempt": {"color": "#edc949", "description": "Climber attempted the event's mountain and lived, without the summit", "family": "events"},
        "ascent": {"color": "#76b7b2", "description": "Climber summited the event's mountain (not a first ascent)", "family": "events"},
        "first-ascent": {"color": "#4e79a7", "description": "Climber stood on top on the first ascent", "family": "events"},
        "on": {"color": "#c9cdd2", "description": "The event happened on this mountain", "family": "structure"},
        "skewer-order": {"color": "#c9cdd2", "description": "Skewer membership; data.index gives the order along the skewer", "family": "layout"},
    },
}

view = {
    "id": "default",
    "name": "Default",
    "visibleNodeTypes": None,
    "visibleEdgeTypes": None,
    "nodeOverrides": [],
    "edgeOverrides": [],
    "focus": None,
    "focusShow": [],
    "focusHide": [],
    "skewerGroups": {},
    "layout": {"engine": "fcose", "seedPositions": {}, "pinned": [], "skewers": {}, "rules": []},
}

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "views").mkdir(exist_ok=True)
# Seed the default view only if absent: regeneration must not clobber a
# layout the user has arranged and saved.
if not (OUT / "views" / "default.json").is_file():
    (OUT / "views" / "default.json").write_text(json.dumps(view, indent=2) + "\n")
(OUT / "schema.json").write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n")
(OUT / "nodes.json").write_text(
    json.dumps({"nodes": sorted(nodes, key=lambda n: n["id"])}, indent=2, ensure_ascii=False) + "\n")
(OUT / "edges.json").write_text(
    json.dumps({"edges": sorted(edges, key=lambda e: (e["from"], e["type"], e["to"]))}, indent=2, ensure_ascii=False) + "\n")

kinds: dict[str, int] = {}
for n in nodes:
    kinds[n["type"]] = kinds.get(n["type"], 0) + 1
ekinds: dict[str, int] = {}
for e in edges:
    ekinds[e["type"]] = ekinds.get(e["type"], 0) + 1
print("nodes:", len(nodes), kinds)
print("edges:", len(edges), ekinds)
print("timeline:", len(timeline), "events,", timeline[0]["data"]["date"], "→", timeline[-1]["data"]["date"])
